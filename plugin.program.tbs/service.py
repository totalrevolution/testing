# -*- coding: utf-8 -*-
import default
import koding
import os
import re
import sys
import time
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

######################################################
AddonID          = 'plugin.program.tbs'
AddonName        = 'Maintenance'
######################################################
ADDON            =  xbmcaddon.Addon(id=AddonID)
dialog           =  xbmcgui.Dialog()
dp               =  xbmcgui.DialogProgress()
HOME             =  xbmc.translatePath('special://home/')
USERDATA         =  xbmc.translatePath('special://home/userdata')
ADDON_DATA       =  xbmc.translatePath(os.path.join(USERDATA,'addon_data'))
ADDONS           =  xbmc.translatePath(os.path.join(HOME,'addons'))
cfgfile          =  xbmc.translatePath(os.path.join(ADDON_DATA,AddonID,'cfg'))
sleeper          =  os.path.join(ADDONS,AddonID,'resources','tmr')
internetcheck    =  ADDON.getSetting('internetcheck')
cachecheck       =  ADDON.getSetting('cleancache')
cbnotifycheck    =  ADDON.getSetting('cbnotifycheck')
mynotifycheck    =  ADDON.getSetting('mynotifycheck')
flashsplash      = '/flash/oemsplash.png'
newsplash        =  xbmc.translatePath('special://home/media/branding/Splash.png')
epgdst           =  xbmc.translatePath('special://home/addons/packages/epg')
runwizard        =  os.path.join(ADDON_DATA,'script.openwindow','RUN_WIZARD')
install_complete =  os.path.join(ADDON_DATA,'script.openwindow','INSTALL_COMPLETE')
#---------------------------------------------------------------------------------------------------
default.Adult_Filter('false','startup')
default.Sync_Settings()
# Make sure this doesn't interfere with startup wizard
if not os.path.exists(runwizard) and os.path.exists(install_complete):
    xbmc.log('### TBS SERVICE - RUNWIZARD EXISTS AND INSTALL COMPLETE. RUNNING FUNCTIONS')
    if os.path.exists(xbmc.translatePath('special://home/addons/script.openwindow/functions.py')):
        xbmc.executebuiltin('RunScript(special://home/addons/script.openwindow/functions.py)')
    elif os.path.exists(xbmc.translatePath('special://xbmc/addons/script.openwindow/functions.py')):
        xbmc.executebuiltin('RunScript(special://xbmc/addons/script.openwindow/functions.py)')
   
if internetcheck == 'true':
    xbmc.executebuiltin('XBMC.AlarmClock(internetloop,XBMC.RunScript(special://home/addons/%s/connectivity.py,silent=true),00:01:00,silent,loop)'%AddonID)

if cachecheck == 'true':
    xbmc.executebuiltin('XBMC.AlarmClock(cleancacheloop,XBMC.RunScript(special://home/addons/%s/cleancache.py,silent=true),12:00:00,silent,loop)'%AddonID)

sleep = koding.Text_File(sleeper,'r')

#get filesizes
if os.path.exists(flashsplash):
    flashsize = os.path.getsize(flashsplash)
else:
    flashsize = 0

if os.path.exists(newsplash):
    newsize = os.path.getsize(newsplash)
else:
    newsize = 0

if flashsize != newsize and newsize != 0 and flashsize != 0:
    try:
        os.system('mount -o remount,rw /flash')
        os.system('cp /storage/.kodi/media/branding/Splash.png /flash/oemsplash.png')
        os.system('cp /storage/.kodi/media/branding/Splash.png /storage/.kodi/media/Splash.png')
    except:
        pass

if sleep == '':
    if os.path.exists(sleeper):
        koding.Text_File(sleeper,'w','23:59:59')

if not os.path.exists(runwizard):
    xbmc.executebuiltin('RunScript(special://home/addons/%s/checknews.py,shares)'%AddonID)

xbmc.executebuiltin('XBMC.AlarmClock(Shareloop,XBMC.RunScript(special://home/addons/%s/checknews.py,shares),12:00:00,silent,loop)'%AddonID)

xbmc.log('### SLEEP: %s'%sleep)

if sleep != '':
    xbmc.executebuiltin('XBMC.AlarmClock(Notifyloop,XBMC.RunScript(special://home/addons/%s/checknews.py,silent=true),%s,silent,loop)'%(AddonID, sleep))