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
    from tools.source import python_ast_classes, python_ast_names, get_luaast_names, get_ast_names
    allow_local_modules()
from luaparser.astnodes import Node
from luaparser import astnodes
from templates.lua import get_subtype


class Require(Node):
    def __init__(self, name: str, path: str, comments: astnodes.List[astnodes.Comment] | None = None, first_token: astnodes.CommonToken | None = None, last_token: astnodes.CommonToken | None = None):
        super().__init__(name, comments, first_token, last_token)
        self.path = path

LUAAST = Node
lua_to_python_node = {
    astnodes.AddOp: ast.Add,                           # Addition operator
    astnodes.AndLoOp: ast.And,                         # Logical AND operator
    astnodes.AnonymousFunction: ast.Lambda,            # Anonymous function (lambda)
    astnodes.AriOp: [ast.Add, ast.Sub, ast.Mult, ast.Div],   # Arithmetic operators
    astnodes.Assign: ast.Assign,                       # Assignment
    astnodes.BAndOp: ast.BitAnd,                       # Bitwise AND operator
    astnodes.BOrOp: ast.BitOr,                         # Bitwise OR operator
    astnodes.BShiftLOp: ast.LShift,                    # Left bitwise shift
    astnodes.BShiftROp: ast.RShift,                    # Right bitwise shift
    astnodes.BXorOp: ast.BitXor,                       # Bitwise XOR operator
    astnodes.BinaryOp: ast.BinOp,                      # Binary operation
    astnodes.BitOp: [ast.BitAnd, ast.BitOr, ast.BitXor, ast.LShift, ast.RShift],  # Bitwise operations
    astnodes.Block: ast.Module,                        # Block of statements (module)
    astnodes.Break: ast.Break,                         # Break statement
    astnodes.Call: ast.Call,                           # Function call
    astnodes.Chunk: ast.Module,                        # Entire chunk of code (module)
    astnodes.Comment: None,                          # Comments (ignored in Python AST)
    astnodes.Concat: [ast.BinOp],                        # Concatenation (binary operation)
    astnodes.Do: ast.Expr,                             # Do statement (expression grouping)
    astnodes.Dots: ast.Ellipsis,                         # Vararg (`...`)
    astnodes.ElseIf: ast.If,                           # ElseIf clause (part of If)
    astnodes.EqToOp: ast.Eq,                           # Equality operator
    astnodes.ExpoOp: ast.Pow,                          # Exponentiation operator
    astnodes.Expression: ast.Expr,                     # Expression
    astnodes.FalseExpr: ast.Constant,                  # False literal (constant)
    astnodes.Field: ast.Dict,                          # Table field (dictionary)
    astnodes.FloatDivOp: ast.Div,                      # Float division operator
    astnodes.FloorDivOp: ast.FloorDiv,                 # Floor division operator
    astnodes.Forin: ast.For,                           # Generic for loop
    astnodes.Fornum: ast.For,                          # Numeric for loop
    astnodes.Function: ast.FunctionDef,                # Function definition
    astnodes.Goto: None,                             # Goto statement (no direct equivalent)
    astnodes.GreaterOrEqThanOp: ast.GtE,               # Greater than or equal operator
    astnodes.GreaterThanOp: ast.Gt,                    # Greater than operator
    astnodes.If: ast.If,                               # If statement
    astnodes.Index: ast.Subscript,                     # Table indexing (subscripting)
    astnodes.Invoke: ast.Call,                         # Method invocation (function call)
    astnodes.Label: None,                            # Label (no direct equivalent)
    astnodes.LessOrEqThanOp: ast.LtE,                  # Less than or equal operator
    astnodes.LessThanOp: ast.Lt,                       # Less than operator
    astnodes.Lhs: ast.Name,                            # Left-hand side of assignment
    astnodes.LoOp: [ast.And, ast.Or],                    # Logical operations
    astnodes.LocalAssign: ast.Assign,                  # Local assignment
    astnodes.LocalFunction: ast.FunctionDef,           # Local function definition
    astnodes.Method: ast.FunctionDef,                  # Method definition (treated as function)
    astnodes.ModOp: ast.Mod,                           # Modulus operator
    astnodes.MultOp: ast.Mult,                         # Multiplication operator
    astnodes.Name: ast.Name,                           # Identifier (name)
    astnodes.Nil: ast.Constant,                        # Nil literal (constant None)
    astnodes.Node: ast.AST,                            # Base node type
    astnodes.NotEqToOp: ast.NotEq,                     # Inequality operator
    astnodes.Number: ast.Constant,                     # Number literal (constant)
    astnodes.Op: [ast.BinOp, ast.UnaryOp],               # General operator (binary or unary)
    astnodes.OrLoOp: ast.Or,                           # Logical OR operator
    astnodes.RelOp: [ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE],  # Relational operations
    astnodes.Repeat: ast.While,                        # Repeat-until loop (while loop)
    astnodes.Return: ast.Return,                       # Return statement
    astnodes.SemiColon: None,                        # Semicolon (no direct equivalent)
    astnodes.Statement: ast.stmt,                      # General statement
    astnodes.String: ast.Constant,                     # String literal (constant)
    astnodes.SubOp: ast.Sub,                           # Subtraction operator
    astnodes.Table: ast.Dict,                          # Table constructor (dictionary)
    astnodes.TrueExpr: ast.Constant,                   # True literal (constant)
    astnodes.UBNotOp: ast.Invert,                      # Bitwise NOT operator
    astnodes.ULNotOp: ast.Not,                         # Logical NOT operator
    astnodes.ULengthOP: ast.Call,                      # Length operator (len() call in Python)
    astnodes.UMinusOp: ast.USub,                       # Unary minus operator
    astnodes.UnaryOp: ast.UnaryOp,                     # Unary operation
    astnodes.Varargs: ast.Starred,                     # Varargs (`...` or starred expression)
    astnodes.While: ast.While,                       # While loop
    Require:ast.Import
}

