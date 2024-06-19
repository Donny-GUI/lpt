import os
import pathlib 
import importlib.util
import sys

desktop_path = f"C:\\Users\\{os.getlogin()}\\Desktop"

sys.path = sys.path

def allow_local_modules():
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    global sys
    sys.path.insert(0, parent_dir)

def add_parent_modules():
    cwd = os.getcwd()
    dds = [os.path.join(cwd, x) for x in os.listdir(cwd) if os.path.isdir(x)]
    for d in dds:
        paths = [os.path.join(d, x) for x in os.listdir(d) if os.path.isfile(x) == True and x.startswith("__init__.py")]
        if len(paths) == 1:
            truepath = os.path.abspath(os.path.join(d, '..'))
            sys.path.insert(0, truepath)
    
    

def get_module_path(module_name):
    try:
        # Find the module's spec
        spec = importlib.util.find_spec(module_name)
        if spec is None:
            raise ModuleNotFoundError(f"Module '{module_name}' not found")

        # Extract the file location
        module_path = spec.origin

        if module_path is None:
            raise FileNotFoundError(f"Cannot find the file for module '{module_name}'")

        # Return the absolute path
        return os.path.abspath(module_path)
    except Exception as e:
        return str(e)

