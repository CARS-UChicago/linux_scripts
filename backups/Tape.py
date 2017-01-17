#!/usr/bin/python
#
#  variation on Tape backup to backup to daily incremental files
#
#  Matt Newville: U Chicago, 2005
#
import fnmatch, os, sys, string, re, time
import FileFinder

WORKDIR  = "/var/work/backups"

class Tape:
    """ Tape class """

    
    params = {"tar"       : "tar czSlf ",
              'dir':        "/work/incrementals",
              "listfile"  : ".NEWFILES",
              "id_file"   : ".TAPENAME",
              "markfile"  : ".MARKFILE",
              "drive_file": "/etc/mtab",
              "drive_type": "xfs"}

    ignore_dirs = ['.mozilla', '.gnome', '.kde',
                   '^/tmp', 
                   '^/var/work/',
                   '^/usr/local/mysql',
                   '^/home/newville/auto_backup',
                   '^/home/epics/backups',
                   '^/home/epics/scratch',
                   '^/home/webmaster/backups',
                   '^/home/epics/public_html/adls',
                   '^/home/epics/public_html/idl',
                   '^/home/web_backup']

    ignore_files = ['~$','.o$','.tmp$', '.bak$', 'core', 'core\.[0-9]*']

    def __init__(self, debug=True, log_file='', age=1.1):
        self.debug  = debug
        for i in self.params.keys():
            setattr(self,i,self.params[i])
            if i in ('log_file','listfile','markfile','id_file'):
                t = os.path.join(WORKDIR, self.params[i])
                setattr(self,i,t)

        if len(log_file) < 2:
            log_file = time.strftime("logs/%Y_%m_%d.log" , time.localtime())

        self.log_file = os.path.join(WORKDIR, log_file)

        self.age = age

        ign_dirs = self.ignore_dirs
        ign_dirs.append(self.params['dir'])

        self.finder = FileFinder.FileFinder(dir='/',
                                            ignore_files = self.ignore_files,
                                            ignore_dirs  = ign_dirs)

        self.find_files  = self.finder.find_files

        f = open(self.drive_file)
        lines = f.readlines()
        f.close()
        self.drives = []
        for i in lines:
            u = i.split()
            if u[2].startswith(self.params['drive_type']): 
                self.drives.append(u[1])
        
        print "drives :",  self.drives

        self.logfile = open(self.log_file, 'w')
        self.write_log("# Backup date: %s\n" % time.ctime())

    def write_log(self,s):
        if self.debug:   sys.stdout.write( s)
        self.logfile.write(s)
        
    def __del__(self):
        self.logfile.close()


    def show_config(self):
        self.write_log("###  Configuration:\n")
        for i in self.params.keys():
            self.write_log("# %15s:  %s\n" % (i,  getattr(self,i)))
        self.write_log("######################\n")


    def shell_execute(self,s):
        self.write_log("# %s\n" % s);
        os.system(s)
        time.sleep(0.25)


    def list_new_files(self,listfile=None,age=None):
        if age: self.age = age
        self.write_log("#== Archived files\n")
        if listfile is not None: self.listfile  = listfile
        flist = open(self.listfile,'w')
        print("Search for files ", age, self.drives)
        for drive in self.drives:
            self.write_log("#== drive %s\n" % drive)
            newf = self.find_files(root=drive, age=float(self.age))
            for f in newf:
                flist.write("%s\n" % f)
                self.write_log("%s\n" % f)
            self.write_log("#== drive %s: %i files \n" % (drive,len(newf)))
        flist.close()

    def backup_to_file(self, fname=None, listfile=None, age=None):
        " save a local-disk copy of the daily incremental"
        if age is not None: 
            self.age = age
        if fname is None:
            fname   = os.path.join(self.params['dir'], 
                                   time.strftime("%d", time.localtime()))
        self.list_new_files(listfile=listfile, age=age)
        cmd = "%s %s.tar.gz -T %s " % (self.params['tar'], fname, self.listfile)
        self.shell_execute(cmd)

if (__name__ == '__main__'):
    t = Tape(debug=True, log_file='test.log',age=1.4)
    t.show_config()
    t.list_new_files()

