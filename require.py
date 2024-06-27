import os
import re

require_pattern = re.compile(r'require\s*[\'"]([^\'"]+)[\'"]')
statement = re.compile(r'[\'"]([^\'"]+)[\'"]')

def get_lua_paths():
    lua_path = os.getenv('LUA_PATH')
    if lua_path != None:
        return lua_path.split(";")
    return []

def get_require_statements(string: str):
    module_names = []
    for modname in require_pattern.finditer(string):
        module_names.append(statement.match(modname))
    return module_names

def remove_require_statements(string: str):
    retv = string
    for modname in require_pattern.finditer(string):
        retv = retv.replace(modname, "")
    return retv

def locate_lua_requires(string):
    retv = []
    paths = get_lua_paths()
    statements = get_require_statements(string)
    for path in paths:
        for statement in statements:
            statement = statement.replace("/", os.sep)
            location = path.replace("?", statement)
            if os.path.exists(location):
                retv.append(location)
            cwdlua = os.path.join(os.getcwd(), statement)
            if os.path.exists(cwdlua):
                retv.append(cwdlua)
    return retv 
