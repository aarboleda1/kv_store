#!/usr/bin/env python3
import pickle
import sys
import binascii
from typing import Optional, Any
import struct
SET = "set"
GET = "get"

"""Key value client
"""

"""
SET PROTOCOL

TIMESTAMP
KEY_LENGTH
KEY
VALUE_LENGTH
VALUE
"""

def set(key: str, value: Any) -> None:
    if isinstance(value, float):
        value = float(value)
    elif isinstance(value, int) or _represents_int(value):
        value = int(value)        
    try:
        store = pickle.load(open("store.pickle", "rb"))
    except FileNotFoundError:
        store = {}
    store[key] = value
    pickle.dump(store, open("store.pickle", "wb"))
    print("OK")

def get(key: str) -> Optional[str]:
    store = pickle.load(open("store.pickle", "rb"))
    value = store.get(key, None)
    if not value:
        print("None")
    elif isinstance(value, float):
        print(f"(float) {value}")
    elif isinstance(value, int):
        print(f"(int) {value}")
    else:
        print('"' + value + '"')
    return value

def _represents_float(_float: Any) -> bool:
    try: 
        float(_float) == _float
        return True
    except ValueError: 
        return False    

def _represents_int(s: str) -> bool:
    """Checks whether a string value represents an integer
    """
    try: 
        int(s)
        return True
    except ValueError: 
        return False

if __name__ == "__main__":
    while 1:
        user_input = input("kv> ")
        args = user_input.split(" ")
        if args[0] == SET:
            _, key, value = args
            set(key, value)
        elif args[0] == GET:
            get(args[1])
        else:
            # TODO error handling
            pass 

