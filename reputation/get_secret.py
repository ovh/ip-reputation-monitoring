#!/usr/bin/env python3
from config import settings
import sys

if __name__ == "__main__":
    secret = settings.get_secret(sys.argv[1])
    if not secret:
        print("{} is empty: '{}'".format(sys.argv[1], secret), file=sys.stderr)
    print(secret)
