# coding:utf-8
'''
2017-01-03 17:36
note and review.
'''

import os
import shutil
import sys
from collections import defaultdict

class HandleNotes:

    def __init__(self, Dirs=["/home/zzp/note"]):
        self.paths = map(os.path.realpath, Dirs)
        self.noteNames = []
        self.openMD = 'mdcharm "{:s}"'
        self.openSSH = 'vim "{:s}"'
        self.openPDF = 'okular "{:s}"'
        self.openPIC = 'eog "{:s}"'
        self.opendefault = 'xdg-open "{:s}"'
        self.ssh = False
        if 'SSH_CLIENT' in os.environ:
            self.ssh = True

    def open(self, filename):
        # print "filename: %s" % filename
        """open note according to file type"""
        fix = os.path.splitext(filename)[1]
        order = ""
        # print "fix: %s" % fix
        if fix == '.md':
            if not self.ssh:
                order = self.openMD.format(filename)
            else:
                order = self.openSSH.format(filename)
        elif fix == '.pdf':
            order = self.openPDF.format(filename)
        elif fix in ['.jpg', 'png', 'jpeg']:
            order = self.openPIC.format(filename)
        elif not self.ssh:
            order = self.opendefault.format(filename)
        else:
            order = self.openSSH.format(filename)
        os.system(order)

    def getNames(self):
        for path in self.paths:
            for d, sf, sd in os.walk(path):
                for i in sf:
                    pass
                for j in sd:
                    self.noteNames.append(os.path.join(d, j))

    def search(self, tags):
        tags = [tag.lower() for tag in tags]  # lower the tags
        self.getNames()
        results = []
        for i in self.noteNames:
            ipath = ""
            for path in self.paths:
                if path in i:
                    ipath = path
                    break
            i_low = i.lower()
            tg = True
            for tag in tags:
                if tag not in i[len(ipath) + 1:].lower():
                    tg = False
            if tg == True:
                results.append(i)

        results_group = defaultdict(lambda: [])
        # make results into groups by dirname.
        for re in results:
            results_group[os.path.dirname(re)].append(os.path.basename(re))

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
            choice = int(raw_input("input id: "))
            self.open(results_map[choice])
        except Exception as e:
            # print "Error: %s" %e
            pass

if __name__ == '__main__':
    Dirs = ["/home/zzp/note/"]
    hn = HandleNotes(Dirs=Dirs)
    hn.search(sys.argv[1:])
