#!/usr/bin/env python3

import os
import json

home = os.path.expanduser('~')
r2dir = home + "/.r2/"
store = r2dir + "store/"
defs = r2dir + "config.json"

def mkdir(d):
    if not os.path.exists(d):
        os.mkdir(d)

def file_append(filename, contents):
    f = open(filename, "a")
    f.write(contents)
    f.close()

def file_overwrite(filename, contents):
    f = open(filename, "w")
    f.write(contents)
    f.close()

def file_read(filename):
    f = open(filename, "r")
    return f.read()

def init():
    mkdir(r2dir)
    mkdir(store)
    initial_state = {
        "r2config": {
            "path": defs,
            "reference": "core",
            "target": "config.json"
        }
    }
    file_overwrite(defs, json.dumps(initial_state))

def add_file_to_def(name, path):
    pass

def main():
    init()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\nexit')
        exit()
