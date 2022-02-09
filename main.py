#!/usr/bin/env python3

import os
import json
import shutil
import hashlib
import argparse

home = os.path.expanduser('~')
r2dir = home + "/.r2/"
store = r2dir + "store/"
gendir = r2dir + "generations/"
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

def hash_file(filename):
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    with open(filename, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return hasher.hexdigest()

def build_generation(n):
    mkdir(gendir + n)
    file_overwrite(r2dir + "latest_generation", n)
    file_overwrite(r2dir + "current_generation", n)
    config = json.loads(file_read(defs))
    for a, b in config.items():
        if a == "r2config":
            path = b['path']
            target = b['target']
            hash = hash_file(path)
            store_location = store + hash + "-" + target
            shutil.copyfile(path, store_location)
            if not os.path.exists(gendir + n + "/" + target):
                os.symlink(store_location, gendir + n + "/" + target)

def init():
    mkdir(r2dir)
    mkdir(store)
    mkdir(gendir)
    initial_state = {
        "r2config": {
            "path": defs,
            "reference": "core",
            "target": "config.json"
        }
    }
    file_overwrite(defs, json.dumps(initial_state))
    build_generation("0")
    os.remove(defs)

def add_file_to_def(name, path):
    pass

def main():
    parser = argparse.ArgumentParser(
        description = "",
        epilog = ""
    )

    parser.add_argument('--init', action='store_true', help='Setup r2')

    args = parser.parse_args()

    if args.init:
        init()
    else:
        print("try --help")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\nexit')
        exit()
