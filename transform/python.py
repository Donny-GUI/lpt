import sys
import os
try:
    from tools.path import allow_local_modules
except:
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.insert(0, parent_dir)
finally:
    from tools.path import allow_local_modules
    allow_local_modules()
from luaparser.astnodes import Node
from luaparser import astnodes
from transform.lua import get_subtype, all_nodes
from functools import lru_cache

total_nodes = []

LUAAST = Node


def make_Expression(node: astnodes.Expression):
    if node == None:
        return ""
    return str(node_function_map[tokey(node)](node))

def panic(node: astnodes.Node):
    try:
        x = make_Number(node)
        return x
    except:
        pass
    try:
        x = make_Table(node)
        return x
    except: 
        pass
    
    for n in all_nodes:
        k = tokey(n)
        try:
            x= node_function_map[k](node)
            if x == None:
                return ""
            return x
        except:
            pass
    try:
        x = make_either(node)
        return x
    except:
        raise Exception(f"Panic Failed....\n{k} \n{node}")

def make_Statement(node: astnodes.Statement):
    #if node == None:
    #    return "? None"
    sbtypes = get_subtype(tokey(node))
    if sbtypes != None:
        for st in sbtypes:
            try:
                x = node_function_map[tokey(st)](node)
                return str(x)  
            except:
                pass
    return panic(node)
    
def make_either(node: astnodes.Expression|astnodes.Statement):
    try:
        x = make_Expression(node)
        if x == None or x == "":
            try:
                return make_Statement(node)
            except:
                return panic(node)
        return x
    except:
        pass
    try:
        return make_Statement(node)
    except:
        panic(node)

def make_AddOp(node: astnodes.AddOp) -> str:
    return f"{make_either(node.left)} + {make_either(node.right)}"

def make_AndLoOp(node: astnodes.AndLoOp) -> str:
    return f"{make_either(node.left)} and {make_either(node.right)}"

def make_AnonymousFunction(node: astnodes.AnonymousFunction) -> str:
    return f"lambda: {node.display_name}"

def make_Assign(node: astnodes.Assign) -> str:
    return f"{make_Namelist(node.targets)} = {make_Namelist(node.values)}"

def make_BAndOp(node: astnodes.BAndOp) -> str:
    return f"{make_either(node.left)} & {make_either(node.right)}"

def make_BOrOp(node: astnodes.BOrOp) -> str:
    return f"{make_either(node.left)}|{make_either(node.right)}"

def make_BShiftLOp(node: astnodes.BShiftLOp) -> str:
    return f"{make_either(node.left)}<<{make_either(node.right)}"

def make_BShiftROp(node: astnodes.BShiftROp) -> str:
    return f"{make_either(node.left)}>>{make_either(node.right)}"

def make_BXorOp(node: astnodes.BXorOp) -> str:
    return f"{make_either(node.left)}^{make_either(node.right)}"

def make_Block(node: astnodes.Block) -> str:
    collection = []
    for x in node.body:
        collection.append(transform_lua_node(x))
    return collection

def make_Break(node: astnodes.Break) -> str:
    return "break"

def make_Call(node: astnodes.Call) -> str:
    argstr = ", ".join([make_Expression(arg) for arg in node.args])
    return f"{make_Expression(node.func)}({argstr})"

def make_Chunk(node: astnodes.Chunk) -> str:
    collection = []
    for n in node.body:
        collection.append(transform_lua_node(n))
    return collection

def make_Comment(node: astnodes.Comment) -> str:
    return f"# {node.s[2:]}"

def make_Concat(node: astnodes.Concat) -> str:
    return f"+"

def make_Do(node: astnodes.Do) -> str:
    return ""

def make_Dots(node: astnodes.Dots) -> str:
    return "..."

def make_ElseIf(node: astnodes.ElseIf) -> str:
    return "elif"

def make_EqToOp(node: astnodes.EqToOp) -> str:
    return f"{make_either(node.left)} == {make_either(node.right)}"

def make_ExpoOp(node: astnodes.ExpoOp) -> str:
    return make_either(node.left) + "**" + make_either(node.right)

