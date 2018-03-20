# coding:utf-8
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

from config import Dirs


class HandleNotes:

    def __init__(self, Dirs=["/home/zzp/note"], recache=False,
                 fileExplorer=False, pkfile="note.pkl", mapfile="maps.txt"):
        self.paths = map(os.path.realpath, Dirs)
        self.recache = recache
        self.fileExplorer = fileExplorer
        self.path = os.path.dirname(__file__)
        self.pkfile = os.path.join(self.path, pkfile)
        self.mpfile = os.path.join(self.path, mapfile)
        self.noteNames = []

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
            if self.fileExplorer:
                os.popen2("nautilus '{}'".format(filename))
        os.system(order)
        # os.popen2(order)

    def getNames(self):
        if self.recache is True:
            for path in self.paths:
                for d, sf, sd in os.walk(path):
                    for i in sf:
                        pass
                    for j in sd:
                        self.noteNames.append(os.path.join(d, j))
            with open(self.pkfile, "wb") as f:
                pickle.dump(self.noteNames, f)
        else:
            print("[✓] read cache from pkfile.")
            with open(self.pkfile, 'rb') as f:
                self.noteNames = pickle.load(f)

    def search(self, tags):
        tags = [tag.lower() for tag in tags]  # lower the tags
        self.getNames()
        results = []
        if os.path.exists(self.mpfile):
            # read map file.
            mps = {}
            for line in open(self.mpfile):
                tmp = line.strip().split("#")
                if len(tmp) == 2:
                    mps[tmp[0]] = tmp[1]
            tag = " ".join(tags)
        if tag in mps:
            # specific map from mapfile.
            results.append(mps[tag])
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
                        print("Maybe your RE is not correct.\nError: {}"
                              .format(e))
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

        for group, bases in results_group.items():
            # sorted by mtime.
            results_group[group] = sorted(
                bases, key=lambda x: os.path.getmtime(os.path.join(group, x)))
        idx = 1
        results_map = {}
        # record idmap
        for group, bases in results_group.items():
            print(group)
            for ba in bases:
                print("%3d: %s %s" % (idx, "└─" + 2 * "─", ba))
                results_map[idx] = os.path.join(group, ba)
                idx += 1
        try:
            if len(results_map) == 0:
                pass
            elif len(results_map) == 1:
                self.open(results_map[1])
            else:
                choice = int(raw_input("input id: "))
                self.open(results_map[choice])
        except Exception as e:
            # print "Error: %s" %e
            pass


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("python note.py help")
        sys.exit(0)
    if sys.argv[1:] == ["recache"]:
        hn = HandleNotes(Dirs=Dirs, recache=True)
        hn.getNames()
        print("[+] recache done.")
        sys.exit(0)
    elif sys.argv[1:] == ["help"]:
        print("Usage: python note.py substring1 substring2 ...\n\
            \nAttention: please don't forget quotate each substring\
if using RE.\n\
            \npython note.py help\n  display this help page.\n\
            \npython note.py file substring1 substring2 ...\n\
open file in fileExplorer.")
        sys.exit(0)
    elif sys.argv[1] == "file":
        hn = HandleNotes(Dirs=Dirs, fileExplorer=True)
        hn.search(sys.argv[2:])
    else:
        hn = HandleNotes(Dirs=Dirs)
        hn.search(sys.argv[1:])
