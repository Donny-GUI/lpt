import ast

import sys
import os
try:
    from tools.path import allow_local_modules
except:
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.insert(0, parent_dir)
finally:
    from tools.path import allow_local_modules
    from tools.source import class_names
    allow_local_modules()

from tools.source import python_ast_path

def get_ast_names():
    return [attr for attr in dir(ast) 
                  if isinstance(getattr(ast, attr), type) 
                  and issubclass(getattr(ast, attr), ast.AST)]

print(get_ast_names())

