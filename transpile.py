import os
import re
from typing import List
from tokenize import detect_encoding
from datetime import datetime
from pathlib import Path as _path
from random import randint
from typing import List, Union, Tuple, Optional
import logging
from stat import S_IRWXO
# Non-Standard
from windows_tools.file_utils import get_paths_recursive_and_fix_permissions
from luaparser.ast import parse
from luaparser.ast import get_token_stream
# Local 
from typedef import LuaNode
from transnode import TransNode
from tools.updater import set_debug



class Path(_path):
    def __init__(self, *args: str | os.PathLike[str]) -> None:
        super().__init__(*args)
    
    def string(self):
        return str(self)
    


CWD = Path(os.getcwd())
update, debug, init = set_debug(True)


def timestamp():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

def random_number_sequence(length=5):
    retv = []
    for i in range(0, length):
        retv.append(str(randint(0, 9)))
    return "".join(retv)

def get_encoding(filepath: str) -> str:
    """
    Get the encoding of a file
    Arguments:
        filepath (str): path to the file
    Return:
        encoding (str): string rep of the encoding
    """
    fp = open(filepath, "r")
    try:
        enc = detect_encoding(fp.readline)
        fp.close()
        return enc
    except:
        fp.close()
        return "utf-8"

def string_to_transnodes(string: str) -> List[TransNode]:
    return [TransNode(node=node, index=index, source=string) 
            for index, node 
            in enumerate(string_to_lua_nodes(string))]

def lua_file_to_transnodes(filepath: str) -> List[TransNode]:
    """
    Takes a string of a lua file path returns a list of Transnode
    Arguments:
        filepath (str): path to the lua file to make nodes of
    Returns:
        nodes(List[TransNode]): a list of TransNodes
    """
    enc = get_encoding(filepath=filepath)
    with open(file=filepath, mode="r", encoding=enc, errors="ignore") as f:
        src = f.read()
    return [TransNode(node=node, index=index, source=src) 
            for index, node 
            in enumerate(string_to_lua_nodes(src))]

def read_lua(filepath:str):
    """
    Get encoding of file and open file line by line
    and encoding by encoding then return a string
    Arguments:
        filepath(str) : path the lua file
    Returns:
        str : string representation of a lua file
    """
    with open(file=filepath, mode="r", encoding="utf-8", errors="ignore") as f:
        src = f.read()
    return src

def string_to_lua_nodes(string: str) -> List[LuaNode]:
    """Converts a string of lua code to 
    a list of LuaNode
    """
    nodes = parse(string)
    return [node for node in nodes.body.body]

def lua_file_to_lua_nodes(filepath:str) -> List[LuaNode]:
    string = read_lua(filepath=filepath)
    nodes = parse(string)
    return [node for node in nodes.body.body]

def lua_check_require(lua_string:str) -> bool:
    lines = lua_string.split("\n")
    for line in lines:
        if line.startswith("require"):
            return True
    return False

def _extract_require_statements(lua_source: str):
    """
    Extracts all Lua `require` statements from the given source code.

    Args:
        lua_source (str): The Lua source code as a string.

    Returns:
        list: A list of module names required in the Lua source code.
    """
    # Regular expression to match require statements
    pattern = r'require\s*\(\s*["\']([^"\']+)["\']\s*\)'
    
    # Find all matches in the source code
    matches = re.findall(pattern, lua_source)
    if matches:
        return [CWD.string() + os.sep + str(m).replace(".", os.sep) for m in matches]
    else:
        return []
    
def _transpile_submodule(filepath: str, project_directory: str, sm_name: str) -> str:
    """
    Transpile a Lua submodule to a Python file within a specified project directory.

    This function reads a Lua file, converts it to a Python-equivalent script, and writes
    the output to a specified submodule directory within a project directory. The resulting 
    Python file contains metadata like creation time, module name, and user.

    Args:
        filepath (str): The path to the Lua file to transpile.
        project_directory (str): The root directory of the project where the transpiled submodule will be saved.
        sm_name (str): The name of the submodule directory where the transpiled file will be placed.

    Returns:
        str: The path to the generated Python file.

    Raises:
        IOError: If there is an issue reading the Lua file or writing the Python file.
        ValueError: If the Lua file content cannot be parsed or transpiled.

    Dependencies:
        - read_lua: A function that reads Lua content from a file and returns it as a string.
        - string_to_transnodes: A function that converts a Lua script string into a list of `TransNode` objects.
        - get_token_stream: A function that generates a token stream from Lua content.
        - timestamp: A function that returns the current timestamp as a string.
        - TransNode: A class or type that has a `collect_tokens` method and `python_string` property.

    Example:
        transpile_path = _transpile_submodule('path/to/lua_file.lua', '/project/root', 'submodule_name')
        print(f'Transpiled file created at: {transpile_path}')
    """
    if isinstance(filepath, Path):
        filepath = filepath.string()
    if isinstance(project_directory, Path):
        filepath = project_directory.string()

    final = []
    # Make the Python file path
    file = os.path.basename(filepath)
    dn = os.path.dirname(filepath)
    base_filename = file.split(".")[0]
    module_name = os.path.basename(dn)
    python_full_fp = os.path.join(dn, sm_name, f"{base_filename}.py")
    
    # Read the Lua file and convert to Python
    try:
        content: str = read_lua(filepath)
        transnodes: List[TransNode] = string_to_transnodes(content)
        token_stream = get_token_stream(content)
    except Exception as e:
        raise ValueError(f"Error processing Lua file: {e}")

    for tnode in transnodes:
        tnode.collect_tokens(token_stream=token_stream)
        final.append(tnode.python_string)
    
    # Create metadata stamp
    stamp = f"# Creation Time: {timestamp()}\n# Module: {module_name}\n# File: {base_filename}.py\n# User:{os.getlogin()}\n\n"
    
    
    # Write the transpiled Python file
    try:
        change_file_perms(python_full_fp)
        with open(python_full_fp, "w") as f:
            f.write(stamp)
            f.write("\n".join(final))
            f.write("\n")
    except IOError as e:
        raise IOError(f"Error writing Python file: {e}")

    return python_full_fp