def make_FieldValue(node: astnodes.Field):
    return make_Expression(node)

def make_Field(node: astnodes.Field) -> str:
    if isinstance(node.key, astnodes.Number):
        kk = make_Number(node.key)
        return f"'{kk}' : {make_FieldValue(node.value)},"
    else:
        kk = node.key
        if isinstance(kk, astnodes.String):
            return f"'{kk.s}' : {make_FieldValue(node.value)},"    
        return f"'{kk.id}' : {make_FieldValue(node.value)},"

def make_FloatDivOp(node: astnodes.Node) -> str:
    return "/"

def make_FloorDivOp(node: astnodes.Node) -> str:
    return "//"

def make_Forin(node: astnodes.Forin) -> str:
    targets = ", ".join([make_either(x) for x in node.targets])
    tag = f"for {targets} in {node.display_name}:"
    try:
        bb = [make_Expression(x) for x in node.body]
    except: 
        bb = [make_Expression(x) for x in node.body.body]
    return tag + "\n\t".join(bb)

def make_Fornum(node: astnodes.Fornum) -> str:
    try:
        s = make_Number(node.step)
        s = f"{s},"
    except:
        s = ""
    tag = f"for {node.target} in range({make_Expression(node.start)}{s}{make_Expression(node.stop)}):"
    try:
        bb = [make_Expression(x) for x in node.body]
    except:
        bb = [make_Expression(x) for x in node.body.body]
    return tag + "\n\t".join(bb)

def make_Body(node: astnodes.Function|astnodes.Call|astnodes.AnonymousFunction|
              astnodes.Do|astnodes.ElseIf|astnodes.Forin|astnodes.Fornum|astnodes.If|
              astnodes.Invoke|astnodes.LocalFunction|astnodes.Method):
    retv = []
    indent = 1
    nbi = node.body

    if isinstance(nbi, astnodes.Block):
        nbi = node.body.body

    for x in nbi:
        y = [make_Expression(x)]

        for i in range(0, indent):
            y.insert(0, "    ")

        if y[-1].strip().endswith(":"):
            indent+=1

        retv.append("".join(y))
    return retv 

def make_Function(node: astnodes.Function) -> str:
    tag = f"def {make_Name(node.name)}({make_Namelist(node.args)}):"
    try:
        return tag + '\n' + "\n\t".join([make_Body(node)])
    except:
        return tag + '\n' + "\n\t".join(make_Body(node))

def make_Goto(node: astnodes.Goto) -> str:
    return "<NOT IMPLEMENTED>"

def make_GreaterOrEqThanOp(node: astnodes.GreaterOrEqThanOp) -> str:
    return make_either(node.left) + " >= " + make_either(node.right)

def make_GreaterThanOp(node: astnodes.GreaterThanOp) -> str:
    return f"{make_either(node.left)} > {make_either(node.right)}"

def make_If(node: astnodes.If) -> str:
    tag = f"if {make_Expression(node.test)}:"
    body = make_Body(node.body)
    other = make_Expression(node.orelse)
    return f"{tag}\n{"\n".join(body)}{other}"

def make_Index(node: astnodes.Index) -> str:
    return f"{make_Expression(node.value)}.{make_Expression(node.idx)}"

def make_Invoke(node: astnodes.Invoke) -> str:
    return ":"

def make_Label(node: astnodes.Node) -> str:
    return "<NOT IMPLEMENTED (make_Label)>"

def make_LessOrEqThanOp(node: astnodes.LessOrEqThanOp) -> str:
    return f"{make_either(node.left)} >= {make_either(node.right)}"

def make_LessThanOp(node: astnodes.LessThanOp) -> str:
    return f"{make_either(node.left)} < {make_either(node.right)}"

def make_Lhs(node: astnodes.Lhs) -> str:
    total_nodes.append([astnodes.Lhs, node])
    return f"<NOT IMPLEMENTED (make_Lhs) [{node.display_name}]>"

def make_LocalAssign(node: astnodes.LocalAssign) -> str:
    return make_Assign(node)

