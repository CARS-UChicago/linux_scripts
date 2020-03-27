import fnmatch, os, string, time,re, sys

stattimes = ('a', 'm', 'c') # access, modify, create
day2sec   = 86400.

ig_dirs = [ '^/usr/local/mysql.*',  '^/tmp']

ig_files = ['~$','\.o$','\.tmp$', '\.bak$', 'core', 'core\.[0-9]*']


class FileFinder:
    """ File Finder Class
    methods:

      set_ignore_dirs(d)   give list of directory patterns (regexes) to ignore
      set_ignore_files(f)  give list of file patterns (regexes) to ignore

    """

    def __init__(self, top=None, recurse=True, use_time='m', age=1.0,
                 ignore_dirs=None, ignore_files=None, debug=False):
        try:
            self.tstat = 7 + self.stattimes[use_time]
        except:
            self.tstat = 8

        self.top = top
        self.recurse = recurse     # recurse directories?
        self.age  = age * day2sec
        self.starttime = time.time()
        self.dcount = 1
        self.debug  = debug

        #  set files and directories to ignore
        self.set_ignore_dirs(ignore_dirs or ig_dirs)
        self.set_ignore_files(ignore_files or ig_files)


    def set_ignore_dirs(self, s):
        self.exclude_dirs  = re.compile(r".*(%s).*" % '|'.join(s),re.IGNORECASE).match

    def set_ignore_files(self, s):
        self.exclude_files = re.compile(r".*(%s).*" % '|'.join(s),re.IGNORECASE).match

    def find_files(self, top=None, pattern='*', age=None):
        if age is not None:
            self.age  = age * day2sec
        if top is None:
            top = self.top

        result = []
        # must have at least top folder
        try:
            names = os.listdir(top)
        except os.error:
            return result
        # expand pattern
        if self.debug:
            self.dcount = self.dcount + 1
            if ((self.dcount % 20) == 0):
                sys.stdout.flush()
                self.dcount = 1

        pat_list = pattern.split(';' )
        # check each file
        for name in names:
            fullname = os.path.normpath(os.path.join(top, name))
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
                        result = result + self.find_files(top=fullname, pattern=pattern)
        return result


if __name__ == '__main__':
    import time
    w = FileFinder(top='../..', debug=False)
    try:
        print("# searching ... ", end='')
        sys.stdout.flush()
        m = w.find_files(age=0.5)
    except KeyboardInterrupt:
        print( "interrupted.")
        sys.exit(1)
    print("finished.")
    for i in  m:
        print(i)
