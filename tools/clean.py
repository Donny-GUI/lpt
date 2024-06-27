import shutil
import os
from pathlib import Path



def clean_test_dirs():
    remove = []
    r = Path(os.getcwd())
    for root, dirs, files in os.walk(str(r)):
        for d in dirs:
            if d.startswith("test_"):
               remove.append(r.joinpath(d)) 
    for x in remove:
        print(f"Removing: {x}")
        shutil.rmtree(x)


