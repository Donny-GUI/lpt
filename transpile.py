import os
from tokenize import detect_encoding
from datetime import datetime
from pathlib import Path
from random import randint
from typing import List, Optional
# Non-Standard
from luaparser.ast import parse
from luaparser.ast import get_token_stream
from luaparser.astnodes import Name
import shutil
# Local 
from typedef import LuaNode
from transnode import TransNode
from dir_creator import reproduce_directory_with_conversion
from require import remove_require_statements, locate_lua_requires, get_lua_require_type, require_path_to_python_import
from dataclasses import dataclass 


@dataclass
class LuaPythonPackage:
    imports = []
    requires = []
    names = []


CWD = Path(os.getcwd())

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

def transpile_lua_directory(directory: str) -> Optional[Path]:
    dn = directory+"_python"
    mapping = reproduce_directory_with_conversion(directory, dn)

    reqs = []
    for lua, py in mapping.items():
        src = []
        names = []
        # read file to string
        luacontent = read_lua(lua)
        # get the require statements 
        all_reqs = locate_lua_requires(luacontent)
        # convert them to import statements

        for r in reqs:
            imp = require_path_to_python_import(r)
            src.append(imp)

        src.append("\n")
        # add it too all reqs
        reqs.extend(all_reqs)
        # remove the require statements
        luacont = remove_require_statements(luacontent)
        # get the ast nodes for the lua_content 
        transnodes: List[TransNode] = string_to_transnodes(luacont)
        token_stream = get_token_stream(luacont)
        # Get the python string representation of the ast nodes

        for tnode in transnodes:
            tnode.collect_tokens(token_stream=token_stream)
            src.append(tnode.python_string)
        py = py.replace("/./", "/")
        os.makedirs(os.path.dirname(py), exist_ok=True)
        with open(py, "w") as f:
            for block in src:
                f.write(block+"\n")


        

    

if __name__ == "__main__":
    transpile_lua_directory("..\\decompiled")
