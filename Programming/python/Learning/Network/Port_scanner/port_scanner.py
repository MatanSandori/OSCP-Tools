#!/bin/python3

import sys
import socket
from datetime import datetime as dt

if(len(sys.argv) == 2):
    print("[NAME] finding ip address by name");
    target = socket.gethostbyname(sys.argv[1]);
else:
    print("[AUTO] automaticly finding ip address");
    target = socket.gethostbyname(socket.gethostname());

print("-" * 50);
print(f"[IP] {target}");
print("-" * 50);

try:
    for port in range(1, 10000):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        socket.setdefaulttimeout(1);
        res = s.connect_ex((target, port));
        if(res == 0):
            print(f"[FOUND PORT] port connection found: {res}");
        s.close();
except KeyboardInterrupt:
    print("\n[EXIT] exiting program");
    sys.exit();
except socket.gaierror:
    print("\n[NOT FOUND] hostname could not be resolved");
    sys.exit();
except socket.error:
    print("\n[SERVER ERROR] couldn't connect to server");
    sys.exit();

print("Done");