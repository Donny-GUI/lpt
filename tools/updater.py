from tools.color import *
from datetime import datetime



def timestamp():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

def update(msg: str):
    print(f"[{timestamp()}][ {CYAN_BOLD}UPDATE{RESET}     ]: {ITALIC}{msg}{RESET}")

def _update(msg: str):
    pass 

def debug(msg: str):
    print(f"[{timestamp()}[ {BLUE_BOLD}DEBUG{RESET}      ]: {ITALIC}{msg}{RESET}")

def _debug(msg: str):
    pass

def init(msg:str):
    print(f"[{timestamp()}][ {GREEN_BOLD}INITIALIZED{RESET}]: {BOLD}{msg}{RESET}")
    
def _init(msg:str):
    pass



def method(msg:str):...
    

def method(msg:str):
    print(f"[{timestamp()}][ {GREEN_BOLD}METHOD{RESET}     ]: {BOLD}{msg}{RESET}")

def _method(msg):
    pass 




def set_debug(debug_state=False):
    if debug_state == True:
        from tools.updater import update as update
        from tools.updater import debug as debug
        from tools.updater import init as init
    elif debug_state == False:
        from tools.updater import _update as update
        from tools.updater import _debug as debug
        from tools.updater import _init as init
    return update, debug, init



