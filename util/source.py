import ast
from ast import ClassDef
import os

def python_ast_path():
    a = os.path.abspath(ast)
    b = os.path.realpath(ast)
    return a, b 

def luaastpath():
    return os.path.join(os.getcwd(), "luaparser", "astnodes.py")

def astnodes():
    classes = get_all_classes(luaastpath())
    names = [c.name for c in classes]
    return names

def is_python_file(filepath):
    if filepath.endswith(".py"):
        return True
    if os.path.isfile(filepath) == True:
        with open(filepath, "r") as f:
            content = f.read()
        try:
            tree = ast.parse(content)
            ast.unparse(tree)
            return True
        except:
            return False
    return False

def get_all_classes(filepath:str) -> list[ClassDef]:
    with open(filepath, "r") as f:
        content = f.read()
    tree = ast.parse(content)
    return [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef) == True]

astns = astnodes()
print(astns)