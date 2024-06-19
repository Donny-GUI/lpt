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

total_nodes = []

LUAAST = Node


def make_Expression(node: astnodes.Expression, tnodes: list=total_nodes):
    tnodes.append(astnodes.Expression)
    if node == None:
        return ""
    tk = tokey(node)
    f = node_function_map[tk]
    retv = f(node)
    return retv

def panic(node: astnodes.Node, tnodes: list=total_nodes):
    tnodes.append(astnodes.Node)
    print(f"Panic Started: {node}")
    try:
        x = make_Number(node)
        print("RESOLVED NUMBER")
        return x
    except:
        pass
    try:
        x = make_Table(node)
        print("RESOLVED Table")
        return x
    except: 
        pass
    
    for n in all_nodes:
        k = tokey(n)
        try:
            x= node_function_map[k](node)
            print(f"Panic Resolve {x}")
            if x == None:
                return ""
            return x
        except:
            pass
    print("PANIC AMPLIFIED - not a Node")
    try:
        x = make_either(node)
        print(f"Panic Resolved - {x}")
        return x
    except:
        print("PANIC FAILED")
        raise Exception(f"Panic Failed....\n{k} \n{node}")

def make_Statement(node: astnodes.Statement, tnodes: list=total_nodes):
    tnodes.append(astnodes.Statement)

    tnodes.append(astnodes.Statement)
    if node == None:
        return "? None"
    sbtypes = get_subtype(tokey(node))
    if sbtypes != None:
        for st in sbtypes:
            try:
                x = node_function_map[tokey(st)](node)
                return x  
            except:
                pass
    return panic(node)
    
def make_either(node: astnodes.Expression, tnodes: list=total_nodes|astnodes.Statement):
    tnodes.append(astnodes.Expression)

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

def make_AddOp(node: astnodes.Node, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.Node)

    tnodes.append(astnodes.AddOp)
    return "+"

def make_AndLoOp(node: astnodes.AndLoOp, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.AndLoOp)

    tnodes.append(astnodes.AndLoOp)
    return f"{make_either(node.left)} and {make_either(node.right)}"

def make_AnonymousFunction(node: astnodes.AnonymousFunction, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.AnonymousFunction)
    return f"lambda: {node.display_name}"

def make_Assign(node: astnodes.Assign, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.Assign)
    return f"{make_Namelist(node.targets)} = {make_Namelist(node.values)}"

def make_BAndOp(node: astnodes.BAndOp, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.BAndOp)
    return "&"

def make_BOrOp(node: astnodes.BOrOp, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.BOrOp)
    return "|"

def make_BShiftLOp(node: astnodes.BShiftLOp, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.BShiftLOp)
    return "<<"

def make_BShiftROp(node: astnodes.BShiftROp, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.BShiftROp)
    return ">>"

def make_BXorOp(node: astnodes.BXorOp, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.BXorOp)
    return "^"

def make_Block(node: astnodes.Block, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.Block)
    collection = []
    for x in node.body:
        collection.append(transform_lua_node(x))
    return collection

def make_Break(node: astnodes.Break, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.Break)
    return "break"

def make_Call(node: astnodes.Call, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.Call)
    argstr = ", ".join([make_Expression(arg) for arg in node.args])
    return f"{make_Expression(node.func)}({argstr})"

def make_Chunk(node: astnodes.Chunk, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.Chunk)
    collection = []
    for n in node.body:
        collection.append(transform_lua_node(n))
    return collection

def make_Comment(node: astnodes.Comment, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.Comment)
    return f"# {node.s[2:]}"

def make_Concat(node: astnodes.Node, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.Node)
    return "+"

def make_Do(node: astnodes.Node, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.Node)
    return ""

def make_Dots(node: astnodes.Node, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.Node)
    return "..."

def make_ElseIf(node: astnodes.Node, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.Node)
    return "elif"

def make_EqToOp(node: astnodes.Node, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.Node)
    return "=="

