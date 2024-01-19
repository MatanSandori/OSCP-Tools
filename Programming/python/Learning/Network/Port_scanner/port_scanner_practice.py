#!/bin/python3

import sys
import socket

print("[STARTING] starting program")

target = socket.gethostbyname(socket.gethostname());
port_range = range(0, 10000);

ports_founds = [];

try:
    for port in port_range:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        socket.setdefaulttimeout(1);
        res = s.connect_ex((target, port));
        if(res == 0):
            print(f"[PORT FOUND] port found: {port}");
            ports_founds.append(port);
except KeyboardInterrupt:
    print("[EXIT] exiting program");
    sys.exit();
except:
    pass;

if(len(ports_founds) == 0):
    print("No ports found");
else:
    print(f"[ALL PORTS] {ports_founds}");