import os
import re

require_pattern = re.compile(r'require\s*[\'"]([^\'"]+)[\'"]')
statement = re.compile(r'[\'"]([^\'"]+)[\'"]')

class LuaRequire:
    Submodule = 0
    SubmoduleFile = 1
    StandardFile = 2
    Standard = 3
    Local = 4
    LocalFile = 5
    Unknown = 6
    DoesntExist = 7

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

def get_lua_require_type(require_statement:str):
    if require_statement in [os.path.join(os.getcwd(), x) for x in os.listdir() if os.path.isfile(x)]:
        return LuaRequire.LocalFile
    
    these_dirs = [os.path.join(os.getcwd(), x) for x in os.listdir() if os.path.isdir(x)]
    if require_statement in these_dirs:
        return LuaRequire.Local 
    
    for d in these_dirs:
        if require_statement == d:
            return LuaRequire.Local
        for r, d, fs in os.walk(d):
            for dd in d:
                if os.path.join(r, dd) == require_statement:
                    return LuaRequire.Submodule
            for f in fs:
                if os.path.join(r, f) == require_statement:
                    return LuaRequire.SubmoduleFile
        
    if os.path.isdir(require_statement):
        return LuaRequire.Standard
    elif os.path.isfile(require_statement):
        return LuaRequire.StandardFile

    if os.path.exists(require_statement):
        return LuaRequire.Unknown

    return LuaRequire.DoesntExist 


def require_path_to_python_import(require_path:str):
    
    rp = get_lua_require_type(require_path)
    match rp:
        case LuaRequire.Local: 
            pass
        case LuaRequire.LocalFile:
            pass
        case LuaRequire.Standard:
            pass 
        case LuaRequire.StandardFile:
            pass
        case LuaRequire.Submodule:
            pass
        case LuaRequire.SubmoduleFile:
            pass
        case LuaRequire.DoesntExist:
            pass
        case LuaRequire.Unknown:
            pass
    


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
