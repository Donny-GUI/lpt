from tokenize import detect_encoding
from typing import List, Generator
from io import TextIOWrapper
import tempfile
# Non Standard
from luaparser.ast import parse
# Local Modules
from transform.python import transform_lua_node
from typedef import LuaNode
from tools.file import force_open
from transnode import TransNode

from tools.color import *
from tools.updater import *



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

def generate_transnodes(filepath: str) -> Generator[TransNode]:
    """
    Generator for Transnodes
    Arguments:
        filepath(str): path to the file to create nodes from
    Returns (yield) :
        yields TransNodes from the filepath
    """
    enc = get_encoding(filepath)
    # get file ptr and source, then reset seek
    fp: TextIOWrapper = open(filepath, "r", encoding=enc)
    src: str
    try:
        src = fp.read()
    except:
        # safety first 
        fp.close()
        raise FileNotFoundError("Could not read from the buffer")
    finally:
        # and second
        fp.close()
    # write source to tempfile
    fp: tempfile._TemporaryFileWrapper = tempfile.TemporaryFile(prefix="__lua_source__", suffix=".lua", encoding=enc)
    fp.write(src.encode(enc))
    fp.seek(0)
    
    # generate nodes
    for index, node in enumerate(string_to_lua_nodes(src)):
        yield TransNode(node=node, index=index, source=fp)

def read_lua(filepath:str):
    """
    Get encoding of file and open file line by line
    and encoding by encoding then return a string
    Arguments:
        filepath(str) : path the lua file
    Returns:
        str : string representation of a lua file
    """
    return force_open(filepath)

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

def make_project():
    pass

def make_script():
    pass 

def transpile_lua_file(filepath:str):
    content: str = read_lua(filepath)
    has_require = lua_check_require(content)
    lua_nodes = string_to_lua_nodes(content)
    total = len(lua_nodes)
    converted = 0
    for index, node in enumerate(lua_nodes):
        pynode = transform_lua_node(node)

        converted+=1
    python_nodes = [transform_lua_node(node)
                    for node in
                    lua_file_to_lua_nodes(filepath)]

