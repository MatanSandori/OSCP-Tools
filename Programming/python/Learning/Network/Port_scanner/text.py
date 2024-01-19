#!/bin/python3

import time

for i in range(5):
	time.sleep(0.5);
	print(f"{0.5 * (i + 1)} sec passed | {i+1}/{5}");
