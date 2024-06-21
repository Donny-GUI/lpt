import tempfile
import os
import re 
from io import TextIOWrapper
from typing import List, Generator
from tokenize import detect_encoding
from datetime import datetime
# Non-Standard
from luaparser.ast import parse
from luaparser.ast import get_token_stream
# Local 
from typedef import LuaNode
from tools.file import force_open
from transnode import TransNode
from tools.color import *
from tools.updater import *
from stringtable import AllowAllModulesString, MadeByString
DEBUG = True 
from tools.updater import set_debug


update, debug, init = set_debug(DEBUG)


def timestamp():
    return datetime.now().strftime()

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

def extract_require_statements2(lua_source:str) -> list[str]:
    retv = []
    for line in lua_source.splitlines():
        if line.startswith("require("):
            try:
                lidx = line.index("'")
                ridx = line.rindex("'")
            except IndexError:
                idx = line.index('"')
                idx = line.rindex('"')
            finally:
                p = line[lidx:ridx].replace(".", os.sep)
                pp = os.path.join(os.getcwd(), p)
                retv.append(pp)
    return retv 

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
    
    return matches

def transpile_lua(filepath:str, follow_requires=True):
    """
    Convert a string of lua source filepath to a string of 
    python source code.
    """
    update(f"transpile_lua(filepath={filepath} follow_requires={follow_requires})")
    content: str = read_lua(filepath)
    filename = os.path.basename(filepath).split(".")[0]
    root_dir = os.path.dirname(filepath)

    def transpile_submodule(filepath: str, project_directory, sm_name:str) -> str:
        update(f"transpile_submodule {filepath} {project_directory} {sm_name}")
        final = []
        content: str = read_lua(filepath)
        filename = os.path.basename(filepath).split(".")[0]
        root_dir = os.path.dirname(filepath)
        module_name = os.path.basename(root_dir)
        transnodes:list[TransNode] = string_to_transnodes(content)
        token_stream = get_token_stream(content)

        for tnode in transnodes:
            tnode.collect_tokens(token_stream=token_stream)
            final.append(tnode.python_string)

        filename+=".py"
        fullp = os.path.join(project_directory, sm_name, filename)
        f = f"# Creation Time: {timestamp()}\n# Module: {module_name}\n# File: {filename}\n# User: {os.getlogin()}\n"

        with open(fullp, "w") as f:
            f.write(f)
            for x in final:
                f.write(x)
                f.write("\n")
            f.write("\n")

        return fullp
    
    def transpile_root_module(filepath:str, project_dir: str) -> str:
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
    
    def get_submodule_name(filepath:str):
        return os.path.basename(os.path.dirname(filepath))
    
    def init_submodule(module_name: str, project_dir:str):
        p = os.path.join(project_dir, module_name)
        if os.path.exists(p) == True:
            return
        os.makedirs(p, exist_ok=True)
        init_ = os.path.join(p, "__init__.py")
        with open(init_, "w") as r:
            r.close()
    
    cwd = os.getcwd()
    print(cwd)
    if filepath.startswith(".."):
        filepath = os.path.join(cwd, filepath[2:])
    
    if filepath.startswith("."):
        filepath = os.path.join(cwd, filepath[1:])

    # make project directory
    project_name = os.path.basename(filepath).split(".")[0] + "_" + str(hash(filepath))
    project_directory = os.path.join(os.getcwd(), project_name)
    os.makedirs(name=project_directory, exist_ok=True)

    #[1] begin root transpile

    ##[1.1] Read source string
    root_dir = os.path.dirname(filepath)
    print("filepath: ", filepath)
    content: str = read_lua(filepath)
    
    ###[1.2] Get require statements (imports)
    requires = extract_require_statements2(content) \
        if lua_check_require(content) == True else []
    
    ####[1.3] Get requires and transpile them if necessary
    if follow_requires == True:
        for req in requires:
            # transpile a module that is on the same level as the root file
            if os.path.dirname(req) == root_dir:
                # is same directory as root
                transpile_root_module(req, project_directory)
            # make a submodule if it doesnt exist and transpile source to it
            elif os.path.dirname(req) != root_dir:
                # is sub module 
                sub_module_name = get_submodule_name(req)
                init_submodule(sub_module_name, project_dir=project_directory)
                transpile_submodule(req, project_directory, sub_module_name)

    ####[1.3] Acquire Trans nodes and stream
    transnodes:list[TransNode] = string_to_transnodes(content)
    token_stream = get_token_stream(content)

    root_strings = []
    for tnode in transnodes:
        tnode.collect_tokens(token_stream=token_stream)
        root_strings.append(tnode.python_string)
    
    filename = os.path.basename(filepath).split(".")[0]
    root_dir = os.path.dirname(filepath)
    signature = f"# Creation Time: {timestamp()}\n# File: {filename}\n"
    filename+=".py"
    fp = os.path.join(project_directory, filename)
    
    with open(fp, "w") as f:
        f.write(signature)
        for x in root_strings:
            f.write(x+"\n")
        f.write("\n")
    
    
if __name__ == "__main__":
    transpile_lua(".\\testproject\\test.lua")