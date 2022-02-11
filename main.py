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
    #for a, b in config['definitions'].items():
    for a, b in config.items():
        path = b['path']
        target = b['target']
        hash = hash_file(path)
        store_location = store + hash + "-" + target
        if not os.path.exists(store_location):
            shutil.copyfile(path, store_location)
        if not os.path.exists(store_location + "-reference"):
            file_overwrite(store_location + "-reference", n)
        if not os.path.exists(gendir + n + "/" + target):
            os.symlink(store_location, gendir + n + "/" + target)

def init():
    mkdir(r2dir)
    mkdir(store)
    mkdir(gendir)
    initial_state = {
        #"definitions": {
            "r2config": {
                "path": defs,
                "target": "config.json"
            }
        #}
    }
    file_overwrite(defs, json.dumps(initial_state))
    build_generation("0")

def add_file(name, path):
    if not os.path.exists(path):
        print("Error: no such path " + path)
        return
    current = file_read(r2dir + "current_generation")
    latest = file_read(r2dir + "latest_generation")
    if os.path.exists(defs):
        def_location = defs
    else:
        def_location = gendir + current
    config = json.loads(file_read(def_location))
    new = {
        name: {
            "path": path,
            "target": name
        }
    }
    config.update(new)
    file_overwrite(defs, json.dumps(config))
    build_generation(str(int(latest) + 1))

def main():
    parser = argparse.ArgumentParser(
        description = "",
        epilog = ""
    )

    parser.add_argument('--init', action='store_true', help='Setup r2')
    parser.add_argument('-a', '--add-file', nargs = 2, type = str, default = '',
                        metavar = ('<name>', '<path>'), help = "Add file to r2")
    parser.add_argument('-q', '--quick-add', nargs = 1, type = str, default = '',
                        metavar = ('<file>'), help = "quick add file")
    parser.add_argument('-c', '--cat-file', nargs = 2, type = str, default = '',
                        metavar = ('<name>', '<generation>'), help = "show file contents")

    args = parser.parse_args()

    if args.init:
        init()
        exit()
    elif args.add_file != '':
        add_file(args.add_file[0], args.add_file[1])
    elif args.quick_add != '':
        add_file(args.quick_add[0], os.getcwd() + "/" + args.quick_add[0])
    elif args.cat_file != '':
        # TODO this is just a POC rn and breaks if the generation doesn't exist
        print(file_read(gendir + args.cat_file[1] + "/" + args.cat_file[0]))
    else:
        print("try --help")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\nexit')
        exit()
