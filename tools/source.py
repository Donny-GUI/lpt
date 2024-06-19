import ast
from ast import ClassDef
import os
import luaparser.astnodes

python_ast_names = ['AST', 'Add', 'And', 'AnnAssign', 'Assert', 'Assign', 'AsyncFor', 'AsyncFunctionDef', 'AsyncWith', 'Attribute', 'AugAssign', 'AugLoad', 'AugStore', 'Await', 'BinOp', 'BitAnd', 'BitOr', 'BitXor', 'BoolOp', 'Break', 'Call', 'ClassDef', 'Compare', 'Constant', 'Continue', 'Del', 'Delete', 'Dict', 'DictComp', 'Div', 'Eq', 'ExceptHandler', 'Expr', 'Expression', 'ExtSlice', 'FloorDiv', 'For', 'FormattedValue', 'FunctionDef', 'FunctionType', 'GeneratorExp', 'Global', 'Gt', 'GtE', 'If', 'IfExp', 'Import', 'ImportFrom', 'In', 'Index', 'Interactive', 'Invert', 'Is', 'IsNot', 'JoinedStr', 'LShift', 'Lambda', 'List', 'ListComp', 'Load', 'Lt', 'LtE', 'MatMult', 'Match', 'MatchAs', 'MatchClass', 'MatchMapping', 'MatchOr', 'MatchSequence', 'MatchSingleton', 'MatchStar', 'MatchValue', 'Mod', 'Module', 'Mult', 'Name', 'NamedExpr', 'Nonlocal', 'Not', 'NotEq', 'NotIn', 'Or', 'Param', 'ParamSpec', 'Pass', 'Pow', 'RShift', 'Raise', 'Return', 'Set', 'SetComp', 'Slice', 'Starred', 'Store', 'Sub', 'Subscript', 'Suite', 'Try', 'TryStar', 'Tuple', 'TypeAlias', 'TypeIgnore', 'TypeVar', 'TypeVarTuple', 'UAdd', 'USub', 'UnaryOp', 'While', 'With', 'Yield', 'YieldFrom', '_ast_Ellipsis', 'alias', 'arg', 'arguments', 'boolop', 'cmpop', 'comprehension', 'excepthandler', 'expr', 'expr_context', 'keyword', 'match_case', 'mod', 'operator', 'pattern', 'slice', 'stmt', 'type_ignore', 'type_param', 'unaryop', 'withitem']
python_ast_classes = [ast.AST, ast.Add, ast.And, ast.AnnAssign, ast.Assert, ast.Assign, ast.AsyncFor, ast.AsyncFunctionDef, ast.AsyncWith, ast.Attribute, ast.AugAssign, ast.AugLoad, ast.AugStore, ast.Await, ast.BinOp, ast.BitAnd, ast.BitOr, ast.BitXor, ast.BoolOp, ast.Break, ast.Call, ast.ClassDef, ast.Compare, ast.Constant, ast.Continue, ast.Del, ast.Delete, ast.Dict, ast.DictComp, ast.Div, ast.Eq, ast.ExceptHandler, ast.Expr, ast.Expression, ast.ExtSlice, ast.FloorDiv, ast.For, ast.FormattedValue, ast.FunctionDef, ast.FunctionType, ast.GeneratorExp, ast.Global, ast.Gt, ast.GtE, ast.If, ast.IfExp, ast.Import, ast.ImportFrom, ast.In, ast.Index, ast.Interactive, ast.Invert, ast.Is, ast.IsNot, ast.JoinedStr, ast.LShift, ast.Lambda, ast.List, ast.ListComp, ast.Load, ast.Lt, ast.LtE, ast.MatMult, ast.Match, ast.MatchAs, ast.MatchClass, ast.MatchMapping, ast.MatchOr, ast.MatchSequence, ast.MatchSingleton, ast.MatchStar, ast.MatchValue, ast.Mod, ast.Module, ast.Mult, ast.Name, ast.NamedExpr, ast.Nonlocal, ast.Not, ast.NotEq, ast.NotIn, ast.Or, ast.Param, ast.ParamSpec, ast.Pass, ast.Pow, ast.RShift, ast.Raise, ast.Return, ast.Set, ast.SetComp, ast.Slice, ast.Starred, ast.Store, ast.Sub, ast.Subscript, ast.Suite, ast.Try, ast.TryStar, ast.Tuple, ast.TypeAlias, ast.TypeIgnore, ast.TypeVar, ast.TypeVarTuple, ast.UAdd, ast.USub, ast.UnaryOp, ast.While, ast.With, ast.Yield, ast.YieldFrom, ast._ast_Ellipsis, ast.alias, ast.arg, ast.arguments, ast.boolop, ast.cmpop, ast.comprehension, ast.excepthandler, ast.expr, ast.expr_context, ast.keyword, ast.match_case, ast.mod, ast.operator, ast.pattern, ast.slice, ast.stmt, ast.type_ignore, ast.type_param, ast.unaryop, ast.withitem]


def python_ast_path():
    import ast as x
    a = os.path.abspath(x.__file__)
    b = os.path.realpath(x.__file__)
    return a, b 

def get_ast_names():
    return [attr for attr in dir(ast) 
                  if isinstance(getattr(ast, attr), type) 
                  and issubclass(getattr(ast, attr), ast.AST)]

def get_luaast_names():
    return [attr for attr in dir(luaparser.astnodes)
                  if isinstance(getattr(luaparser.astnodes, attr), type)
                  and issubclass(getattr(luaparser.astnodes, attr), luaparser.astnodes.Node)]

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

def class_names(filepath: str):
    classes = get_all_classes(filepath=filepath)
    return [x.name for x in classes]