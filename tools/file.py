import os
from tokenize import detect_encoding
from builtins import open as _builtin_open
from io import TextIOWrapper
from pathlib import Path
import stat


def public_domain(file: str|Path):
    if isinstance(file, Path) == False:
        file = Path(file)
    if os.path.isdir(file) and os.path.exists(file) == False:
        os.makedirs(file)
    
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