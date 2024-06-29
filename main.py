from transpile import transpile_lua_directory
from shutil import rmtree

if __name__ == "__main__":
    proj = transpile_lua_directory("..\\decompiled")
    x = input("enter [d] to delete project or [enter] to continue...")
    if x == "d":
        rmtree(proj)
        