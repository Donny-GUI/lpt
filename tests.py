from transpiler.transpiler import LuaToPythonTranspiler
from luaparser import ast as lua_ast
from luaparser import parser as lua_parser
from tools.file import get_files_by_extension
from tools.path import desktop_path
from tools.source import python_ast_path

print(python_ast_path())


def read_lua(filepath:str):
    with open(filepath, "r") as r:
        content = r.read()
    return content

def test_trans():
        
    transpiler = LuaToPythonTranspiler()
    for file in get_files_by_extension(desktop_path, ".lua"):
        chunk = read_lua(file)
        python = transpiler.convert_file(file)
        input()


