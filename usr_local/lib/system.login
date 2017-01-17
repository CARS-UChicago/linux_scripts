#!/bin/tcsh                                         
#                                                  
#  This is system.login file for Linux and csh / tcsh shells
# 
#  This file should be source'd by all users' .cshrc files. 
#  to set default search paths, terminal properties, and 
#  shell behavior.
# 
#  For non-linux systems, see system.login-nonlinux
#                                                   
#  last update: 9-Sept-2008  M Newville
#
######################################################

#
#  determine system type
#
# echo ' system.login'
setenv OSTYPE Linux

#
#  set terminal dependent parameters
switch ( "`tty`" )
case /dev/console:
    breaksw
case /dev/ttyp*:	# SunOS 4
case /dev/ttyq*:	# IRIX 5
case /dev/pts/*:	# SunOS 5 / Linux
    if ( ! $?TERM ) then
        set noglob
        eval `tset -s -Q -m ':?vt100'`
        set term=$TERM
	set glob
    else if ( "$TERM" == "" ||  $TERM == network ) then
        set noglob
        eval `tset -s -Q -m ':?vt100'`
        set term=$TERM
	set glob
    endif
    stty echoe echok -ixany erase "^?" kill "^U" intr "^C"
    breaksw
endsw

# EPICS configuration
setenv EPICS_BASE /usr/local/epics/base
setenv EPICS_EXTENSIONS /usr/local/epics/extensions
setenv EPICS_HOST_ARCH linux-x86_64
setenv EPICS_CA_AUTO_ADDR_LIST NO
setenv EPICS_CA_ADDR_LIST 164.54.160.255
setenv EPICS_DISPLAY_PATH /home/epics/adl/all
setenv QT_PLUGIN_PATH /usr/local/caqtdm-4.1.3/caQtDM_Binaries
setenv CAQTDM_DISPLAY_PATH /usr/local/caqtdm-4.1.3/caQtDM_Tests:/home/epics/ui
setenv SUPPORT /home/epics/support


# IDL configuration
setenv LM_LICENSE_FILE 1700@corvette.cars.aps.anl.gov
source /usr/local/excelis/idl/bin/idl_setup
setenv IDL_PATH "<IDL_DEFAULT>":+/usr/local/idl_user
setenv IDL_STARTUP /usr/local/idl_user/idl_startup.pro

# We no longer set this environment variable because it is a hassle to switch 32/64 bit.  
# IDL now looks in the IDL path for a file of the correct name
# setenv EZCA_IDL_SHARE $EPICS_EXTENSIONS/lib/linux-x86/libezcaIDL.so

setenv MCA_PREFERENCES ~/mca.preferences
setenv XRF_PEAK_LIBRARY  /usr/local/idl_user/epics_mca/xrf_peak_library.txt
setenv JCPDS_PATH        /usr/local/idl_user/epics_mca/jcpds/
setenv IDL_ABS_COEFFS    /usr/local/idl_user/synchrotron/sruff/mass_abs_coeffs.sav
# setenv MOTOR_CALIBRATION /home/epics/support/CARS/iocBoot/motor_calibration.dat
# setenv GRIDREC_SHARE /usr/local/Gridrec/GridrecIDL.so

#  system specific settings: command path, MAN path, etc.
set autologout=14400

# set terminal characteristics for non-CDE login
if ( ! ${?TERM} ) then
    stty sane
    tset -I -Q
endif
if ( ! $?DISPLAY ) then
   if ($?REMOTEHOST) then
      setenv DISPLAY $REMOTEHOST":"0
   endif
endif

# set other environment settings
setenv MAIL /usr/spool/mail/$USER
setenv LANG C   # MN 09-25-03   C or en_US????

setenv LS_COLORS 'no=00:fi=00:di=01;34:ln=04;31:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:su=30:sg=30:tw=30:ow=34:st=30:ex=04;30:*.tar=01;31:*.tgz=01;31:*.svgz=01;31:*.arj=01;31:*.taz=01;31:*.lzh=01;31:*.lzma=01;31:*.zip=01;31:*.z=01;31:*.Z=01;31:*.dz=01;31:*.gz=01;31:*.bz2=01;31:*.bz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.rar=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.jpg=01;35:*.jpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.aac=00;34:*.au=00;34:*.flac=00;34:*.mid=00;34:*.midi=00;34:*.mka=00;34:*.mp3=00;34:*.mpc=00;34:*.ogg=00;34:*.ra=00;34:*.wav=00;34:'

# setenv LANG en_US


alias append_to 'if ( $\!:1 !~ \!:2\:* && $\!:1 !~ *\:\!:2\:* && $\!:1 !~ *\:\!:2 && $\!:1 !~ \!:2 ) setenv \!:1 ${\!:1}\:\!:2'

# add to front of path
alias prepend_to 'if ( $\!:1 !~ \!:2\:* && $\!:1 !~ *\:\!:2\:* && $\!:1 !~ *\:\!:2 && $\!:1 !~ \!:2 ) setenv \!:1 \!:2\:${\!:1}; if ( $\!:1 !~ \!:2\:* ) setenv \!:1 \!:2`echo \:${\!:1} | /usr/bin/sed -e s%^\!:2\:%% -e s%:\!:2\:%:%g -e s%:\!:2\$%%`'

# set path -- default is ( . /usr/sbin /usr/bsd /sbin /usr/bin /bin /usr/bin/X11 )
setenv PATH .:$HOME/bin:/bin:/usr/bin:/usr/local/bin:/usr/X11R6/bin
if ( "$USER" == "root" ) then
  append_to PATH /sbin
  append_to PATH /usr/sbin
endif

# append_to PATH $EPICS_BASE/tools 
append_to PATH $EPICS_BASE/bin/linux-x86_64
append_to PATH /usr/local/epics/epicsV4/bundleCPP/pvAccessCPP/bin/linux-x86_64
append_to PATH $EPICS_EXTENSIONS/bin/linux-x86_64
# append_to PATH /usr/local/Trolltech/Qt-4.8.4/bin/


setenv LD_LIBRARY_PATH $EPICS_EXTENSIONS/lib/linux-x86
setenv CLASSPATH $EPICS_EXTENSIONS/javalib

set history=1000
set savehist=1000
alias gnumake make

setenv PYTHONPATH /usr/local/python/epics

# PSPRINTER is for MEDM
setenv PSPRINTER gse_lom

