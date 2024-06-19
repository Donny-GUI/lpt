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
from transform.lua import get_subtype, has_args, has_body, hasbody, hasargs


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
    #  start here
    possible = []
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
    argstr = ", ".join([make_Expression(arg) for arg in node.args])
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

def make_Namelist(nodes: list[astnodes.Expression]) -> str:
    return ", ".join([make_Expression(node) for node in nodes])

def make_Body(node: astnodes.Function|astnodes.Call|astnodes.AnonymousFunction|
              astnodes.Do|astnodes.ElseIf|astnodes.Forin|astnodes.Fornum|astnodes.If|
              astnodes.Invoke|astnodes.LocalFunction|astnodes.Method):
    return [transform_lua_node(x) for x in node.body]

def make_Function(node: astnodes.Function) -> str:
    tag = f"def {make_Name(node.name)}({make_Namelist(node.args)}):"
    return tag + '\n' "\n\t".join([make_Body(node)])
    
def make_Goto(node: astnodes.Goto) -> str:
    pyeqv = lua_to_python_node[node]
    return "<NOT IMPLEMENTED>"
    
def make_GreaterOrEqThanOp(node: astnodes.GreaterOrEqThanOp) -> str:
    return make_Expression(node.left) + " >= " + make_Expression(node.right)
    
def make_GreaterThanOp(node: astnodes.GreaterThanOp) -> str:
    return " > "
    
def make_If(node: astnodes.If) -> str:
    tag = f"if {make_Expression(node.test)}:"
    body = make_Body(node.body)
    other = make_Expression(node.orelse)
    return f"{tag}\n\t{'\n\t'.join(body)}{other}"
    
def make_Index(node: astnodes.Index) -> str:
    return f"{node.display_name}[{make_Expression(node.idx)}]"
    
def make_Invoke(node: astnodes.Invoke) -> str:
    args = make_Namelist(node.args)
    s = make_Expression(node.source)
    return f"\tdef {node.func.display_name}(self, {args}):"
    
def make_Label(node: astnodes.Node) -> str:
    pyeqv = lua_to_python_node[node]
    return "<NOT IMPLEMENTED (make_Label)>"
    
def make_LessOrEqThanOp(node: astnodes.LessOrEqThanOp) -> str:
    return ">="
    
def make_LessThanOp(node: astnodes.LessThanOp) -> str:
    return "<"
    
def make_Lhs(node: astnodes.Lhs) -> str:
    return f"<NOT IMPLEMENTED (make_Lhs) [{node.display_name}]>"

def make_LocalAssign(node: astnodes.Node) -> str:
    return make_Assign(node)
    
def make_LocalFunction(node: astnodes.Node) -> str:
    return make_Function(node)
    
def make_Method(node: astnodes.Method) -> str:
    return make_Invoke(node)
    
def make_ModOp(node: astnodes.Node) -> str:
    return "%"
    
def make_MultOp(node: astnodes.Node) -> str:
    return "*"
    
def make_Name(node: astnodes.Node) -> str:
    return f"{node.display_name}"
    
def make_Nil(node: astnodes.Node) -> str:
    return "None"
       
def make_NotEqToOp(node: astnodes.NotEqToOp) -> str:
    return "!="
    
def make_Number(node: astnodes.Number) -> str:
    return f"{make_Expression(node)}"
    
def make_OrLoOp(node: astnodes.OrLoOp) -> str:
    return  "|"
    
def make_Repeat(node: astnodes.Repeat) -> str:
    return f"<NOT IMPLEMENTED (make_Repeat)>"
    
def make_Return(node: astnodes.Return) -> str:
    return f"return {make_Namelist(node.values)}"
    
def make_SemiColon(node: astnodes.SemiColon) -> str:
    return ";"
    
def make_Statement(node: astnodes.Node) -> str:
    for sc in get_subtype(node):
        try:
            return node_function_map[sc](node)
        except:
            pass
    return ""
    
def make_String(node: astnodes.String) -> str:
    return f'"{node.s}"'
    
def make_SubOp(node: astnodes.SubOp) -> str:
    return "-"
    
def make_Table(node: astnodes.Table) -> str:
    rbracket = "{"
    lbracket = "}"
    tag = f"{node.display_name} = {rbracket}\t"
    fs = ",\n\t".join([make_Field(x) for x in node.fields])
    return f"{tag}{fs}\n\t{lbracket}"
    
def make_TrueExpr(node: astnodes.TrueExpr) -> str:
    return f"<Not Implemented (make_TrueExpr) [{node.display_name}]>"
    
def make_UBNotOp(node: astnodes.UBNotOp) -> str:
    return "!="
    
def make_ULNotOp(node: astnodes.ULNotOp) -> str:
    return "not"
    
def make_ULengthOP(node: astnodes.ULengthOP) -> str:
    return f"len({node.display_name})"
    
def make_UMinusOp(node: astnodes.Node) -> str:
    return "-"
    
def make_Varargs(node: astnodes.Varargs) -> str:
    return f"<Not Implemented (make_Varargs) {node.display_name}>"
    
def make_While(node: astnodes.While) -> str:
    tag = "while True:"
    bb= "\n\t".join(make_Body(node))
    return f"{tag}\n\t{bb}"
    
def make_Require(node: Require) -> str:
    return f"<Not Implemented (make_Require) {node}>"
    
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
    astnodes.LocalAssign:make_LocalAssign,
    astnodes.LocalFunction:make_LocalFunction,
    astnodes.Method:make_Method,
    astnodes.ModOp:make_ModOp,
    astnodes.MultOp:make_MultOp,
    astnodes.Name:make_Name,
    astnodes.Nil:make_Nil,
    astnodes.NotEqToOp:make_NotEqToOp,
    astnodes.Number:make_Number,
    astnodes.OrLoOp:make_OrLoOp,
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
    astnodes.Varargs:make_Varargs,
    astnodes.While:make_While,
    astnodes.Expression: make_Expression,
    Require:make_Require,
}

lua_operators = [astnodes.AddOp, astnodes.AndLoOp, astnodes.AriOp, astnodes.BAndOp, astnodes.BOrOp, astnodes.BShiftLOp, astnodes.BShiftROp, astnodes.BXorOp, astnodes.BinaryOp, astnodes.BitOp, astnodes.EqToOp, astnodes.ExpoOp, astnodes.FloatDivOp, astnodes.FloorDivOp, astnodes.GreaterOrEqThanOp, astnodes.GreaterThanOp, astnodes.LessOrEqThanOp, astnodes.LessThanOp, astnodes.LoOp, astnodes.ModOp, astnodes.MultOp, astnodes.NotEqToOp, astnodes.Op, astnodes.OrLoOp, astnodes.RelOp, astnodes.SubOp, astnodes.UBNotOp, astnodes.ULNotOp, astnodes.ULengthOP, astnodes.UMinusOp, astnodes.UnaryOp]

def try_subtypes(node:astnodes.Node):
    for x in get_subtype(node):
        try:
            return transform_lua_node(x)
        except:
            pass
    return "<NOT IMPLEMENT (try_subtypes)>"

def transform_lua_node(node: LUAAST) -> str:
    try:
        function = node_function_map[node]
        return function(node)
    except KeyError:
        return try_subtypes(node)





