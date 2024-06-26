from luaparser import astnodes


all_nodes = [astnodes.Node, astnodes.Comment, astnodes.Expression, astnodes.Statement, astnodes.Block, astnodes.Chunk, astnodes.Lhs, astnodes.Name, astnodes.IndexNotation, astnodes.Index, astnodes.Assign, astnodes.LocalAssign, astnodes.While, astnodes.Do, astnodes.Repeat, astnodes.ElseIf, astnodes.If, astnodes.Label, astnodes.Goto, astnodes.SemiColon, astnodes.Break, astnodes.Return, astnodes.Fornum, astnodes.Forin, astnodes.Call, astnodes.Invoke, astnodes.Function, astnodes.LocalFunction, astnodes.Method, astnodes.Nil, astnodes.TrueExpr, astnodes.FalseExpr, astnodes.Number, astnodes.Varargs, astnodes.StringDelimiter, astnodes.String, astnodes.Field, astnodes.Table, astnodes.Dots, astnodes.AnonymousFunction, astnodes.Op, astnodes.BinaryOp, astnodes.AriOp, astnodes.AddOp, astnodes.SubOp, astnodes.MultOp, astnodes.FloatDivOp, astnodes.FloorDivOp, astnodes.ModOp, astnodes.ExpoOp, astnodes.BitOp, astnodes.BAndOp, astnodes.BOrOp, astnodes.BXorOp, astnodes.BShiftROp, astnodes.BShiftLOp, astnodes.RelOp, astnodes.LessThanOp, astnodes.GreaterThanOp, astnodes.LessOrEqThanOp, astnodes.GreaterOrEqThanOp, astnodes.EqToOp, astnodes.NotEqToOp, astnodes.LoOp, astnodes.AndLoOp, astnodes.OrLoOp, astnodes.Concat, astnodes.UnaryOp, astnodes.UMinusOp, astnodes.UBNotOp, astnodes.ULNotOp, astnodes.ULengthOP]
all_expressions = [astnodes.Expression, astnodes.Statement, astnodes.Lhs, astnodes.Name, astnodes.Index, astnodes.Assign, astnodes.LocalAssign, astnodes.While, astnodes.Do, astnodes.Repeat, astnodes.ElseIf, astnodes.If, astnodes.Label, astnodes.Goto, astnodes.SemiColon, astnodes.Break, astnodes.Return, astnodes.Fornum, astnodes.Forin, astnodes.Call, astnodes.Invoke, astnodes.Function, astnodes.LocalFunction, astnodes.Method, astnodes.Nil, astnodes.TrueExpr, astnodes.FalseExpr, astnodes.Number, astnodes.Varargs, astnodes.String, astnodes.Field, astnodes.Table, astnodes.Dots, astnodes.AnonymousFunction, astnodes.Op, astnodes.BinaryOp, astnodes.AriOp, astnodes.AddOp, astnodes.SubOp, astnodes.MultOp, astnodes.FloatDivOp, astnodes.FloorDivOp, astnodes.ModOp, astnodes.ExpoOp, astnodes.BitOp, astnodes.BAndOp, astnodes.BOrOp, astnodes.BXorOp, astnodes.BShiftROp, astnodes.BShiftLOp, astnodes.RelOp, astnodes.LessThanOp, astnodes.GreaterThanOp, astnodes.LessOrEqThanOp, astnodes.GreaterOrEqThanOp, astnodes.EqToOp, astnodes.NotEqToOp, astnodes.LoOp, astnodes.AndLoOp, astnodes.OrLoOp, astnodes.Concat, astnodes.UnaryOp, astnodes.UMinusOp, astnodes.UBNotOp, astnodes.ULNotOp, astnodes.ULengthOP]
all_statements = [astnodes.Statement, astnodes.Assign, astnodes.LocalAssign, astnodes.While, astnodes.Do, astnodes.Repeat, astnodes.ElseIf, astnodes.If, astnodes.Label, astnodes.Goto, astnodes.SemiColon, astnodes.Break, astnodes.Return, astnodes.Fornum, astnodes.Forin, astnodes.Call, astnodes.Invoke, astnodes.Function, astnodes.LocalFunction, astnodes.Method ]
subtypes = {}
has_body = [x for x in all_nodes if hasattr(x, "body") == True]
has_args = [x for x in all_nodes if hasattr(x, "args") == True]


def has(node:astnodes.Node, attribute:str):
    if hasattr(node, attribute):
        return True

def hasbody(node: astnodes.Node):
    if hasattr(node, "body"):
        return True
    return False

def hasargs(node: astnodes.Node):
    if hasattr(node, "args"):
        return True
    return False

def tokey(node):
    return node.__class__[8:-2]

for x in all_nodes:
    try:
        subtypes[tokey(x)] = [tokey(z) for z in x.__subclasses__()]
    except:
        pass

def get_subtype(node: astnodes.Node) -> list[astnodes.Node]:
    if isinstance(node, str):
        return subtypes[node]
    try:
        return subtypes[tokey(node)]
    except:
        return