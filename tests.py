from transpiler.transpiler import LuaToPythonTranspiler
from luaparser import ast as lua_ast
from luaparser.ast import parse
from luaparser import parser as lua_parser
from tools.file import get_files_by_extension
from tools.path import desktop_path
from tools.source import python_ast_path
from transform.python import transform_lua_node



def read_lua(filepath:str):
    with open(filepath, "r") as r:
        content = r.read()
    return content

def test_transform():
    for file in get_files_by_extension(desktop_path, ".lua"):
        string = read_lua(file)
        nodes = parse(string)
        for node in nodes.body:
            n = transform_lua_node(node)
            print(n)

def test_trans():
        
    transpiler = LuaToPythonTranspiler()
    for file in get_files_by_extension(desktop_path, ".lua"):
        chunk = read_lua(file)
        python = transpiler.convert_file(file)
        input()


test_transform()