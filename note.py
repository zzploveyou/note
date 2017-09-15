# coding:utf-8
'''
2017-01-03 17:36
Function:
    find note from note-Dirs.
    support re.
'''

import os
import re
import shutil
import sys
from collections import defaultdict
import pickle

class HandleNotes:

    def __init__(self, Dirs=["/home/zzp/note"], recache=False, 
            pkfile="note.pkl", mapfile="maps.txt"):
        self.paths = map(os.path.realpath, Dirs)
        self.recache = recache
        self.path = os.path.dirname(__file__)
        self.pkfile = os.path.join(self.path, pkfile)
        self.mpfile = os.path.join(self.path, mapfile)
        self.noteNames = []
        self.openMD = 'mdcharm "{:s}"'
        self.openSSH = 'vim "{:s}"'
        self.opendefault = 'gvfs-open "{:s}"' # xdg-open(gnome)
        self.openipynb = 'ipython notebook "{:s}"'
        self.ssh = False
        if 'SSH_CLIENT' in os.environ:
            self.ssh = True

    def open(self, filename):
        # print "filename: %s" % filename
        """open note according to file type"""
        fix = os.path.splitext(filename)[1]
        order = ""
        # print "fix: %s" % fix
        if self.ssh:
            self.openSSH.format(filename)
        else:
            if fix == '.md':
                order = self.openMD.format(filename)
            elif fix == '.ipynb':
                order = self.openipynb.format(filename)
            else:
                order = self.opendefault.format(filename)
        order = order + " &"
        os.system(order)

    def getNames(self):
        if self.recache == True:
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
                i_low = i.lower()
                tg = True
                for tag in tags:
                    if re.search(tag, i[len(ipath) + 1:].lower()) == None:
                        tg = False
                if tg == True:
                    results.append(i)
        
        results_group = defaultdict(lambda : [])
        # make results into groups by dirname.
        for res in results:
            results_group[os.path.dirname(res)].append(os.path.basename(res))

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
    Dirs = ["/home/zzp/note/"]
    if sys.argv[1:] == ["recache"]:
        hn = HandleNotes(Dirs=Dirs, recache=True)
        hn.getNames()
        print("recache done.")
        sys.exit(0)
    else:
        hn = HandleNotes(Dirs=Dirs, recache=False)
        try:
            hn.search(sys.argv[1:])
        except Exception as e:
            """cache need updates"""
            print("maybe you need recache.\nError: %s" %(e))
