import os


def get_files_by_extension(directory: str, extension:str=".py"):
    ext = "." + extension if extension.startswith(".") == False else extension

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(ext):
                yield os.path.join(root, file)