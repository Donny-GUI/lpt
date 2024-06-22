
import os
import re 
from typing import List
from tokenize import detect_encoding
from datetime import datetime
from pathlib import Path as _path
from random import randint
# Non-Standard
from luaparser.ast import parse
from luaparser.ast import get_token_stream
# Local 
from typedef import LuaNode
from transnode import TransNode
from tools.color import *
from tools.updater import *
DEBUG = True 
from tools.updater import set_debug



class Path(_path):
    def __init__(self, *args: str | os.PathLike[str]) -> None:
        super().__init__(*args)
    
    def string(self):
        return str(self)


CWD = Path(os.getcwd())


update, debug, init = set_debug(DEBUG)


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

def extract_require_statements(lua_source: str):
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

def _transpile_submodule(filepath: str, project_directory, sm_name:str) -> str:
        
        update(f"transpile_submodule {filepath} {project_directory} {sm_name}")
        final = []
        # make the python file path
        file = os.path.basename(filepath)
        dn = os.path.dirname(filepath)
        ff = file.split(".")[0]
        module_name = os.path.basename(dn)
        python_full_fp = dn + os.sep + sm_name + os.sep + ff + ".py"
        # read the lua file to string to nodes and get string
        content: str = read_lua(filepath)
        transnodes:list[TransNode] = string_to_transnodes(content)
        token_stream = get_token_stream(content)
        for tnode in transnodes:
            tnode.collect_tokens(token_stream=token_stream)
            final.append(tnode.python_string)
        stamp = f"# Creation Time: {timestamp()}\n# Module: {module_name}\n# File: {ff}.py\n# User: {os.getlogin()}\n"
        with open(python_full_fp, "w") as f:
            f.write(stamp)
            for x in final:
                f.write(x)
                f.write("\n")
            f.write("\n")

        return python_full_fp

def _get_submodule_name(filepath:str):
        
        dn = os.path.dirname(filepath)
        bn = Path(os.path.basename(dn))
        print("submodule: ", bn)
        return str(bn)

def _init_submodule(module_name: str|Path, project_dir:str):

    p = Path(str(project_dir) + os.sep + module_name)
    if p.exists() == False:
        p.mkdir()
    init_ = p.joinpath("__init__.py")
    with open(init_, "w") as r:
        r.close()
    return p, init_

def _transpile_root_module(filepath:str, project_dir: str) -> str:
    update(f"transpile_root_node {filepath} {project_dir}")
    final = []
    content: str = read_lua(filepath)
    filename = os.path.basename(filepath).split(".")[0]
    root_dir = os.path.dirname(filepath)
    transnodes:list[TransNode] = string_to_transnodes(content)
    token_stream = get_token_stream(content)

    for tnode in transnodes:
        tnode.collect_tokens(token_stream=token_stream)
        final.append(tnode.python_string)
    
    signature = f"# Creation Time: {timestamp()}\n# File: {filename}\n"
    filename+=".py"
    fp = os.path.join(project_dir, filename)
    
    with open(fp, "w") as f:
        f.write(signature)
        for x in final:
            f.write(x+"\n")
    
    return fp

def transpile_lua(filepath:str, follow_requires=True):
    """
    Convert a string of lua source filepath to a string of 
    python source code.
    """
    update(f"transpile_lua(filepath='{filepath}' follow_requires={follow_requires})")
    
    if filepath.startswith("."):
        filepath = os.getcwd() + filepath[1:]
    filepath:Path = Path(filepath)
    filename = Path(os.path.basename(filepath.string()).split(".")[0])
    root_dir = Path(os.path.dirname(filepath.string()))
    content: str = read_lua(filepath.string())

    # make project directory
    project_name = Path(os.path.basename(filepath.string()).split(".")[0] + "_" + random_number_sequence(10))
    project_directory = Path(os.path.join(os.getcwd(), project_name.string()))
    project_directory.mkdir()

    ##[1.1] Read source string
    print("filepath: ", filepath.string())
    content: str = read_lua(filepath.string())
    
    ###[1.2] Get require statements (imports)
    requires = extract_require_statements(content) if follow_requires == True else []

    ####[1.3] Get requires and transpile them if necessary
    if follow_requires == True:
        for req in requires:
            if os.path.isfile(req):
                if os.path.dirname(req) == root_dir:
                    _transpile_root_module(req, project_directory)
            else:
                sub_module_name = _get_submodule_name(req)
                smpath, initfile = _init_submodule(sub_module_name, project_dir=project_directory)
                files = [Path(os.path.join(CWD.string(), x)) 
                         for x in os.listdir(smpath.string())]
                for file in files:
                    _transpile_submodule(file.string(), project_directory, sub_module_name)

    ####[1.4] Acquire Trans nodes and stream
    transnodes:list[TransNode] = string_to_transnodes(content)
    token_stream = get_token_stream(content)
    root_strings = []
    for tnode in transnodes:
        tnode.collect_tokens(token_stream=token_stream)
        root_strings.append(tnode.python_string)
    
    signature = f"# Creation Time: {timestamp()}\n# File: {filename}\n"
    fp = os.path.join(project_directory, filename.string() + ".py")
    
    with open(fp, "w") as f:
        f.write(signature)
        for x in root_strings:
            f.write(x+"\n")
        f.write("\n")
    
    
if __name__ == "__main__":
    transpile_lua(".\\testproj\\test.lua")