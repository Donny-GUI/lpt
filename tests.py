from transpiler.transpiler import LuaToPythonTranspiler
from luaparser import ast as lua_ast
from luaparser import parser as lua_parser
from utility.file import get_files_by_extension
from utility.path import desktop_path


def read_lua(filepath:str):
    with open(filepath, "r") as r:
        content = r.read()
    return content

transpiler = LuaToPythonTranspiler()
for file in get_files_by_extension(desktop_path, ".lua"):
    chunk = read_lua(file)
    python = transpiler.convert_file(file)
    input()