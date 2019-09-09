#!/usr/bin/env python3
'''Simple scripts'''

from subprocess import run
import sys


def main() -> None:
    cmd = ['uvicorn', 'jsonschema_test.main:app', '--reload']
    result = run(cmd, stdin=sys.stdin, stdout=sys.stdout)
    sys.exit(result.returncode)
