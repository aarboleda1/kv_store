#!/usr/bin/env python3
import pickle
import sys
import binascii
from typing import Optional, Any
import struct
SET = "set"
GET = "get"

# Value type
INT = 0
STRING = 1
FLOAT = 2

def set(key: str, value: Any) -> None:
    if isinstance(value, float) and _represents_float(value):
        _type = FLOAT
    elif isinstance(value, int) and _represents_int(value):
        _type = INT
    else:
        _type = STRING
    
    try:
        store = pickle.load(open("store.pickle", "rb"))
    except FileNotFoundError:
        store = {}

    store[key] = value, _type
    pickle.dump(store, open("store.pickle", "wb"))
    print("OK")

def get(key: str) -> Optional[str]:
    store = pickle.load(open("store.pickle", "rb"))
    value, _type = store.get(key, (None, None))

    if not value:
        print("Value not found")
    elif _type == FLOAT:
        print(f"(float) {value}")
    elif _type == INT:
        print(f"(int) {value}")
    else:
        print(f'(string) "{value}"')
        
    return value

def _represents_float(_float: str) -> bool:
    """Checks whether a string represents an floating point value
    """    
    try: 
        float(_float) == _float
        return True
    except ValueError: 
        return False    

def _represents_int(s: str) -> bool:
    """Checks whether a string represents an integer value
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
            if _represents_int(value):
                value = int(value)
            elif _represents_float(value):
                value = float(value)
            else: 
                value = value[1: len(value) - 1] if value else value # remove quotations
            set(key, value)
        elif args[0] == GET:
            get(args[1])
        elif args[0] == "exit":
            break

