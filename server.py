#!/usr/bin/env python3

import time
from socketserver import TCPServer, BaseRequestHandler
from key_value_store import set, get
from struct import unpack, calcsize
from collections import namedtuple
FORMAT_STRING = "hsl"

Key = namedtuple("Key", ["key_length", "key_value"])
Value = namedtuple("Value", ["type", "value", "byte_size"])

# Value type
INT = 0
STRING = 1
FLOAT = 2

# https://docs.python.org/3/library/struct.html
value_to_fmt_string = {
    INT: "q",
    STRING: "",
    FLOAT: "f",
}

class KeyValueRequestHandler(BaseRequestHandler):
    def handle(self) -> None:
        data = self.request.recv(1024)
        offset = 0
        operation, = unpack("H", data[:2])
        offset += 2

        # gets the size of the key
        key_len, = unpack("I", data[offset:offset + 4])
        offset += 4

        # Get the key
        bytes_key, = unpack("%ds" % (key_len), data[offset: offset + key_len])
        key = bytes_key.decode("utf-8")
        offset += key_len


        # Get value type
        value_type, = unpack("H", data[offset:offset + 2])
        offset += 2
        value_type_fmt_string = value_to_fmt_string[value_type]
        value, = unpack(
            value_type_fmt_string, 
            data[offset:offset + calcsize(value_type_fmt_string)]
        )
        set(key, value)
        self.request.sendall("OK".encode("utf8"))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    print(f"Serving on port {PORT}")
    with TCPServer((HOST, PORT), KeyValueRequestHandler) as server:
        server.serve_forever()