from socket import socket, SOCK_STREAM, AF_INET
import sys
from struct import pack, unpack, calcsize
from collections import namedtuple
HOST, PORT = "localhost", 8080
Key = namedtuple("Key", ["length", "string_val"])

GET = 0
SET = 1

# Value type
INT = 0
STRING = 1
FLOAT = 2
k, v = "abc", 30

key = Key(len(k), k)

data = pack(
    "<HI%dsHq" % (key.length,), 
    SET, 
    key.length, 
    bytes(key.string_val, "utf8"),
    INT,
    v
)

# get operation GET or SET
offset = 0
operation, = unpack("H", data[:2])
offset += 2


# gets the size of the key
key_len, = unpack("I", data[offset:offset + 4])
offset += 4

# Get the key
key, = unpack("%ds" % (key_len), data[offset: offset + key_len])
key = key.decode("utf-8")
offset += key_len

key_struct = Key(key_len, key)

# BEGIN VALUE
# Get value type
value_type, = unpack("H", data[offset:offset + 2])
offset += 2

value, = unpack("q", data[offset:offset + calcsize("q")])

assert key_len == 3, "Key shoudl equal 3"
assert key == "abc"
assert value_type == INT, f"Value type is {value_type}, not int"
assert value == v, f"Value is equal to {value}, not {v}"