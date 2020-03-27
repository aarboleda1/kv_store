#!/usr/bin/env python3

from socketserver import TCPServer, BaseRequestHandler
from key_value_store import set, get
from struct import unpack, calcsize
from collections import namedtuple

Key = namedtuple("Key", ["key_length", "key_value"])
Value = namedtuple("Value", ["type", "value", "byte_size"])

# Value type
INT = 0
STRING = 1
FLOAT = 2

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

        # Get the value 
        if value_type == STRING:
            value_length, = unpack("I", data[offset: offset + 4])
            offset += 4
            _bytes, = unpack("%ds" % value_length, data[offset: offset + value_length])
            value = _bytes.decode("utf-8")
            print(value, 'IS THE VALUE')
        else: 
            if value_type == INT:
                format_string = "q"
            else:
                format_string = "f"
            value, = unpack(
                format_string, 
                data[offset:offset + calcsize(format_string)]
            )

        set(key, value)
        self.request.sendall("OK".encode("utf8"))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    print(f"Serving on port {PORT}")
    with TCPServer((HOST, PORT), KeyValueRequestHandler) as server:
        server.serve_forever()