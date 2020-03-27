#!/usr/bin/env python
#
#  incremental or full backup for a list of folders
#
#  Matt Newville: U Chicago, 2020

import os
import time
from filefinder import FileFinder

tarcmd = 'tar czlf '
newfiles_list = '.NEWFILES'
ignore_files = ['~$','.o$','.tmp$', '.bak$', 'core\.[0-9]*']

def incremental_backup(folders, top='.', target='.', age=1.1, tformat='%d'):
    '''incremental backup for a list of folders

    Arguments
    ----------
    folders    list of folders to backup (relative to top)
    top        full path to top-level folder ('.')
    target     full path to target folder ('.')
    age        age (in days) for incremental backup
    tformat    format string for time.strformat for output tar file ('%d')
    '''
    filelist = []
    for fname in folders:
        fname = os.path.abspath(os.path.join(top, fname))
        finder = FileFinder(top=fname, age=age,
                            ignore_files=ignore_files)
        filelist.extend(finder.find_files())

    filelist.append('')
    with open(newfiles_list, 'w') as fh:
        fh.write('\n'.join(filelist))
        fh.flush()

    # make sure file has been written
    time.sleep(0.5)

    fname = time.strftime(tformat, time.localtime())
    fname = os.path.join(target, '%s.tar.gz' % fname)
    cmd = '%s %s -T %s ' % (tarcmd, fname, newfiles_list)
    print('#  %s (%d files)' % (cmd, len(filelist)))
    os.system(cmd)

def full_backup(folders=None, top=None, target=None):
    '''full backup = incremental_backup(age=50000) '''
    incremental_backup(folders=folders, top=top, target=target,
                       age=50000, tformat='%Y_%b%d')


if __name__ == '__main__':
    folders = ('bin', 'Desktop', 'Codes')
    home = os.environ['HOME']
    incremental_backup(folders=folders, top=home, target=home, age=1.1)
