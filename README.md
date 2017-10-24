# linux_scripts

This is a collection of scripts and configuration files used at CARS for configuring linux systems.  There is no explicit installation order, and the files are expected to be placed in the correct location on the system, generally given by the directory and file name.



Yum packages required:
==========================

  yum install 
  IDL License manager may complain with 
    error: lib64ld-lsb-x86-64.so.3: bad ELF interpreter

  The solution:
     yum install redhat-lsb


Services
=========

   systemctl enable nfs
   systemctl enable sssd
   systemctl enable smb



   systemctl start rsh.socket
   systemctl start rexec.socket
   systemctl start rlogin.socket

   systemctl enable rsh.socket
   systemctl enable rexec.socket
   systemctl enable rlogin.socket

    

Setting up rsh:
   systemctl start rsh.socket
   systemctl start rexec.socket
   systemctl start rlogin.socket

   systemctl enable rsh.socket
   systemctl enable rexec.socket
   systemctl enable rlogin.socket

  add iocboot account:

 /etc/passwd:
     iocboot:x:1001:400:IOC Boot:/home/iocboot:/bin/bash
 /etc/group
     epics:x:400:epics,iocboot
     iocboot:x:1001

 /etc/hosts.allow
    in.rshd: LOCAL, .cars.aps.anl.gov

 /home/iocboot/.rhosts:   chown iocboot.iocboot, chmod 644
     ioc13bma.cars.aps.anl.gov iocboot
     ioc13bmc.cars.aps.anl.gov iocboot
     ioc13bmd.cars.aps.anl.gov iocboot
     ioc13ida.cars.aps.anl.gov iocboot
     ioc13idc.cars.aps.anl.gov iocboot
     ioc13idd.cars.aps.anl.gov iocboot
     ioc13ide.cars.aps.anl.gov iocboot
     ioc13lab.cars.aps.anl.gov iocboot
     ioc13lab2.cars.aps.anl.gov iocboot
     ioc13ge1.cars.aps.anl.gov iocboot
     ioc13ge2.cars.aps.anl.gov iocboot
     ioc15lab.cars.aps.anl.gov iocboot
     ioc15ida.cars.aps.anl.gov iocboot
     millenia.cars.aps.anl.gov epics
     corvette.cars.aps.anl.gov epics
     corvette.cars.aps.anl.gov iocboot
     ion.cars.aps.anl.gov epics