def make_ExpoOp(node: astnodes.ExpoOp, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.ExpoOp)
    return "**"

def make_FieldValue(node: astnodes.Field, tnodes: list=total_nodes):
    tnodes.append(astnodes.Field)
    return make_Expression(node)

def make_Field(node: astnodes.Field, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.Field)
    if isinstance(node.key, astnodes.Number):
        kk = make_Number(node.key)
        return f"'{kk}' : {make_FieldValue(node.value)},"
    else:
        kk = node.key
        return f"'{kk.id}' : {make_FieldValue(node.value)},"


def make_FloatDivOp(node: astnodes.Node, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.Node)
    return "/"

def make_FloorDivOp(node: astnodes.Node, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.Node)
    return "//"

def make_Forin(node: astnodes.Forin, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.Forin)
    targets = ", ".join([make_Name(x) for x in node.targets])
    tag = f"for {targets} in {node.display_name}:"
    bb = [make_Expression(x) for x in node.body]
    return tag + "\n\t".join(bb)

def make_Fornum(node: astnodes.Fornum, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.Fornum)
    try:
        s = make_Expression(node.step)
        s = f"{s},"
    except:
        s = ""
    tag = f"for {node.target} in range({make_Expression(node.start)}{s}{make_Expression(node.stop)}):"
    bb = [make_Expression(x) for x in node.body]
    return tag + "\n\t".join(bb)

def make_Body(node: astnodes.Function, tnodes: list=total_nodes|astnodes.Call|astnodes.AnonymousFunction|
              astnodes.Do|astnodes.ElseIf|astnodes.Forin|astnodes.Fornum|astnodes.If|
              astnodes.Invoke|astnodes.LocalFunction|astnodes.Method):
    retv = []
    indent = 1
    for x in node.body:
        y = [make_Expression(x)]
        for i in range(0, indent):
            y.insert(0, "    ")
        if y[-1].strip().endswith(":"):
            indent+=1
        retv.append("".join(y))
    return retv 

def make_Function(node: astnodes.Function, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.Function)
    tag = f"def {make_Name(node.name)}({make_Namelist(node.args)}):"
    return tag + '\n' "\n\t".join([make_Body(node)])

def make_Goto(node: astnodes.Goto, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.Goto)
    return "<NOT IMPLEMENTED>"

def make_GreaterOrEqThanOp(node: astnodes.GreaterOrEqThanOp, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.GreaterOrEqThanOp)
    return make_either(node.left) + " >= " + make_either(node.right)

def make_GreaterThanOp(node: astnodes.GreaterThanOp, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.GreaterThanOp)
    return " > "

def make_If(node: astnodes.If, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.If)
    tag = f"if {make_Expression(node.test)}:"
    body = make_Body(node.body)
    other = make_Expression(node.orelse)
    return f"{tag}\n{"\n".join(body)}{other}"

def make_Index(node: astnodes.Index, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.Index)
    return f"{make_Expression(node.value)}.{make_Expression(node.idx)}"

def make_Invoke(node: astnodes.Invoke, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.Invoke)
    return ":"

def make_Label(node: astnodes.Node, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.Node)
    return "<NOT IMPLEMENTED (make_Label)>"

def make_LessOrEqThanOp(node: astnodes.LessOrEqThanOp, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.LessOrEqThanOp)
    return ">="

def make_LessThanOp(node: astnodes.LessThanOp, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.LessThanOp)
    return "<"

def make_Lhs(node: astnodes.Lhs, tnodes: list=total_nodes) -> str:
    total_nodes.append(astnodes.Lhs)
    return f"<NOT IMPLEMENTED (make_Lhs) [{node.display_name}]>"

def make_LocalAssign(node: astnodes.LocalAssign, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.LocalAssign)
    return make_Assign(node)

def make_LocalFunction(node: astnodes.Node, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.Node)
    return make_Function(node)