def _init_submodule(module_name: Union[str, Path], project_dir: str) -> Tuple[Path, Path]:
    """
    Initialize a submodule directory and create an `__init__.py` file.

    This function creates a directory for the specified submodule within the project directory,
    and an `__init__.py` file inside it. If the submodule directory already exists, it will not
    be created again.

    Args:
        module_name (Union[str, Path]): The name of the submodule to initialize.
        project_dir (str): The root directory of the project where the submodule will be created.

    Returns:
        Tuple[Path, Path]: A tuple containing the path to the submodule directory and the path to the `__init__.py` file.

    Raises:
        IOError: If there is an issue creating the directory or the `__init__.py` file.

    Example:
        submodule_path, init_file_path = _init_submodule('new_module', '/project/root')
        print(f'Submodule directory created at: {submodule_path}')
        print(f'__init__.py file created at: {init_file_path}')
    """
    
    submodule_path = Path(project_dir).joinpath(module_name)
    try:
        free_fp(submodule_path)
        init_file_path = submodule_path.joinpath("__init__.py")
        free_fp(init_file_path)
    except Exception as e:
        raise IOError(f"Error initializing submodule: {e}")
    
    return submodule_path, init_file_path

def _get_submodule_name(filepath: str|Path) -> str:
    """
    Extract the submodule name from a given file path.

    This function retrieves the submodule name by obtaining the base name of the 
    directory containing the file specified by the given file path.

    Args:
        filepath (str): The path to the file for which the submodule name is to be extracted.

    Returns:
        str: The name of the submodule.

    Example:
        submodule_name = _get_submodule_name('/path/to/module/file.lua')
        print(f'Submodule name: {submodule_name}')
    """
    if isinstance(filepath, Path):
        filepath = filepath.string()
    directory_name = os.path.dirname(filepath)
    base_name = Path(directory_name).name
    # For debugging purposes, consider using logging instead of print
    # print(f"submodule: {base_name}")
    return str(base_name)

def _transpile_root_module(filepath: str, project_dir: str) -> str:
    """
    Transpile a Lua root module to a Python file within a specified project directory.

    This function reads a Lua file, converts it to a Python-equivalent script, and writes
    the output to the root project directory. The resulting Python file contains metadata 
    like creation time and filename.

    Args:
        filepath (str): The path to the Lua file to transpile.
        project_dir (str): The root directory of the project where the transpiled file will be saved.

    Returns:
        str: The path to the generated Python file.

    Raises:
        IOError: If there is an issue reading the Lua file or writing the Python file.
        ValueError: If the Lua file content cannot be parsed or transpiled.

    Dependencies:
        - read_lua: A function that reads Lua content from a file and returns it as a string.
        - string_to_transnodes: A function that converts a Lua script string into a list of `TransNode` objects.
        - get_token_stream: A function that generates a token stream from Lua content.
        - timestamp: A function that returns the current timestamp as a string.
        - TransNode: A class or type that has a `collect_tokens` method and `python_string` property.

    Example:
        transpile_path = _transpile_root_module('path/to/lua_file.lua', '/project/root')
        print(f'Transpiled file created at: {transpile_path}')
    """
    
    final = []
    
    # Read the Lua file and convert to Python
    try:
        content: str = read_lua(filepath)
        transnodes: List[TransNode] = string_to_transnodes(content)
        token_stream = get_token_stream(content)
    except Exception as e:
        raise ValueError(f"Error processing Lua file: {e}")
    
    for tnode in transnodes:
        tnode.collect_tokens(token_stream=token_stream)
        final.append(tnode.python_string)
    
    # Create metadata signature
    filename = os.path.basename(filepath).split(".")[0]
    signature = f"# Creation Time: {timestamp()}\n# File: {filename}.py\n"
    python_filename = f"{filename}.py"
    python_filepath = os.path.join(project_dir, python_filename)
    
    NL = "\n"
    # Write the transpiled Python file
    try:
        free_fp(python_filepath)
        with open(python_filepath, "w") as f:
            f.write(signature)
            n = NL.join(final)
            f.write(n)
            f.write(NL)
    except IOError as e:
        raise IOError(f"Error writing Python file: {e}")

    return python_filepath

