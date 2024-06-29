import os
from tokenize import detect_encoding
from datetime import datetime
from pathlib import Path
from random import randint
from typing import List
from shutil import copy as shutil_copy
# Non-Standard
from luaparser.ast import parse
from luaparser.ast import get_token_stream
# Local 
from typedef import LuaNode
from transnode import TransNode
from dir_creator import reproduce_directory_with_conversion
from require import remove_require_statements, locate_lua_requires, require_path_to_python_import


CWD = Path(os.getcwd())

def timestamp():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

def random_number_sequence(length=5):
    retv = []
    for i in range(0, length):
        retv.append(str(randint(0, 9)))
    return "".join(retv)

def get_encoding(filepath: str) -> str:
    """
    Get the encoding of a file
    Arguments:
        filepath (str): path to the file
    Return:
        encoding (str): string rep of the encoding
    """
    fp = open(filepath, "r")
    try:
        enc = detect_encoding(fp.readline)
        fp.close()
        return enc
    except:
        fp.close()
        return "utf-8"

def string_to_transnodes(string: str) -> List[TransNode]:
    return [TransNode(node=node, index=index, source=string) 
            for index, node 
            in enumerate(string_to_lua_nodes(string))]

def lua_file_to_transnodes(filepath: str) -> List[TransNode]:
    """
    Takes a string of a lua file path returns a list of Transnode
    Arguments:
        filepath (str): path to the lua file to make nodes of
    Returns:
        nodes(List[TransNode]): a list of TransNodes
    """
    enc = get_encoding(filepath=filepath)
    with open(file=filepath, mode="r", encoding=enc, errors="ignore") as f:
        src = f.read()
    return [TransNode(node=node, index=index, source=src) 
            for index, node 
            in enumerate(string_to_lua_nodes(src))]

def read_lua(filepath:str):
    """
    Get encoding of file and open file line by line
    and encoding by encoding then return a string
    Arguments:
        filepath(str) : path the lua file
    Returns:
        str : string representation of a lua file
    """
    with open(file=filepath, mode="r", encoding="utf-8", errors="ignore") as f:
        src = f.read()
    return src

def string_to_lua_nodes(string: str) -> List[LuaNode]:
    """Converts a string of lua code to 
    a list of LuaNode
    """
    nodes = parse(string)
    return [node for node in nodes.body.body]

def lua_file_to_lua_nodes(filepath:str) -> List[LuaNode]:
    string = read_lua(filepath=filepath)
    nodes = parse(string)
    return [node for node in nodes.body.body]

def transpile_subfile(filepath: str):
    src = []
    print("[#]  TRANSPILING ", filepath)
    print("  [-] READING    ")
    luacontent = read_lua(filepath)
    # get the require statements

    print("  [-] CONVERTING ", "imports for: ", os.path.basename(filepath)) 
    all_reqs = locate_lua_requires(luacontent)
    # convert them to import statements
    for r in all_reqs:
        imp = require_path_to_python_import(r)
        src.append(imp)
        src.append("\n")

    print("  [-] BUILDING    Abstract Tree")
    # remove the require statements from the source
    luacont = remove_require_statements(luacontent)
    # get the ast nodes for the lua_content 
    transnodes: List[TransNode] = string_to_transnodes(luacont)
    token_stream = get_token_stream(luacont)
    # Get the python string representation of the ast nodes

    print("   [-] Building Python Nodes\n\t[", end="")
    for tnode in transnodes:
        print("|", end="")
        tnode.collect_tokens(token_stream=token_stream)
        src.append(tnode.python_string)
    print("]", end="")
    print("\n", "    [-] Writing ", filepath)
    with open(filepath, "w") as f:
        for block in src:
            f.write(block+"\n")

    print("[✔️ ] TRANSPILED ", filepath)

def lua_file_to_python_string(filepath: str):
    src = []
    print("[#]  TRANSPILING ", filepath)
    print("  [-] READING    ")
    luacontent = read_lua(filepath)
    # get the require statements

    print("  [-] CONVERTING ", "imports for: ", os.path.basename(filepath)) 
    all_reqs = locate_lua_requires(luacontent)
    # convert them to import statements
    for r in all_reqs:
        imp = require_path_to_python_import(r)
        src.append(imp)
        src.append("\n")

    print("  [-] BUILDING    Abstract Tree")
    # remove the require statements from the source
    luacont = remove_require_statements(luacontent)
    # get the ast nodes for the lua_content 
    transnodes: List[TransNode] = string_to_transnodes(luacont)
    token_stream = get_token_stream(luacont)
    # Get the python string representation of the ast nodes

    print("   [-] Building Python Nodes\n\t[", end="")
    for tnode in transnodes:
        print("|", end="")
        tnode.collect_tokens(token_stream=token_stream)
        src.append(tnode.python_string)
    print("]", end="")
    return "\n".join(src)

