import os
from tokenize import detect_encoding
from builtins import open as _builtin_open
from io import TextIOWrapper


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