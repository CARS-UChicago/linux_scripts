#!/usr/bin/env python

import os
import time


def do_backup(prefix, flist):
    datestr = time.strftime("%Y_%m_%d" , time.localtime())
    args = " ".join(flist)
    cmd  = "tar czSlf %s_%s.tar.gz %s" % (prefix, datestr, args)
    print(cmd)
    os.system(cmd)

sys_folders = ('/boot', '/etc', '/opt', '/var/account/', '/var/.updated ',
               '/var/adm/', '/var/cache/ ', '/var/crash/ ', '/var/cvs/',
               '/var/db/', '/var/kerberos/', '/var/lib/ ', '/var/local/ ',
               '/var/log/ ', '/var/mail/ ', '/var/nis/ ', '/var/opt/',
            '/var/spool/', '/var/yp/ ', '/var/work/backups/ ')

do_backup('sys', sys_folders)
do_backup('usr', ['/usr/'])
do_backup('home', ['/home/'])

