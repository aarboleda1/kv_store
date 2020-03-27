from socket import socket, SOCK_STREAM, AF_INET
import sys
from struct import pack
from collections import namedtuple
HOST, PORT = "localhost", 8080
data = " ".join(sys.argv[1:])
args = sys.argv[2:]

# https://docs.python.org/3/library/struct.html
format_str = "hl"
# operation, key, Optional[value]

Key = namedtuple("Key", ["length", "string_val"])

GET = 0
SET = 1

# Value type
INT = 0
STRING = 1
FLOAT = 2
# Variable length encoding
# AF_INET means IP/SOCK_STREAM means a TCP socket
with socket(AF_INET, SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    k, v = "float_val", 24.111
    
    key = Key(len(k), k)

    data = pack(
        "<HI%dsHf" % (key.length,), 
        SET, 
        key.length, 
        bytes(key.string_val, "utf8"),
        FLOAT,
        v
    )

    sock.sendall(data)

    # Receive data from the server and shut down
    received = str(sock.recv(1024), "utf-8")

print("Sent:     {}".format(data))
print("Received: {}".format(received))
