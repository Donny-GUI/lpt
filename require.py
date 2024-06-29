import os
import re
from pathlib import Path

require_pattern = re.compile(r'require\s*[\'"]([^\'"]+)[\'"]')
statement = re.compile(r'[\'"]([^\'"]+)[\'"]')

class LuaRequire:
    Submodule = 0
    SubmoduleFile = 1
    StandardFile = 2
    Standard = 3
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
        if isinstance(modname, re.Match):
            module_names.append(statement.match(modname.string))
    return module_names

def remove_require_statements(string: str):
    retv = string
    for modname in require_pattern.finditer(string):
        if isinstance(modname, re.Match):
            retv = retv.replace(modname.string, "")
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
    
    def _from_importize(require: str):
        parts = ".".join(require.split("/"))
        return "from " + parts + " import *"
    
    def _stylize_file_import(require: str):
        c = require.count(os.sep)
        if c == 0:
            return f"import {require}"
        elif c == 1:
            parts = require.split(os.sep)
            return f"from {parts[0]} import {parts[1]}"
        elif c == 2:
            parts = require.split(os.sep)
            return f"from {parts[0]}.{parts[1]} import {parts[2]}"
        elif c > 2:
            parts = require.split(os.sep)
            attr_str = ".".join(parts[1:-1])
            return f"from {parts[0]}.{attr_str} import {parts[-1]}"

    def _remove_front(require: str):
        parts = require.split("/")
        dn = os.getcwd().split(os.sep)[-1]
        dindex = parts.index(dn)
        return os.sep.join(parts[dindex:])

    rp = get_lua_require_type(require_path)
    match rp:
        case LuaRequire.LocalFile:
            # if the lua file is a file is one the first level of the directory
            return _stylize_file_import(os.path.basename(require_path))
            
        case LuaRequire.Standard:
            return f"from {os.path.basename(os.path.dirname(require_path))} import {os.path.basename(require_path)}"
        
        case LuaRequire.StandardFile:
            return f"import {os.path.basename(require_path)}"
        
        case LuaRequire.Submodule:
            return _stylize_file_import(_remove_front(require_path))
        
        case LuaRequire.SubmoduleFile:
            return _stylize_file_import(_remove_front(require_path))
            
        case LuaRequire.DoesntExist:
            pass
        case LuaRequire.Unknown:
            pass
    
    return ""

def locate_lua_requires(string):
    retv = []
    paths = get_lua_paths()
    statements = [x for x in get_require_statements(string) if x != None]
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
