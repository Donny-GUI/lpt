from transpiler.transpiler import LuaToPythonTranspiler
from luaparser.ast import parse
from luaparser.astnodes import Chunk, Node
from tools.file import get_files_by_extension
from tools.path import desktop_path
from transform.python import transform_lua_node, get_total_nodes
from tools.symbols import LARROWS, RARROWS, NODE, RESULT
from tools.file import force_open





def read_lua(filepath:str):
    return force_open(filepath)

def string_to_nodes(string):
    nodes = parse(string)
    return [node for node in nodes.body.body]

def file_to_nodes(filepath:str) -> list[Node]:
    string = read_lua(filepath=filepath)
    nodes = parse(string)
    return [node for node in nodes.body.body]

def transpile_lua(filepath:str):
    python_nodes = [transform_lua_node(node)
                    for node in
                    file_to_nodes(filepath)]

def test_transform():
    for file in get_files_by_extension(desktop_path, ".lua"):
        printtest(file)
        for node in file_to_nodes(file):
            printtest(f"{NODE}{node}")
            n = transform_lua_node(node)
            printtest(f"{RESULT} \n{LARROWS}\n{n}\n{RARROWS}")


def printtest(obj):
    print(f"[\033[32mDEBUG\033[0m]: {obj}")

def test_trans():
    transpiler = LuaToPythonTranspiler()
    for file in get_files_by_extension(desktop_path, ".lua"):
        chunk = read_lua(file)
        python = transpiler.convert_file(file)

test_transform()