def make_LocalFunction(node: astnodes.Node) -> str:
    return make_Function(node)

def make_Method(node: astnodes.Method) -> str:
    nl = make_Namelist(node.args)
    s = ", "
    if nl == "":
        s = ""
    tag = f"def {make_Name(node.name)}(self{s}{make_Namelist(node.args)}):"
    bb = "\n".join(make_Body(node.body))
    return f"{tag}\n{bb}\n"

def make_ModOp(node: astnodes.ModOp) -> str:
    return f"{make_either(node.left)} % {make_either(node.right)}"

def make_MultOp(node: astnodes.MultOp) -> str:
    return f"{make_either(node.left)}*{make_either(node.right)}"

def make_Name(node: astnodes.Name) -> str:
    if isinstance(node, astnodes.Index):
        return node.idx.id
    return f"{node.id}"

def make_Namelist(nodes: list[astnodes.Expression]) -> str:
    items = []
    if isinstance(nodes, bool):
        return str(nodes)
    for item in nodes:
        x = make_Expression(item)
        items.append(str(x))
    return ", ".join(items)

def make_Nil(node: astnodes.Nil) -> str:
    return "None"

def make_NotEqToOp(node: astnodes.NotEqToOp) -> str:
    return f"{make_either(node.left)} != {make_either(node.right)}"

def make_Number(node: astnodes.Number) -> str:
    return node.n

def make_OrLoOp(node: astnodes.OrLoOp) -> str:
    l = make_either(node.left)
    r = make_either(node.right)
    return  f"{l} if {l}  else {r}"

def make_Repeat(node: astnodes.Repeat) -> str:
    return f"<NOT IMPLEMENTED (make_Repeat)>"

def make_Return(node: astnodes.Return) -> str:
    return f"return {make_Namelist(node.values)}"

def make_SemiColon(node: astnodes.SemiColon) -> str:
    return ";"

def make_String(node: astnodes.String) -> str:
    return f'"{node.s}"'

def make_SubOp(node: astnodes.SubOp) -> str:
    return f"{make_either(node.left)} - {make_either(node.right)}"

def make_Table(node: astnodes.Table) -> str:
    rbracket = "{"
    lbracket = "}"
    tag = f"{rbracket}\n\t\t"
    fs = ",\n\t\t".join([make_Field(x) for x in node.fields])
    return f"{tag}{fs}\n\t{lbracket}"

def make_TrueExpr(node: astnodes.TrueExpr) -> str:
    return f"True"

def make_UBNotOp(node: astnodes.UBNotOp) -> str:
    return "~" + make_either(node.operand)

def make_ULNotOp(node: astnodes.ULNotOp) -> str:
    return f"not({make_either(node.operand)})"

def make_ULengthOP(node: astnodes.ULengthOP) -> str:
    return "len({{NEXT}})"

def make_UMinusOp(node: astnodes.UMinusOp) -> str:
    return "-" + make_either(node.operand)

def make_Varargs(node: astnodes.Varargs) -> str:
    return f"<Not Implemented (make_Varargs) {node.display_name}>"

def make_While(node: astnodes.While) -> str:
    tag = "while True:"
    bb= "\n\t".join(make_Body(node))
    return f"{tag}\n\t{bb}"

def make_FalseExpr(node: astnodes.FalseExpr):
    return "False"

def go(node):
    return ""

