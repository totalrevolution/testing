# -*- coding: utf-8 -*-
import koding
import os
import pyxbmct
import re
import sys
import time
import urllib
import urllib2
import urlparse
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import shutil
import zipfile

try: from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database

from koding import *

try:
    AddonID = xbmcaddon.Addon().getAddonInfo('id')
except:
    AddonID = Caller()

ADDON            =  xbmcaddon.Addon(id=AddonID)
ADDON_PATH       =  ADDON.getAddonInfo('path')
USB              =  Addon_Setting(setting='zip')
thirdparty       =  Addon_Setting(setting='thirdparty')
userid           =  Addon_Setting(setting='userid')
debug            =  Addon_Setting(setting='debug')
HOME             =  xbmc.translatePath('special://home/')
USERDATA         =  xbmc.translatePath('special://profile/')
ADDON_DATA       =  os.path.join(USERDATA,  'addon_data')
TBSDATA          =  os.path.join(ADDON_DATA,AddonID)
PLAYLISTS        =  os.path.join(USERDATA,  'playlists')
MEDIA            =  os.path.join(HOME,      'media')
DATABASE         =  os.path.join(USERDATA,  'Database')
THUMBNAILS       =  os.path.join(USERDATA,  'Thumbnails')
ADDONS           =  os.path.join(HOME,      'addons')
PACKAGES         =  os.path.join(ADDONS,    'packages')
BRANDART         =  os.path.join(MEDIA,     'branding','Splash.png')
KEYMAPS          =  os.path.join(USERDATA,  'keymaps','keyboard.xml')
KEYWORD_FILE     =  os.path.join(HOME,      'userdata','addon_data','script.openwindow','keyword')
FAVS             =  os.path.join(USERDATA,  'favourites.xml')
GUI              =  os.path.join(USERDATA,  'guisettings.xml')
SOURCE           =  os.path.join(USERDATA,  'sources.xml')
ADVANCED         =  os.path.join(USERDATA,  'advancedsettings.xml')
RSS              =  os.path.join(USERDATA,  'RssFeeds.xml')
PROGRESS_TEMP    =  os.path.join(TBSDATA,   'progresstemp')
SLEEPER          =  os.path.join(ADDON_PATH,'resources','tmr')
KEYWORD_CREATE   =  os.path.join(TBSDATA,   'keyword_create.txt')
CONFIG           =  '/storage/.config/'
STORAGE          =  '/storage/'

dialog           =  xbmcgui.Dialog()
dp               =  xbmcgui.DialogProgress()
skin             =  xbmc.getSkinDir()
artpath          =  os.path.join(ADDON_PATH,'resources')
checkicon        =  os.path.join(artpath,'check.png')
unknown_icon     =  os.path.join(artpath,'update.png')
dialog_bg        =  os.path.join(artpath,'background.png')
black            =  os.path.join(artpath,'black.png')
db_social        =  xbmc.translatePath('special://profile/addon_data/plugin.program.tbs/social.db')
pos              =  0
listicon         =  ''

ACTION_NAV_BACK  =  92
ACTION_MOVE_UP   =  3
ACTION_MOVE_DOWN =  4

if os.path.exists(BRANDART):
    FANART = BRANDART
else:
    FANART = os.path.join(ADDONS,AddonID,'fanart.jpg')

if thirdparty == 'true':
    social_shares = 1
else:
    social_shares = 0

master_modes = {
# Required for certain koding functions to work
    "show_tutorial"      : "Show_Tutorial(url)",
    "tutorials"          : "Grab_Tutorials()",
    'addon_browser'      : 'Addon_Browser(url)',
    'addon_removal_menu' : 'Addon_Removal_Menu(url)',
    'adult_filter'       : 'Adult_Filter(url)',
    'ASCII_Check'        : 'ASCII_Checker()',
    'backup'             : 'BACKUP()',
    'backup_restore'     : 'Backup_Restore()',
    'backup_option'      : 'Backup_Option()',
    'browse_repos'       : 'Browse_Repos()',
    'change_id'          : 'Change_ID()',
    'check_shares'       : 'Check_My_Shares(url)',
    'check_updates'      : 'Addon_Check_Updates()',
    'clear_cache'        : 'Clear_Cache()',
    'create_username'    : 'Create_Username()',
    'disable_master'     : 'Disable_Master()',
    'enable_shares'      : 'Enable_Shares(url)',
    'exec_xbmc'          : 'Exec_XBMC(url)',
    'fresh_install'      : 'Fresh_Install()',
    'full_clean'         : 'Full_Clean()',
    'grab_updates'       : 'Grab_Updates(url)',
    'hide_passwords'     : 'Hide_Passwords()',
    'install_venz_menu'  : 'Install_Venz_Menu(url)',
    'install_content'    : 'Install_Content(url)',
    'install_from_zip'   : 'Install_From_Zip()',
    'ipcheck'            : 'IP_Check()',
    'keywords'           : 'Keyword_Search()',
    'kill_xbmc'          : 'Force_Close()',
    'log'                : 'Log_Viewer()',
    'main_menu_install'  : 'Main_Menu_Install(url)',
    'open_sf'            : 'Open_SF()',
    'openelec_settings'  : 'OpenELEC_Settings()',
    'play_video'         : 'Play_Video(url)',
    'remove_addon_data'  : 'Remove_Addon_Data()',
    'remove_addons'      : 'Remove_Addons(url)',
    'remove_crash_logs'  : 'Remove_Crash_Logs()',
    'remove_packages'    : 'Remove_Packages()',
    'remove_textures'    : 'Remove_Textures_Dialog()',
    'restore_backup'     : 'Restore_Backup_XML(video,url,description)',
    'restore_option'     : 'Restore_Option()',
    'restore_zip'        : 'Restore_Zip_File(url)',
    'search_content'     : 'Search_Content(url)',
    'search_content_main': 'Search_Content_Main(url)',
    'social_menu'        : 'Social_Menu()',
    'start'              : 'Categories()',
    'startup_wizard'     : 'xbmc.executebuiltin("RunAddon(script.openwindow)")',
    'sync_settings'      : 'Sync_Settings()',
    'text_guide'         : 'Text_Guide(url)',
    'tools'              : 'Tools()',
    'tools_addon_removal': 'Tools_Addon_Removal()',
    'tools_addons'       : 'Tools_Addons()',
    'tools_clean'        : 'Tools_Clean()',
    'tools_misc'         : 'Tools_Misc()',
    'unhide_passwords'   : 'Unhide_Passwords()',
    'update'             : 'Update_Repo()',
    'uploadlog'          : 'Upload_Log()',
    'xbmcversion'        : 'XBMC_Version(url)',
    'wipe_xbmc'          : 'Wipe_Kodi()'
}

#-----------------------------------------------------------------------------------------------------------------    
# Popup class - thanks to whoever codes the help popup in TVAddons Maintenance for this section. Unfortunately there doesn't appear to be any author details in that code so unable to credit by name.
class SPLASH(xbmcgui.WindowXMLDialog):
    
    def __init__(self,*args,**kwargs):
        self.shut=kwargs['close_time']
        xbmc.executebuiltin("Skin.Reset(AnimeWindowXMLDialogClose)")
        xbmc.executebuiltin("Skin.SetBool(AnimeWindowXMLDialogClose)")
    
    def onFocus(self,controlID):
        pass
    
    def onClick(self,controlID): 
        if controlID==12:
            xbmc.Player().stop()
            self._close_dialog()
    
    def onAction(self,action):
        if action in [5,6,7,9,10,92,117] or action.getButtonCode() in [275,257,261]:
            xbmc.Player().stop()
            self._close_dialog()
    
    def _close_dialog(self):
        xbmc.executebuiltin("Skin.Reset(AnimeWindowXMLDialogClose)")
        xbmc.sleep(400)
        self.close()
#---------------------------------------------------------------------------------------------------
# Add-on removal menu
def Addon_Removal_Menu(removal_types='all'):
    skiparray = ['repository.xbmc.org','repository.spartacus','plugin.program.tbs','script.openwindow','plugin.program.super.favourites','plugin.video.metalliq','script.qlickplay','script.trtv','plugin.video.addons.ini.creator']
    namearray = []
    iconarray = []
    descarray = []
    patharray = []
    finalpath = []
    Main('adult_enable')
    Refresh('addons')
    my_addons = []

    currently_installed = Get_Contents(ADDONS,['packages','temp'])
    dolog(repr(currently_installed))
    if removal_types == 'all' or 'video' in removal_types:
        my_addons = Installed_Addons(content='video', properties='name,path,description,thumbnail')
    if removal_types == 'all' or 'audio' in removal_types:
        my_addons += Installed_Addons(content='audio', properties='name,path,description,thumbnail')
    if removal_types == 'all' or 'image' in removal_types:
        my_addons += Installed_Addons(content='image', properties='name,path,description,thumbnail')
    if removal_types == 'all' or 'program' in removal_types:
        my_addons += Installed_Addons(content='executable', properties='name,path,description,thumbnail')
    if removal_types == 'all' or 'repo' in removal_types:
        my_addons += Installed_Addons(types='xbmc.addon.repository', properties='name,path,description,thumbnail')
    for item in my_addons:
        if not item["addonid"] in skiparray and item["path"] in currently_installed:
            namearray.append(item["name"])
            iconarray.append(item["thumbnail"])
            descarray.append(item["description"])
            patharray.append(item["path"])

    finalarray = multiselect(String(30312),namearray,iconarray,descarray)
    for item in finalarray:
        newpath = patharray[item]
        newname = namearray[item]
        finalpath.append([newname,newpath])
    if len(finalpath) > 0:
        Remove_Addons(finalpath)
#---------------------------------------------------------------------------------------------------
# Function to browse the userdata/addon_data folder
def Addon_Browser(function='list',header='',skiparray=[]):
    dolog('addon browser array: '+repr(skiparray))
    if function == 'keyword':
        skiparray = ['plugin.program.tbs','script.openwindow','script.trtv','script.qlickplay','plugin.video.metalliq']
    if header == '':
        header = String(30043)

    namearray = []
    iconarray = []
    descarray = []
    finallist = []
    idarray   = []
    my_addons = []

    my_addons =  Installed_Addons(content='video', properties='name,description,thumbnail')
    my_addons += Installed_Addons(content='audio', properties='name,description,thumbnail')
    my_addons += Installed_Addons(content='image', properties='name,description,thumbnail')
    my_addons += Installed_Addons(content='executable', properties='name,path,description,thumbnail')

    for item in my_addons:
        if not item["addonid"].encode('utf-8') in skiparray:
            namearray.append(item["name"])
            iconarray.append(item["thumbnail"])
            descarray.append(item["description"])
            idarray.append(item["addonid"].encode('utf-8'))

    finalarray = multiselect(String(30043),namearray,iconarray,descarray)
    for item in finalarray:
        if function == 'list':
            finallist.append([namearray[item].encode('utf-8'),idarray[item]])
        else:
            finallist.append(idarray[item])

    if function == 'list':
        return finallist

    elif function == 'keyword':
            Text_File(KEYWORD_CREATE,'w',str(finallist))
#-----------------------------------------------------------------------------------------------------------------
# Enable/disable the visibility of adult add-ons (use true or false)
def Adult_Filter(value, loadtype = ''):
    success = 0
    if value == 'true':
        try:
            password = converthex(Text_File(xbmc.translatePath('special://home/userdata/addon_data/plugin.program.tbs/x'),'r'))
        except:
            password = ''

# If the password in the local file is blank we set it to the default of 69
        if password == '' or password == 'not set':
            password = '69'

        userpw   = Keyboard(String(30002)).replace('%20',' ')
        if userpw != password:
            value = 'false'
            dialog.ok(String(30000),String(30001))
            xbmc.executebuiltin('HOME')
        else:
            success = 1

    if value == 'false':
        filter_type = 'disabled'
        Main('adult_disable')
    else:
        filter_type = 'enabled'
        from koding import Main
        Sleep_If_Function_Active(function=Main, args=['adult_enable'])
    if loadtype != 'menu' and loadtype != 'startup':
        dialog.ok(String(30003) % filter_type.upper(), String(30004) % filter_type)
    return success
#-----------------------------------------------------------------------------------------------------------------
# Check for storage location on android
def Android_Path_Check():
    content = Grab_Log()
    localstorage  = re.compile('External storage path = (.+?);').findall(content)
    localstorage  = localstorage[0] if (len(localstorage) > 0) else 'Unknown'
    return localstorage
#---------------------------------------------------------------------------------------------------
# Check for non ascii files and folders
def ASCII_Checker():
    failed_array = []
    sourcefile   = dialog.browse(3, String(30005), 'files', '', False, False)
    dp.create(String(30006),'',String(30007),'')
    asciifiles = ASCII_Check(sourcefile,dp)
    if len(asciifiles) > 0:
        mytext = String(30008)
        for item in asciifiles:
            mytext += item+'\n'
        Text_Box(String(30009),mytext)
        Sleep_If_Window_Active()
        if dialog.yesno(String(30010),String(30011)):
            if dialog.yesno(String(30012),String(30013)):
                for item in asciifiles:
                    if os.path.exists(item):
                        try:
                            os.remove(item)
                        except:
                            try:
                                shutil.rmtree(item)
                            except:
                                failed_array.append(item)
        if len(failed_array) > 0:
            mytext = String(30014)
            for item in asciifiles:
                mytext += item+'\n'
            Text_Box(String(30015),mytext)
            Sleep_If_Window_Active()
        else:
            dialog.ok(String(30016),String(30017))
    else:
        dialog.ok(String(30018),String(30019),String(30020))
#---------------------------------------------------------------------------------------------------
# Create backup menu
def Backup_Option():
    Add_Dir(String(30021),'addons','restore_zip',False,'','','Back Up Your Addons')
    Add_Dir(String(30022),'addon_data','restore_zip',False,'','','Back Up Your Addon Userdata')
    Add_Dir(String(30023),GUI,'restore_backup',False,'','','Back Up Your guisettings.xml')
    
    if os.path.exists(FAVS):
        Add_Dir(String(30024),FAVS,'restore_backup',False,'Backup.png','','Back Up Your favourites.xml')
    
    if os.path.exists(SOURCE):
        Add_Dir(String(30025),SOURCE,'restore_backup',False,'Backup.png','','Back Up Your sources.xml')
    
    if os.path.exists(ADVANCED):
        Add_Dir(String(30026),ADVANCED,'restore_backup',False,'Backup.png','','Back Up Your advancedsettings.xml')
    
    if os.path.exists(KEYMAPS):
        Add_Dir(String(30027),KEYMAPS,'restore_backup',False,'Backup.png','','Back Up Your keyboard.xml')
    
    if os.path.exists(RSS):
        Add_Dir(String(30028),RSS,'restore_backup',False,'Backup.png','','Back Up Your RssFeeds.xml')
#---------------------------------------------------------------------------------------------------
# Backup/Restore root menu
def Backup_Restore():
    Add_Dir(String(30029),'none','backup_option',True,'Backup.png','','')
    Add_Dir(String(30030),'none','restore_option',True,'Restore.png','','')