def free_fp(filepath:str|Path):
    """ Creates a dir or file if it doesnt exist, then fixes 
    the file permissions to the at of who created it"""
    fpexists = os.path.exists(filepath)
    if os.path.isdir(filepath):
        if fpexists == False:
            os.mkdir(path=filepath)
    elif os.path.isfile(filepath):
        if fpexists == False:
            with open(filepath, "w") as f:
                f.close()
    os.chmod(path=filepath, mode=S_IRWXO)

def transpile_lua(filepath: str, follow_requires: bool = True) -> Optional[Path]:
    """
    Transpile a Lua file to a Python file within a project directory.

    This function reads a Lua file, converts it to a Python-equivalent script, and writes the
    output to a new project directory. Optionally, it also handles `require` statements in Lua
    by recursively transpiling the required files.

    Args:
        filepath (str): The path to the Lua file to transpile.
        follow_requires (bool): Whether to follow and transpile `require` statements. Default is `True`.

    Returns:
        Optional[Path]: The path to the main Python file created in the project directory. 
                        Returns `None` if an error occurs.

    Raises:
        IOError: If there is an issue reading the Lua file or writing the Python file.
        ValueError: If the Lua file content cannot be parsed or transpiled.

    Dependencies:
        - read_lua: A function that reads Lua content from a file and returns it as a string.
        - extract_require_statements: A function that extracts `require` statements from Lua content.
        - string_to_transnodes: A function that converts a Lua script string into a list of `TransNode` objects.
        - get_token_stream: A function that generates a token stream from Lua content.
        - timestamp: A function that returns the current timestamp as a string.
        - random_number_sequence: A function that generates a random sequence of digits for project naming.
        - _transpile_root_module: A function that transpiles a root Lua module.
        - _get_submodule_name: A function that extracts a submodule name.
        - _init_submodule: A function that initializes a submodule directory.
        - _transpile_submodule: A function that transpiles a submodule Lua file.

    Example:
        transpile_path = transpile_lua('path/to/lua_file.lua')
        if transpile_path:
            print(f'Transpiled main Python file created at: {transpile_path}')
    """
    

    # Resolve filepath and read content
    filepath = Path(filepath).resolve()
    if not filepath.is_file():
        raise ValueError(f"Provided filepath does not point to a valid file: {filepath}")
    
    content: str = read_lua(filepath)
    
    # Determine project directory name
    project_name = filepath.stem + "_" + random_number_sequence(10)
    project_directory = Path(os.getcwd()).joinpath(project_name)
    project_directory.mkdir(parents=True)
    
    # Read source string
    logging.info(f"Transpiling Lua file at: {filepath}")
    
    # Extract and transpile require statements
    requires = _extract_require_statements(content) if follow_requires  else []
    if follow_requires:
        for req in requires:
            req_path = Path(req)
            free_fp(req_path)

            if req_path.is_file():
                if req_path.parent == filepath.parent:
                    try:
                        _transpile_root_module(req, project_directory)
                    except Exception as e:
                        print(f"{e}\nfailed to transpile root module with _transpile_root_module('{req}', '{project_directory}')")
                        logging.critical(f"{e}\nfailed to transpile root module with _transpile_root_module('{req}', '{project_directory}')")
            else:
                submodule_name = _get_submodule_name(req)
                submodule_path, init_file_path = _init_submodule(submodule_name, project_directory)
                submodule_files = [file for file in submodule_path.iterdir() if file.is_file()]
                for sub_file in submodule_files:
                    try:
                        _transpile_submodule(str(sub_file), project_directory, submodule_name)
                    except Exception as e:
                        print(f"{e}\nfailed to transpile root module with _transpile_submodule('{sub_file}', '{project_directory}', '{submodule_name}')")
                        logging.critical(f"{e}\nfailed to transpile root module with _transpile_root_module")

    # Acquire Trans nodes and stream
    transnodes: List[TransNode] = string_to_transnodes(content)
    token_stream = get_token_stream(content)
    root_strings = []
    for tnode in transnodes:
        tnode.collect_tokens(token_stream=token_stream)
        root_strings.append(tnode.python_string)
    
    # Write the transpiled Python file
    signature = f"# Creation Time: {timestamp()}\n# File: {filepath.stem}.py\n"
    python_filepath = project_directory.joinpath(f"{filepath.stem}.py")
    free_fp(python_filepath)
    with open(python_filepath, "w") as f:
        f.write(signature)
        f.write("\n".join(root_strings))
        f.write("\n")
    
    return python_filepath
    
    

    
    
if __name__ == "__main__":
    transpile_lua(".\\testproj\\test.lua")
