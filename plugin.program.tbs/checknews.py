# -*- coding: utf-8 -*-
import binascii
import koding
import os
import xbmc
import xbmcaddon

from default import Grab_Updates, Check_My_Shares
from koding import converthex

AddonID 	    = 'plugin.program.tbs'
start_option 	= 'normal'
ADDON           = xbmcaddon.Addon(id=AddonID)
mastercheck 	= ADDON.getSetting('master')

try:
    if sys.argv[1] == 'shares' and mastercheck == 'false':
        start_option = 'shares'
except:
    start_option  = 'normal'
    
if start_option == 'shares':
    xbmc.log('### Checking for any updated local shares')
    Check_My_Shares()

else:
    Grab_Updates(converthex('687474703a2f2f746c62622e6d652f636f6d6d2e7068703f783d'),'silent')
    if os.path.exists(xbmc.translatePath('special://home/addons/script.openwindow/functions.py')):
	    xbmc.executebuiltin('RunScript(special://home/addons/script.openwindow/functions.py)')