#---------------------------------------------------------------------------------------------------
# Browse pre-installed repo's via the kodi add-on browser
def Browse_Repos():
    xbmc.executebuiltin('ActivateWindow(10040,"addons://repos/",return)')
#---------------------------------------------------------------------------------------------------
def Build_Info():
    Build = ''
    if os.path.exists('/etc/release'):
        Build    = Text_File('/etc/release','r')

    if Build == '':
        logtext = Grab_Log()
        Buildmatch  = re.compile('Running on (.+?)\n').findall(logtext)
        Build       = Buildmatch[0] if (len(Buildmatch) > 0) else ''
    return Build.replace(' ','%20')
#---------------------------------------------------------------------------------------------------
# Main category list
def Categories():
    if debug == 'true':
        Add_Dir('Koding','', "tutorials", True,'','','')
    if OpenELEC_Check():
        Add_Dir(String(30031),'','openelec_settings',False,'Wi-Fi.png','','')

    Add_Dir(String(30032),'', 'social_menu', True,'','','')
    Add_Dir(String(30033),'','install_content',True,'Search_Addons.png','','')
    Add_Dir(String(30034),'','startup_wizard',False,'Startup_Wizard.png','','')
    Add_Dir(String(30035),'none', 'tools',True,'Additional_Tools.png','','')
    # Add_Dir('folder','Android Apps','', 'android_apps', 'Additional_Tools.png','','','')
#---------------------------------------------------------------------------------------------------
def Change_ID():
    newid = Keyboard(String(30036))
    if newid != '':
        ADDON.setSetting('userid', encryptme('e',newid))
    else:
        ADDON.setSetting('userid', '')
    Refresh('container')
#---------------------------------------------------------------------------------------------------
# Function to check the download path set in settings
def Check_Download_Path():
    path = os.path.join(USB,'testCBFolder')
    if not os.path.exists(USB):
        dialog.ok(String(30037),String(30038)) 
        Open_Settings()
#-----------------------------------------------------------------------------------------------------------------    
def Check_File_Date(url, datefile, localdate, dst):
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        conn = urllib2.urlopen(req)
        last_modified = conn.info().getdate('last-modified')
        last_modified = time.strftime('%Y%m%d%H%M%S', last_modified)
        if int(last_modified) > int(localdate):
            urllib.urlretrieve(url,dst)
            if dst==epgdst:
                Extract(dst,ADDON_DATA)         
            else:
                Extract(dst,STORAGE)
            Text_File(last_modified,'w')
        try:
            if os.path.exists(dst):
                os.remove(dst)
        except:
            pass
    except:
        dolog("Failed with update: %s" % str(url))
        dolog(Last_Error())
    Remove_Files()
#-----------------------------------------------------------------------------------------------------------------
# Check to see if any local shares require updating on server
def Check_My_Shares(url = ''):
    message = 0
    SF_Root = os.path.join(ADDON_DATA, 'plugin.program.super.favourites', 'Super Favourites')
    DB_Open(db_social)
    for row in cur.execute("SELECT * FROM shares;"):
        cleanpath = urllib.unquote(row[0])
        dolog(cleanpath)
        localcheck = md5_check(os.path.join(SF_Root, 'HOME_'+cleanpath, 'favourites.xml'))
        if row[1] != localcheck:
            message = 1
            if dialog.yesno(String(30247), String(30248) % cleanpath):
                success = Update_Share(os.path.join(SF_Root, 'HOME_'+cleanpath))
                if success:
                    cur.execute("UPDATE shares SET stamp=? WHERE path=?", [localcheck, row[0]])
                    con.commit()
    if url == 'manual' and message == 0:
        dialog.ok(String(30249), String(30249))
    con.close()
#-----------------------------------------------------------------------------------------------------------------    
def Check_Updates(url, datefile, dst):
    if os.path.exists(datefile):
        readfile = open(datefile,'r')
        localdate = readfile.read()
        readfile.close()
    else:
        localdate = 0
    Check_File_Date(url, datefile, int(localdate), dst)
#---------------------------------------------------------------------------------------------------
# Function to clean HTML into plain text. Not perfect but it's better than raw html code!
def Clean_HTML(data):        
    data = data.replace('</p><p>','[CR][CR]').replace('&ndash;','-').replace('&mdash;','-').replace("\n", " ").replace("\r", " ").replace("&rsquo;", "'").replace("&rdquo;", '"').replace("</a>", " ").replace("&hellip;", '...').replace("&lsquo;", "'").replace("&ldquo;", '"')
    data = " ".join(data.split())   
    p    = re.compile(r'< script[^<>]*?>.*?< / script >')
    data = p.sub('', data)
    p    = re.compile(r'< style[^<>]*?>.*?< / style >')
    data = p.sub('', data)
    p    = re.compile(r'')
    data = p.sub('', data)
    p    = re.compile(r'<[^<]*?>')
    data = p.sub('', data)
    data = data.replace('&nbsp;',' ')
    return data
#---------------------------------------------------------------------------------------------------
# Function to clear all known cache files
def Clear_Cache():
    choice = xbmcgui.Dialog().yesno(String(30039), String(30040), nolabel=String(30041),yeslabel=String(30042))
    if choice == 1:
        Wipe_Cache()
        Remove_Textures_Dialog()
#---------------------------------------------------------------------------------------------------
# Function to delete the userdata/addon_data folder
def CPU_Check():
    logtext     = Grab_Log()
    CPUmatch    = re.compile('Host CPU: (.+?) available').findall(logtext)
    CPU         = CPUmatch[0] if (len(CPUmatch) > 0) else ''
    return CPU.replace(' ','%20')
#-----------------------------------------------------------------------------------------------------------------
def Create_Username():
    command = Open_URL 
#-----------------------------------------------------------------------------------------------------------------
# Open a database
def DB_Open(db_path):
    global cur
    global con
    con = database.connect(db_path)
    cur = con.cursor()
#---------------------------------------------------------------------------------------------------
# Function to delete the userdata/addon_data folder
def Delete_Userdata():
    tbs_data    = os.path.join(ADDON_DATA,'plugin.program.tbs')
    ow_data     = os.path.join(ADDON_DATA,'script.openwindow')
    ignore_list = [tbs_data, ow_data]
    Delete_Folders(filepath=ADDON_DATA, ignore=ignore_list)
    zipcheck = xbmc.translatePath(os.path.join(ADDON_DATA,'plugin.program.tbs','zipcheck'))
    if os.path.exists(zipcheck):
        os.remove(zipcheck)
#---------------------------------------------------------------------------------------------------
# Disable the master mode
def Disable_Master():
    ADDON.setSetting('master','false')
    xbmc.executebuiltin('Container.Refresh')
#---------------------------------------------------------------------------------------------------
# Function to pull commands and update
def DLE(command,repo_link,repo_id):
    check1='DLE'
    downloadpath = os.path.join(PACKAGES,'updates.zip')
    if not os.path.exists(PACKAGES):
        os.makedirs(PACKAGES)
    
    if command=='delete':
        shutil.rmtree(xbmc.translatePath(repo_link))
        Refresh(['addons','repos'])
    
    if command=='addons' or command=='ADDON_DATA' or command=='media' or command=='config' or command=='playlists' or command == 'custom':
#        dp.create('Installing Content','','')
        if not os.path.exists(os.path.join(ADDONS,repo_id)) or repo_id == '':
            try:
                Download(repo_link, downloadpath)
            except:
                pass       
        if command=="addons":
            try:
                Extract(downloadpath, ADDONS)
                Refresh(['addons','repos'])
            except:
                pass

        if command=='ADDON_DATA':
            try:
                Extract(downloadpath, ADDON_DATA)
            except:
                dolog("### FAILED TO EXTRACT TO "+ADDON_DATA)
        
        if command=='media':
            try:
                Extract(downloadpath, MEDIA)
            except:
                pass
        
        if command=='config':
            try:
                Extract(downloadpath, CONFIG)
            except:
                pass

        if command=='playlists':
            try:
                Extract(downloadpath, PLAYLISTS)
            except:
                pass

        if command=='custom':
            try:
                Extract(downloadpath, repo_id)
            except:
                dolog("### Failed to extract update "+repo_link)
            
    if os.path.exists(downloadpath):
        try:
            os.remove(downloadpath)
        except:
            pass
#---------------------------------------------------------------------------------------------------
# Enables/disables the social sharing
def Enable_Shares(mode):
    choice = 1
    if mode == 'true':
        if not dialog.yesno(String(30049), String(30050)):
            choice = 0
    if choice:
        ADDON.setSetting('thirdparty', mode)
        xbmc.executebuiltin('Container.Refresh')
#---------------------------------------------------------------------------------------------------
def encryptme(mode, message):
    if mode == 'e':
        import random
        count = 0
        finaltext = ''
        while count < 4:
            count += 1
            randomnum = random.randrange(1, 31)
            hexoffset = hex(randomnum)[2:]
            if len(hexoffset)==1:
                hexoffset = '0'+hexoffset
            finaltext = finaltext+hexoffset
        randomchar = random.randrange(1,4)
        if randomchar == 1: finaltext = finaltext+'0A'
        if randomchar == 2: finaltext = finaltext+'04'
        if randomchar == 3: finaltext = finaltext+'06'
        if randomchar == 4: finaltext = finaltext+'08'
        key1    = finaltext[-2:]
        key2    = int(key1,16)
        hexkey  = finaltext[-key2:-(key2-2)]
        key     = -int(hexkey,16)

# enctrypt/decrypt the message
        translated = ''
        finalstring = ''
        for symbol in message:
            num = ord(symbol)
            num2 = int(num) + key
            hexchar = hex(num2)[2:]
            if len(hexchar)==1:
                hexchar = '0'+hexchar
            finalstring = str(finalstring)+str(hexchar)
        return finalstring+finaltext
    else:
        key1    = message[-2:]
        key2    = int(key1,16)
        hexkey  = message[-key2:-(key2-2)]
        key     = int(hexkey,16)
        message = message [:-10]
        messagearray = [message[i:i+2] for i in range(0, len(message), 2)]
        numbers = [ int(x,16)+key for x in messagearray ]
        finalarray = [ str(unichr(x)) for x in numbers ]
        finaltext = ''.join(finalarray)
        return finaltext.encode('utf-8')
#---------------------------------------------------------------------------------------------------
# Function to execute a command
def Exec_XBMC(command):
    xbmc.executebuiltin(command)
    xbmc.executebuiltin('Container.Refresh')
#-----------------------------------------------------------------------------
# Extract function used for threading
def Extract_Function(local_path, ADDONS, dpmode):
    Extract(local_path, ADDONS, dpmode)
#-----------------------------------------------------------------------------------------------------------------          
# Firmware update
def Firmware_Update(url):
    dl_path = '/tmp/cache/update.zip'
    os.system('mkdir -p /tmp/cache\nmount -t ext4 /dev/cache /tmp/cache\nrm -f /tmp/cache/*.zip')
    dp.create(String(30051),String(30048))
    Download(url,dl_path,dp)
    os.system('mkdir -p /tmp/cache/recovery')
    os.system('echo -e "--update_package=/cache/update.zip\n--wipe_cache" > /tmp/cache/recovery/command || exit 1\numount /tmp/cache\nreboot recovery')
#---------------------------------------------------------------------------------------------------
# Clean up all known cache files
def Full_Clean():
    size                      = 0
    atv2_cache_a              = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
    atv2_cache_b              = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')        
    downloader_cache_path     = os.path.join(xbmc.translatePath('special://profile/addon_data/script.module.simple.downloader'), '')
    imageslideshow_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/script.image.music.slideshow/cache'), '')
    iplayer_cache_path        = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.iplayer/iplayer_http_cache'), '')
    itv_cache_path            = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.itv/Images'), '')
    navix_cache_path          = os.path.join(xbmc.translatePath('special://profile/addon_data/script.navi-x/cache'), '')
    phoenix_cache_path        = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.phstreams/Cache'), '')
    ramfm_cache_path          = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.audio.ramfm/cache'), '')
    wtf_cache_path            = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.whatthefurk/cache'), '')
    genesisCache              = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.genesis'), 'cache.db')
    tempdir                   = os.path.join(HOME,'temp')
    dp.create(String(30052),'',String(30048),'')

# For more accurate info we need to add a loop to only check folders with cache in the name. Actual wipe does this but getsize does not.
    if os.path.exists(atv2_cache_a):
        size += Folder_Size(atv2_cache_a,'b')
    if os.path.exists(atv2_cache_b):
        size += Folder_Size(atv2_cache_b,'b')
    if os.path.exists(downloader_cache_path):
        size += Folder_Size(downloader_cache_path,'b')
    if os.path.exists(imageslideshow_cache_path):
        size += Folder_Size(imageslideshow_cache_path,'b')
    if os.path.exists(iplayer_cache_path):
        size += Folder_Size(iplayer_cache_path,'b')
    if os.path.exists(itv_cache_path):
        size += Folder_Size(itv_cache_path,'b')
    if os.path.exists(navix_cache_path):
        size += Folder_Size(navix_cache_path,'b')
    if os.path.exists(phoenix_cache_path):
        size += Folder_Size(phoenix_cache_path,'b')
    if os.path.exists(ramfm_cache_path):
        size += Folder_Size(ramfm_cache_path,'b')
    if os.path.exists(wtf_cache_path):
        size += Folder_Size(wtf_cache_path,'b')
    if os.path.exists(genesisCache):
        size += Folder_Size(genesisCache,'b')
    if os.path.exists(tempdir):
        size += Folder_Size(tempdir,'b')
    size += Folder_Size(THUMBNAILS,'b')
    size += Folder_Size(PACKAGES,'b')
    size = "%.2f" % (float(size / 1024) / 1024)
    choice = dialog.yesno(String(30053),String(30054)%size)
    if choice == 1:
        Wipe_Cache()
        try:
            shutil.rmtree(PACKAGES)
        except:
            pass
        choice = dialog.yesno(String(30055),String(30056),yeslabel=String(30057),nolabel=String(30058))
        if choice == 1:
            Remove_Textures()
            Delete_Folders(THUMBNAILS)
            Force_Close()
        else:
            Cleanup_Textures()
