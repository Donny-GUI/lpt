import ast


#[-] Python Keyword Classes

class PythonFalseKeyword(ast.keyword):
    def __init__(self) -> None:
        super().__init__()
    def __repr__(self) -> str:
        return "False"

class PythonTrueKeyword(ast.keyword):
    def __init__(self) -> None:
        super().__init__()
    def __repr__(self) -> str:
        return "True"

class PythonNone(ast.keyword):
    def __init__(self) -> None:
        super().__init__()

#[-] Literal String Classes

class PythonNothing:
    def __init__(self) -> None:
        pass
    def __repr__(self) -> str:
        return ""

class AccessValue(ast.operator):
    def __init__(self) -> None:
        super().__init__()
    
    def __repr__(self) -> str:
        return ":"

