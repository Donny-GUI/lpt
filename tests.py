from transpiler.transpiler import LuaToPythonTranspiler
from luaparser.ast import parse
from luaparser.astnodes import Chunk, Node
from tools.file import get_files_by_extension
from tools.path import desktop_path
from transform.python import transform_lua_node

NODE = "\033[35mnode\033[0m"
RESULT = "\033[36mresult\033[0m"
L = "\033[46m<<<                       \033[0m"
R = "\033[46m>>>                       \033[0m"
def read_lua(filepath:str):
    with open(filepath, "r") as r:
        content = r.read()
    return content

def string_to_nodes(string):
    nodes = parse(string)
    return [node for node in nodes.body.body]

def file_to_nodes(filepath:str) -> list[Node]:
    string = read_lua(filepath=filepath)
    nodes = parse(string)
    return [node for node in nodes.body.body]


def test_transform():
    for file in get_files_by_extension(desktop_path, ".lua"):
        printtest(file)
        for node in file_to_nodes(file):
            printtest(f"{NODE}{node}")
            n = transform_lua_node(node)
            printtest(f"{RESULT} \n{L}\n{n}\n{R}")

def printtest(obj):
    print(f"[\033[32mDEBUG\033[0m]: {obj}")

def test_trans():
    transpiler = LuaToPythonTranspiler()
    for file in get_files_by_extension(desktop_path, ".lua"):
        chunk = read_lua(file)
        python = transpiler.convert_file(file)

test_transform()