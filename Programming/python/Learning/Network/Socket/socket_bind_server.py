#!/bin/python3

import sys
import socket
import threading

import os
import time

from termcolor import colored

rhost = "192.168.37.132";
rport = 5050;
r_addr = (rhost, rport);

def main():
    print(f"{colored('[*]', 'green')} Starting...");

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    s.bind(r_addr);

    def handle_connections(conn, addr):
        print(f"{colored('[*]', 'orange')} {addr} connected.");

        connected = True;
        while connected:
            msg_length = int(conn.recv(64).decode("utf-8"));
            msg = conn.recv(msg_length).decode("utf-8");
            print(f"{colored('[*]', 'yellow')} {addr} send:\n{msg}");

    def start():
        s.listen();
        while True:
            try:
                conn, addr = s.accept();
                handle_func = threading.Thread(target=handle_connections, args=(conn, addr,));
                handle_func.start();
                print(f"{colored('[*]', 'green')} Server is running...");
            except:
                print(f"{colored('[*]', 'red')} No connection.");
                break;
                
        s.close();

    start();

main();