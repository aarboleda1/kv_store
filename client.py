from socket import socket, SOCK_STREAM, AF_INET
import sys
from struct import pack, unpack
from collections import namedtuple

HOST, PORT = "localhost", 8080
Key = namedtuple("Key", ["length", "string_val"])

GET = 0
SET = 1

# Value type
INT = 0
STRING = 1
FLOAT = 2

# AF_INET means IP/SOCK_STREAM means a TCP socket
with socket(AF_INET, SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    if sys.argv[1] == "float":
        k, v = "float_key", 24
        key = Key(len(k), k)
        data = pack(
            "<HI%dsHf" % (key.length,), 
            SET, 
            key.length, 
            bytes(key.string_val, "utf8"),
            FLOAT,
            v
        )
    elif sys.argv[1] == "string":
        k = "string_key"
        value = "value_string"
        key = Key(len(k), k)
        # "<HI%dsHI%ds"
        data = pack(
            "<HI%dsHI%ds" % (key.length, len(value)), 
            SET, 
            key.length, 
            bytes(key.string_val, "utf8"),
            STRING,
            len(value),
            bytes(value, "utf8")
        )
    elif sys.argv[1] == "int":
        k = "int_key"
        key = Key(len(k), k)
        value = 123456
        # "<HI%dsHI%ds"
        data = pack(
            "<HI%dsHq" % (key.length,), 
            SET, 
            key.length, 
            bytes(key.string_val, "utf8"),
            INT,
            value
        )     

    sock.sendall(data)
    # Receive data from the server and shut down
    received = str(sock.recv(1024), "utf-8")

# print("Sent:     {}".format(data))
# print("Received: {}".format(received))