def make_Method(node: astnodes.Method, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.Method)
    nl = make_Namelist(node.args)
    s = ", "
    if nl == "":
        s = ""
    tag = f"def {make_Name(node.name)}(self{s}{make_Namelist(node.args)}):"
    bb = "\n".join(make_Body(node.body))
    return f"{tag}\n{bb}\n"

def make_ModOp(node: astnodes.Node, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.Node)
    return "%"

def make_MultOp(node: astnodes.Node, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.Node)
    return "*"

def make_Name(node: astnodes.Name, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.Name)
    return f"{node.id}"

def make_Namelist(nodes: list[astnodes.Expression]) -> str:
    items = []
    if isinstance(nodes, bool):
        return str(nodes)
    for item in nodes:
        x = make_Expression(item)
        items.append(x)
    return ", ".join(items)

def make_Nil(node: astnodes.Node, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.Node)
    return "None"

def make_NotEqToOp(node: astnodes.NotEqToOp, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.NotEqToOp)
    return "!="

def make_Number(node: astnodes.Number, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.Number)
    return node.n
    try:
        x = make_Expression(node)
        return x
    except:
        x= make_Expression(node)
        return x

def make_OrLoOp(node: astnodes.OrLoOp, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.OrLoOp)
    l = make_either(node.left)
    print("left", l, f"\n{node.left}")
    r = make_either(node.right)
    return  f"{str(l)} if {str(l)}  else {str(r)}"

def make_Repeat(node: astnodes.Repeat, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.Repeat)
    return f"<NOT IMPLEMENTED (make_Repeat)>"

def make_Return(node: astnodes.Return, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.Return)
    return f"return {make_Namelist(node.values)}"

def make_SemiColon(node: astnodes.SemiColon, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.SemiColon)
    return ";"

def make_String(node: astnodes.String, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.String)
    return f'"{node.s}"'

def make_SubOp(node: astnodes.SubOp, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.SubOp)
    return f"{make_either(node.left)} - {make_either(node.right)}"

def make_Table(node: astnodes.Table, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.Table)
    rbracket = "{"
    lbracket = "}"
    tag = f"{rbracket}\n\t\t"
    fs = ",\n\t\t".join([make_Field(x) for x in node.fields])
    return f"{tag}{fs}\n\t{lbracket}"

def make_TrueExpr(node: astnodes.TrueExpr, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.TrueExpr)
    return f"True"

def make_UBNotOp(node: astnodes.UBNotOp, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.UBNotOp)
    return "~" + make_either(node.operand)

def make_ULNotOp(node: astnodes.ULNotOp, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.ULNotOp)
    return f"not({make_either(node.operand)})"

def make_ULengthOP(node: astnodes.ULengthOP, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.ULengthOP)
    return f"len({node.display_name})"

def make_UMinusOp(node: astnodes.UMinusOp, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.UMinusOp)
    return "-" + make_either(node.operand)

def make_Varargs(node: astnodes.Varargs, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.Varargs)
    return f"<Not Implemented (make_Varargs) {node.display_name}>"

def make_While(node: astnodes.While, tnodes: list=total_nodes) -> str:
    tnodes.append(astnodes.While)
    tag = "while True:"
    bb= "\n\t".join(make_Body(node))
    return f"{tag}\n\t{bb}"


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
    'type':make_either,
    "enum.EnumType":go

}

def try_subtypes(node:astnodes.Node):
    for item in get_subtype(node):
        try:
            return node_function_map[item](node)
        except:
            pass

    try:
        return make_either(node)
    except:
        panic(node)

def tokey(node):
    x = str(node.__class__)[8:-2]
    return x

def transform_lua_node(node: LUAAST) -> str:

    tk = tokey(node)
    function = node_function_map[tk]
    s = function(node)
    x = s.replace(r",,", r",")
    return x

def transform_nodes(nodes: list[astnodes.Node]):
    global total_nodes
    total_nodes = []
    return [transform_lua_node(x) for x  in nodes]

def get_total_nodes():
    global total_nodes
    return total_nodes