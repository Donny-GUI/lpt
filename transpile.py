import os
import re
from tokenize import detect_encoding
from datetime import datetime
from pathlib import Path as _path
from random import randint
from typing import List, Optional
# Non-Standard
from luaparser.ast import parse
from luaparser.ast import get_token_stream
# Local 
from typedef import LuaNode
from transnode import TransNode
from dir_creator import reproduce_directory_with_conversion
from require import remove_require_statements, locate_lua_requires


class Path(_path):
    def __init__(self, *args: str | os.PathLike[str]) -> None:
        super().__init__(*args)
    
    def string(self):
        return str(self)


CWD = Path(os.getcwd())

def filename(filepath:str|Path):
    return os.path.basename(str(filepath)).split(".")[0]

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

def transpile_lua_file(lua_path: str, python_path):
    content: str = read_lua(lua_path)
    require_pattern = re.compile(r'require\s*[\'"]([^\'"]+)[\'"]')

    module_names = []
    startindex = 0
    for modname in require_pattern.finditer(content):
        startindex = modname.end()
        reqstring = modname.string[7:].strip("'").strip('"').strip("()").strip()
        req = reqstring.replace("/", ".")
        module_names.append(req)

    content = content[startindex+1:]
    transnodes: List[TransNode] = string_to_transnodes(content)
    token_stream = get_token_stream(content)

    root_strings = []
    for tnode in transnodes:
        tnode.collect_tokens(token_stream=token_stream)
        root_strings.append(tnode.python_string)

    with open(python_path, "w") as f:
        f.write("\n".join(root_strings))
        f.write("\n")

def transpile_lua_directory(directory: str) -> Optional[Path]:
    dn = directory+"_python"
    mapping = reproduce_directory_with_conversion(directory, dn)
    reqs = []
    for lua, py in mapping.items():
        luacontent = read_lua(lua)
        require_paths = locate_lua_requires(luacontent)
        reqs.extend(require_paths)
        luacont = remove_require_statements(luacontent)
        transnodes: List[TransNode] = string_to_transnodes(luacont)
        token_stream = get_token_stream(luacont)

        root_strings = []
        for tnode in transnodes:
            tnode.collect_tokens(token_stream=token_stream)
            root_strings.append(tnode.python_string)

    reqs = list(set(reqs))
    for path in reqs:
        pass 


        

def make_new_project_path(lua_name:str):
    return os.path.join(CWD, lua_name)
    
if __name__ == "__main__":

    transpile_lua(".\\testproj\\test.lua")
