#!/usr/bin/env python3

import requests
import argparse
from termcolor import colored
from concurrent.futures import ThreadPoolExecutor
import sys

class LFIScanner:
    def __init__(self, url, wordlist, status_code=None, not_found_text=None, verbose=False, threads=1):
        self.url = url
        self.wordlist = wordlist
        self.status_code = status_code
        self.not_found_text = not_found_text
        self.verbose = verbose
        self.threads = threads

        # Tracking variables
        self.vulnerable_count = 0
        self.not_vulnerable_count = 0
        self.error_count = 0

    def update_status(self):
        if not self.verbose:
            sys.stdout.write("\r" + colored(f"Vulnerable: {self.vulnerable_count} ", "green") + 
                            colored(f"| Not Vulnerable: {self.not_vulnerable_count} ", "red") +
                            colored(f"| Errors: {self.error_count}", "yellow"))
            sys.stdout.flush()

    def test_payload(self, payload):
        payload = payload.strip()
        test_url = self.url + payload

        try:
            response = requests.get(test_url)
            content = response.text

            if self.status_code:
                if response.status_code == int(self.status_code):
                    self.vulnerable_count += 1
                    print(colored(f"\n[+] Found potential LFI with payload: {payload}", "green"))
                else:
                    self.not_vulnerable_count += 1
                    if self.verbose:
                        print(colored(f"\n[-] Payload {payload} is not vulnerable", "red"))

            elif self.not_found_text:
                if self.not_found_text not in content:
                    self.vulnerable_count += 1
                    print(colored(f"\n[+] Found potential LFI with payload: {payload}", "green"))
                else:
                    self.not_vulnerable_count += 1
                    if self.verbose:
                        print(colored(f"\n[-] Payload {payload} is not vulnerable", "red"))

            self.update_status()

        except Exception as e:
            self.error_count += 1
            self.update_status()

    def scan(self):
        print(colored("Starting LFI Scanner:", "cyan") + "\n")
        with open(self.wordlist, 'r') as f:
            payloads = f.readlines()

        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            executor.map(self.test_payload, payloads)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LFI Scanner Tool")
    parser.add_argument('-u', '--url', type=str, required=True, help="Target URL (e.g., http://10.10.10.151/blog/?lang=)")
    parser.add_argument('-w', '--wordlist', type=str, required=True, help="Path to the wordlist")
    parser.add_argument('-s', '--status-code', type=str, required=False, help="Expected status code for positive LFI detection")
    parser.add_argument('-t', '--not-found-text', type=str, required=False, help="Text indicating a non-vulnerable/404 page")
    parser.add_argument('-v', '--verbose', action='store_true', help="Show all tested payloads, including non-vulnerable ones")
    parser.add_argument('-T', '--threads', type=int, default=1, help="Number of threads to use")

    args = parser.parse_args()

    scanner = LFIScanner(args.url, args.wordlist, args.status_code, args.not_found_text, args.verbose, args.threads)
    scanner.scan()
