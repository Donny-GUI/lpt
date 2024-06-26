import os
import shutil


def lua_to_python_name(name):
    """
    Rename Lua module file/directory to Python module file/directory.
    For example, 'module.lua' -> 'module.py'
    """
    if name.endswith('.lua'):
        name = name[:-4] + '.py'
    name.replace("/./", "/")
    return name

def reproduce_directory_with_conversion(src, dest) -> dict:
    """
    Recursively reproduce directory structure from src to dest, converting Lua modules to Python modules.
    
    :param src: Source directory path
    :param dest: Destination directory path
    """
    mapping = {}
    # Ensure destination directory exists
    os.makedirs(dest, exist_ok=True)
    
    for root, dirs, files in os.walk(src):
        # Compute relative path to maintain the structure
        rel_path = os.path.relpath(root, src)
        dest_dir = os.path.join(dest, lua_to_python_name(rel_path).replace(".", ""))
        
        # Create directories in destination
        os.makedirs(dest_dir, exist_ok=True)
        print("CREATE ", dest_dir)
        
        # Copy and rename files
        for file in files:
            
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_dir, lua_to_python_name(file))
            dest_init = os.path.join(dest_dir, "__init__.py")
            shutil.copy2(src_file, dest_file)
            print("COPY  ", src_file, " ", dest_file)
            # add init file
            with open(dest_init, "w") as create:
                    create.close()
            print("CREATE ", dest_init)
            mapping[src_file] = dest_file
        
        # Rename directories after files are handled
        for dir in dirs:
            new_root = dest_dir + os.sep + os.path.basename(dir)
            add_me = reproduce_directory_with_conversion(dir, new_root)
            try:
                for lua, py in add_me.items():
                    mapping[lua] = py
            except:
                pass
        return mapping        
        

