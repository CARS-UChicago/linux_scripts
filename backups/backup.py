#!/usr/bin/env python
#
#  variation on backup:  back-up from explicit list of folders
#
#  Matt Newville: U Chicago, 2020

import os
import time
from filefinder import FileFinder

tarcmd = 'tar czlf '
newfiles_list = ".NEWFILES"
ignore_files = ['~$','.o$','.tmp$', '.bak$', 'core\.[0-9]*']

class Backup:
    def __init__(self, folder_list=None, age=1.1):
        self.folder_list = folder_list
        self.age = age

    def incremental_backup(self, folder_list=None, age=None):
        if folder_list is not None:
            self.folder_list = folder_list
        if age is not None:
            self.age = age

        filelist = []
        for fname in self.folder_list:
            print("fname " , fname)
            finder = FileFinder(top=fname, age=self.age,
                                ignore_files=ignore_files)
            filelist.extend(finder.find_files())


        filelist.append('')
        with open(newfiles_list, 'w') as fh:
            fh.write('\n'.join(filelist))
            fh.flush()

        # make sure file has been written
        time.sleep(0.5)

        fname = time.strftime("%b%d", time.localtime())
        cmd = "%s %s.tar.gz -T %s " % (tarcmd, fname, newfiles_list)
        print("#  %s" % cmd)
        os.system(cmd)

    def full_backup(self, folder_list=None):
        """full backup - all files that are younger than 50,000 days old"""
        self.incremental_backup(age=50000)


if __name__ == '__main__':
    flist = ('bin', 'Desktop', 'Codes')
    folders = [os.path.abspath(os.path.join('/Users/Newville', f)) for f in flist]
    backup = Backup(folder_list=folders)
    backup.incremental_backup(age=1.1)
