import ast
import os


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

def get_all_classes(filepath:str) -> list[ast.ClassDef]:
    with open(filepath, "r") as f:
        content = f.read()
    tree = ast.parse(content)
    return [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef) == True]

