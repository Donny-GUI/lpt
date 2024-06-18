import ast
from luaparser import ast as lua_ast
from typing import List

###[+] Type Definitions
 
ASTNode = ast.AST|lua_ast.AST
LuaNode = lua_ast.AST
PythonNode = ast.AST
"""NOTE:
In data structures, graphs, and network theory, 
an edge [ie: PythonEdge] is a fundamental concept used to denote
a connection or relationship between nodes (also known as vertices).
"""
Edge = List[ASTNode]
LuaEdge = List[LuaNode]
PythonEdge = List[PythonNode]