def _fetch_require_dir(luapath, project_root=None, depth=0):

    flpy = Path(project_root)
    # aggregate dirs if depth is greater than one
    if depth != 0:
        parts = str(luapath).split("/")[:-1]
        for i in range(0, depth):
            flpy = flpy.joinpath(parts.pop(-1))
    # make the new dir
    flpy = flpy.joinpath(os.path.basename(luapath))
    os.makedirs(flpy, exist_ok=True)

    # go one deeper
    for file in os.listdir(luapath):
        # aggregate new file object
        pathp: str = os.path.join(luapath, file)
        # if it is a file make it
        if os.path.isfile(pathp) and file.endswith(".lua"):
            string = lua_file_to_python_string(pathp)
            fullfilepath = flpy.joinpath(str(os.path.basename(luapath)))
            with open(str(fullfilepath), "w") as f:
                f.write(string)
        # if its a dir, go deeper
        if os.path.isdir(pathp):
            depth+=1
            _fetch_require_dir(file, project_root=project_root, depth=depth)

def _fetch_require_file(luapath:str, project_root=None):
    string = lua_file_to_python_string(luapath)
    name = project_root + os.sep + os.path.basename(luapath).split(".")[0] + ".py"
    with open(name, "w") as f:
        f.write(string)

def fetch_require(luapath:str, project_root:str=None):
    """Fetch copies of lua requires to add to the project

    Args:
        luapath (str): the lua require path
        project_root (str, optional): root path to the project directory.
    """
    print("  [-] Fetching ", luapath)
    if os.path.isdir(luapath):
        _fetch_require_dir(luapath, project_root)
    elif os.path.isfile(luapath):
        _fetch_require_file(luapath, project_root)

def transpile_lua_directory(directory: str) -> str:
    """takes a path to a lua project directory,
    transpiles it to python

    Args:
        directory (str): path to the lua dir

    Returns:
        str: the project directory with python
    """

    print("[+] Transpiling Project", directory)
    dn = directory+"_python"
    print("  [-] Scaffolding Project")
    mapping = reproduce_directory_with_conversion(directory, dn)

    reqs = []

    for lua, py in mapping.items():
        # copy over non-lua files exactly
        if not lua.endswith(".lua"):
            shutil_copy(lua, dn + os.sep + os.path.basename(lua))
            continue
        print("  [-] Mapping ", lua)
        src = []
        # read file to string
        luacontent = read_lua(lua)
        # get the require statements 
        print("  [-] Locating imports...")
        all_reqs = locate_lua_requires(luacontent)
        # convert them to import statements
        print("  [-] Converting import statements")
        for r in all_reqs:
            imp = require_path_to_python_import(r)
            src.append(imp)
            print(imp)
        src.append("\n")
        # add it too all reqs
        reqs.extend(all_reqs)
        # remove the require statements
        luacont = remove_require_statements(luacontent)
        # get the ast nodes for the lua_content 
        print("  [-] Transpiling ", lua)
        transnodes: List[TransNode] = string_to_transnodes(luacont)
        token_stream = get_token_stream(luacont)
        # Get the python string representation of the ast nodes
        for tnode in transnodes:
            tnode.collect_tokens(token_stream=token_stream)
            src.append(tnode.python_string)
        
        py = py.replace("/./", "/")
        os.makedirs(os.path.dirname(py), exist_ok=True)
        print("  [-] Writing ", py)
        with open(py, "w", encoding=get_encoding(lua)) as f:
            for block in src:
                try:
                    f.write(block+"\n")
                except UnicodeEncodeError:
                    block: str = block.encode().decode()
                    f.write(block+"\n")
    
    print("  [-] fetching requires")
    for req in reqs:
        fetch_require(luapath=req, project_root=dn)

    for x in os.listdir(dn):
        if os.path.isdir(x):
            for y in os.listdir(x):
                if os.path.isfile(y):
                    transpile_subfile(y)

    # go one level deeper
    for file in os.listdir(directory):
        newsubobj = directory + os.sep + file
        if os.path.isdir(newsubobj):
            new_proj_dir = dn + os.sep + file
            os.makedirs(name=new_proj_dir, exist_ok=True)
            for subfile in os.listdir(newsubobj):
                subpath = newsubobj + os.sep + subfile
                if os.path.isfile(subpath) and subfile.endswith(".lua"):
                    cont = lua_file_to_python_string(subpath)
                    newsubfile = new_proj_dir + os.sep + os.path.basename(subfile).split(".")[0] + ".py"
                    with open(newsubfile, "w") as f:
                        f.write(cont)

    return dn


