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
        tags = [tag.lower() for tag in tags] # lower the tags
        self.getNames()
        results = []
        for i in self.noteNames:
            i_low = i.lower()
            tg = True
            for tag in tags:
                if tag not in i[len(self.path)+1:].lower(): tg = False
            if tg == True: results.append(i)
        for idx, r in enumerate(results):
            print "%d: %s" % (idx, r[len(self.path)+1:])
        try:
            choice = int(raw_input("input id: "))
            self.open(results[choice])
        except Exception as e:
            # print "Error: %s" %e
            pass

if __name__ == '__main__':
    hn = HandleNotes(Dir="/home/zzp/note/")
    hn.search(sys.argv[1:])
