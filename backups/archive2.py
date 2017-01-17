#!/usr/bin/env python

import os
import time

sources = {'millenia': '/www/incrementals',
           'corvette': '/work/incrementals'}

destbase = '/corvette/work/Archives'
destbase = '/home/newville/cars5/Data/LinuxArchives'

months = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

rsync_cmd = 'rsync -vaz '
def do_sys(cmd):
    print '# %s' % cmd
    # os.system(cmd)

for mach, folder in sources.items():
    srcdir = '/%s/%s' % (mach, folder)
    # os.path.join('/', mach, folder)
    # print 'source : ', mach,  ' --> ', srcdir
    for fname in os.listdir(srcdir):
        if not fname.endswith('.tar.gz'): continue
        srcfile = os.path.join(srcdir, fname)
        mtime = time.localtime(os.stat(srcfile).st_mtime)
        year = "%i" % mtime.tm_year
        oname  = "%s/%s" % (months[mtime.tm_mon], fname)
        destfile = os.path.join(destbase, mach, 'daily', oname)
        do_sys('%s %s %s' % (rsync_cmd, srcfile, destfile))
