#!/bin/python3

import subprocess as sp
import random
import re

def GetSP(input):
    stdout = input.stdout;
    stderr = input.stderr;

    def GetUnempty(string, name=None):
        if(string != "" and string != None):
            if(name is not None):
                return f"\n{name}:\n";
            return string;
        
    return (GetUnempty(stdout), GetUnempty(stderr));

def Run(cmd_array):
    return sp.run(cmd_array, capture_output=True, text=True);

def GetMAC(ip_string):
    ip_info_split = ip_string.split();

    for i in range(len(ip_info_split)):
        if(ip_info_split[i] == "ether"):
            return ip_info_split[i+1];

def ErrorCheck(input, msg=""):
    if(input.returncode != 0):
        raise ValueError(f"[ERROR] {msg}");

iface = input("[INPUT] Connection name (ex: eth0): ");
fake_mac_addres = input("[INPUT] Fake MAC address (ex: cc:38:c9:f7:28:d9): ");

r = Run(["sudo", "ifconfig", iface, "down"]);
print("\n[SHUTDOWN] Shutting down orignal MAC address");
ErrorCheck(r, msg=GetSP(r));

ip_info = Run(["ifconfig", iface]);
ip_info, _ = GetSP(ip_info);

MAC_Address = GetMAC(ip_info);

print("[FAKE-MAC] Setting fake MAC address");
r = Run(["sudo","ifconfig", iface, "hw", "ether", fake_mac_addres]);
ErrorCheck(r, msg=GetSP(r));

print("[RUNING] Opening with fake MAC address");
r = Run(["sudo", "ifconfig", iface, "up"]);
ErrorCheck(r, msg=GetSP(r));

# 00:0c:29:f7:24:d2