node_function_map = {
    'luaparser.astnodes.AddOp':make_AddOp,
    'luaparser.astnodes.AndLoOp':make_AndLoOp,
    'luaparser.astnodes.AnonymousFunction':make_AnonymousFunction,
    'luaparser.astnodes.Assign':make_Assign,
    'luaparser.astnodes.BAndOp':make_BAndOp,
    'luaparser.astnodes.BOrOp':make_BOrOp,
    'luaparser.astnodes.BShiftLOp':make_BShiftLOp,
    'luaparser.astnodes.BShiftROp':make_BShiftROp,
    'luaparser.astnodes.BXorOp':make_BXorOp,
    'luaparser.astnodes.Block':make_Block,
    'luaparser.astnodes.Break':make_Break,
    'luaparser.astnodes.Call':make_Call,
    'luaparser.astnodes.Chunk':make_Chunk,
    'luaparser.astnodes.Comment':make_Comment,
    'luaparser.astnodes.Concat':make_Concat,
    'luaparser.astnodes.Do':make_Do,
    'luaparser.astnodes.Dots':make_Dots,
    'luaparser.astnodes.ElseIf':make_ElseIf,
    'luaparser.astnodes.EqToOp':make_EqToOp,
    'luaparser.astnodes.ExpoOp':make_ExpoOp,
    'luaparser.astnodes.Field':make_Field,
    'luaparser.astnodes.FloatDivOp':make_FloatDivOp,
    'luaparser.astnodes.FloorDivOp':make_FloorDivOp,
    'luaparser.astnodes.Forin':make_Forin,
    'luaparser.astnodes.Fornum':make_Fornum,
    'luaparser.astnodes.Function':make_Function,
    'luaparser.astnodes.Goto':make_Goto,
    'luaparser.astnodes.GreaterOrEqThanOp':make_GreaterOrEqThanOp,
    'luaparser.astnodes.GreaterThanOp':make_GreaterThanOp,
    'luaparser.astnodes.If':make_If,
    'luaparser.astnodes.Index':make_Index,
    'luaparser.astnodes.Invoke':make_Invoke,
    'luaparser.astnodes.Label':make_Label,
    'luaparser.astnodes.LessOrEqThanOp':make_LessOrEqThanOp,
    'luaparser.astnodes.LessThanOp':make_LessThanOp,
    'luaparser.astnodes.Lhs':make_Lhs,
    'luaparser.astnodes.LocalAssign':make_LocalAssign,
    'luaparser.astnodes.LocalFunction':make_LocalFunction,
    'luaparser.astnodes.Method':make_Method,
    'luaparser.astnodes.ModOp':make_ModOp,
    'luaparser.astnodes.MultOp':make_MultOp,
    'luaparser.astnodes.Name':make_Name,
    'luaparser.astnodes.Nil':make_Nil,
    'luaparser.astnodes.NotEqToOp':make_NotEqToOp,
    'luaparser.astnodes.Number':make_Number,
    'luaparser.astnodes.OrLoOp':make_OrLoOp,
    'luaparser.astnodes.Repeat':make_Repeat,
    'luaparser.astnodes.Return':make_Return,
    'luaparser.astnodes.SemiColon':make_SemiColon,
    'luaparser.astnodes.Statement':make_Statement,
    'luaparser.astnodes.String':make_String,
    'luaparser.astnodes.SubOp':make_SubOp,
    'luaparser.astnodes.Table':make_Table,
    'luaparser.astnodes.TrueExpr':make_TrueExpr,
    'luaparser.astnodes.UBNotOp':make_UBNotOp,
    'luaparser.astnodes.ULNotOp':make_ULNotOp,
    'luaparser.astnodes.ULengthOP':make_ULengthOP,
    'luaparser.astnodes.UMinusOp':make_UMinusOp,
    'luaparser.astnodes.Varargs':make_Varargs,
    'luaparser.astnodes.While':make_While,
    'luaparser.astnodes.Expression': make_Expression,
    'luaparser.astnodes.FalseExpr':make_FalseExpr,
    'type':make_either,
    "enum.EnumType":go
}

def tokey(node):
    return str(node.__class__)[8:-2]

def python_version(node: astnodes.Node) -> str:
    return node_function_map[str(node.__class__)[8:-2]](node).replace(r",,", r",")
    
def transform_lua_node(node: LUAAST) -> str:
    """
    Transform a luaparser.astnodes.Node into a python string source
    
    Arguments:
        node (luaparser.astnodes.Node|Any): the lua node to parse 
    Returns:
        A string representing the python code
    """
    return python_version(node)

def transform_nodes(nodes: list[astnodes.Node]):
    return [transform_lua_node(x) for x  in nodes]

def get_total_nodes():
    global total_nodes
    return total_nodes