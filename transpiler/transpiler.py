from luaparser import ast as lua_ast
from transpiler.typehints import LuaNode, PythonNode
import ast
from transpiler.util import cos, change_extension
from transpiler.nodes import PythonFalseKeyword, PythonNone, PythonNothing, PythonTrueKeyword
import os 
import astor


fix = ast.fix_missing_locations
src = astor.code_gen.to_source

def unparse_node(node: ast.AST):
    n = fix(node)
    try:
        return n 
    except Exception as e:
        print(e)
        if isinstance(n, ast.FunctionDef):
            n.decorator_list = []
            return unparse_node(n)

def create_function_def(name, args, body=None, returns=None, decorators=None):
    """
    Create an ast.FunctionDef node.

    Parameters:
    - name (str): The name of the function.
    - args (list of str): List of argument names.
    - body (list of str): List of strings representing the body of the function.
    - returns (str, optional): The return type hint as a string.
    - decorators (list of str, optional): List of strings representing decorators.

    Returns:
    - ast.FunctionDef: An ast.FunctionDef node.
    """
    # Convert argument names to ast.arg nodes
    arguments = ast.arguments(
        posonlyargs=[],  # Positional-only arguments
        args=[ast.arg(arg=arg_name, annotation=None) for arg_name in args],
        vararg=None,  # *args
        kwonlyargs=[],  # Keyword-only arguments
        kw_defaults=[],  # Defaults for kwonlyargs
        kwarg=None,  # **kwargs
        defaults=[]  # Defaults for args
    )
    
    # Convert body lines to ast.Expr nodes
    if body!=None:
        body_nodes = [ast.parse(stmt).body[0] for stmt in body]
    else:
        body_nodes = body
    # Convert return type hint to ast
    return_node = ast.parse(returns).body[0].value if returns else None
    
    # Convert decorators to ast.Expr nodes
    decorator_nodes = [ast.Name(id=deco, ctx=ast.Load()) for deco in (decorators or [])]
    
    # Create the FunctionDef node
    function_def = ast.FunctionDef(
        name=name,
        args=arguments,
        body=body_nodes,
        decorator_list=decorator_nodes,
        returns=return_node,
        type_comment=None
    )
    function_def.decorator_list = []
    return ast.fix_missing_locations(function_def)

###[-] Object Classes