#-----------------------------------------------------------------------------------------------------------------  
# Return mac address, not currently checked on Mac OS
def Get_Mac(protocol):
    cont    = 0
    counter = 0
    mac     = ''
    while mac == '' and counter < 5: 
        if sys.platform == 'win32': 
            mac = ''
            for line in os.popen("ipconfig /all"):
                if protocol == 'wifi':
                    if line.startswith('Wireless LAN adapter Wi'):
                        cont = 1
                    if line.lstrip().startswith('Physical Address') and cont == 1:
                        mac = line.split(':')[1].strip().replace('-',':').replace(' ','')
                        if len(mac) == 17:
                            break
                        else:
                            mac = ''
                            counter += 1

                else:
                    if line.lstrip().startswith('Physical Address'): 
                        mac = line.split(':')[1].strip().replace('-',':').replace(' ','')
                        if len(mac) == 17:
                            break
                        else:
                            mac = ''
                            counter += 1

        elif sys.platform == 'darwin': 
            mac = ''
            if protocol == 'wifi':
                for line in os.popen("ifconfig en0 | grep ether"):
                    if line.lstrip().startswith('ether'):
                        mac = line.split('ether')[1].strip().replace('-',':').replace(' ','')
                        dolog('(count: %s) (len: %s) wifi: %s' % (counter, len(mac), mac))
                        if len(mac) == 17:
                            break
                        else:
                            mac = ''
                            counter += 1

            else:
                for line in os.popen("ifconfig en1 | grep ether"):
                    if line.lstrip().startswith('ether'):
                        mac = line.split('ether')[1].strip().replace('-',':').replace(' ','')
                        dolog('(count: %s) (len: %s) ethernet: %s' % (counter, len(mac), mac))
                        if len(mac) == 17:
                            break
                        else:
                            mac = ''
                            counter += 1

        elif xbmc.getCondVisibility('System.Platform.Android'):
            mac = ''
            if os.path.exists('/sys/class/net/wlan0/address') and protocol == 'wifi':
                readfile = open('/sys/class/net/wlan0/address', mode='r')
            if os.path.exists('/sys/class/net/eth0/address') and protocol != 'wifi':
                readfile = open('/sys/class/net/eth0/address', mode='r')
            mac = readfile.read()
            readfile.close()
            try:
                mac = mac.replace(' ','')
                mac = mac[:17]
            except:
                mac = ''
                counter += 1

        else:
            if protocol == 'wifi':
                for line in os.popen("/sbin/ifconfig"): 
                    if line.find('wlan0') > -1: 
                        mac = line.split()[4]
                        if len(mac) == 17:
                            break
                        else:
                            mac = ''
                            counter += 1

            else:
               for line in os.popen("/sbin/ifconfig"): 
                    if line.find('eth0') > -1: 
                        mac = line.split()[4] 
                        if len(mac) == 17:
                            break
                        else:
                            mac = ''
                            counter += 1
    if mac == '':
        dolog('Unknown mac')
        mac = 'Unknown'

    return str(mac)
#---------------------------------------------------------------------------------------------------
def Grab_Updates(url, runtype = ''):
    if runtype != 'ignoreplayer':
        isplaying = xbmc.Player().isPlaying()
        while isplaying:
            xbmc.sleep(1000)
            isplaying = xbmc.Player().isPlaying()

    urlparams   = URL_Params()
    mysuccess   = 0
    failed      = 0
    counter     = 0
    changetimer = 0
    multi       = 0
    previous    = ''

    if urlparams != 'Unknown':
        if url == 'http://tlbb.me/boxer/comm_live.php?multi&z=c&x=':
            multi = 1
            url=url.replace('multi&','')
        if url == 'http://tlbb.me/boxer/comm_live.php?update&z=c&x=':
            Notify(String(30059),String(30007),'1000',os.path.join(ADDONS,'script.openwindow','resources','images','update_software.png'))
            url=url.replace('update&','')
        xbmc.executebuiltin("ActivateWindow(busydialog)")
        while mysuccess != 1 and failed != 1:

            try:
                dolog("### URL: "+url+encryptme('e',urlparams))
                link = Open_URL(post_type='post',url=url+encryptme('e',urlparams))
                if link != '' and not 'sleep' in link:
                    link = encryptme('d',link).replace('\n',';').replace('|_|',' ').replace('|!|','\n').replace('http://venztech.com/repo_jpegs/','http://tlbb.me/repo_jpegs/')
                try:
                    dolog("### Return: "+link)
                except:
                    pass

                if link == '':
                    dolog("### Blank page returned")
                    counter += 1
                    if counter == 3:
                        failed = 1

# Check that no body tag exists, if it does then we know TLBB is offline
                if not '<body' in link and link != '':
                    linematch  = re.compile('com(.+?)="').findall(link)
                    commline   = linematch[0] if (len(linematch) > 0) else ''
                    commatch   = re.compile('="(.+?)endcom"').findall(link)
                    command    = commatch[0] if (len(commatch) > 0) else 'End'
                
                    SF_match   = re.compile('<favourite[\s\S]*?</favourite>').findall(command)
                    SF_command = SF_match[0] if (len(SF_match) > 0) else 'None'

# Create array of commands so we can check if the install video needs to be played
                    previous += command
                    dolog("### command: "+command)
                    dolog("### SF_command: "+SF_command)

                    Open_URL(post_type='post',url=converthex('687474703a2f2f746c62622e6d652f636f6d6d2e7068703f783d')+encryptme('e',urlparams)+'&y='+commline)
                    dolog("### COMMAND *CLEANED: "+command.replace('|#|',';'))
                    dolog("### LINK *ORIG: "+link)
                    if SF_command!='None':
                        Text_File(PROGRESS_TEMP, 'w', SF_command)

                    elif command!='End' and not 'sleep' in link:
                        if ';' in command:
                            dolog(command)
                            newcommands = command.split(';')
                            for item in newcommands:
                                if 'branding/install.mp4' in item:
                                    item = ''

                                if 'extract.all' in item:
                                    try:
                                        item = item.replace('extract.all','Extract')
                                        exec item
                                        if os.path.exists(os.path.join(PACKAGES,'updates.zip')):
                                            os.remove(os.path.join(PACKAGES,'updates.zip'))
                                    except:
                                        dolog(Last_Error())
                                else:
                                    try:
                                        if 'Dialog().ok(' in item:
                                            xbmc.sleep(1000)
                                            while xbmc.Player().isPlaying():
                                                xbmc.sleep(500)
                                        exec item.replace('|#|',';') # Change to semicolon for user agent otherwise it splits into a new command
                                        dolog("### RUNNING ITEM: "+item.replace('|#|',';'))
                                    except:
                                        log("### Failed with item: "+item.replace('|#|',';'))
                                        dolog(Last_Error())
                        else:
                            try:
                                if 'Dialog().ok(' in command:
                                    if not multi:
                                        xbmc.sleep(1000)
                                        dolog("### Dialog.ok in this command, checking if xbmc is playing....")
                                        while xbmc.Player().isPlaying():
                                            xbmc.sleep(500)
                                    else: command = ''

                                if 'extract.all' in command:
                                    try:
                                        command = command.replace('extract.all','Extract')
                                        exec command
                                        if os.path.exists(os.path.join(PACKAGES,'updates.zip')):
                                            os.remove(os.path.join(PACKAGES,'updates.zip'))
                                    except:
                                        dolog("### Failed with command: "+command.replace('|#|',';'))
                                        dolog(Last_Error())

                                if 'branding/install.mp4' in command:
                                    command = ''

                                else:
                                    exec command.replace('|#|',';') # Change to semicolon for user agent otherwise it splits into a new command
                                    dolog("### RUNNING COMMAND: "+item.replace('|#|',';'))
                            except:
                                dolog("### Failed with command: "+command.replace('|#|',';'))
                        previous = ''
                        if os.path.exists(PROGRESS_TEMP):
                            os.remove(PROGRESS_TEMP)
                        
                    elif command=='End':
                        if 'sleep' in link:
                            content=Text_File(SLEEPER, 'r')
                            if content != "sleep=STOPALL":
                                sleep = str(link[6:])
                            else:
                                sleep = "23:59:59"
                                dolog("### SLEEP MODE - SERVER MAINTENANCE")
                            if str(sleep) != str(content):
                                Text_File(SLEEPER, 'w',sleep)
                                dolog("### Changed timer to "+sleep)
                                changetimer = 1
                            else:
                                dolog("### Timer same, no changes required")
                        if sleep != '23:59:59':
                            Refresh(['addons','repos'])
                            mysuccess = 1
            except:
                dolog("### Failed with update command: "+Last_Error())
                failed = 1
        try:
            xbmc.executebuiltin("Dialog.Close(busydialog)")
        except:
            pass

        if changetimer == 1:
            dolog('### TBS GRAB UPDATES - TIMER CHANGED, STOPPING/RUNNING SERVICE')
            xbmc.executebuiltin('StopScript(special://home/addons/plugin.program.tbs/service.py)')
            xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.tbs/service.py)')

    dolog('### TBS GRAB UPDATES - RUNNING FUNCTIONS')
    if os.path.exists(xbmc.translatePath('special://home/addons/script.openwindow/functions.py')):
        xbmc.executebuiltin('RunScript(special://home/addons/script.openwindow/functions.py)')
    elif os.path.exists(xbmc.translatePath('special://xbmc/addons/script.openwindow/functions.py')):
        xbmc.executebuiltin('RunScript(special://xbmc/addons/script.openwindow/functions.py)')
    Sync_Settings()
    Remove_Files()
    if runtype != 'silent':
        Notify(String(30330),String(30331),'1000',os.path.join(ADDONS,'plugin.program.tbs','resources','tick.png'))
#---------------------------------------------------------------------------------------------------
# Hide passwords in addon settings
def Hide_Passwords():
    if dialog.yesno(String(30094), String(30095)):
        for root, dirs, files in os.walk(ADDONS):
            for f in files:
                if f =='settings.xml':
                    FILE=open(os.path.join(root, f)).read()
                    match=re.compile('<setting id=(.+?)>').findall (FILE)
                    for LINE in match:
                        if 'pass' in LINE:
                            if not 'option="hidden"' in LINE:
                                try:
                                    CHANGEME=LINE.replace('/',' option="hidden"/') 
                                    f = open(os.path.join(root, f), mode='w')
                                    f.write(str(FILE).replace(LINE,CHANGEME))
                                    f.close()
                                except:
                                    pass
        dialog.ok(String(30096), String(30097)) 
#-----------------------------------------------------------------------------------------------------------------
# Show final results for installing (if multiple shares of same name order by popularity)
def Install_Shares(function, menutype, menu, choices, contentarray = '', imagearray = '', descarray = ''):
        shares_contentarray = []
        shares_imagearray   = []
        shares_descarray    = []
        shares_contenturl   = []
        urlparams           = URL_Params()

#    try:
        for item in choices:
            dolog('http://tlbb.me/boxer/cat_search_live.php?&x=%s' % (encryptme('e','%s&%s&1&%s&%s' % (urlparams, function, social_shares, contentarray[item]))))
            sharelist_URL  = 'http://tlbb.me/boxer/cat_search_live.php?&x=%s' % (encryptme('e','%s&%s&1&%s&%s' % (urlparams, function, social_shares, contentarray[item])))
            content_list   = Open_URL(post_type='post',url=sharelist_URL)
            clean_link     = encryptme('d',content_list)
            dolog('#### %s' % clean_link)

# Grab all the shares which match the master sub-category
            match = re.compile('n="(.+?)"t="(.+?)"d="(.+?)"l="(.+?)"', re.DOTALL).findall(clean_link)
            for name, thumb, desc, link in match:
                shares_contentarray.append(name)
                shares_imagearray.append(thumb)
                shares_descarray.append(desc)
                shares_contenturl.append(link)

# If we have more than one item in the list we present them so the user can select which one they want installed
            if len(shares_contentarray) > 1:
                choice = dialog.select('Select share for [COLOR=dodgerblue]%s[/COLOR]' % contentarray[item].replace('ADD ',''), shares_contentarray)
                install_share = shares_contenturl[choice]

            else:
                install_share = shares_contenturl[0]

# Remove any matching menu items previously installed from different boxes
            if len(shares_contentarray)>0:
                for item in shares_contentarray:
                    dolog('### Removing any old instances of %s' % item)
                    if item.startswith('Add'):
                        item         = 'Remove'+item[3:]
                    change_text  = re.compile(' to the (.+?)Menu').findall(item)[0]
                    if change_text.endswith(' '):
                        change_text = change_text[:-1]
                    item         = item.replace(' to the %s' % change_text, '%'+' from the %s' % change_text)
                    if 'by box' in item:
                        change_text2 = re.compile('by box (.+?)from').findall(item)[0]
                        dolog('by box: %s' % change_text2)
                        item         = item.replace(change_text2, '%')
                    Remove_Menu('from_the_%s_menu' % change_text.lower().replace(' ', '_'), item)
#            content_list   = Open_URL2(sharelist_URL)

                Open_URL(post_type='post',url=install_share)

# Clean the arrays so they don't show old data
            del shares_contentarray[:]
            del shares_imagearray[:]
            del shares_descarray[:]
            del shares_contenturl[:]
            del match[:]
        xbmc.executebuiltin('ActivateWindow(HOME)')
        Grab_Updates('http://tlbb.me/boxer/comm_live.php?multi&z=c&x=','ignoreplayer')
#---------------------------------------------------------------------------------------------------
# Menu to install content via the TR add-on
def Install_Content(url):
    if ADDON.getSetting('master') == 'true':
        Add_Dir(String(30098),'','disable_master',False,'','','')
    if ADDON.getSetting('userid') != '':
        Add_Dir(String(30099) % encryptme('d',userid),'','change_id',False,'','','')
    Add_Dir(String(30100),'http://tlbb.me/boxer/comm_live.php?z=c&x=', 'grab_updates',False,'','','')
    Add_Dir(String(30101),'','keywords',False,'Keywords.png','','')
    Add_Dir(String(30102),'','install_from_zip',False,'','','')
    Add_Dir(String(30103),'','browse_repos',False,'','','')
#---------------------------------------------------------------------------------------------------
# Browse pre-installed repo's via the kodi add-on browser
def Install_From_Zip():
    xbmc.executebuiltin('ActivateWindow(10040,"addons://install/",return)')
#---------------------------------------------------------------------------------------------------
# Function to grab the main sub-categories 
def Install_Venz_Menu(function):
    menutype    = ''
    menu        = ''
    if '||' in function:
        function,menutype,menu = function.split('||')
    menu = menu.replace('_',' ').lower()

    urlparams  = URL_Params()
    if urlparams != 'Unknown':
        try:

# Inititalise the arrays for sending to multi-select window
            contentarray = []
            imagearray   = []
            descarray    = []
            contenturl   = []

# Add an item to one of the main menu categories or add a sub-menu item
            if menutype == 'add_main' or menutype == 'add_sub' or function.startswith('manualsearch'):
                categoryURL  = 'http://tlbb.me/boxer/cat_search_live.php?&x=%s' % (encryptme('e','%s&%s&0&%s' % (urlparams, function, social_shares)))
                dolog(categoryURL)
                link_orig  = Open_URL(post_type='post',url=categoryURL)
                link       = encryptme('d',link_orig)
                dolog('#### '+encryptme('d',link_orig))
            
                match  = re.compile('n="(.+?)"t="(.+?)"d="(.+?)"', re.DOTALL).findall(link)
                for name, thumb, desc in match:
                    contentarray.append(name)
                    imagearray.append(thumb)
                    descarray.append(desc)

                if len(contentarray)>0:
                    choices = multiselect(String(30078), contentarray, imagearray, descarray)
                    xbmc.executebuiltin('ActivateWindow(HOME)')
                    dolog('Choices: %s' % choices)
                    if len(choices) > 0:
                        Install_Shares(function, menutype, menu, choices, contentarray, imagearray, descarray)
                else:
                    if thirdparty == 'true':
                        dialog.ok(String(30079),String(30080))
                    else:
                        dialog.ok(String(30079),String(30081))