lua_to_python_operators = {
    '+': '+',               # Addition
    '-': '-',               # Subtraction
    '*': '*',               # Multiplication
    '/': '/',               # Division
    '%': '%',               # Modulo
    '^': '**',              # Exponentiation
    '//': '//',             # Floor division

    '==': '==',             # Equality
    '~=': '!=',             # Inequality
    '<': '<',               # Less than
    '<=': '<=',             # Less than or equal to
    '>': '>',               # Greater than
    '>=': '>=',             # Greater than or equal to

    'and': 'and',           # Logical AND
    'or': 'or',             # Logical OR
    'not': 'not',           # Logical NOT

    '&': '&',               # Bitwise AND
    '|': '|',               # Bitwise OR
    '~': '^',               # Bitwise XOR
    '<<': '<<',             # Left shift
    '>>': '>>',             # Right shift
    '~': '~',               # Bitwise NOT

    '..': '+',              # String concatenation
    '#': 'len'              # Length of table or string
}
node_map = {
    astnodes.Block: ast.Module,  # Top-level structure for both
    astnodes.Assign: ast.Assign,  # Variable assignment
    astnodes.LocalAssign: ast.Assign,  # Local variable assignment in Lua
    astnodes.Function:[ast.FunctionDef, ast.AsyncFunctionDef],  # Function definition
    astnodes.LocalFunction:[ast.FunctionDef, ast.AsyncFunctionDef],  # Local function definition
    astnodes.Table: ast.Dict,  # Tables in Lua similar to dictionaries in Python
    astnodes.If: ast.If,  # Conditional statements
    astnodes.Fornum: ast.For,  # Numeric for loop in Lua to for loop in Python
    astnodes.Forin: ast.For,  # Generic for loop in Lua to for loop in Python
    astnodes.While: ast.While,  # While loop
    astnodes.Repeat: ast.While,  # Repeat-until loop in Lua to while loop in Python
    astnodes.Call: ast.Call,  # Function call
    astnodes.Return: ast.Return,  # Return statement
    astnodes.BinaryOp: ast.BinOp,  # Binary operations
    astnodes.UnaryOp: ast.UnaryOp,  # Unary operations
    astnodes.Name: ast.Name,  # Identifiers
    astnodes.Index: ast.Subscript,  # Indexing in Lua tables to subscripting in Python
    astnodes.Do: None,  # Do statements for expression execution
    astnodes.Break: ast.Break,  # Break statement in loops
    astnodes.String: ast.Constant,  # Literal values
    astnodes.Table: ast.Dict,  # Key-value pairs in Lua tables
    astnodes.Field: [ast.List, ast.Dict, ast.Constant, ast.Call, ast.Name, ast.Tuple],  # Values in Lua tables
    astnodes.AnonymousFunction: ast.Lambda,  # Anonymous functions
    astnodes.Varargs: ast.Starred,  # Vararg expressions similar to starred expressions
    astnodes.Comment: None,  # Comments are ignored in the AST
    astnodes.Label: None,  # Labels for gotos (no direct Python equivalent)
    astnodes.Goto:None,  # Goto statements (no direct Python equivalent)
    astnodes.While: ast.While  # Repeat-until loop (mapped to while with condition inversion)
}

