#!/usr/bin/env python3
"""Print a unique random password. Usage: gen_password.py [length]"""
import secrets, string, sys

n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
sets = [string.ascii_lowercase, string.ascii_uppercase, string.digits, "!@#$%^&*-_"]
pw = [secrets.choice(s) for s in sets]
pool = "".join(sets)
pw += [secrets.choice(pool) for _ in range(max(n, 12) - len(pw))]
secrets.SystemRandom().shuffle(pw)
print("".join(pw))