# If this is a remove item
            else:
                Remove_Menu(function)
        except:
            Notify(String(30082),String(30083),'1000',os.path.join(ADDONS,'plugin.program.tbs','resources','cross.png'))
    else:
        dialog.ok(String(30084), String(30085))    
# Return details about the IP address lookup       
def IP_Check():
    ip_site = ADDON.getSetting('ip_site')
    try:
        if ip_site == "whatismyipaddress.com":
           BaseURL       = 'http://whatismyipaddress.com/'
           link          = Open_URL(BaseURL).replace('\n','').replace('\r','')
           if not 'Access Denied' in link:
               ipmatch       = re.compile('whatismyipaddress.com/ip/(.+?)"').findall(link)
               ipfinal       = ipmatch[0] if (len(ipmatch) > 0) else 'Unknown'
               details       = re.compile('"font-size:14px;">(.+?)</td>').findall(link)
               provider      = details[0] if (len(details) > 0) else 'Unknown'
               location      = details[2]+', '+details[3]+', '+details[4] if (len(details) > 3) else 'Unknown'
               dialog.ok('www.whatismyipaddress.com',"[B][COLOR gold]Address: [/COLOR][/B] %s" % ipfinal, '[B][COLOR gold]Provider: [/COLOR][/B] %s' % provider, '[B][COLOR gold]Location: [/COLOR][/B] %s' % location)
        else:
            BaseURL       = 'https://www.iplocation.net/find-ip-address'
            link          = Open_URL(BaseURL).replace('\n','').replace('\r','')
            segment       = re.compile('<table class="iptable">(.+?)<\/table>').finall(link)
            ipmatch       = re.compile('font-weight: bold;">(.+?)<\/span>').findall(segment[0])
            ipfinal       = ipmatch[0] if (len(ipmatch) > 0) else 'Unknown'
            providermatch = re.compile('Host Name<\/th><td>(.+?)<\/td>').findall(segment[0])
            hostname      = details[0] if (len(details) > 0) else 'Unknown'
            locationmatch = re.compile('IP Location<\/th><td>(.+?)&nbsp;').findall(segment[0])
            location      = details[0] if (len(details) > 0) else 'Unknown'
            dialog.ok('www.iplocation.net',"[B][COLOR gold]Address: [/COLOR][/B] %s" % ipfinal, '[B][COLOR gold]Host: [/COLOR][/B] %s' % hostname, '[B][COLOR gold]Location: [/COLOR][/B] %s' % location)
    except:
        dialog.ok(String(30104), String(30105))
#---------------------------------------------------------------------------------------------------
# Install a keyword
def Keyword_Search():
    if not os.path.exists(PACKAGES):
        os.makedirs(PACKAGES)
    restore_dir =  '/storage/.restore/'
    counter     = 0
    success     = 0
    downloadurl = ''
    title       = 'Enter Keyword'
    keyword     = Keyboard(title)
    if keyword == 'masteron':
        ADDON.setSetting('master','true')
        xbmc.executebuiltin('Container.Refresh')
        return
    if keyword == 'masteroff':
        ADDON.setSetting('master','false')
        xbmc.executebuiltin('Container.Refresh')
        return
    if keyword == 'uidoff':
        ADDON.setSetting('userid','')
        xbmc.executebuiltin('Container.Refresh')
        return
    if keyword.startswith('uid'):
        idsetting = keyword.replace('uid','')
        ADDON.setSetting('userid', encryptme('e',idsetting))
        xbmc.executebuiltin('Container.Refresh')
        return
    elif keyword:
        url='http://urlshortbot.com/totalrevolution'
        if os.path.exists(KEYWORD_FILE):
            url  = Text_File(KEYWORD_FILE,'r')
        downloadurl = url+keyword
        lib         = os.path.join(PACKAGES, keyword+'.zip')
        urlparams   = URL_Params()
        if urlparams != 'Unknown':
            dp.create('Contacting Server','Attempt: 1', '', 'Please wait...')
            while counter <3 and success == 0:
                counter += 1
                dp.update(0,'Attempt: '+str(counter), '', 'Please wait...')
            if keyword.startswith('switchme'):
                keywordoem = keyword.replace('switchme','')
                try:
                    link = Open_URL(post_type='post',url='http://tlbb.me/boxer/add_to_oem_live.php?x='+encryptme('e',urlparams)+'&o='+encryptme('e',keywordoem))
                except:
                    link = 'fail'
            else:
                try:
                    link = Open_URL(post_type='post',url='http://tlbb.me/boxer/keyword.php?x='+encryptme('e',urlparams)+'k='+encryptme('e',keyword))
                except:
                    link = 'fail'
            if 'Success' in link:
                success = 1
                dp.close()
                if os.path.exists(xbmc.translatePath('special://home/addons/script.openwindow/functions.py')):
                    xbmc.executebuiltin('RunScript(special://home/addons/script.openwindow/functions.py)')
                elif os.path.exists(xbmc.translatePath('special://xbmc/addons/script.openwindow/functions.py')):
                    xbmc.executebuiltin('RunScript(special://xbmc/addons/script.openwindow/functions.py)')
                dialog.ok(String(30106),String(30107))
        if success == 0:
            try:
                dolog("Attempting download "+downloadurl+" to "+lib)
                dp.create(String(30108),String(30109),'', String(30048))
                Download(downloadurl,lib)
                dolog("### Keyword "+keyword+" Successfully downloaded")
            
                if zipfile.is_zipfile(lib):
                
                    try:
                        Sleep_If_Function_Active(Extract_Function, [lib, HOME, dp])
                        dolog('## %s EXTRACTED SUCCESSFULLY' % keyword)
                        
                        if os.path.exists(xbmc.translatePath('special://home/addons/script.openwindow/functions.py')):
                            xbmc.executebuiltin('RunScript(special://home/addons/script.openwindow/functions.py,dp)')
                        elif os.path.exists(xbmc.translatePath('special://xbmc/addons/script.openwindow/functions.py')):
                            xbmc.executebuiltin('RunScript(special://xbmc/addons/script.openwindow/functions.py,dp)')
                            
                        kw_temp = xbmc.translatePath('special://profile/addon_data/script.openwindow/keyword_installed')
                        keyword_installed = os.path.exists(kw_temp)
                        while not keyword_installed:
                            xbmc.sleep(1000)
                            keyword_installed = os.path.exists(kw_temp)
                        dialog.ok(String(30108), "",String(30110))
                        shutil.rmtree(kw_temp)
                        dp.close()
                    except Exception as e:
                        dolog("### Unable to install keyword (%s): %s" % (keyword, e))
            
                else:
                    try:
                        if os.path.getsize(lib) > 100000 and 'venztech' in url:
                            dp.create("Restoring Backup","Copying Files...",'', 'Please Wait')
                            os.rename(lib,restore_dir+'20150815123607.tar')
                            dp.update(0,"", String(30111))
                            xbmc.executebuiltin('reboot')
                        else: dialog.ok(String(30112),String(30113))
                    except:
                        dialog.ok(String(30114),String(30115))
                        dolog("### UNABLE TO INSTALL BACKUP - IT IS NOT A ZIP")                
            except:
                dialog.ok(String(30116),String(30117))

        if os.path.exists(lib):
            os.remove(lib)
#---------------------------------------------------------------------------------------------------
# View the log from within Kodi
def Log_Viewer():
    logpath = xbmc.translatePath('special://logpath')
    valid_logfile = Get_Contents(path=logpath,folders=False,filter='.log')
    if len(valid_logfile) >= 1:
        if dialog.yesno(String(30118),String(30119),yeslabel=String(30120),nolabel=String(30121)):
            Upload_Log()
        else:
            viewer = [String(30122),String(30123),String(30124),String(30125),String(30126)]
            choice = dialog.select(String(30127),viewer)
            if choice == -1: return
            elif choice == 0: content=Grab_Log(formatting='errors')
            elif choice == 1: content=Grab_Log(formatting='warnings_errors')
            elif choice == 2: content=Grab_Log()
            elif choice == 3: content=Grab_Log(sort_order='original')
            elif choice == 4: content=Grab_Log(log_type='old')
            Text_Box(String(30118), content)
            Sleep_If_Window_Active()
    else:
        dialog.ok(String(30327),String(30328))
#---------------------------------------------------------------------------------------------------
def Main_Menu_Visibility(menu_list='',menu_options='',enabled=True):
    listcount = 0
    if enabled:
        for item in menu_list:
            if item[1] in menu_options and xbmc.getCondVisibility('Skin.String(%s)'%item[0]):
                listcount += 1
    else:
        for item in menu_list:
            if not xbmc.getCondVisibility('Skin.String(%s)'%item[0]):
                listcount += 1
    return listcount
