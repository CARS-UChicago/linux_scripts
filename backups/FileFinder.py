import fnmatch, os, string, time,re, sys

class FileFinder:
    """ File Finder Class
    methods:
    
      set_ignore_dirs(d)   give list of directory patterns (regexes) to ignore
      set_ignore_files(f)  give list of file patterns (regexes) to ignore

    """
    stattimes = ('a','m','c') # access, modify, create
    day2sec   = 86400.

    ig_dirs = ['netscape','gnome','webcam', 'kde',
                   '^/usr/local/mysql.*/data',
                   '^/www/htdocs/cgi-data/plots','^/tmp']
    
    ig_files = ['~$','\.o$','\.tmp$', '\.bak$', 'core', 'core\.[0-9]*']


    def __init__(self,recurse = 1, dir='.', use_time = 'm',  age = 1.0,
                 ignore_dirs=None, ignore_files=None):
        try:
            self.tstat = 7 + self.stattimes[use_time]
        except:
            self.tstat = 8
           
        self.dir = dir

        #  set files and directories to ignore
        if (not ignore_dirs):  ignore_dirs  = self.ig_dirs
        self.set_ignore_dirs(ignore_dirs)
        
        if (not ignore_files): ignore_files = self.ig_files
        self.set_ignore_files(ignore_files)

        self.recurse   = recurse     # recurse directories?
        self.age       = age * self.day2sec
        self.starttime = time.time()
        self.dcount    = 1
        self.debug     = 0

    def set_ignore_dirs(self,s):
        self.exclude_dirs  = re.compile(r".*(%s).*" % string.join(s, '|'),re.IGNORECASE).match

    def set_ignore_files(self,s):
        self.exclude_files = re.compile(r".*(%s).*" % string.join(s, '|'),re.IGNORECASE).match
    
    def find_files(self,pattern='*',root=None,age=None):
        if (age):        self.age  = age * self.day2sec
        if (not root):   root = self.dir
        result = []
        # must have at least root folder
        try:
            names = os.listdir(root)
        except os.error:
            return result
        # expand pattern
        if (self.debug == 1):
            self.dcount = self.dcount + 1
            if ((self.dcount % 20) == 0):
                # print root 
                sys.stdout.flush()
                self.dcount = 1

        pat_list = string.splitfields( pattern , ';' )
        # check each file
        for name in names:
            fullname = os.path.normpath(os.path.join(root, name))
            # grab if it matches our pattern and entry type
            for pat in pat_list:
                if fnmatch.fnmatch(name, pat):
                    if (os.path.isfile(fullname) and
                        (not self.exclude_files(fullname))):
                        file_age = self.starttime - os.stat(fullname)[self.tstat] 
                        if (file_age < self.age):
                            result.append(fullname)
                
            # recursively scan other folders, appending results
            if self.recurse:
                if (os.path.isdir(fullname) and
                    (not os.path.islink(fullname))  and
                    (not os.path.ismount(fullname)) and
                    (not self.exclude_dirs(fullname))):
                        result = result + self.find_files(root=fullname, pattern=pattern)
        # print result
        return result


if __name__ == '__main__':
    import time
    w = FileFinder(dir='/root')
    w.debug = 1
    try:
        print "searching ",
        sys.stdout.flush()
        m = w.find_files(age=0.5)
    except KeyboardInterrupt:
        print "interrupted."
        sys.exit(1)
    print "finished."
    for i in  m:
        print i
    