def make_Expression(node: astnodes.Expression):
    for st in get_subtype(node):
        try:
            x = node_function_map[st](node)
            return x  
        except:
            pass

def make_Statement(node: astnodes.Statement):
    for st in get_subtype(node):
        try:
            x = node_function_map[st](node)
            return x  
        except:
            pass

def make_AddOp(node: astnodes.Node) -> str:
    return "+"
    
def make_AndLoOp(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return "and"
    
def make_AnonymousFunction(node: astnodes.AnonymousFunction) -> str:
    return f"lambda: {node.display_name}"
    
def make_Assign(node: astnodes.Assign) -> str:
    return f"{node.display_name} = "
    
def make_BAndOp(node: astnodes.BAndOp) -> str:
    return "||"
    
def make_BOrOp(node: astnodes.BOrOp) -> str:
    return "|"
    
def make_BShiftLOp(node: astnodes.Node) -> str:
    return "<<"
    
def make_BShiftROp(node: astnodes.Node) -> str:
    return ">>"
    
def make_BXorOp(node: astnodes.Node) -> str:
    return "^"

def make_Block(node: astnodes.Block) -> str:
    collection = []
    for x in node.body:
        collection.append(transform_lua_node(x))
    return collection
    
def make_Break(node: astnodes.Node) -> str:
    return "break"
    
def make_Call(node: astnodes.Call) -> str:
    argstr = ", ".join([arg.display_name for arg in node.args])
    return f"{node.func.display_name}({argstr})"
    
    
def make_Chunk(node: astnodes.Chunk) -> str:
    collection = []
    for n in node.body:
        collection.append(transform_lua_node(n))
    return collection
    
def make_Comment(node: astnodes.Comment) -> str:
    return f"# {node.s[2:]}"
    
def make_Concat(node: astnodes.Node) -> str:
    return "+"
    
def make_Do(node: astnodes.Node) -> str:
    return ""
    
def make_Dots(node: astnodes.Node) -> str:
    return "..."
    
def make_ElseIf(node: astnodes.Node) -> str:
    return "elif"
    
def make_EqToOp(node: astnodes.Node) -> str:
    return "=="
    
def make_ExpoOp(node: astnodes.ExpoOp) -> str:
    return "^"
    
def make_Field(node: astnodes.Field) -> str:
    if node.between_brackets == True:
        return f"{node.key} = {node.value},"
    return node.display_name

def make_FloatDivOp(node: astnodes.Node) -> str:
    return "/"
    
def make_FloorDivOp(node: astnodes.Node) -> str:
    return "//"
    
def make_Forin(node: astnodes.Forin) -> str:
    targets = ", ".join([make_Name(x) for x in node.targets])
    tag = f"for {targets} in {node.display_name}:"
    bb = [make_Expression(x) for x in node.body]
    return tag + "\n\t".join(bb)
    
def make_Fornum(node: astnodes.Fornum) -> str:
    try:
        s = make_Expression(node.step)
        s = f"{s},"
    except:
        s = ""
    tag = f"for {node.target} in range({make_Expression(node.start)}{s}{make_Expression(node.stop)}):"
    bb = [make_Expression(x) for x in node.body]
    return tag + "\n\t".join(bb)
    
def make_Function(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_Goto(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_GreaterOrEqThanOp(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_GreaterThanOp(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_If(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_Index(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_Invoke(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_Label(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_LessOrEqThanOp(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_LessThanOp(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_Lhs(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_LoOp(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_LocalAssign(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_LocalFunction(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_Method(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_ModOp(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_MultOp(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_Name(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_Nil(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_Node(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_NotEqToOp(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_Number(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_Op(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_OrLoOp(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_RelOp(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_Repeat(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_Return(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_SemiColon(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_Statement(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_String(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_SubOp(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_Table(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_TrueExpr(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_UBNotOp(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_ULNotOp(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_ULengthOP(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_UMinusOp(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_UnaryOp(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_Varargs(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_While(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    
def make_Require(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return None
    



node_function_map = {
    astnodes.AddOp:make_AddOp,
    astnodes.AndLoOp:make_AndLoOp,
    astnodes.AnonymousFunction:make_AnonymousFunction,
    astnodes.Assign:make_Assign,
    astnodes.BAndOp:make_BAndOp,
    astnodes.BOrOp:make_BOrOp,
    astnodes.BShiftLOp:make_BShiftLOp,
    astnodes.BShiftROp:make_BShiftROp,
    astnodes.BXorOp:make_BXorOp,
    astnodes.Block:make_Block,
    astnodes.Break:make_Break,
    astnodes.Call:make_Call,
    astnodes.Chunk:make_Chunk,
    astnodes.Comment:make_Comment,
    astnodes.Concat:make_Concat,
    astnodes.Do:make_Do,
    astnodes.Dots:make_Dots,
    astnodes.ElseIf:make_ElseIf,
    astnodes.EqToOp:make_EqToOp,
    astnodes.ExpoOp:make_ExpoOp,
    astnodes.Field:make_Field,
    astnodes.FloatDivOp:make_FloatDivOp,
    astnodes.FloorDivOp:make_FloorDivOp,
    astnodes.Forin:make_Forin,
    astnodes.Fornum:make_Fornum,
    astnodes.Function:make_Function,
    astnodes.Goto:make_Goto,
    astnodes.GreaterOrEqThanOp:make_GreaterOrEqThanOp,
    astnodes.GreaterThanOp:make_GreaterThanOp,
    astnodes.If:make_If,
    astnodes.Index:make_Index,
    astnodes.Invoke:make_Invoke,
    astnodes.Label:make_Label,
    astnodes.LessOrEqThanOp:make_LessOrEqThanOp,
    astnodes.LessThanOp:make_LessThanOp,
    astnodes.Lhs:make_Lhs,
    astnodes.LoOp:make_LoOp,
    astnodes.LocalAssign:make_LocalAssign,
    astnodes.LocalFunction:make_LocalFunction,
    astnodes.Method:make_Method,
    astnodes.ModOp:make_ModOp,
    astnodes.MultOp:make_MultOp,
    astnodes.Name:make_Name,
    astnodes.Nil:make_Nil,
    astnodes.Node:make_Node,
    astnodes.NotEqToOp:make_NotEqToOp,
    astnodes.Number:make_Number,
    astnodes.Op:make_Op,
    astnodes.OrLoOp:make_OrLoOp,
    astnodes.RelOp:make_RelOp,
    astnodes.Repeat:make_Repeat,
    astnodes.Return:make_Return,
    astnodes.SemiColon:make_SemiColon,
    astnodes.Statement:make_Statement,
    astnodes.String:make_String,
    astnodes.SubOp:make_SubOp,
    astnodes.Table:make_Table,
    astnodes.TrueExpr:make_TrueExpr,
    astnodes.UBNotOp:make_UBNotOp,
    astnodes.ULNotOp:make_ULNotOp,
    astnodes.ULengthOP:make_ULengthOP,
    astnodes.UMinusOp:make_UMinusOp,
    astnodes.UnaryOp:make_UnaryOp,
    astnodes.Varargs:make_Varargs,
    astnodes.While:make_While,
    astnodes.Expression: make_Expression,
    Require:make_Require,
}

lua_operators = [astnodes.AddOp, astnodes.AndLoOp, astnodes.AriOp, astnodes.BAndOp, astnodes.BOrOp, astnodes.BShiftLOp, astnodes.BShiftROp, astnodes.BXorOp, astnodes.BinaryOp, astnodes.BitOp, astnodes.EqToOp, astnodes.ExpoOp, astnodes.FloatDivOp, astnodes.FloorDivOp, astnodes.GreaterOrEqThanOp, astnodes.GreaterThanOp, astnodes.LessOrEqThanOp, astnodes.LessThanOp, astnodes.LoOp, astnodes.ModOp, astnodes.MultOp, astnodes.NotEqToOp, astnodes.Op, astnodes.OrLoOp, astnodes.RelOp, astnodes.SubOp, astnodes.UBNotOp, astnodes.ULNotOp, astnodes.ULengthOP, astnodes.UMinusOp, astnodes.UnaryOp]

def transform_lua_node(node: LUAAST) -> str:
    try:
        function = node_function_map[node]
        return function(node)
    except KeyError:
        print(type(node))
        print("ERROR TRANSFORMING!!!!!")
        raise Exception(f"ERROR transforming this node {node}")
    