#---------------------------------------------------------------------------------------------------
# Function to enable/disable the main menu items - added due to glitch on server
def Main_Menu_Install(menumode):
    menu_list = (['Custom6HomeItem.Disable','comedy'],['Custom3HomeItem.Disable','cooking'],['Custom4HomeItem.Disable','fitness'],
    ['Custom5HomeItem.Disable','gaming'],['FavoritesHomeItem.Disable','kids'],['LiveTVHomeItem.Disable','livetv'],
    ['MovieHomeItem.Disable','movies'],['MusicHomeItem.Disable','music'],['ProgramsHomeItem.Disable','news'],
    ['VideosHomeItem.Disable','sports'],['Custom2HomeItem.Disable','technology'],['WeatherHomeItem.Disable','travel'],
    ['TVShowHomeItem.Disable','tvshows'],['PicturesHomeItem.Disable','world'],['ShutdownHomeItem.Disable','youtube'],
    ['MusicVideoHomeItem.Disable','xxx'])

    if menumode == 'add':
        urlparams = URL_Params()
        menu_options = Open_URL(post_type='post',url='http://tlbb.me/boxer/my_details_live.php?x=%s&m=1' % encryptme('e', urlparams))
        menu_options = encryptme('d', menu_options)
        listcount = Sleep_If_Function_Active(function=Main_Menu_Visibility,args=[menu_list,menu_options,True])
        if xbmc.getCondVisibility('Skin.String(Custom6HomeItem.Disable)') and 'comedy' in menu_options:
            Add_Dir('%s %s'%(String(30060),String(30061)),'Skin.SetString(Custom6HomeItem.Disable,)','exec_xbmc',False,'special://home/media/branding/backgrounds/HOME_COMEDY/HOME_COMEDY_001.jpg','','')
        if xbmc.getCondVisibility('Skin.String(Custom3HomeItem.Disable)') and 'cooking' in menu_options:
            Add_Dir('%s %s'%(String(30060),String(30077)),'Skin.SetString(Custom3HomeItem.Disable,)','exec_xbmc',False,'special://home/media/branding/backgrounds/HOME_COOKING/HOME_COOKING_001.jpg','','')
        if xbmc.getCondVisibility('Skin.String(Custom4HomeItem.Disable)') and 'fitness' in menu_options:
            Add_Dir('%s %s'%(String(30060),String(30062)),'Skin.SetString(Custom4HomeItem.Disable,)','exec_xbmc',False,'special://home/media/branding/backgrounds/HOME_FITNESS/HOME_FITNESS_001.jpg','','')
        if xbmc.getCondVisibility('Skin.String(Custom5HomeItem.Disable)') and 'gaming' in menu_options:
            Add_Dir('%s %s'%(String(30060),String(30063)),'Skin.SetString(Custom5HomeItem.Disable,)','exec_xbmc',False,'special://home/media/branding/backgrounds/HOME_GAMING/HOME_GAMING_001.jpg','','')
        if xbmc.getCondVisibility('Skin.String(FavoritesHomeItem.Disable)') and 'kids' in menu_options:
            Add_Dir('%s %s'%(String(30060),String(30064)),'Skin.SetString(FavoritesHomeItem.Disable,)','exec_xbmc',False,'special://home/media/branding/backgrounds/HOME_KIDS/HOME_KIDS_001.jpg','','')
        if xbmc.getCondVisibility('Skin.String(LiveTVHomeItem.Disable)') and 'livetv' in menu_options:
            Add_Dir('%s %s'%(String(30060),String(30065)),'Skin.SetString(LiveTVHomeItem.Disable,)','exec_xbmc',False,'special://home/media/branding/backgrounds/HOME_LIVE_TV/HOME_LIVE_TV_001.jpg','','')
        if xbmc.getCondVisibility('Skin.String(MovieHomeItem.Disable)') and 'movies' in menu_options:
            Add_Dir('%s %s'%(String(30060),String(30066)),'Skin.SetString(MovieHomeItem.Disable,)','exec_xbmc',False,'special://home/media/branding/backgrounds/HOME_MOVIES/HOME_MOVIES_001.jpg','','')
        if xbmc.getCondVisibility('Skin.String(MusicHomeItem.Disable)') and 'music' in menu_options:
            Add_Dir('%s %s'%(String(30060),String(30067)),'Skin.SetString(MusicHomeItem.Disable,)','exec_xbmc',False,'special://home/media/branding/backgrounds/HOME_MUSIC/HOME_MUSIC_001.jpg','','')
        if xbmc.getCondVisibility('Skin.String(ProgramsHomeItem.Disable)') and 'news' in menu_options:
            Add_Dir('%s %s'%(String(30060),String(30068)),'Skin.SetString(ProgramsHomeItem.Disable,)','exec_xbmc',False,'special://home/media/branding/backgrounds/HOME_NEWS/HOME_NEWS_001.jpg','','')
        if xbmc.getCondVisibility('Skin.String(VideosHomeItem.Disable)') and 'sports' in menu_options:
            Add_Dir('%s %s'%(String(30060),String(30069)),'Skin.SetString(VideosHomeItem.Disable,)','exec_xbmc',False,'special://home/media/branding/backgrounds/HOME_SPORTS/HOME_SPORTS_001.jpg','','')
        if xbmc.getCondVisibility('Skin.String(Custom2HomeItem.Disable)') and 'technology' in menu_options:
            Add_Dir('%s %s'%(String(30060),String(30070)),'Skin.SetString(Custom2HomeItem.Disable,)','exec_xbmc',False,'special://home/media/branding/backgrounds/HOME_TECHNOLOGY/HOME_TECHNOLOGY_001.jpg','','')
        if xbmc.getCondVisibility('Skin.String(WeatherHomeItem.Disable)') and 'travel' in menu_options:
            Add_Dir('%s %s'%(String(30060),String(30071)),'Skin.SetString(WeatherHomeItem.Disable,)','exec_xbmc',False,'special://home/media/branding/backgrounds/HOME_TRAVEL/HOME_TRAVEL_001.jpg','','')
        if xbmc.getCondVisibility('Skin.String(TVShowHomeItem.Disable)') and 'tvshows' in menu_options:
            Add_Dir('%s %s'%(String(30060),String(30072)),'Skin.SetString(TVShowHomeItem.Disable,)','exec_xbmc',False,'special://home/media/branding/backgrounds/HOME_TV_SHOWS/HOME_TV_SHOWS_001.jpg','','')
        if xbmc.getCondVisibility('Skin.String(PicturesHomeItem.Disable)') and 'world' in menu_options:
            Add_Dir('%s %s'%(String(30060),String(30073)),'Skin.SetString(PicturesHomeItem.Disable,)','exec_xbmc',False,'special://home/media/branding/backgrounds/HOME_WORLD/HOME_WORLD_001.jpg','','')
        if xbmc.getCondVisibility('Skin.String(ShutdownHomeItem.Disable)') and 'youtube' in menu_options:
            Add_Dir('%s %s'%(String(30060),String(30074)),'Skin.SetString(ShutdownHomeItem.Disable,)','exec_xbmc',False,'special://home/media/branding/backgrounds/HOME_YOUTUBE/HOME_YOUTUBE_001.jpg','','')
        if xbmc.getCondVisibility('Skin.String(MusicVideoHomeItem.Disable)') and 'xxx' in menu_options:
            Add_Dir('%s %s'%(String(30060),String(30075)),'Skin.SetString(MusicVideoHomeItem.Disable,)','exec_xbmc',False,'special://home/media/branding/backgrounds/HOME_XXX/HOME_XXX_001.jpg','','')
        if listcount > 0:
            dialog.ok(String(30079),String(30310))
            xbmc.executebuiltin('ActivateWindow(home)')

    if menumode == 'remove':
        listcount = Sleep_If_Function_Active(function=Main_Menu_Visibility,args=[menu_list,'',False])
        if not xbmc.getCondVisibility('Skin.String(Custom6HomeItem.Disable)'):
            Add_Dir('%s %s'%(String(30076),String(30061)),'Skin.SetString(Custom6HomeItem.Disable,True)','exec_xbmc',False,'special://home/media/branding/backgrounds/HOME_COMEDY/HOME_COMEDY_001.jpg','','')
        if not xbmc.getCondVisibility('Skin.String(Custom3HomeItem.Disable)'):
            Add_Dir('%s %s'%(String(30076),String(30077)),'Skin.SetString(Custom3HomeItem.Disable,True)','exec_xbmc',False,'special://home/media/branding/backgrounds/HOME_COOKING/HOME_COOKING_001.jpg','','')
        if not xbmc.getCondVisibility('Skin.String(Custom4HomeItem.Disable)'):
            Add_Dir('%s %s'%(String(30076),String(30062)),'Skin.SetString(Custom4HomeItem.Disable,True)','exec_xbmc',False,'special://home/media/branding/backgrounds/HOME_FITNESS/HOME_FITNESS_001.jpg','','')
        if not xbmc.getCondVisibility('Skin.String(Custom5HomeItem.Disable)'):
            Add_Dir('%s %s'%(String(30076),String(30063)),'Skin.SetString(Custom5HomeItem.Disable,True)','exec_xbmc',False,'special://home/media/branding/backgrounds/HOME_GAMING/HOME_GAMING_001.jpg','','')
        if not xbmc.getCondVisibility('Skin.String(FavoritesHomeItem.Disable)'):
            Add_Dir('%s %s'%(String(30076),String(30064)),'Skin.SetString(FavoritesHomeItem.Disable,True)','exec_xbmc',False,'special://home/media/branding/backgrounds/HOME_KIDS/HOME_KIDS_001.jpg','','')
        if not xbmc.getCondVisibility('Skin.String(LiveTVHomeItem.Disable)'):
            Add_Dir('%s %s'%(String(30076),String(30065)),'Skin.SetString(LiveTVHomeItem.Disable,True)','exec_xbmc',False,'special://home/media/branding/backgrounds/HOME_LIVE_TV/HOME_LIVE_TV_001.jpg','','')
        if not xbmc.getCondVisibility('Skin.String(MovieHomeItem.Disable)'):
            Add_Dir('%s %s'%(String(30076),String(30066)),'Skin.SetString(MovieHomeItem.Disable,True)','exec_xbmc',False,'special://home/media/branding/backgrounds/HOME_MOVIES/HOME_MOVIES_001.jpg','','')
        if not xbmc.getCondVisibility('Skin.String(MusicHomeItem.Disable)'):
            Add_Dir('%s %s'%(String(30076),String(30067)),'Skin.SetString(MusicHomeItem.Disable,True)','exec_xbmc',False,'special://home/media/branding/backgrounds/HOME_MUSIC/HOME_MUSIC_001.jpg','','')
        if not xbmc.getCondVisibility('Skin.String(ProgramsHomeItem.Disable)'):
            Add_Dir('%s %s'%(String(30076),String(30068)),'Skin.SetString(ProgramsHomeItem.Disable,True)','exec_xbmc',False,'special://home/media/branding/backgrounds/HOME_NEWS/HOME_NEWS_001.jpg','','')
        if not xbmc.getCondVisibility('Skin.String(VideosHomeItem.Disable)'):
            Add_Dir('%s %s'%(String(30076),String(30069)),'Skin.SetString(VideosHomeItem.Disable,True)','exec_xbmc',False,'special://home/media/branding/backgrounds/HOME_SPORTS/HOME_SPORTS_001.jpg','','')
        if not xbmc.getCondVisibility('Skin.String(Custom2HomeItem.Disable)'):
            Add_Dir('%s %s'%(String(30076),String(30070)),'Skin.SetString(Custom2HomeItem.Disable,True)','exec_xbmc',False,'special://home/media/branding/backgrounds/HOME_TECHNOLOGY/HOME_TECHNOLOGY_001.jpg','','')
        if not xbmc.getCondVisibility('Skin.String(WeatherHomeItem.Disable)'):
            Add_Dir('%s %s'%(String(30076),String(30071)),'Skin.SetString(WeatherHomeItem.Disable,True)','exec_xbmc',False,'special://home/media/branding/backgrounds/HOME_TRAVEL/HOME_TRAVEL_001.jpg','','')
        if not xbmc.getCondVisibility('Skin.String(TVShowHomeItem.Disable)'):
            Add_Dir('%s %s'%(String(30076),String(30072)),'Skin.SetString(TVShowHomeItem.Disable,True)','exec_xbmc',False,'special://home/media/branding/backgrounds/HOME_TV_SHOWS/HOME_TV_SHOWS_001.jpg','','')
        if not xbmc.getCondVisibility('Skin.String(PicturesHomeItem.Disable)'):
            Add_Dir('%s %s'%(String(30076),String(30073)),'Skin.SetString(PicturesHomeItem.Disable,True)','exec_xbmc',False,'special://home/media/branding/backgrounds/HOME_WORLD/HOME_WORLD_001.jpg','','')
        if not xbmc.getCondVisibility('Skin.String(ShutdownHomeItem.Disable)'):
            Add_Dir('%s %s'%(String(30076),String(30074)),'Skin.SetString(ShutdownHomeItem.Disable,True)','exec_xbmc',False,'special://home/media/branding/backgrounds/HOME_YOUTUBE/HOME_YOUTUBE_001.jpg','','')
        if not xbmc.getCondVisibility('Skin.String(MusicVideoHomeItem.Disable)'):
            Add_Dir('%s %s'%(String(30076),String(30075)),'Skin.SetString(MusicVideoHomeItem.Disable,True)','exec_xbmc',False,'special://home/media/branding/backgrounds/HOME_XXX/HOME_XXX_001.jpg','','')
        if listcount > 0:
            dialog.ok(String(30079),String(30311))
            xbmc.executebuiltin('ActivateWindow(home)')
#---------------------------------------------------------------------------------------------------
# Function to move a directory to another location, use 1 for clean paramater if you want to remove original source.
def Move_Tree(src,dst,clean):
    dolog('SOURCE TO MOVE: %s'%src)
    for src_dir, dirs, files in os.walk(src):
        dst_dir = src_dir.replace(src, dst, 1)
        if not os.path.exists(dst_dir):
            dolog('Creating path: %s'% dst_dir)
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.move(src_file, dst_dir)
            dolog('moved: %s to %s'% (src_file, dst_dir))
    if clean:
        try:
            shutil.rmtree(src)
            dolog('Successfully removed %s'% src)
        except:
            dolog('Failed to remove %s'% src)
#---------------------------------------------------------------------------------------------------
# Multiselect Dialog - try the built-in multiselect or fallback to pre-jarvis workaround
def multidialog(title, mylist, images, description):
    try:
        ret = dialog.multiselect(title, mylist)
    except:
        ret = multiselect(title, mylist, images, description)
    return ret if not ret == None else []
#---------------------------------------------------------------------------------------------------
# Multiselect Dialog for older Kodi versions (pre Jarvis)
def multiselect(title, mylist, images, description):
    global pos
    global listicon
    class MultiChoiceDialog(pyxbmct.AddonDialogWindow):
        def __init__(self, title="", items=None, images=None, description=None):
            super(MultiChoiceDialog, self).__init__(title)
            self.setGeometry(1100, 700, 9, 9)
            self.selected = []
            self.set_controls()
            self.connect_controls()
            self.listing.addItems(items or [])
            self.set_navigation()
            self.connect(ACTION_NAV_BACK, self.close)
            self.connect(ACTION_MOVE_UP, self.update_list)
            self.connect(ACTION_MOVE_DOWN, self.update_list)
            
        def set_controls(self):
            Background  = pyxbmct.Image(dialog_bg, aspectRatio=0) # set aspect ratio to stretch
            Background.setImage(dialog_bg)
            self.listing = pyxbmct.List(_imageWidth=15)
            self.placeControl(Background, 0, 0, rowspan=20, columnspan=20)
            self.placeControl(self.listing, 0, 0, rowspan=9, columnspan=5, pad_y=10) # grid reference, start top left and span 9 boxes down and 5 across
            Icon=pyxbmct.Image(images[0], aspectRatio=2) # set aspect ratio to keep original
            Icon.setImage(images[0])
            self.placeControl(Icon, 0, 5, rowspan=3, columnspan=3, pad_x=10, pad_y=10)
            self.textbox = pyxbmct.TextBox()
            self.placeControl(self.textbox, 4, 5, rowspan=3, columnspan=3, pad_x=10, pad_y=10)
            self.textbox.setText(description[0])
            self.ok_button = pyxbmct.Button("OK")
            self.placeControl(self.ok_button, 7, 5, pad_x=10, pad_y=10)
            self.cancel_button = pyxbmct.Button("Cancel")
            self.placeControl(self.cancel_button, 7, 6, pad_x=10, pad_y=10)

        def connect_controls(self):
            self.connect(self.listing, self.check_uncheck)
            self.connect(self.ok_button, self.ok)
            self.connect(self.cancel_button, self.close)

        def set_navigation(self):
            self.listing.controlLeft(self.ok_button)
            self.listing.controlRight(self.ok_button)
            self.ok_button.setNavigation(self.listing, self.listing, self.cancel_button, self.cancel_button)
            self.cancel_button.setNavigation(self.listing, self.listing, self.ok_button, self.ok_button)
            if self.listing.size():
                self.setFocus(self.listing)
            else:
                self.setFocus(self.cancel_button)
            
        def update_list(self):
            pos      = self.listing.getSelectedPosition()
            listicon = images[pos]
            Icon=pyxbmct.Image(listicon, aspectRatio=2)
            Icon.setImage(listicon)
            self.placeControl(Icon, 0, 5, rowspan=3, columnspan=3, pad_x=10, pad_y=10)
            self.textbox.setText(description[pos])

        def check_uncheck(self):
            list_item = self.listing.getSelectedItem()
            if list_item.getLabel2() == "checked":
                list_item.setIconImage("")
                list_item.setLabel2("unchecked")
            else:
                list_item.setIconImage(checkicon)
                list_item.setLabel2("checked")

        def ok(self):
            self.selected = [index for index in xrange(self.listing.size())
                            if self.listing.getListItem(index).getLabel2() == "checked"]
            super(MultiChoiceDialog, self).close()

        def close(self):
            self.selected = []
            super(MultiChoiceDialog, self).close()
            
    dialog = MultiChoiceDialog(title, mylist, images, description)
    dialog.doModal()
    return dialog.selected
    del dialog
#---------------------------------------------------------------------------------------------------
# Open Kodi File Manager
def Open_SF():
    menu_array = [String(30061), String(30077), String(30062), String(30063), String(30064), String(30065), String(30066), String(30067), String(30068), String(30069), String(30070), String(30071), String(30072), String(30073), String(30074), String(30075)]
    choice = dialog.select(String(30128),menu_array)
    choice = menu_array[choice]
    xbmc.executebuiltin('ActivateWindow(programs,"plugin://plugin.program.super.favourites/?folder=HOME_%s",return)' % choice.replace(' ', '_'))
#-----------------------------------------------------------------------------------------------------------------
# Function to install venz pack
def Open_Link(url):
    response = Open_URL(post_type='post',url=url)
    dolog("### "+response)
    if "record" in response:
        Grab_Updates('http://tlbb.me/boxer/comm_live.php?z=c&x=','ignoreplayer')
        xbmc.executebuiltin('Container.Refresh')
    else:
        dialog.ok(String(30131),String(30132))
#---------------------------------------------------------------------------------------------------
# Check if system is OE or LE
def OpenELEC_Check():
    try:
        content = Grab_Log()
        if 'Running on OpenELEC' in content or 'Running on LibreELEC' in content:
            return True
        else:
            return False
    except:
        return False
#---------------------------------------------------------------------------------------------------
def OpenELEC_Settings():
    if xbmc.getCondVisibility("System.HasAddon(service.openelec.settings)") or xbmc.getCondVisibility("System.HasAddon(service.libreelec.settings)"):
        if xbmc.getCondVisibility("System.HasAddon(service.openelec.settings)"): 
            xbmc.executebuiltin('RunAddon(service.openelec.settings)')
        elif xbmc.getCondVisibility("System.HasAddon(service.libreelec.settings)"): 
            xbmc.executebuiltin('RunAddon(service.libreelec.settings)')
        xbmc.sleep(1500)
        xbmc.executebuiltin('Control.SetFocus(1000,2)')
        xbmc.sleep(500)
        xbmc.executebuiltin('Control.SetFocus(1200,0)')
#---------------------------------------------------------------------------------------------------
# Scrape Google PlayStore
def Play_Store_Scrape(i):
    name        = i
    fanart      = Fanart_Path
    iconimage   = "androidapp://sources/apps/%s.png" % i
    category    = 'Unknown'
    genre       = 'Unknown'
    video       = 'none'
    PEGI        = 'N/A'
    author      = 'N/A'
    description = 'N/A'

    base_url = "https://play.google.com/store/apps/details?id=" +i
    link = Open_URL(url=base_url)
    if link != False:
        link = link.replace('\n','').replace('\r','')
        raw_content = re.compile(r'<div class="id-app-title[\s\S]*?id-cluster-container details-section recommendation').findall(link)
        link = raw_content[0]

# App Name
        regexTitle = r'<div class="id-app-title".tabindex=".">(.+?)</div>'
        match = re.search(regexTitle, link)
        if match != None:
            name = urllib.unquote(match.group(1))
        else:
            name = i
 
# Category
        regexCategory = r'/store/apps/category/(.+?).">'
        match = re.compile(regexCategory).findall(link)
        category = urllib.unquote(match[0]) if len(match) > 0 else 'Unknown'

# Fanart
        regexBackdrop = r'data-expand-to="full-screenshot-[0-9]{1,2}" src="(//\w+?.\w+?.\S+?=h900)"'
        match = re.compile(regexBackdrop).findall(link)
        if len(match) > 0:
            fanart = "https:" +match[len(match) - 1]