class LuaToPythonTranspiler(lua_ast.ASTVisitor):
    def __init__(self, nodes: list[LuaNode]= []):
        self.lnodes = nodes
        self.python_ast = None
        self.nmap = {}
    
    def set(self, lua_nodes: list[LuaNode]):
        self.lnodes = lua_nodes

    def _convArgs(self, args: list[lua_ast.Expression]):
        _args = []
        for item in args:
            _args.append(ast.arg(arg=item.display_name, lineno=item.line, col_offset=cos(item)))
        return ast.arguments(args=_args)
    
    def _convBody(self, node: lua_ast.AST):
        return [self.generic_visit(x) for x in node.body]
    
    def visit_Block(self, node: lua_ast.Block) -> ast.AST:
        body = [self.generic_visit(statement) for statement in node.body]
        return ast.Module(body=body)

    def visit_Assignment(self, node: lua_ast.Assign) -> ast.AST:
        targets = [fix(self.generic_visit(v)) for v in node.targets]
        value = self.generic_visit(node.values[0]) if node.values else fix(ast.Constant(value=None))
        return fix(ast.Assign(targets=targets, value=value))

    def visit_Name(self, node: lua_ast.Name) -> ast.AST:
        return ast.Name(id=node.id, ctx=ast.Load())

    def visit_Number(self, node: lua_ast.Number) -> ast.AST:
        return ast.Constant(value=node.n)

    def visit_String(self, node: lua_ast.String) -> ast.AST:
        return ast.Constant(value=node.s)

    def mapit(self, node, node2):
        self.nmap[node] = node2

    def visit_Function(self, node: lua_ast.Function) -> ast.AST:
        return create_function_def(name=node.name.display_name, args=[n.display_name for n in node.args])

    def visit_Call(self, node: lua_ast.Call) -> ast.AST:
        func = self.generic_visit(node.func)
        args = [self.generic_visit(arg) for arg in node.args]
        return ast.Call(func=func, args=args, keywords=[])

    def visit_AnonymousFunction(self, node: lua_ast.AnonymousFunction) -> ast.Lambda:
        return ast.Lambda(args=node.args, body=self._convBody(node), lineno=node.line, col_offset=cos(node))
        
    def visit_AddOperator(self, node: lua_ast.AddOp) -> ast.AST:
        return ast.Add()
        
    def visit_LogicalAnd(self, node: lua_ast.AndLoOp) -> ast.AST:
        return ast.And()
        
    def visit_BitwiseAnd(self, node: lua_ast.BAndOp) -> ast.AST:
        return ast.BitAnd()
        
    def visit_BitwiseOr(self, node: lua_ast.BOrOp) -> ast.AST:
        return ast.BitOr()
        
    def visit_BitwiseLShift(self, node: lua_ast.BShiftLOp) -> ast.AST:
        return ast.LShift()
        
    def visit_BitwiseXOR(self, node: lua_ast.BXorOp) -> ast.AST:
        return ast.BitXor()
        
    def visit_BitwiseRShift(self, node: lua_ast.BShiftROp) -> ast.AST:
        return ast.RShift()
        
    def visit_Comment(self, node: lua_ast.Comment) -> ast.AST:
        # Todo
        return None
        
    def visit_Concat(self, node: lua_ast.Concat) -> ast.AST:
        #TODO
        return ast.FormattedValue()
        
    def visit_Do(self, node: lua_ast.Do) -> ast.AST:
        return 
        
    def visit_Dots(self, node: lua_ast.Dots) -> ast.AST:
        return ast.Ellipsis()
        
    def visit_ElseIf(self, node: lua_ast.ElseIf) -> ast.AST:
        # TODO
        return ast.If()
        
    def visit_EqualTo(self, node: lua_ast.EqToOp) -> ast.AST:
        return ast.Eq()
        
        
    def visit_Exponent(self, node: lua_ast.ExpoOp) -> ast.AST:
        # TODO
        return ast.Starred()
        
    def visit_NotEqualTo(self, node: lua_ast.NotEqToOp) -> ast.AST:
        return ast.NotEq()
        
    def visit_FalseKeyword(self, node: lua_ast.FalseExpr) -> ast.AST:
        return PythonFalseKeyword()
        
    def visit_Field(self, node: lua_ast.Field) -> ast.AST:
        nodes = [ast.Constant(value=node.key), ]
        
        return ast.Name()
        
    def visit_FloatDivision(self, node: lua_ast.FloatDivOp) -> ast.AST:
        return ast.Div()
        
    def visit_FloorDivision(self, node: lua_ast.FloorDivOp) -> ast.AST:
        return ast.FloorDiv()
        
    def visit_NumericalFor(self, node: lua_ast.Fornum) -> ast.AST:
        return ast.Expression()

    def visit_ForIn(self, node: lua_ast.Forin) -> ast.AST:
        tts = []
        for nn in node.targets:
            tts.append(self.generic_visit(nn))
        return ast.For(target=tts, body=node.body, orelse=None, lineno=node.line, col_offset=cos(node))
        
    def visit_GoTo(self, node: lua_ast.Goto) -> ast.AST:
        # TODO
        pass
    
    def visit_InKeyword(self):
        return ast.In()
    
    def visit_GreaterOrEqual(self, node: lua_ast.GreaterOrEqThanOp) -> ast.AST:
        return ast.GtE()
        
    def visit_GreaterThan(self, node: lua_ast.GreaterThanOp) -> ast.AST:
        return ast.Gt()
        
    def visit_If(self, node: lua_ast.If) -> ast.AST:
        return ast.If(test=node.test, orelse=node.orelse, lineno=node.line, col_offset=cos(node))
        
    def visit_IndexAccess(self, node: lua_ast.Index) -> ast.AST:
        return ast.Subscript()
        
    def visit_Label(self, node: lua_ast.Label) -> ast.AST:
        # TODO
        return
        
    def visit_LessThanOrEqual(self, node: lua_ast.LessOrEqThanOp) -> ast.AST:
        return ast.LtE()
        
    def visit_LessThan(self, node: lua_ast.LessThanOp) -> ast.AST:
        return ast.Lt()
        
    def visit_LocalAssign(self, node: lua_ast.LocalAssign) -> ast.AST:
        return ast.Assign()
    
    def visit_LocalFunction(self, node: lua_ast.LocalFunction) -> ast.AST:
        return ast.FunctionDef(name=node.name, 
                               args=self._convArgs(node.args), 
                               body=self._convBody(node), 
                               decorator_list=[], 
                               lineno=node.line, 
                               col_offset=cos(node))
        
    def visit_ClassMethod(self, node: lua_ast.Method) -> ast.AST:
        return ast.FunctionDef(name=node.name, )
        
    def visit_Modulo(self, node: lua_ast.ModOp) -> ast.AST:
        return ast.Mod()
        
    def visit_MultiplicationOperator(self, node: lua_ast.MultOp) -> ast.AST:
        return ast.Mult()
        
    def visit_NilKeyword(self, node: lua_ast.Nil) -> ast.AST:
        return PythonNone()
        
    def visit_NotEqualToOperator(self, node: lua_ast.NotEqToOp) -> ast.AST:
        return ast.NotEq()
        
    def visit_LogicalOrOperator(self, node: lua_ast.OrLoOp) -> ast.AST:
        return ast.Or()
        
    def visit_RepeatUntil(self, node: lua_ast.Repeat) -> ast.AST:
        # TODO
        return None
        
    def visit_ReturnKeyword(self, node: lua_ast.Return) -> ast.AST:
        return ast.Return()
        
    def visit_SubtractionOperator(self, node: lua_ast.SubOp) -> ast.AST:
        return ast.Sub()
    
    def _fieldToDictKey(self, field: lua_ast.Field):
        return ast.Constant(value=field.key, kind=str)
    
    def _fieldToDictValue(self, field: lua_ast.Field):
        return self.generic_visit(field.value)
    
    def visit_Table(self, node: lua_ast.Table) -> ast.AST:
        py = ast.Dict(
            keys=[], values=[],
            lineno=node.line, 
            col_offset=cos(node))
        for field in node.fields:
            py.keys.append(self._fieldToDictKey(field))
            py.values.append(self._fieldToDictValue(field))
        return py
    
    def visit_LogicalOrOperator(self, node: lua_ast.OrLoOp) -> ast.AST:
        return ast.Or()
        
    def visit_UnaryNotOperator(self, node: lua_ast.UBNotOp) -> ast.AST:
        return ast.Not()
        
    def visit_UnaryLengthOperator(self, node: lua_ast.ULengthOP) -> ast.AST:
        return ast.Name("len", ctx=ast.Call())
        
    def visit_UnaryLogicalNotOperator(self, node: lua_ast.ULNotOp) -> ast.AST:
        return ast.NotEq()
        
    def visit_UnaryMinusOperator(self, node: lua_ast.UMinusOp) -> ast.AST:
        return ast.USub()
        
    def visit_While(self, node: lua_ast.While) -> ast.AST:
        return ast.While()
    
    def convert_nodes(self, nodes:list[LuaNode]=[]):
        if nodes == []:
            nodes = self.lnodes
        retv = []
        for node in nodes:
            retv.append(self.generic_visit(node))
        return retv 
        
    def generic_visit(self, node) -> ast.AST:
        pynode = None
        if isinstance(node, lua_ast.Block):
            pynode = self.visit_Block(node)
        elif isinstance(node, lua_ast.Assign):
            pynode = self.visit_Assignment(node)
        elif isinstance(node, lua_ast.Name):
            pynode = self.visit_Name(node)
        elif isinstance(node, lua_ast.Number):
            pynode = self.visit_Number(node)
        elif isinstance(node, lua_ast.String):
            pynode = self.visit_String(node)
        elif isinstance(node, lua_ast.Function):
            pynode = self.visit_Function(node)
        elif isinstance(node, lua_ast.Call):
            pynode = self.visit_Call(node)
        elif isinstance(node, lua_ast.AnonymousFunction):
            pynode = self.visit_AnonymousFunction(node)
        elif isinstance(node, lua_ast.AddOp):
            pynode = self.visit_AddOperator(node)
        elif isinstance(node, lua_ast.AndLoOp):
            pynode = self.visit_LogicalAnd(node)
        elif isinstance(node, lua_ast.BAndOp):
            pynode = self.visit_BitwiseAnd(node)
        elif isinstance(node, lua_ast.BOrOp):
            pynode = self.visit_BitwiseOr(node)
        elif isinstance(node, lua_ast.BShiftLOp):
            pynode = self.visit_BitwiseLShift(node)
        elif isinstance(node, lua_ast.BXorOp):
            pynode = self.visit_BitwiseXOR(node)
        elif isinstance(node, lua_ast.BShiftROp):
            pynode = self.visit_BitwiseRShift(node)
        elif isinstance(node, lua_ast.Comment):
            pynode = self.visit_Comment(node)
        #bitwise concat
        elif isinstance(node, lua_ast.Concat):
            pynode = self.visit_Concat(node)
        #bitwise do
        elif isinstance(node, lua_ast.Do):
            pynode = self.visit_Do(node)
        #bitwise dots
        elif isinstance(node, lua_ast.Dots):
            pynode = self.visit_Dots(node)
        elif isinstance(node, lua_ast.ElseIf):
            pynode = self.visit_ElseIf(node)
        elif isinstance(node, lua_ast.EqToOp):
            pynode = self.visit_EqualTo(node)
        elif isinstance(node, lua_ast.ExpoOp):
            pynode = self.visit_Exponent(node)
        elif isinstance(node, lua_ast.NotEqToOp):
            pynode = self.visit_NotEqualTo(node)
        elif isinstance(node, lua_ast.FalseExpr):
            pynode = self.visit_FalseKeyword(node)
        elif isinstance(node, lua_ast.Field):
            pynode = self.visit_Field(node)
        elif isinstance(node, lua_ast.FloatDivOp):
            pynode = self.visit_FloatDivision(node)
        elif isinstance(node, lua_ast.FloorDivOp):
            pynode = self.visit_FloorDivision(node)
        elif isinstance(node, lua_ast.Fornum):
            pynode = self.visit_NumericalFor(node)
        elif isinstance(node, lua_ast.Forin):
            pynode = self.visit_ForIn(node)
        elif isinstance(node, lua_ast.Goto):
            pynode = self.visit_GoTo(node)
        elif isinstance(node, lua_ast.GreaterOrEqThanOp):
            pynode = self.visit_GreaterOrEqual(node)
        elif isinstance(node, lua_ast.GreaterThanOp):
            pynode = self.visit_GreaterThan(node)
        elif isinstance(node, lua_ast.If):
            pynode = self.visit_If(node)
        elif isinstance(node, lua_ast.Index):
            pynode = self.visit_IndexAccess(node)
        elif isinstance(node, lua_ast.Label):
            pynode = self.visit_Label(node)
        elif isinstance(node, lua_ast.LessOrEqThanOp):
            pynode = self.visit_LessThanOrEqual(node)
        elif isinstance(node, lua_ast.LessThanOp):
            pynode = self.visit_LessThan(node)
        elif isinstance(node, lua_ast.LocalAssign):
            pynode = self.visit_LocalAssign(node)
        elif isinstance(node, lua_ast.LocalFunction):
            pynode = self.visit_LocalFunction(node)
        elif isinstance(node, lua_ast.Method):
            pynode = self.visit_ClassMethod(node)
        elif isinstance(node, lua_ast.ModOp):
            pynode = self.visit_Modulo(node)
        elif isinstance(node, lua_ast.MultOp):
            pynode = self.visit_MultiplicationOperator(node)
        elif isinstance(node, lua_ast.Nil):
            pynode = self.visit_NilKeyword(node)
        elif isinstance(node, lua_ast.NotEqToOp):
            pynode = self.visit_NotEqualToOperator(node)
        elif isinstance(node, lua_ast.OrLoOp):
            pynode = self.visit_LogicalOrOperator(node)
        elif isinstance(node, lua_ast.Repeat):
            pynode = self.visit_RepeatUntil(node)
        elif isinstance(node, lua_ast.Return):
            pynode = self.visit_ReturnKeyword(node)
        elif isinstance(node, lua_ast.SubOp):
            pynode = self.visit_SubtractionOperator(node)
        elif isinstance(node, lua_ast.Table):
            pynode = self.visit_Table(node)
        elif isinstance(node, lua_ast.TrueExpr):
            pynode = self.visit_LogicalOrOperator(node)
        elif isinstance(node, lua_ast.UBNotOp):
            pynode = self.visit_UnaryNotOperator(node)
        elif isinstance(node, lua_ast.ULengthOP):
            pynode = self.visit_UnaryLengthOperator(node)
        elif isinstance(node, lua_ast.ULNotOp):
            pynode = self.visit_UnaryLogicalNotOperator(node)
        elif isinstance(node, lua_ast.UMinusOp):
            pynode = self.visit_UnaryMinusOperator(node)
        elif isinstance(node, lua_ast.While):
            pynode = self.visit_While(node)
        else:
            print(f"Unsupported node type: {type(node).__name__}")
            print(node)
            return None
        return ast.fix_missing_locations(pynode)
    
    def convert_file(self, filepath: str) -> str:
        """
        Convert a lua filepath to a py source file and return the path
        Arguments:
            filepath (str) : path to the lua source file
        Returns:
            str : path to the new py file
        """
        if os.path.exists(filepath) == True:
            with open(filepath, "r") as f:
                content = f.read()
            return self.convert_string(content)
            
        return None
            
    def convert_string(self, lua: str):
        """
        Description:
            Converts a string of lua code into a string of python code
        Arguments:
            lua (str) : The string in question to convert. 
        Returns:
            str : python equivalent as a string of code. 
        """
        lua_chunk: lua_ast.Chunk = lua_ast.parse(lua)
        nodes = []
        try:
            for x in lua_chunk.body.body:
                y = self.generic_visit(x)
                if y == None:
                    continue
                nodes.append(src(fix(y)))
        except TypeError as te:
            print(te)
            print("ABORTED")
            return
        for node in nodes:
            print(node)
        input()
        
        return x