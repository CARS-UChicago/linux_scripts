#!/usr/bin/python
#
# download and save imageis from  web cameras

import epics
from epics.devices import ad_image

from PIL import Image
import shutil
import os
import sys
import time
import threading
import signal
import getopt
from  urllib import urlopen

webcam_root= '/www/apache/htdocs/gsecars/webcam'

pidfile = os.path.join(webcam_root, 'cameras.pid')

os.chdir(webcam_root)
                          
image_urls = {'Canon': "-wvhttp-01-/GetOneShot?image_size=640x480",
              'Axis': 'jpg/%i/image.jpg',
              'Panasonic': 'cgi-bin/camera',
}


cameras =  { 'bmd_canon': ('Canon',   'http://164.54.160.134/'),
             'bmc_canon': ('Canon',   'http://164.54.160.138/'), 
             'idd_panasonic': ('Panasonic', 'http://gse-webcam1.cars.aps.anl.gov/'),
             'idc_panasonic': ('Panasonic', 'http://gse-webcam2.cars.aps.anl.gov/'),
             'idc_axis':  ('Axis',    'http://164.54.160.40/'), 
             'idd_axis':  ('Axis',    'http://164.54.160.142/'), 
             'ide_axis':  ('Axis',    'http://164.54.160.115/'), 
             'bmc_axis':  ('Axis',    'http://164.54.160.141/'), 
             'bmd_axis':  ('Axis',    'http://164.54.160.25/'), 
             'ide_pg1':   ('File',    '/cars5/Data/xas_user/config/liveimages/ide_microscope.jpg'),
             'ide_ps1':   ('EpicsAD', '13IDEPS1:image1:'),
             'idd_pg1':   ('EpicsAD', '13IDD_PG1:image1:'),
             'idd_pg2':   ('EpicsAD', '13IDD_PG2:image1:'),
             'idd_pg3':   ('EpicsAD', '13IDD_PG3:image1:'),
            }

