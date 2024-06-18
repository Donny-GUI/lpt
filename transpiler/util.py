from luaparser import ast as lua_ast

###[+] MACROS

def change_extension(filepath: str, extension: str="py"):
    ext = extension if extension.endswith(".") else "." + extension 
    return filepath.rsplit(".", 1)[0] + "." + extension

def cos(node: lua_ast.Node) -> int:
    """
    [C]olumn [O]ff[S]et

    gets the column offset from a lua node
    """
    return node.end_char - node.start_char
