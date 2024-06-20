MadeByString = """\
# Transpiled by LPT  
# author: Donald Guiles\
"""
AllowAllModulesString = """\
# IMPORTANT:  Allows local module imports
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)\
"""
