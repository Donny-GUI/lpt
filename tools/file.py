import os
from tokenize import detect_encoding
from builtins import open as _builtin_open
from io import TextIOWrapper
from pathlib import Path
from shutil import chown
import stat
import sys





binary_access={
    1:"ACCESS_READ",            #0x00000001
    2:"ACCESS_WRITE",           #0x00000002
    4:"ACCESS_CREATE",          #0x00000004
    8:"ACCESS_EXEC",            #0x00000008
    16:"ACCESS_DELETE",         #0x00000010
    32:"ACCESS_ATRIB",          #0x00000020
    64:"ACCESS_PERM",           #0x00000040
    32768:"ACCESS_GROUP",       #0x00008000
    65536:"DELETE",             #0x00010000
    131072:"READ_CONTROL",      #0x00020000
    262144:"WRITE_DAC",         #0x00040000
    524288:"WRITE_OWNER",       #0x00080000
    1048576:"SYNCHRONIZE",      #0x00100000
    16777216:"ACCESS_SYSTEM_SECURITY",#0x01000000
    33554432:"MAXIMUM_ALLOWED", #0x02000000
    268435456:"GENERIC_ALL",    #0x10000000
    536870912:"GENERIC_EXECUTE",#0x20000000
    1073741824:"GENERIC_WRITE", #0x40000000
    65535:"SPECIFIC_RIGHTS_ALL",#0x0000ffff
    983040:"STANDARD_RIGHTS_REQUIRED",#0x000f0000
    2031616:"STANDARD_RIGHTS_ALL",#0x001f0000
    }


def public_domain(file: str|Path):
    if isinstance(file, Path) == False:
        file = Path(file)
    os.chmod(path=file, mode=stat.S_IRWXO)

def change_file_perms(filepath:str|Path):
    filep = str(filepath)
    try:
        if os.path.isfile(filep) and os.path.exists(filep):
            os.chmod(filep, 0o666)
        else:
            with open(filep, "w") as f:
                f.close()
            os.chmod(filep, 0o666)
    except PermissionError:
        print("You dont have the mermissions to change the contents of this file")

def force_open(filename):
    """Open a file in read only mode using the encoding detected by
    detect_encoding().
    """
    buffer = _builtin_open(filename, 'rb')
    try:
        encoding, lines = detect_encoding(buffer.readline)
        buffer.seek(0)
        text = TextIOWrapper(buffer, encoding, line_buffering=True)
        text.mode = 'r'
        return text.read()
    except:
        buffer.close()
        raise

def get_files_by_extension(directory: str, extension:str=".py"):
    ext = "." + extension if extension.startswith(".") == False else extension

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(ext):
                yield os.path.join(root, file)