html_text = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<html><meta http-equiv='Pragma'  content='no-cache'>
<meta http-equiv='Refresh' content=30>
<head><title>%s Web Camera</title></head>
<body><h2>%s Web Camera</h2>
<a href="%s%s">
<img src="%s.jpg" width=640 height=480></a>
<p><a href="%s/?C=M;O=D">Image Archive</a>
&nbsp; &nbsp; <a href="%s">Camera Control</a>
&nbsp; &nbsp; <a href=index.html>GSECARS Web Cameras</a> 
</body></html>
"""

def make_directory(base, n=0):
    ctype, cname = cameras[base]
    print("Make Dir ", base, n, ctype, cname)

    if n==0:
        dirname  = base
        img_name = image_urls.get(ctype, cname)
        name     = "13-%s %s" % (cname, ctype)
    else:
        dirname  = "%s%i" % (base,n)
        img_name =  image_urls.get(ctype, 'name') % (n)
        name     = "13-%s %s (%i)" % (cname, ctype, n)

    dir = os.path.join(webcam_root,dirname)
    try:
        os.makedirs(dir)
        print 'made directory ', dir
    except:
        print ' could not make directory ', dir

    html_file = os.path.join(webcam_root,"%s.html" % dirname)
    f = open(html_file,'w')
    f.write(html_text  % (name, name, cname, 
                          img_name, dirname, dirname, cname))
    f.close()
    print 'wrote ', html_file    
    
def create_directories():
    for key,val in cameras.items():
        ctype, source = val
        if ctype == 'Axis':
            for i in range(4):
                make_directory(key,i+1)
        else:
            make_directory(key)
    
#################################################33

class SaverThread(threading.Thread):
    def __init__(self, source, name, delay=2.0, archive_minutes=5.0):
        threading.Thread.__init__(self)
        self.setName(name)
        self.source = source
        self.delay = delay
        self.last_archive = 0
        self.archive_minutes = archive_minutes
        self.filename = os.path.join(webcam_root,  "%s.jpg" % self.getName())
        print('SAVER Thread ', self.filename, self.source)
        
    def archive(self):
        tstr  = time.strftime("%h%d_%H%M", time.localtime())
        fname = os.path.join(webcam_root, self.getName(), "%s.jpg" % tstr)
        shutil.copy(self.filename, fname)
        self.last_archive = time.time()
        # print(" Wrote %s " % fname)
        
    def save_image(self):
        pass
    
    def run(self):
        while True:
            try:
                self.save_image()
                delay = self.delay
                if ((time.localtime()[4] % self.archive_minutes == 0) and
                    ((time.time() - self.last_archive) > 61)):
                    self.archive()
            except:
                delay = self.archive_minutes * 60. * 2.0
            time.sleep(delay)

class FetchEpicsADThread(SaverThread):
    def __init__(self, source, name):
        SaverThread.__init__(self, source, name)
        self.ad = ad_image.AD_ImagePlugin(source)

    def save_image(self):
        colormode =  self.ad.ColorMode_RBV
        im_mode = 'L'
        im_size = [self.ad.ArraySize0_RBV, self.ad.ArraySize1_RBV]

        if colormode == 2:
            im_mode = 'RGB'
            im_size = [self.ad.ArraySize1_RBV, self.ad.ArraySize2_RBV]

        if im_size[0] not in (0, None):            
            img = Image.frombuffer(im_mode, im_size, self.ad.ArrayData,
                                   'raw', im_mode, 0, 1)
            img.save(self.filename, quality=90)
        time.sleep(self.delay)


class FetchFileThread(SaverThread):
    def __init__(self, source, name):
        SaverThread.__init__(self, source, name)

    def save_image(self):
        shutil.copy(self.source, self.filename)
        time.sleep(0.1)
        # print 'File save_image ', self.filename
        
class FetchURLThread(SaverThread):
    def __init__(self, source, name):
        SaverThread.__init__(self, source, name)

    def save_image(self):
        img = urlopen(self.source).read()
        out = open(self.filename, "wb")
        out.write(img)
        out.close()
        # print 'URL save_image ', self.filename
        time.sleep(self.delay)
        
def write_pidfile(pidfile):
    pid = os.getpid()
    try:
        f = open(pidfile,"w")
        f.write("%i\n" % pid)
        f.close()
    except IOError:
        print( 'could not write pid ', pidfile)

def read_pid():
    f = open(pidfile,"r")
    txt = f.readline().strip()
    f.close()
    try:
        pid = int(txt)
    except ValueError:
        pid = 0
    return pid

def kill_process():
    pid = read_pid()
    if check_process():
        print "killing %i\n" % pid
        try:
            os.kill(pid,signal.SIGTERM)
        except OSError:
            pass

def check_process():
    pid = read_pid()
    return  os.path.exists('/proc/%i' % pid)


def start_image_thread(base_url, image, key):
    url = "%s%s" % (base_url,image)
    print ' Would image thread for ' , key
    t = FetchURLThread(url, key, delay=2.0, archive_minutes=5.0)
    t.start()

def run():
    print '=== Start Run ====='
    try:
        write_pidfile(pidfile)
    except IOError:
        time.sleep(10)
        write_pidfile(pidfile)

    print 'starting webcam process with pid = ', read_pid()
    for key, val in cameras.items():
        ctype, source = val
        print ctype, source
        if ctype == 'Axis':
            img_url = image_urls[ctype]
            for i in range(4):
                img =  img_url % (i+1)
                nam =  "%s%i" % (key,i+1)
                url = "%s%s" % (source, img)
                proc = FetchURLThread(url, nam)
                proc.start()
        elif ctype in ('Canon', 'Panasonic'):
            img_url = image_urls[ctype]
            source = "%s%s" % (source, img_url)
            proc = FetchURLThread(source, key)
            proc.start()
        elif ctype == 'File':
            proc = FetchFileThread(source, key)
            proc.start()
        elif ctype == 'EpicsAD':
            proc = FetchEpicsADThread(source, key)
            proc.start()


def check_archive(minutes=60):
    """returns number of files archived in past 60 minutes """
    os.chdir(webcam_root)
    subdirs = [i for i in os.listdir('.') if os.path.isdir(i)]
    newfiles = -1
    now = time.time()

    for s in subdirs:
        tstr  = time.strftime("%h%d_")
        for f in os.listdir(s):
            if f.startswith(tstr):
                age = now - os.stat("%s/%s" %(s,f))[7]
                if age < 60*minutes:
                    newfiles = newfiles + 1
            
    return newfiles
        
    
def main():
    opts, rawargs = getopt.getopt(sys.argv[1:], "h", ["help"])
    try:
        cmd = rawargs.pop(0)
    except IndexError:
        cmd = 'check'

    if cmd not in ('check','status'): 
        cmd = 'check'
   
    for (k,v) in opts:
        if k in ("-h", "--help"): cmd = 'help'

    if 'status' == cmd:
        if check_process():
            print 'webcam appears to be running.'
        else:
            print 'webcam appears to not be running.'            
        newfiles = check_archive()
        print '%i images archived in past hour' % newfiles
        
    else:
        running = check_process()
        newfiles = check_archive()
        if not running:
            run()
        if running and newfiles < 10:
            print 'Restarting web camera: i new files (%s)' % (newfiles, time.ctime())
            kill_process()
            time.sleep(15.0)
            run()
        else:
            print 'webcam running, %i images archived in past hour (%s)' % (newfiles,time.ctime())

if __name__ == '__main__':
    main()
