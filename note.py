'''
2017-01-03 17:36
Function:
    find note from note-Dirs.
    support re.
'''

import os
import pickle
import re
import sys
from collections import defaultdict
import json
import argparse


class HandleNotes(object):
    """search notes from dirs."""

    def __init__(self,
                 dirs,
                 recache=False,
                 fileExplorer=False,
                 pkfile="note.pkl",
                 maps=defaultdict(lambda: "")):
        self.paths = list(map(os.path.realpath, dirs))
        self.recache = recache
        self.file_explorer = fileExplorer
        self.path = os.path.dirname(__file__)
        self.pkfile = os.path.join(self.path, pkfile)
        self.maps = maps
        self.note_names = []

    def open(self, filename):
        """open note according to file type"""
        fix = os.path.splitext(filename)[1]
        order = ""
        if 'SSH_CLIENT' in os.environ:
            order = "vim '{}'".format(filename)
        else:
            if fix == '.ipynb':
                order = "ipython notebook '{}'".format(filename)
            else:
                order = "gio open '{}'".format(filename)
            order = order + " &"
            if self.file_explorer:
                os.popen("nautilus '{}'".format(filename))
        os.system(order)
        # os.popen2(order)

    def getNames(self):
        if self.recache is True:
            for path in self.paths:
                for d, sf, sd in os.walk(path):
                    for j in sd:
                        self.note_names.append(os.path.join(d, j))
            with open(self.pkfile, "wb") as f:
                pickle.dump(self.note_names, f)
        else:
            print("[✓] read cache from pkfile.")
            with open(self.pkfile, 'rb') as f:
                self.noteNames = pickle.load(f)

    def search(self, tags):
        tags = [tag.lower() for tag in tags]  # lower the tags
        self.getNames()
        results = []
        tag = " ".join(tags)
        if tag in self.maps:
            # specific map from mapfile.
            results.append(self.maps[tag])
        else:
            for i in self.noteNames:
                ipath = ""
                for path in self.paths:
                    if path in i:
                        ipath = path
                        break
                tg = True
                for tag in tags:
                    try:
                        if re.search(tag, i[len(ipath) + 1:].lower()) is None:
                            tg = False
                    except Exception as e:
                        print(("Maybe your RE is not correct.\nError: {}"
                               .format(e)))
                        sys.exit(1)
                if tg is True:
                    results.append(i)
        results_group = defaultdict(lambda: [])
        # make results into groups by dirname.
        for res in results:
            if os.path.exists(res):
                # if file exists, add to results.
                results_group[os.path.dirname(res)].append(
                    os.path.basename(res))

        for group, bases in list(results_group.items()):
            # sorted by mtime.
            results_group[group] = sorted(
                bases, key=lambda x: os.path.getmtime(os.path.join(group, x)))
        idx = 1
        results_map = {}
        # record idmap
        for group, bases in list(results_group.items()):
            print(group)
            for ba in bases:
                print(("{:3d}: └─── {}".format(idx, ba)))
                results_map[idx] = os.path.join(group, ba)
                idx += 1
        try:
            if len(results_map) == 0:
                pass
            elif len(results_map) == 1:
                self.open(results_map[1])
            else:
                choice = int(input("input id: "))
                self.open(results_map[choice])
        except Exception as e:
            # print "Error: %s" %e
            pass


def check(iter):
    for i in iter:
        if not os.path.exists(i):
            raise Exception("Not found: {}.".format(i))


def read_config(PATH):
    # read config file(dirs and maps)
    configfile = os.path.join(PATH, "config.json")
    DIRS = []
    MAPS = defaultdict(lambda: "")
    if os.path.exists(configfile):
        try:
            with open(configfile) as jf:
                jsdic = json.load(jf)
                DIRS = jsdic['DIRS']
                MAPS = jsdic['MAPS']
        except Exception as e:
            print(e)
            sys.exit(1)
    # check exists.
    check(DIRS)
    check(MAPS.values())
    return DIRS, MAPS


if __name__ == '__main__':

    PATH = os.path.dirname(__file__)
    DIRS, MAPS = read_config(PATH)

    # print("dirs >>> {}".format(DIRS))
    # print("maps >>> {}".format(MAPS))

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--fileExplorer",
        action="store_true",
        help="open it in file explorer at the same time.")
    parser.add_argument(
        "-r",
        "--recache",
        action="store_true",
        help="recache dirs and files into pkl file.")
    parser.add_argument(
        "-k", "--key", dest="key", nargs='*', help="specify search keyword.")
    args = parser.parse_args()

    # recache to pkl file.
    if args.recache:
        hn = HandleNotes(dirs=DIRS, recache=True, maps=MAPS)
        hn.getNames()
        print("[+] recache done.")
        sys.exit(0)

    hn = HandleNotes(dirs=DIRS, maps=MAPS, fileExplorer=args.fileExplorer)
    if args.key != []:
        hn.search(args.key)
    else:
        sys.exit("Not found: search keywords.")
