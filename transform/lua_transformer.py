from dataclasses import dataclass
from luaparser import astnodes
from luaparser.ast import parse, walk
from luaparser.astnodes import Chunk, Node
from luaparser.ast import to_pretty_str
from luaparser.ast import to_lua_source

all_nodes = [astnodes.Node, astnodes.Comment, astnodes.Expression, astnodes.Statement, astnodes.Block, astnodes.Chunk, astnodes.Lhs, astnodes.Name, astnodes.IndexNotation, astnodes.Index, astnodes.Assign, astnodes.LocalAssign, astnodes.While, astnodes.Do, astnodes.Repeat, astnodes.ElseIf, astnodes.If, astnodes.Label, astnodes.Goto, astnodes.SemiColon, astnodes.Break, astnodes.Return, astnodes.Fornum, astnodes.Forin, astnodes.Call, astnodes.Invoke, astnodes.Function, astnodes.LocalFunction, astnodes.Method, astnodes.Nil, astnodes.TrueExpr, astnodes.FalseExpr, astnodes.Number, astnodes.Varargs, astnodes.StringDelimiter, astnodes.String, astnodes.Field, astnodes.Table, astnodes.Dots, astnodes.AnonymousFunction, astnodes.Op, astnodes.BinaryOp, astnodes.AriOp, astnodes.AddOp, astnodes.SubOp, astnodes.MultOp, astnodes.FloatDivOp, astnodes.FloorDivOp, astnodes.ModOp, astnodes.ExpoOp, astnodes.BitOp, astnodes.BAndOp, astnodes.BOrOp, astnodes.BXorOp, astnodes.BShiftROp, astnodes.BShiftLOp, astnodes.RelOp, astnodes.LessThanOp, astnodes.GreaterThanOp, astnodes.LessOrEqThanOp, astnodes.GreaterOrEqThanOp, astnodes.EqToOp, astnodes.NotEqToOp, astnodes.LoOp, astnodes.AndLoOp, astnodes.OrLoOp, astnodes.Concat, astnodes.UnaryOp, astnodes.UMinusOp, astnodes.UBNotOp, astnodes.ULNotOp, astnodes.ULengthOP]
all_expressions = [astnodes.Expression, astnodes.Statement, astnodes.Lhs, astnodes.Name, astnodes.Index, astnodes.Assign, astnodes.LocalAssign, astnodes.While, astnodes.Do, astnodes.Repeat, astnodes.ElseIf, astnodes.If, astnodes.Label, astnodes.Goto, astnodes.SemiColon, astnodes.Break, astnodes.Return, astnodes.Fornum, astnodes.Forin, astnodes.Call, astnodes.Invoke, astnodes.Function, astnodes.LocalFunction, astnodes.Method, astnodes.Nil, astnodes.TrueExpr, astnodes.FalseExpr, astnodes.Number, astnodes.Varargs, astnodes.String, astnodes.Field, astnodes.Table, astnodes.Dots, astnodes.AnonymousFunction, astnodes.Op, astnodes.BinaryOp, astnodes.AriOp, astnodes.AddOp, astnodes.SubOp, astnodes.MultOp, astnodes.FloatDivOp, astnodes.FloorDivOp, astnodes.ModOp, astnodes.ExpoOp, astnodes.BitOp, astnodes.BAndOp, astnodes.BOrOp, astnodes.BXorOp, astnodes.BShiftROp, astnodes.BShiftLOp, astnodes.RelOp, astnodes.LessThanOp, astnodes.GreaterThanOp, astnodes.LessOrEqThanOp, astnodes.GreaterOrEqThanOp, astnodes.EqToOp, astnodes.NotEqToOp, astnodes.LoOp, astnodes.AndLoOp, astnodes.OrLoOp, astnodes.Concat, astnodes.UnaryOp, astnodes.UMinusOp, astnodes.UBNotOp, astnodes.ULNotOp, astnodes.ULengthOP]
all_statements = [astnodes.Statement, astnodes.Assign, astnodes.LocalAssign, astnodes.While, astnodes.Do, astnodes.Repeat, astnodes.ElseIf, astnodes.If, astnodes.Label, astnodes.Goto, astnodes.SemiColon, astnodes.Break, astnodes.Return, astnodes.Fornum, astnodes.Forin, astnodes.Call, astnodes.Invoke, astnodes.Function, astnodes.LocalFunction, astnodes.Method ]
subtypes = {}
has_body = [x for x in all_nodes if hasattr(x, "body") == True]
has_args = [x for x in all_nodes if hasattr(x, "args") == True]


def tokey(node):
    return node.__class__[8:-2]

def get_structure(node: astnodes.Node):
    if node in all_expressions == True:
        return "luaparser.astnodes.Expression"
    elif node in all_statements == True:
        return "luaparser.astnodes.Statement"
    return "Other"

@dataclass
class TransNode:
    index: int
    node: astnodes.Node # line , name,  first_token, last_token 
    structure: str
    start: int
    end: int
    string: str
    key: str

class PythonNode:
    def __init__(self, tnode: TransNode) -> None:
        self.tnode = tnode


class LuaNodeTransformer:
    def __init__(self, file: str) -> None:
        self.file: str    = file
        with open(self.file, "r") as r:
            self.content  = r.read()
        self.chunk: Chunk = parse(self.content)
        self._nodes       = walk(self.chunk)
        self.nodes        = []

        start, index, end = 0, 0, -1
        while True:
            try:
                node: Node = next(self._nodes)
                start = end + 1
                src = to_lua_source(node)
                end = end + len(src)
                self.nodes.append(
                    TransNode(index=index, 
                              node=node, 
                              start=start, 
                              end=end, 
                              string=src, 
                              key=tokey(node),
                              structure=get_structure(node))
                )
                index+=1

            except StopIteration:
                break
    
    def get_nodes(self):
        return self.nodes
     