# Genre
        regexGenre = r'<span itemprop="genre">(.+?)</span>'
        match = re.search(regexGenre, link)
        if match != None:
            genre = urllib.unquote(match.group(1))

# Apk Description
        regexDescription = r'itemprop="description"> <div jsname=".+?">(.+?)<div class="show-more-end"'
        match = re.compile(regexDescription).findall(link)
        if len(match) !=0:
            description = match[0].replace('<b>','[B]').replace('</b>','[/B]').replace('<i>','[I]').replace('</i>','[/I]').replace('<p>','[CR]').replace('</p>','').replace('&ndash;','-').replace('&mdash;','-').replace("&rsquo;", "'").replace("&rdquo;", '"').replace("</a>", " ").replace("&hellip;", '...').replace("&lsquo;", "'").replace("&ldquo;", '"').replace("&amp;",'&').replace('&#39;',"'").replace('<br>','[CR]').replace('<div>','').replace('</div>','')
            description = description.strip().rstrip()

# Preview Video
        regexVideo = r'data-video-url="https://www.youtube.com/embed/(\S.+?)\?ps=play.+?"'
        match = re.search(regexVideo, link)
        video = match.group(1) if match != None else 'none'

# Age Restriction
        regexAge = r'<div class=".+?ontent-rating-title">(.+?)</div>'
        match = re.search(regexAge, link)
        PEGI = match.group(1) if match != None else 'N/A'
        PEGI = PEGI.replace('</span> ','')

# Author
        regexMaker = r'<span itemprop="name">(.+?)</span>'
        match = re.search(regexMaker, link)
        author = match.group(1) if match != None else 'N/A'

    final_list = [i, name, iconimage, fanart, category, genre, video, PEGI, author, description]
    return final_list
#---------------------------------------------------------------------------------------------------
# Set popup xml based on platform
def pop(xmlfile):
# if popup is an advert from the web
    if 'http' in xmlfile:
        contents = 'none'
        filedate = xmlfile[-10:]
        filedate = filedate[:-4]
        latest = os.path.join(ADDON_DATA,AddonID,'latest')

        if os.path.exists(latest):
            readfile = open(latest, mode='r')
            contents = readfile.read()
            readfile.close()

        if contents == filedate:
            filedate = contents
                
        else:
            Download(xmlfile,os.path.join(ADDONS,AddonID,'resources','skins','DefaultSkin','media','latest.jpg'))
            writefile = open(latest, mode='w+')
            writefile.write(filedate)
            writefile.close()
        xmlfile = 'latest.xml'
    popup = SPLASH(xmlfile,ADDON.getAddonInfo('path'),'DefaultSkin',close_time=34)
    popup.doModal()
    del popup
#---------------------------------------------------------------------------------------------------
# Function to clear the addon_data
def Remove_Addon_Data():
# Offer to remove everything, we don't want this as it will cause a fresh install

    # choice = dialog.yesno(String(30133), String(30134), yeslabel=String(30135), nolabel=String(30136))
    
    # if choice:
    #     choice = dialog.yesno(String(30137),String(30138))
    #     if choice:
    #         Delete_Userdata()
    #         dialog.ok(String(30139), '', String(30140),'')
    # else:
    skiparray = ['.DS_Store','plugin.program.tbs','script.openwindow','script.trtv','plugin.program.super.favourites']
    namearray = []
    iconarray = []
    descarray = []
    patharray = []
    finalpath = []

    for file in os.listdir(ADDON_DATA):
        addon_id    = None
        if os.path.isdir(os.path.join(ADDON_DATA,file)):
            try:
                addon_id    = Get_Addon_ID(file)
                Addon       = xbmcaddon.Addon(addon_id)
                name        = Addon.getAddonInfo('name')
                iconimage   = Addon.getAddonInfo('icon')
                description = Addon.getAddonInfo('description')
            except:
                name        = String(30142)
                iconimage   = unknown_icon
                description = String(30141)

        else:
            name        = 'Unknown Add-on'
            iconimage   =  unknown_icon
            description = 'No add-on has been found on your system that matches this ID. The most likely scenario for this is you\'ve previously uninstalled this add-on and left the old addon_data on the system.'

        if not addon_id in skiparray and addon_id != None:
            filepath = os.path.join(ADDON_DATA,file)
            namearray.append(file)
            iconarray.append(iconimage)
            descarray.append('[COLOR=gold]%s[/COLOR][CR][CR]%s'% (name, description))
            patharray.append(filepath)

    finalarray = multiselect(String(30143),namearray,iconarray,descarray)
    for item in finalarray:
        newpath = patharray[item]
        newname = namearray[item]
        finalpath.append([newname,newpath])
    if len(finalpath) > 0:
        Remove_Addons(finalpath)
#---------------------------------------------------------------------------------------------------
# Function to remove a list of addons including addon_data
def Remove_Addons(url):
    for item in url:
        data_path = item[1].replace(ADDONS,ADDON_DATA)
        if 'addon_data' in item[1]:
            addontype = String(30146)
            dialog_text = String(30144)
        else:
            addontype = String(30147)
            dialog_text = String(30145)
        if dialog.yesno(String(30148) % addontype, String(30149)% dialog_text,'[COLOR=dodgerblue]%s[/COLOR]'% item[0]):
            addon_id = Get_Addon_ID(item[1])
            Set_Setting(setting_type='addon_enable',setting=addon_id, value='false')
            Delete_Folders(item[1])
            if not 'addon_data' in item[1]:
                if dialog.yesno(String(30133),String(30150)):
                    try:
                        Delete_Folders(item[1])
                    except:
                        pass
#---------------------------------------------------------------------------------------------------
# Function to clear the packages folder
def Remove_Crash_Logs():
    if dialog.yesno(String(30153), String(30154), nolabel=String(30041),yeslabel=String(30042)):
        Delete_Crashlogs()
        dialog.ok(String(30155), '', String(30156))
#-----------------------------------------------------------------------------
# Remove a path, whether folder or file it will be deleted
def Remove_Files():
    remlist = os.path.join(TBSDATA,'remlist')
    dolog('### Attempting to Remove Files')
    if os.path.exists(remlist):
        readfile = open(remlist,'r')
        content  = readfile.read().splitlines()
        readfile.close()
        for item in content:
            rempath = xbmc.translatePath('special://home')+item
            if os.path.exists(rempath):
                try:
                    os.remove(rempath)
                    dolog('### Successfully removed file: %s' % rempath)
                except:
                    try:
                        shutil.rmtree(rempath)
                        dolog('### Successfully removed folder: %s' % rempath)
                    except:
                        dolog("### Failed to remove: %s" %rempath)
#---------------------------------------------------------------------------------------------------
# Remove an item from the system
def Remove_Menu(function, menutype = ''):
    contentarray = []
    imagearray   = []
    descarray    = []
    contenturl   = []
    urlparams = URL_Params()
    dolog('### OPENING URL TO GRAB DETAILS OF WHAT TO REMOVE:')
    dolog('http://tlbb.me/boxer/cat_search_live.php?&x=%s' % (encryptme('e','%s&%s&0&%s&%s' % (urlparams, function, social_shares, menutype))))
    sharelist_URL  = 'http://tlbb.me/boxer/cat_search_live.php?&x=%s' % (encryptme('e','%s&%s&0&%s&%s' % (urlparams, function, social_shares, menutype)))
    content_list   = Open_URL(post_type='post',url=sharelist_URL)
    clean_link     = encryptme('d',content_list)
    dolog('#### RETURN: %s' % clean_link)
# Grab all the shares which match the master sub-category
    match = re.compile('n="(.+?)"t="(.+?)"d="(.+?)"l="(.+?)"', re.DOTALL).findall(clean_link)
    for name, thumb, desc, link in match:
        contentarray.append(name)
        imagearray.append(thumb)
        descarray.append(desc)
        contenturl.append(link)

# Return the results and update
    if len(contentarray) > 0:
        if menutype == '':
            choices = multiselect(String(30088),contentarray,imagearray,descarray)
            if len(choices) > 0:
                Notify(String(30086),String(30087),'5000',os.path.join(ADDONS,'plugin.program.tbs','resources','update.png'))
                xbmc.executebuiltin('ActivateWindow(HOME)')
                for item in choices:
                    Open_URL(post_type='post',url=contenturl[item])
        else:
            for item in contenturl:
                dolog('### URL TO REMOVE: %s' % item)
                Open_URL(post_type='post',url=item)

        Grab_Updates('http://tlbb.me/boxer/comm_live.php?multi&z=c&x=','ignoreplayer')
    elif menutype == '':
        dialog.ok(String(30089),String(30090))
#---------------------------------------------------------------------------------------------------
# Function to clear the packages folder
def Remove_Packages(url=''):
    if dialog.yesno(String(30157), String(30158), nolabel=String(30041),yeslabel=String(30042)):
        Delete_Folders(PACKAGES)
    if url == '':
        dialog.ok(String(30155), '', String(30159))
#---------------------------------------------------------------------------------------------------
# Function to clear the packages folder
def Remove_Textures_Dialog():
    if dialog.yesno(String(30160),String(30161)):
        Remove_Textures()
        Delete_Folders(THUMBNAILS)
    
        if dialog.yesno(String(30162), String(30163),'', nolabel=String(30164),yeslabel=String(30165)):
            System('quit')
#---------------------------------------------------------------------------------------------------
# Function to remove textures13.db
def Remove_Textures():
    textures   =  xbmc.translatePath('special://home/userdata/Database/Textures13.db')
    try:
        dbcon = database.connect(textures)
        dbcur = dbcon.cursor()
        dbcur.execute("DROP TABLE IF EXISTS path")
        dbcur.execute("VACUUM")
        dbcon.commit()
        dbcur.execute("DROP TABLE IF EXISTS sizes")
        dbcur.execute("VACUUM")
        dbcon.commit()
        dbcur.execute("DROP TABLE IF EXISTS texture")
        dbcur.execute("VACUUM")
        dbcon.commit()
        dbcur.execute("""CREATE TABLE path (id integer, url text, type text, texture text, primary key(id))""")
        dbcon.commit()
        dbcur.execute("""CREATE TABLE sizes (idtexture integer,size integer, width integer, height integer, usecount integer, lastusetime text)""")
        dbcon.commit()
        dbcur.execute("""CREATE TABLE texture (id integer, url text, cachedurl text, imagehash text, lasthashcheck text, PRIMARY KEY(id))""")
        dbcon.commit()
    except:
        pass
#---------------------------------------------------------------------------------------------------
# Function to restore a backup xml file (guisettings, sources, RSS)
def Restore_Backup_XML(name,url,description):
    if 'Backup' in name:
        Check_Download_Path()
        TO_READ   = open(url).read()
        TO_WRITE  = os.path.join(USB,description.split('Your ')[1])
        f         = open(TO_WRITE, mode='w')
        f.write(TO_READ)
        f.close() 
    
    else:
        if 'guisettings.xml' in description:
            a     = open(os.path.join(USB,description.split('Your ')[1])).read()
            r     ='<setting type="(.+?)" name="%s.(.+?)">(.+?)</setting>'% skin
            match = re.compile(r).findall(a)
            
            for type,string,setting in match:
                setting=setting.replace('&quot;','') .replace('&amp;','&') 
                xbmc.executebuiltin("Skin.Set%s(%s,%s)"%(type.title(),string,setting))  
        
        else:    
            TO_WRITE = os.path.join(url)
            TO_READ  = open(os.path.join(USB,description.split('Your ')[1])).read()
            f        = open(TO_WRITE, mode='w')
            f.write(TO_READ)
            f.close()  

    dialog.ok(String(30166), "", String(30167))
#---------------------------------------------------------------------------------------------------
# Function to restore a backup xml file (guisettings, sources, RSS)
def Restore_Backup_XML(name,url,description):
    if 'Backup' in name:
        Check_Download_Path()
        TO_READ   = open(url).read()
        TO_WRITE  = os.path.join(USB,description.split('Your ')[1])
        f         = open(TO_WRITE, mode='w')
        f.write(TO_READ)
        f.close() 
    
    else:
        if 'guisettings.xml' in description:
            a     = open(os.path.join(USB,description.split('Your ')[1])).read()
            r     ='<setting type="(.+?)" name="%s.(.+?)">(.+?)</setting>'% skin
            match = re.compile(r).findall(a)
            
            for type,string,setting in match:
                setting=setting.replace('&quot;','') .replace('&amp;','&') 
                xbmc.executebuiltin("Skin.Set%s(%s,%s)"%(type.title(),string,setting))  
        
        else:    
            TO_WRITE = os.path.join(url)
            TO_READ  = open(os.path.join(USB,description.split('Your ')[1])).read()
            f        = open(TO_WRITE, mode='w')
            f.write(TO_READ)
            f.close()  

    dialog.ok(String(30166), "", String(30167))
#---------------------------------------------------------------------------------------------------
# Create restore menu
def Restore_Option():
    if os.path.exists(os.path.join(USB,'addons.zip')):   
        Add_Dir('%s %s'%(String(30168),String(30170)),'addons','restore_zip',False,'Restore.png','','Restore Your Addons')

    if os.path.exists(os.path.join(USB,'addon_data.zip')):   
        Add_Dir('%s %s'%(String(30168),String(30146)),'addon_data','restore_zip',False,'Restore.png','','Restore Your Addon UserData')           

    if os.path.exists(os.path.join(USB,'guisettings.xml')):
        Add_Dir('%s %s'%(String(30168),String(30171)),GUI,'restore_backup',False,'Restore.png','','Restore Your guisettings.xml')
    
    if os.path.exists(os.path.join(USB,'favourites.xml')):
        Add_Dir('%s %s'%(String(30168),String(30172)),FAVS,'restore_backup',False,'Restore.png','','Restore Your favourites.xml')
        
    if os.path.exists(os.path.join(USB,'sources.xml')):
        Add_Dir('%s %s'%(String(30168),String(30173)),SOURCE,'restore_backup',False,'Restore.png','','Restore Your sources.xml')
        
    if os.path.exists(os.path.join(USB,'advancedsettings.xml')):
        Add_Dir('%s %s'%(String(30168),String(30174)),ADVANCED,'restore_backup',False,'Restore.png','','Restore Your advancedsettings.xml')        

    if os.path.exists(os.path.join(USB,'keyboard.xml')):
        Add_Dir('%s %s'%(String(30168),String(30175)),KEYMAPS,'restore_backup',False,'Restore.png','','Restore Your keyboard.xml')
        
    if os.path.exists(os.path.join(USB,'RssFeeds.xml')):
        Add_Dir('Restore RssFeeds.xml',RSS,'resore_backup',False,'Restore.png','','Restore Your RssFeeds.xml')    
