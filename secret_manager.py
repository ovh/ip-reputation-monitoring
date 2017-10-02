#!/usr/bin/env python3
import hvac
import os
import sys

if 'VAULT_URL' in os.environ and 'VAULT_TOKEN' in os.environ and os.environ['VAULT_TOKEN']:
    vault = hvac.Client(url=os.environ['VAULT_URL'], token=os.environ['VAULT_TOKEN'])
    secrets = vault.read('ip-reputation/config')
else:
    secrets = os.environ

if __name__ == "__main__":
    print(secrets[sys.argv[1]])
