from tools.color import *
from datetime import datetime



def timestamp():
    return datetime.now().strftime()

def update(msg: str):
    print(f"[{timestamp()}][][ {CYAN_BOLD}UPDATE{RESET}     ]: {ITALIC}{msg}{RESET}")

def debug(msg: str):
    print(f"[{timestamp()}][😿][ {BLUE_BOLD}DEBUG{RESET}      ]: {ITALIC}{msg}{RESET}")

def init(msg:str):
    print(f"[{timestamp()}][✨][ {GREEN_BOLD}INITIALIZED{RESET}]: {BOLD}{msg}{RESET}")

def method(msg:str):
    print(f"[{timestamp()}][🔨][ {GREEN_BOLD}METHOD{RESET}     ]: {BOLD}{msg}{RESET}")