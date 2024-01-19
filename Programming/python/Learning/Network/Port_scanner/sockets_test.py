#!/bin/python3

import socket

port = 7777;
host = socket.gethostbyname(socket.gethostname())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
s.connect((host, port));