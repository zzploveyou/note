# coding:utf-8
'''
2017-01-03 17:36
note and review.
'''

import os
import sys
import log
import shutil

mg = log.Terminal_log()

class Note:
    def __init__(self, filename):
        pass

class HandleNotes:

    def __init__(self, Dir="/home/zzp/note"):
        self.path = os.path.realpath(Dir)
        self.noteNames = []
        self.openMD = 'mdcharm "{:s}"'
        self.openSSH = 'vim "{:s}"'
        self.openPDF = 'okular "{:s}"'
        self.openPIC = 'eog "{:s}"'
    
    def open(self, filename):
        """open note according to file type"""
        fix = os.path.splitext(filename)
        order = ""
        if fix == '.md':
            order = self.openMD.format(filename)
        elif fix == '.pdf':
            order = self.openPDF.format(filename)
        elif fix in ['.jpg', 'png', 'jpeg']:
            order = self.openPIC.format(filename)
        else:
            pass
        os.system(order)

    def getNames(self):
        for d, sf, sd in os.walk(self.path):
            # mg.debug("Dir: %s" % d)
            for i in sf:
                # mg.debug("sub dirs: %s" % i)
                pass
            for j in sd:
                self.noteNames.append(os.path.join(d, j))
                # mg.debug("sub files: %s" % j)

    def search(self, tags):
        self.getNames()
        results = []
        for i in self.noteNames:
            tg = True
            for tag in tags:
                if tag not in i:
                    tg = False
            if tg == True:
                results.append(i)
        for idx, r in enumerate(results):
            print "%d: %s" % (idx, r)
        try:
            choice = int(raw_input("input id: "))
            self.open(results[choice])
        except Exception as e:
            print "Error: %s" %e

if __name__ == '__main__':
    hn = HandleNotes(Dir="/home/zzp/note/")
    hn.search(sys.argv[1:])