#---------------------------------------------------------------------------------------------------
# Function to restore a previously backed up zip, this includes full backup, addons or addon_data.zip
def Restore_Zip_File(url):
    Check_Download_Path()
    if 'addons' in url:
        ZIPFILE    = xbmc.translatePath(os.path.join(USB,'addons.zip'))
        DIR        = ADDONS

    else:
        ZIPFILE = xbmc.translatePath(os.path.join(USB,'addon_data.zip'))
        DIR = ADDON_DATA

    if 'Backup' in url:
        Delete_Folders(PACKAGES)
        dp.create(String(30176), String(30177), '', String(30048))
        zipobj       = zipfile.ZipFile(ZIPFILE , 'w', zipfile.ZIP_DEFLATED)
        rootlen      = len(DIR)
        for_progress = []
        ITEM         = []

        for base, dirs, files in os.walk(DIR):
            for file in files:
                ITEM.append(file)
        N_ITEM = len(ITEM)
        for base, dirs, files in os.walk(DIR):
            for file in files:
                for_progress.append(file) 
                progress = len(for_progress) / float(N_ITEM) * 100  
                dp.update(int(progress),String(30177), '[COLOR yellow]%s[/COLOR]'%file, String(30048))
                fn = os.path.join(base, file)
                if not 'temp' in dirs:
                    if not AddonID in dirs:
                       import time
                       FORCE= '01/01/1980'
                       FILE_DATE=time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(fn)))
                       if FILE_DATE > FORCE:
                           zipobj.write(fn, fn[rootlen:]) 
        zipobj.close()
        dp.close()
        dialog.ok(String(30166), String(30167))   

    else:
        dp.create(String(30178), String(30179), '', String(30048))
        dp.update(0, "", "%s %s" % (String(30178), String(30048)))
        Extract(ZIPFILE,DIR,dp)
        xbmc.sleep(500)
        xbmc.executebuiltin('UpdateLocalAddons ')    
        xbmc.executebuiltin("UpdateAddonRepos")        

        if 'Backup' in url:
            dialog.ok(String(30180), String(30181))
            Force_Close()

        else:
            dialog.ok(String(30166), String(30167))      
#---------------------------------------------------------------------------------------------------
# Function to pull commands and update
def RMT():
    Remove_Textures()
    Wipe_Cache()
#---------------------------------------------------------------------------------------------------
# Function to populate the text file containing apk details
def Scan_APKs(showdialogs = True):
    cont         = True
    content      = ''
    scraped_list = []

    if os.path.exists(Installed_Apps):
        App_List = open(Installed_Apps, 'r')
        content  = App_List.read()
        App_List.close()
    else:
        cont = False

    InstalledAPK = My_Apps()
    endAPK = len(InstalledAPK)
    startAPK = 0
    dp = xbmcgui.DialogProgress()
    if showdialogs:
        dp.create(String(30091),'')
    for app in InstalledAPK:
        dolog('### Checking %s' % app)
        startAPK += 1
        if showdialogs:
            percentAPK = startAPK / float(endAPK) * 100
            stuffAPK = String(30092) % app
            progress = String(30093) % (startAPK, endAPK)
            dp.update(percentAPK,'',stuffAPK,progress)

# Check installed apps against ones already in the list and only scrape ones not previously done
        if app not in content:
            scraped_list.append(Play_Store_Scrape(app))

    if cont==True:
        App_List = open(Installed_Apps,'a')

    else:
        App_List = open(Installed_Apps,'w')

    for item in scraped_list:
        counter = 1
        length  = len(item)
        for value in item:
            App_List.write(value+'|') if counter < length else App_List.write(value+'\n')
            counter += 1
    App_List.close()

    return True
#---------------------------------------------------------------------------------------------------
# Function to pull commands and update
def SF(command,SF_folder,SF_link):
    check4='SF'
# Check if folder exists, if not create folder and favourites.xml file
    folder = xbmc.translatePath(os.path.join(ADDON_DATA,'plugin.program.super.favourites','Super Favourites',SF_folder))
    SF_favs   = os.path.join(folder,'favourites.xml')
    
    if command=='add':

        if not os.path.exists(folder):
            os.makedirs(folder)
            localfile = open(SF_favs, mode='w+')
            localfile.write('<favourites>\n</favourites>')
            localfile.close()
        
# Grab content between favourites tags, we'll replace this later
        localfile2 = open(SF_favs, mode='r')
        content2 = localfile2.read()
        localfile2.close()

        favcontent    = re.compile('<favourite name="[\s\S]*?\/favourites>').findall(content2)
        faves_content = favcontent[0] if (len(favcontent) > 0) else '\n</favourites>'
        
# Copy clean contents of online SF command into memory - if we grab and pass through as paramater the /r /t /n etc. tags fail to translate correctly
        localfile = open(PROGRESS_TEMP, mode='r')
        newcontent = localfile.read()
        localfile.close()
        
#Write new favourites file
        if not newcontent in content2:
            localfile = open(SF_favs, mode='w+')
            if faves_content == '\n</favourites>':
                newfile = localfile.write('<favourites>\n\t'+newcontent+faves_content)
            else:
                newfile = localfile.write('<favourites>\n\t'+newcontent+'\n\t'+faves_content)
            localfile.close()
        
    if command=='delete':

# Grab content between favourites tags, we'll replace this later
        try:
            localfile2 = open(SF_favs, mode='r')
            content2 = localfile2.read()
            localfile2.close()

# Copy clean contents of online SF command into memory - if we grab and pass through as paramater the /r /t /n etc. tags fail to translate correctly
            localfile = open(PROGRESS_TEMP, mode='r')
            newcontent = localfile.read()
            localfile.close()
        
#Write new favourites file
            localfile = open(SF_favs, mode='w+')
            newfile = localfile.write(content2.replace('\n\t'+newcontent,''))
            localfile.close()
        except:
            pass

# Attempt to delete the SF folder
    if command=='delfolder':

        try:
            shutil.rmtree(folder)
        except:
            pass
#---------------------------------------------------------------------------------------------------
# Social TV Menu
def Social_Menu():
    Add_Dir(String(30100), 'http://tlbb.me/boxer/comm_live.php?z=c&x=','grab_updates',False,'','','')
    if thirdparty == 'true':
        Add_Dir(String(30187),'false','enable_shares',False,'','','')
    else:
        Add_Dir(String(30188),'true','enable_shares',False,'','','')
    # Add_Dir(String(30189),'keyword','addon_browser',False,'','','')
    Add_Dir(String(30190),'','open_sf',False,'','','')
    Add_Dir(String(30191),'manual','check_shares',False,'','','')
    Add_Dir('Create username','', "create_username", False,'','','')
#    Add_Dir('','[COLOR=grey]Friend Requests (Coming Soon)[/COLOR]', '', '', '','','','')
#    Add_Dir('','[COLOR=grey]My Content (Coming Soon)[/COLOR]', '', '', '','','','')
#-----------------------------------------------------------------------------------------------------------------
# Main search menu for Venz content
def Search_Content_Main(type):
    dolog(type)
    if 'from_the' in type and '_menu' in type:
        Install_Venz_Menu(type+'||remove_main||'+type.replace('from_the_','').replace('_menu',''))
    elif type == 'main_menu':
        Install_Venz_Menu(type)
    elif not 'from_the' in type and type != 'main_menu' and not "submenu" in type:
        Add_Dir(String(30182) % type.replace('_',' '),'to_the_'+type+'_menu||add_main||'+type,'install_venz_menu',True,'','')
        Add_Dir(String(30183) % type.replace('_',' '),'to_the_'+type+'_menu||add_main||'+type,'search_content',True,'Manual_Search.png','','')
    elif "submenu" in type:
        Add_Dir(String(30184) % type.replace('_submenu','').replace('_',' ').title()+' Sub-menu','to_the_'+type+'||add_sub||'+type.replace('_submenu',''),'install_venz_menu',True,'','','')
        Add_Dir(String(30185) % type.replace('_submenu','').replace('_',' ').title()+' Sub-menu','from_the_'+type+'||remove_sub||'+type.replace('_submenu',''),'install_venz_menu',True,'','')   
#-----------------------------------------------------------------------------------------------------------------
# Search for Venz content
def Search_Content(menutype):
    vq = Keyboard(String(30186))
# if blank or the user cancelled the keyboard, return
    if ( not vq ): return False, 0

# we need to set the title to our query
    title = urllib.quote_plus(vq)
    Install_Venz_Menu('manualsearch'+title+'>>#'+menutype)
#-----------------------------------------------------------------------------------------------------------------
def SetNone():
    urlparams = URL_Params()
    link = Open_URL(post_type='post',url=encryptme('d','6773736f392e2e736b61612d6c642e7264736d6e6d642d6f676f3e773c011510030A')+encryptme('e',urlparams))
#-----------------------------------------------------------------------------------------------------------------
def Sync_Settings():
    dolog('##### SYNC SETTINGS STARTED #####')
    from koding import End_Path, Find_In_Text
    path = os.path.join(ADDON_DATA,AddonID,'settings')
    contents = Get_Contents(path=path,folders=False, subfolders=True, filter='.xml')
    dolog('Settings files found: '+repr(contents))
    for item in contents:
        temp_path    = item.replace(End_Path(item),'')
        plugin       = End_Path(temp_path)
        new_content  = Text_File(item,'r').splitlines()
        resources    = os.path.join(ADDONS,plugin,'resources','settings.xml')
        if os.path.exists(resources):
            res_contents = Text_File(resources,'r')
            res_lines    = res_contents.splitlines()

    # Check each line of new settings and check to see if we need to make changes in resources folder
            for line in new_content:
                setting = Find_In_Text(content=line,start='id="',end='"',show_errors=False)
                setting = setting[0] if (setting != None) else setting
                value   = Find_In_Text(content=line,start='value="',end='"',show_errors=False)
                value   = value[0] if (value != None) else value
                counter = 0
                for res_line in res_lines:
                    counter += 1
                    if 'id="%s"'%setting in res_line:
                        current_value = Find_In_Text(content=res_line,start='default="',end='"',show_errors=False)
                        current_value = current_value[0] if (current_value != None) else None
                        # if (plugin!='script.trtv') and (setting !='SF_CHANNELS'):
                        if current_value != value:
                            if current_value != None:
                                new_line = res_line.replace('default="%s"'%current_value, 'default="%s"'%value)
                            else:
                                new_line = res_line.replace(r'/>',' default="%s"'%value+r'/>')
                            dolog('ORIG: %s'%res_line)  
                            dolog('NEW: %s'%new_line)  
                            res_contents = res_contents.replace(res_line,new_line)
                            break
            Text_File(resources,'w',res_contents)
#-----------------------------------------------------------------------------------------------------------------
# Show full description of build
def Text_Guide(url):
    try:
        heading,text = url.split('|')
        Text_Box(heading, text)
    except:
        Text_Box('', url)
#-----------------------------------------------------------------------------------------------------------------
# Maintenance section
def Tools():
    Add_Dir(String(30192),'none','tools_addons',True,'','','')
    Add_Dir(String(30193),'none','backup_restore',True,'','','')
    Add_Dir(String(30194), '', 'tools_clean',True,'','','')
    Add_Dir(String(30195), '', 'tools_misc',True,'','','')
    if OpenELEC_Check():
        Add_Dir(String(30196),'','openelec_settings',False,'','','')
#-----------------------------------------------------------------------------------------------------------------
# Add-on based tools
def Tools_Addon_Removal():
    Add_Dir(String(30197),'all','addon_removal_menu',False,'','','')
    Add_Dir(String(30198),'audio','addon_removal_menu',False,'','','')
    Add_Dir(String(30199),'image','addon_removal_menu',False,'','','')
    Add_Dir(String(30200),'program','addon_removal_menu',False,'','','')
    Add_Dir(String(30201),'video','addon_removal_menu',False,'','','')
    Add_Dir(String(30202),'repo','addon_removal_menu',False,'','','')
#-----------------------------------------------------------------------------------------------------------------
# Add-on based tools
def Tools_Addons():
    Add_Dir(String(30203),'','tools_addon_removal',True,'','','')
    Add_Dir(String(30204),'url','remove_addon_data',False,'','','')
    Add_Dir(String(30205),'none','hide_passwords',False,'','','')
    Add_Dir(String(30206),'none','unhide_passwords',False,'','','')
    Add_Dir(String(30207),'none','update',False,'','','')
#-----------------------------------------------------------------------------------------------------------------
# Clean Tools
def Tools_Clean():
    Add_Dir(String(30208),'','full_clean',False,'','','')
    Add_Dir(String(30209),'url','clear_cache',False,'','','')
    Add_Dir(String(30210), 'none', 'remove_textures',False,'','','')
    Add_Dir(String(30211),'url','remove_packages',False,'','','')
    Add_Dir(String(30153),'url','remove_crash_logs',False,'','','')
    Add_Dir(String(30212), '', 'wipe_xbmc',False,'','','')
#-----------------------------------------------------------------------------------------------------------------
# Advanced Maintenance section
def Tools_Misc():
    Add_Dir(String(30213), 'none','ipcheck',False,'','','')
    Add_Dir(String(30214),'none','xbmcversion',False,'','','')
    # Add_Dir(String(30215),HOME,'fix_special',False,'','','')
    # Add_Dir(String(30216),'','ASCII_Check',False,'','','')
    Add_Dir(String(30218),'','kill_xbmc','','','','')
    Add_Dir(String(30219),'none','log',False,'','','')
    Add_Dir(String(30217),'false','adult_filter',False,'','','')
    Add_Dir(String(30220),'true','adult_filter',False,'','','')
#-----------------------------------------------------------------------------------------------------------------
# Unhide passwords in addon settings - THANKS TO MIKEY1234 FOR THIS CODE (taken from Xunity Maintenance)
def Unhide_Passwords():
    if dialog.yesno(String(30221), String(30222)):
        for root, dirs, files in os.walk(ADDONS):
            for f in files:
                if f =='settings.xml':
                    FILE=open(os.path.join(root, f)).read()
                    match=re.compile('<setting id=(.+?)>').findall(FILE)
                    for LINE in match:
                        if 'pass' in LINE:
                            if  'option="hidden"' in LINE:
                                try:
                                    CHANGEME=LINE.replace(' option="hidden"', '') 
                                    f = open(os.path.join(root, f), mode='w')
                                    f.write(str(FILE).replace(LINE,CHANGEME))
                                    f.close()
                                except:
                                    pass
        dialog.ok(String(30223), String(30224)) 
#---------------------------------------------------------------------------------------------------
# Option to upload a log
def Upload_Log(): 
    if ADDON.getSetting('email')=='':
        dialog = xbmcgui.Dialog()
        dialog.ok(String(30225), String(30226))
        ADDON.openSettings()
    xbmc.executebuiltin('RunScript(special://home/addons/'+AddonID+'/uploadLog.py)')
#---------------------------------------------------------------------------------------------------
# Simple function to force refresh the repo's and addons folder
def Update_Repo():
    Refresh(['addons','repos'])  
    xbmcgui.Dialog().ok(String(30166), String(30227))
