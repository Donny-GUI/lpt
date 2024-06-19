import ast
from luaparser.astnodes import *
from utility.ast import get_all_classes
import os

astpath = os.path.join(os.getcwd(), "parser", "astnodes.py")

def astnodes():
    classes = get_all_classes(astpath)
    names = [c.name for c in classes]
    return names

astns = astnodes()
print(astns)