from tools.color import *
from datetime import datetime



def timestamp():
    return datetime.now().strftime()

def update(msg: str):
    print(f"[{timestamp()}][][ {CYAN_BOLD}UPDATE{RESET}     ]: {ITALIC}{msg}{RESET}")

def _update(msg: str):
    pass 

def debug(msg: str):
    print(f"[{timestamp()}][😿][ {BLUE_BOLD}DEBUG{RESET}      ]: {ITALIC}{msg}{RESET}")

def _debug(msg: str):
    pass

def init(msg:str):
    print(f"[{timestamp()}][✨][ {GREEN_BOLD}INITIALIZED{RESET}]: {BOLD}{msg}{RESET}")
    
def _init(msg:str):
    pass



def method(msg:str):...
    

def method(msg:str):
    print(f"[{timestamp()}][🔨][ {GREEN_BOLD}METHOD{RESET}     ]: {BOLD}{msg}{RESET}")

def _method(msg):
    pass 

update_function = function
debug_function = function
init_function = function 

def set_debug(debug_state=False) -> tuple[update_function, debug_function, init_function]:
    if debug_state == True:
        method = method
    elif debug_state == False:
        from tools.updater import _update as update
        from tools.updater import _debug as debug
        from tools.updater import _init as init
    return update, debug, init

try:
    update, debug, init = set_debug(DEBUG)
except:
    update, debug, init = set_debug(False)