#---------------------------------------------------------------------------------------------------
# Grab system info
def URL_Params():
    try:
        wifimac = Get_Mac('wifi').strip()
    except:
        wifimac = 'Unknown'
    try:
        ethmac  = Get_Mac('eth0').strip()
    except:
        ethmac  = 'Unknown'
    try:
        cpu     = CPU_Check().strip()
    except:
        cpu     = 'Unknown'
    try:
        build   = Build_Info().strip()
    except:
        build   = 'Unknown'

    if ethmac == 'Unknown' and wifimac != 'Unknown':
        ethmac = wifimac
    if ethmac != 'Unknown' and wifimac == 'Unknown':
        wifimac = ethmac

    if ethmac != 'Unknown' and wifimac != 'Unknown':
        return (wifimac+'&'+cpu+'&'+build+'&'+ethmac).replace(' ','%20')
        dolog('### maintenance: '+(wifimac+'&'+cpu+'&'+build+'&'+ethmac).replace(' ','%20'))
    else:
        return 'Unknown'
        dolog("### BUILD:"+build)
#-----------------------------------------------------------------------------------------------------------------
# Wipe known cache locations
def Wipe_Cache():
    PROFILE_ADDON_DATA = os.path.join(xbmc.translatePath(os.path.join('special://profile','addon_data')))

    cachelist = [
        (PROFILE_ADDON_DATA),
        (ADDON_DATA),
        (os.path.join(HOME,'cache')),
        (os.path.join(HOME,'temp')),
        (os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')),
        (os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')),
        (os.path.join(ADDON_DATA,'script.module.simple.downloader')),
        (os.path.join(xbmc.translatePath(os.path.join('special://profile','addon_data','script.module.simple.downloader')))),
        (os.path.join(ADDON_DATA,'plugin.video.itv','Images')),
        (os.path.join(xbmc.translatePath(os.path.join('special://profile','addon_data','plugin.video.itv','Images'))))]

    for item in cachelist:
        if os.path.exists(item) and item != ADDON_DATA and item != PROFILE_ADDON_DATA:
            for root, dirs, files in os.walk(item):
                file_count = 0
                file_count += len(files)
                if file_count > 0:
                    for f in files:
                        try:
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                            dolog("### Successfully cleared %s files from %s" % (str(file_count), os.path.join(item,d)))
                        except:
                            dolog("### Failed to wipe cache in: %s " % os.path.join(item,d))
        else:
            for root, dirs, files in os.walk(item):
                for d in dirs:
                    if 'CACHE' in d.upper():
                        try:
                            shutil.rmtree(os.path.join(root, d))
                            dolog("### Successfully wiped %s" % os.path.join(item,d))
                        except:
                            dolog("### Failed to wipe cache in: %s" % os.path.join(item,d))

# Genesis cache - held in database file
    try:
        genesisCache = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.genesis'), 'cache.db')
        dbcon = database.connect(genesisCache)
        dbcur = dbcon.cursor()
        dbcur.execute("DROP TABLE IF EXISTS rel_list")
        dbcur.execute("VACUUM")
        dbcon.commit()
        dbcur.execute("DROP TABLE IF EXISTS rel_lib")
        dbcur.execute("VACUUM")
        dbcon.commit()
    except:
        pass
#-----------------------------------------------------------------------------------------------------------------
# Function to completely wipe kodi
def Wipe_Kodi():
    stop = 0
    if dialog.yesno(String(30137), String(30228), yeslabel=String(30229),nolabel=String(30230)):
        if not Fresh_Install():
# Check Confluence is running before doing a wipe
            if skin!="skin.confluence" and skin!="skin.estuary":
                dialog.ok(String(30231),String(30232))
                xbmc.executebuiltin("ActivateWindow(appearancesettings,return)")
                return
            else:
# Give the option to do a full backup before wiping
                if dialog.yesno(String(30233), String(30224)):
                    if USB == '':
                        dialog.ok(String(30225),String(30226))
                        ADDON.openSettings(sys.argv[0])
                        if ADDON.getSetting('zip') == '' or not os.path.exists(ADDON.getSetting('zip')):
                            stop = 1
                            return
                    if not stop:
                        CBPATH       = ADDON.getSetting('zip')
                        mybackuppath = os.path.join(CBPATH,'My_Builds')
                        if not os.path.exists(mybackuppath):
                            os.makedirs(mybackuppath)
                        vq = Keyboard(String(30227))
                        if ( not vq ): return False, 0
                        title = urllib.quote_plus(vq)
                        backup_zip = xbmc.translatePath(os.path.join(mybackuppath,title+'.zip'))
                        exclude_dirs_full =  ['plugin.program.nan.maintenance','plugin.program.tbs']
                        exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf','.gitignore']
                        message_header = String(30228)
                        Archive_Tree(sourcefile=HOME, destfile=backup_zip, exclude_dirs=exclude_dirs_full, exclude_files=exclude_files_full,message_header=message_header)
                if not stop:
                    keeprepos = dialog.yesno(String(30229),String(30240), yeslabel=String(30241), nolabel=String(30242))
                    EXCLUDES  = ['firstrun','plugin.program.tbs','plugin.program.totalinstaller','addons','addon_data','userdata','sources.xml','favourites.xml']
                    Wipe_Home(EXCLUDES)
                    Force_Close()
#-----------------------------------------------------------------------------------------------------------------
# For loop to wipe files in special://home but leave ones in EXCLUDES untouched
def Wipe_Home(excludefiles):
    ow_path       = xbmc.translatePath('special://home/addons/script.openwindow')
    requests_path = xbmc.translatePath('special://home/addons/script.module.requests')
    resolver_path = xbmc.translatePath('special://home/addons/script.module.urlresolver')
    koding_path   = xbmc.translatePath('special://home/addons/script.module.python.aio')
    Delete_Folders(filepath=HOME, ignore=[ow_path,requests_path,resolver_path,koding_path])
#-----------------------------------------------------------------------------------------------------------------
# Report back with the version of Kodi installed
def XBMC_Version(url):
    xbmc_version        = xbmc.getInfoLabel("System.BuildVersion")
    version, compiled   = xbmc_version.split(' ')
    version             = version.strip()
    compiled            = compiled.strip()
    kodi_type           = Running_App() 
    dialog.ok(String(30243), String(30244) % kodi_type, String(30245) % compiled, String(30246) % version)
#-----------------------------------------------------------------------------------------------------------------
# Update a social share
def Update_Share(fullpath):
    urlparams = URL_Params()
    if urlparams != 'Unknown':
# Grab contents of the config file
        try:
            cfgfile=open(os.path.join(fullpath,'folder.cfg'),'r')
            cfg = cfgfile.read()
            cfg = cfg.replace('\r','').replace('\n','').replace('\t','')
            cfgfile.close()
        except:
            cfg=''

# Grab contents of the favourites.xml
        if os.path.exists(os.path.join(fullpath,'favourites.xml')):
            xmlfile  = open(os.path.join(fullpath,'favourites.xml'),'r')
            xml = xmlfile.read()
            xml = xml.replace(xbmc.translatePath('special://home'),'special://home/').replace(urllib.quote(xbmc.translatePath('special://home').encode("utf-8")),'special://home/').replace('\r','').replace('\n','').replace('\t','')
            xmlfile.close()
        else:
            xml="not a SF"

# Grab the clean part of the folder name to send
        itemname  = fullpath.split('/')
        last_item = len(itemname)-1
        fullpath  = os.path.join(itemname[last_item-1], itemname[last_item])
        dolog('### Clean Full Path: %s' % fullpath)

# Attempt to send the share to system
        try:
            sendfaves = Open_URL(post_type='post',url='http://tlbb.me/boxer/share_box_live.php?x=%s&z=gs&k=%s&c=%s&p=%s' % (encryptme('e',urlparams), encryptme('e',xml), encryptme('e',cfg), encryptme('e',fullpath)))
            dolog('http://tlbb.me/boxer/share_box_live.php?x=%s&z=gs&k=%s&c=%s&p=%s' % (encryptme('e',urlparams), encryptme('e',xml), encryptme('e',cfg), encryptme('e',fullpath)))
            if 'success' in sendfaves:
                itemname  = itemname[last_item]
                dialog.ok(String(30251), String30252(30252) % fullpath.split('/')[1])
                return True
            else:
                dialog.ok(String(30253), String(30254))
                return False
        except:
            dialog.ok(String(30253), String(30256))
            return False
    else:
        dialog.ok(String(30084), String(30257))
#-----------------------------------------------------------------------------------------------------------------
# Upload social share
def Upload_Share():
    userid         = ADDON.getSetting('userid')
    choice         = 0
    master         = ADDON.getSetting('master')
    master_share   = 0
    urlparams      = URL_Params()
    item           = sys.listitem.getLabel()
    item           = item.replace('[COLOR ]','').replace('[/COLOR]','')
    path           = xbmc.getInfoLabel('ListItem.FolderPath')
    path           = urllib.unquote(path)

    if master == 'true':
        master_share = 1

    if urlparams != 'Unknown':
        dolog('### ORIG PATH: %s' % path)
        dolog('### UNQUOTED PATH: %s' % path)
        try:
            scrap,fullpath = path.split('path=')
            fullpath       = xbmc.translatePath(fullpath)
            dolog('### FULL PATH ORIG: %s' % fullpath)
        except:
            fullpath = "not a SF"
        dolog('### FULL PATH FINAL: %s' % fullpath)
        
        if fullpath != "not a SF":
            localcheck = md5_check(os.path.join(fullpath,'favourites.xml'))
            mylistpath = urllib.quote(fullpath.split("HOME_",1)[1], safe='')
            dolog('### md5: '+localcheck)
            dolog('clean path: '+mylistpath)
            DB_Open(db_social)
            cur.execute("SELECT COUNT(*) from shares WHERE path = ?", [mylistpath])
            data = cur.fetchone()[0]
            if data:
                dolog('### Updating Share in db: %s' % mylistpath)
                cur.execute("UPDATE shares SET stamp = ? WHERE path = ?", [localcheck, mylistpath])
            else:
                dolog('### Adding Share to db: %s' % mylistpath)
                cur.execute("INSERT INTO shares (path, stamp) VALUES (?, ?)", [mylistpath, localcheck])
            con.commit()
            cur.close()
            con.close()
        else:
            dialog.ok(String(30258) % item.capitalize(), String(30259))


        try:
            scrap,newpath  = path.split('Super Favourites'+os.sep)
        except:
            newpath  = "not a SF"
            newpath = newpath.replace('\\','/')

        if os.path.exists(os.path.join(fullpath,'favourites.xml')):
            xmlfile  = Text_File(os.path.join(fullpath,'favourites.xml'),'r')
            xml = xml.replace(xbmc.translatePath('special://home'),'special://home/').replace(urllib.quote(xbmc.translatePath('special://home').encode("utf-8")),'special://home/').replace('\r','').replace('\n','').replace('\t','')
        else:
            xml="not a SF"
            
        try:
            cfgfile=open(os.path.join(fullpath,'folder.cfg'),'r')
            cfg = cfgfile.read()
            cfg = cfg.replace('\r','').replace('\n','').replace('\t','')
            cfgfile.close()
        except:
            cfg=''


        try:
            cfgfile=open(os.path.join(fullpath,'folder.cfg'),'r')
            cfg_raw = cfgfile.read().splitlines()
            cfgfile.close()
        except:
            cfg_raw = ''

        dolog('### RAW CONFIG: %s'%cfg_raw)
        SF_fanart = encryptme('e','None')
        for line in cfg_raw:
            if line.startswith('FANART='):
                SF_fanart = line.replace('FANART=','').replace('\n','').replace('\t','').replace('\r','')
                SF_fanart = encryptme('e',SF_fanart)
        dolog('### SF Fanart: %s' % SF_fanart)

        try:
            pluginname=xbmc.getInfoLabel('Container.PluginName')
            dolog("### plugin name: %s" % str(pluginname))
        except:
            pluginname='none'

        quit = 0
        if pluginname == 'plugin.program.super.favourites':
# Enable once we have private share options
#        choice = dialog.select('Choose Share Type',['Share publicly','Add to my private share'])
            if xml == "not a SF" or newpath  == "not a SF":
                dialog.ok(String(30260), String(30261))
                quit = 1
            elif quit != 1:
                try:
                    if userid == '':
                        userid = encryptme('e','None')
                    sendfaves = Open_URL('http://tlbb.me/boxer/share_box_new.php?x=%s&z=gs&k=%s&c=%s&p=%s&m=%s&i=%s&f=%s' % (encryptme('e',urlparams), encryptme('e',xml), encryptme('e',cfg), encryptme('e',newpath), master_share, userid, SF_fanart))
                    if 'success' in sendfaves:
                        dialog.ok(String(30262), String(30263) % item)
                    else:
                        dialog.ok(String(30258) % item.capitalize(), String(30259))
                except:
                    dialog.ok(String(30258) % item.capitalize(), String(30256))
        if pluginname != 'plugin.program.super.favourites' and quit != 1:
            xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.super.favourites/capture.py)')
    else:
        dialog.ok(String(30084), String(30085))
#-----------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":

# Grab a list of the global values sent through to sys.argv[2]
    mode = None
    url  = ''
    icon = 'DefaultFolder.png'
    params = dict(urlparse.parse_qsl(sys.argv[2].replace('?', '')))
# Convert each item found into a global variable
    for item in params.items():
        try:
            exec(item[0]+'="%s"'%item[1])
        except:
            pass
            
# If if the mode found in section above is in our custom master_modes dictionary
    if mode in master_modes:
        try:
            eval(master_modes[mode])
        except:
            dialog.ok('MODE EXISTS BUT ERROR','You have a custom mode setup for this in your dictionary but there is an error in the code.')
            Text_Box('ERROR IN CODE','[COLOR=dodgerblue]Mode: [/COLOR]%s\n[COLOR=dodgerblue]Function: [/COLOR]%s\n\n[COLOR=gold]ERROR: [/COLOR]\n%s'%(mode,master_modes[mode],Last_Error()))
            dolog(Last_Error())
# Otherwise we try to execute (eval) that mode, so it could be a function name or even a standalone command
    elif mode != None:
        try:
            eval(mode)
        except:
            dialog.ok('ERROR IN CODE','The mode you tried to call does not exist in your custom dictionary AND it is not a valid function. Please check your syntax and try again.')
            Text_Box('ERROR IN CODE','[COLOR=dodgerblue]Function: [/COLOR]%s\n\n[COLOR=gold]ERROR: [/COLOR]\n%s'%(mode,Last_Error()))
            dolog(Last_Error())
# Finally, if no mode has been picked up it means we're at root level so load the relevant function for your main menu
    elif mode == None:
        Categories()

    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    

if not os.path.exists(TBSDATA):
    os.makedirs(TBSDATA)

if not os.path.exists(MEDIA):
    os.makedirs(MEDIA)

if not os.path.exists(db_social):
    DB_Open(db_social)
    cur.execute('create table shares(path TEXT, stamp TEXT);')
    con.commit()
    cur.execute('create table friends(id INTEGER, name TEXT, friendgroup TEXT, PRIMARY KEY(id));')
    con.commit()
    cur.execute('create table inbox(id INTEGER, fiendid INTEGER, message TEXT, read TEXT, PRIMARY KEY(id));')
    con.commit()
    cur.execute('create table sent(id INTEGER, fiendid INTEGER, message TEXT, read TEXT, PRIMARY KEY(id));')
    con.commit()
    cur.close()
    con.close()