import sys
import koding
import os
import xbmc
import xbmcgui

from koding import Addon_Setting, Default_Setting, String, Text_File

sys.argv[1]     = sys.argv[1].replace("'",'')
redirects       = xbmc.translatePath('special://home/userdata/addon_data/plugin.program.tbs/redirects')
skin_shortcuts  = xbmc.translatePath('special://profile/addon_data/script.skinshortcuts')
current_skin    = koding.System('currentskin')
dialog          = xbmcgui.Dialog()
sfname          = sys.argv[1].upper()
sfname          = 'HOME_'+sfname

if os.path.exists(xbmc.translatePath('special://home/userdata/addon_data/script.trtv/skip.txt')):
    tvgskip = 1
else:
    tvgskip = 0
#----------------------------------------------------------------
def Clear_Providers():
    counter = 1
    while counter != 11:
        try:
            koding.Addon_Setting(setting='offset%s'%counter, value='0', addon_id='script.trtv')
            koding.Addon_Setting(setting='xmlpath%s.url'%counter, value='', addon_id='script.trtv')
            koding.Addon_Setting(setting='xmlpath%s.type'%counter, value='None', addon_id='script.trtv')
            koding.Addon_Setting(setting='country%s'%counter, value='United Kingdom', addon_id='script.trtv')
            koding.Addon_Setting(setting='usecountry%s'%counter, value='false', addon_id='script.trtv')
            counter += 1
        except:
            break
#----------------------------------------------------------------
def Configure_Menus(menutype='HOME_'):
    shortcut_file = {String(30061):'x606.DATA.xml', String(30077):'x303.DATA.xml', String(30062):'x404.DATA.xml', String(30063):'x505.DATA.xml', String(30064):'x8.DATA.xml', String(30065):'x12.DATA.xml',
    String(30066):'x10.DATA.xml', String(30067):'x3.DATA.xml', String(30068):'x1.DATA.xml', String(30069):'x2.DATA.xml', String(30070):'x202.DATA.xml', String(30071):'x.7.DATA.xml', String(30072):'x11.DATA.xml',
    String(30073):'x4.DATA.xml', String(30074):'x6.DATA.xml', String(30075):'x13.DATA.xml'}

    master_list = [String(30061),String(30077),String(30062),String(30063),String(30064),String(30065),String(30066),String(30067),
    String(30068),String(30069),String(30070),String(30071),String(30072),String(30073),String(30074),String(30075)]

    choice = dialog.select(String(30294),sorted(master_list))
    if choice >= 0:
        menu = sorted(master_list)[choice]
        new_list = [String(30295)%menu,String(30296)%menu,String(30297),String(30298),String(30299)]
        choice = dialog.select(String(30303),new_list)
        if choice >= 0:

            my_setting       = menutype+menu.upper().replace(' ','_')
            dialog_plus_user = os.path.join(redirects,'%s_DIALOG_PLUS_USER' % my_setting)
            dialog_user      = os.path.join(redirects,'%s_DIALOG_USER' % my_setting)
            exec_user        = os.path.join(redirects,'%s_EXEC_USER' % my_setting)
            sf_user          = os.path.join(redirects,'%s_SF_USER' % my_setting)

            delete_array = [dialog_plus_user, dialog_user, exec_user, sf_user]

            if choice == 0:
                my_shortcut = my_setting+'_SF'
                if menutype == 'HOME_':
                    Addon_Setting(setting=my_setting, value='super_faves')
                    for item in delete_array:
                        if not my_shortcut in item and os.path.exists(item):
                            os.remove(item)
                if not os.path.exists(sf_user):
                    Text_File(sf_user,'w','')
                else:
                    dialog.ok(String(30308),String(30309))
                    return

            if choice == 1:
                my_shortcut = my_setting+'_DIALOG_PLUS_USER'
                if menutype == 'HOME_':
                    Addon_Setting(setting=my_setting, value='dialog_plus_user')
                    for item in delete_array:
                        if not my_shortcut in item and os.path.exists(item):
                            os.remove(item)
                if not os.path.exists(dialog_plus_user):
                    Text_File(dialog_plus_user,'w','')
                else:
                    dialog.ok(String(30308),String(30309))
                    return

            if choice == 2:
                my_shortcut = my_setting+'_DIALOG_USER'
                if menutype == 'HOME_':
                    Addon_Setting(setting=my_setting, value='dialog_user')
                    for item in delete_array:
                        if not my_shortcut in item and os.path.exists(item):
                            os.remove(item)
                if not os.path.exists(dialog_user):
                    Text_File(dialog_user,'w','')
                else:
                    dialog.ok(String(30308),String(30309))
                    return

            if choice == 3:
                my_shortcut = my_setting+'_EXEC_USER'
                if menutype == 'HOME_':
                    Addon_Setting(setting=my_setting, value='executable_user')
                    for item in delete_array:
                        if not my_shortcut in item and os.path.exists(item):
                            os.remove(item)
                if not os.path.exists(exec_user):
                    my_code = koding.Keyboard('Enter the command you want to run')
                    if not my_code:
                        return
                    Text_File(exec_user,'w',my_code)
                else:
                    dialog.ok(String(30308),String(30309))
                    return
            
            if choice == 4:
                if menutype == 'HOME_':
                    Default_Setting(setting=my_setting, reset=True)
                else:
                    try:
                        os.remove(os.path.join(skin_shortcuts,shortcut_file[menu]))
                        os.remove(os.path.join(skin_shortcuts,current_skin+'.hash'))
                    except:
                        xbmc.log('FAILED TO DEFAULT SKIN SETTINGS: %s'%koding.Last_Error())

                    for item in delete_array:
                        if os.path.exists(item):
                            os.remove(item)
                    koding.Refresh('skin')
# If it's a submenu we try and add to the skinshortcuts and give it a name
            if menutype == 'SUBMENU_' and choice != 4:
                sub_name = koding.Keyboard('Enter a name for this sub-menu item')
                if not sub_name:
                    return
                Edit_Sub_Menu(shortcut=my_shortcut, sub_name=sub_name, shortcut_file=shortcut_file[menu])
#----------------------------------------------------------------
def Edit_Sub_Menu(shortcut, sub_name, shortcut_file):
    shortcut_path   = os.path.join(skin_shortcuts, shortcut_file)
    if os.path.exists(shortcut_path):
        contents        = Text_File(shortcut_path, 'r')
        new_contents    = '\n\t<shortcut>\n\t\t<defaultID />\n\t\t<label>%s</label>\n\t\t<label2>Video Add-On</label2>\n\t\t<icon>DefaultAddonProgram.png</icon>\n\t\t<action>RunScript(special://home/addons/plugin.program.tbs/home.py,%s)</action>\n\t</shortcut>'%(sub_name,shortcut)
        replace_file    = contents.replace(r'</shortcuts>','%s\n</shortcuts>'%new_contents)
        Text_File(shortcut_path,'w',replace_file)
    else:
        contents = "<?xml version='1.0' encoding='UTF-8'?>\n<shortcuts>\n\t<shortcut>\n\t\t<defaultID />\n\t\t<label>%s</label>\n\t\t<label2>Video Add-On</label2>\n\t\t<icon>DefaultAddonProgram.png</icon>\n\t\t<action>RunScript(special://home/addons/plugin.program.tbs/home.py,%s)</action>\n\t</shortcut>\n</shortcuts>"%(sub_name,shortcut)
        Text_File(shortcut_path,'w',contents)
    try:
        os.remove(os.path.join(skin_shortcuts,current_skin+'.hash'))
    except:
        xbmc.log('FAILED TO REMOVE SKIN HASH')
    koding.Refresh('skin')
#----------------------------------------------------------------
def Folder_Check():
    directories = 0
    folderpath = xbmc.translatePath(os.path.join('special://profile/addon_data/plugin.program.super.favourites/Super Favourites/',sfname))
    for dirs in os.walk(folderpath):
        directories += len(dirs[1])
    return directories
#----------------------------------------------------------------
if __name__ == "__main__":
    mode = 'std'
    if sys.argv[1]=='listings':
        mode = 'listings'

# Standard social sharing style menus
    if mode == 'std':
        folders = Folder_Check()
        if sys.argv[1] == "live_tv" and folders == 0 and not tvgskip:
            choice = dialog.select(sys.argv[1].replace('_',' ').upper()+' Menu',['[COLOR=gold]Add[/COLOR] to Live TV','[COLOR=gold]Add / Remove[/COLOR] Sub-menus','','[COLOR=lightsteelblue][TUTORIAL][/COLOR] Add/Remove Live TV Content'])
            if choice == 0:
                xbmc.executebuiltin('ActivateWindow(programs,"plugin://plugin.program.tbs/?description&mode=search_content_main&url=live_tv",return)')
            if choice == 1:
                xbmc.executebuiltin('ActivateWindow(programs,"plugin://plugin.program.tbs/?description&mode=search_content_main&url=live_tv_submenu",return)')
            if choice == 2:
                xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.tbs/epg.py,'+sys.argv[1]+')')
            if choice == 3:
                 koding.Play_Video('-taD-9lqjaw')

        elif sys.argv[1] == "live_tv" and folders > 0 and not tvgskip:
            choice = dialog.select(sys.argv[1].replace('_',' ').upper()+' Menu',['[COLOR=gold]Add[/COLOR] to Live TV','[COLOR=gold]Remove[/COLOR] from Live TV','[COLOR=gold]Add / Remove[/COLOR] Sub-menus','[COLOR=gold]Share[/COLOR] Live TV Item','','[COLOR=lightsteelblue][TUTORIAL][/COLOR] Add/Remove Live TV Content'])
            if choice == 0:
                xbmc.executebuiltin('ActivateWindow(programs,"plugin://plugin.program.tbs/?description&mode=search_content_main&url=live_tv",return)')
            if choice == 1:
                xbmc.executebuiltin('ActivateWindow(programs,"plugin://plugin.program.tbs/?description&mode=search_content_main&url=from_the_live_tv_menu",return)')
            if choice == 2:
                xbmc.executebuiltin('ActivateWindow(programs,"plugin://plugin.program.tbs/?description&mode=search_content_main&url=live_tv_submenu",return)')
            if choice == 3:
                xbmc.executebuiltin('ActivateWindow(programs,"plugin://plugin.program.super.favourites/?folder=HOME_LIVE_TV",return)')
            if choice == 4:
                xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.tbs/epg.py,'+sys.argv[1]+')')
            if choice == 5:
                 koding.Play_Video('-taD-9lqjaw')

# EDIT Menu
        elif sys.argv[1] == "mainmenu":
            choice = dialog.select(String(30280),[String(30281),String(30282),String(30292),String(30300)])
            if choice >= 0:
                if choice == 0:
                    xbmc.executebuiltin('ActivateWindow(programs,"plugin://plugin.program.tbs/?description&mode=main_menu_install&url=add",return)')
                    xbmc.executebuiltin('Container.Refresh')

                if choice == 1:
                    xbmc.executebuiltin('ActivateWindow(programs,"plugin://plugin.program.tbs/?description&mode=main_menu_install&url=remove",return)')
                    xbmc.executebuiltin('Container.Refresh')

                if choice == 2:
                    Configure_Menus()

                if choice == 3:
                    Configure_Menus('SUBMENU_')

# SOCIAL SHARES - If content exists add menu for adding, removing and sharing
        elif (sys.argv[1] != "mainmenu") and (folders > 0) and (not sys.argv[1].endswith('_SF')):
            cleanname = sys.argv[1].replace('_',' ')        
            choice = dialog.select(String(30283),[String(30284)%sys.argv[1].replace('_',' '),String(30285)%sys.argv[1].replace('_',' '),String(30286),String(30287)%cleanname,'',String(30288),String(30289),String(30290)])
            if choice == 0:
                xbmc.executebuiltin('ActivateWindow(programs,"plugin://plugin.program.tbs/?description&mode=search_content_main&url='+sys.argv[1]+'",return)')
            if choice == 1:
                xbmc.executebuiltin('ActivateWindow(programs,"plugin://plugin.program.tbs/?description&mode=search_content_main&url=from_the_'+sys.argv[1]+'_menu",return)')
            if choice == 2:
                xbmc.executebuiltin('ActivateWindow(programs,"plugin://plugin.program.tbs/?description&mode=search_content_main&url='+sys.argv[1]+'_submenu",return)')
            if choice == 3:
                xbmc.executebuiltin('ActivateWindow(programs,"plugin://plugin.program.super.favourites/?folder=HOME_'+sys.argv[1].replace(' ','_').upper()+'",return)')
            if choice == 4:
                xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.tbs/epg.py,'+sys.argv[1]+')')
            if choice == 5:
                 koding.Play_Video('eDK20XkyGXE')
            if choice == 6:
                 koding.Play_Video('IkRZJgup4gk')
            if choice == 7:
               koding.Play_Video('FSOOED9v1RE')

# SOCIAL SHARES - If no content exists add menu for adding and sharing only
        elif (sys.argv[1] != "mainmenu") and (folders == 0) and (not sys.argv[1].endswith('_SF')):
            cleanname = sys.argv[1].replace('_',' ')        
            choice = dialog.select(String(30283),[String(30284)%sys.argv[1].replace('_',' '),String(30291),'',String(30288),String(30289),String(30290)])
            if choice == 0:
                xbmc.executebuiltin('ActivateWindow(programs,"plugin://plugin.program.tbs/?description&mode=search_content_main&url='+sys.argv[1]+'",return)')
            if choice == 1:
                xbmc.executebuiltin('ActivateWindow(programs,"plugin://plugin.program.tbs/?description&mode=search_content_main&url='+sys.argv[1]+'_submenu",return)')
            if choice == 2:
                xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.tbs/epg.py,'+sys.argv[1]+')')
            if choice == 3:
                 koding.Play_Video('eDK20XkyGXE')
            if choice == 4:
                 koding.Play_Video('IkRZJgup4gk')
            if choice == 5:
               koding.Play_Video('FSOOED9v1RE')
        
        else:
            xbmc.executebuiltin('ActivateWindow(programs,"plugin://plugin.program.super.favourites/?folder=HOME_'+sys.argv[1].replace(' ','_').upper()+'",return)')

# If we're opening the EPG Tools menu
    elif mode=='listings':

        custom_url = koding.Addon_Setting(setting='custom.url',addon_id='script.trtv')
        if 'http' in custom_url:
            countries = ['Afghanistan', 'Albania', 'Algeria', 'Angola', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan',
            'Bahamas', 'Belarus', 'Belgium', 'Bolivia', 'Bosnia', 'Brazil', 'Bulgaria', 'Cambodia', 'Cameroon', 'Canada', 'Chile',
            'China', 'Colombia', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 'Denmark', 'Dominican Republic', 'Ecuador',
            'Egypt', 'El Salvador', 'Estonia', 'Ethiopia', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece',
            'Guatemala', 'Guinea', 'Haiti', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland',
            'Israel', 'Italy', 'Ivory Coast', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kosovo', 'Kuwait', 'Kyrgyzstan',
            'Laos', 'Latvia', 'Lebanon', 'Liberia', 'Libya', 'Liechstenstein', 'Lithuania', 'Luxembourg', 'Macedonia', 'Madagascar',
            'Malawi', 'Malaysia', 'Mali', 'Malta', 'Mauritius', 'Mexico', 'Moldova', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique',
            'Myanmar', 'Namibia', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Norway', 'Oman', 'Pakistan',
            'Palestine', 'Panama', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Romania', 'Russia',
            'Rwanda', 'Saudi Arabia', 'Senegal', 'Serbia', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Somalia', 'South Africa',
            'South Korea', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria', 'Taiwan',
            'Tajikistan', 'Tanzania', 'Thailand', 'Togo', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Uganda', 'Ukraine',
            'United Arab Emireates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia',
            'Zimbabwe']

            # content    = koding.Open_URL('https://friendpaste.com/5Xu6ETfd0vjj8lvpvQ390b/raw')
            content    = koding.Open_URL(custom_url)
            raw_list   = koding.Find_In_Text(content,'name="','\n\n')
            final_list = []
            my_list    = []
            Clear_Providers()
            xbmc.executebuiltin('RunScript(special://home/addons/script.trtv/deleteDB.py,wipeEPG)')
            for item in raw_list:
                name, url, country, offset = item.split('\n')
                name    = name.replace('"','').strip()
                url     = url.replace('url="','').replace('"','').strip()
                country = country.replace('country="','').replace('"','').strip()
                offset  = offset.replace('offset="','').replace('"','').strip()
                final_list.append('[COLOR=dodgerblue]%s:[/COLOR] %s' % (country, name))
                my_list.append([name,url,country,offset])


# Select main provider
            dialog.ok(String(30264).upper(),String(30265))
            choice  = dialog.select(String(30264),final_list)
            counter = 1
            if choice >= 0:
                koding.Addon_Setting(setting='offset%s'%counter, value=my_list[choice][3], addon_id='script.trtv')
                koding.Addon_Setting(setting='xmlpath%s.url'%counter, value=my_list[choice][1], addon_id='script.trtv')
                koding.Addon_Setting(setting='xmlpath%s.type'%counter, value='URL', addon_id='script.trtv')
                if my_list[choice][2] in countries:
                    koding.Addon_Setting(setting='country%s'%counter, value=my_list[choice][2], addon_id='script.trtv')
                    koding.Addon_Setting(setting='usecountry%s'%counter, value='true', addon_id='script.trtv')
                else:
                    koding.Addon_Setting(setting='usecountry%s'%counter, value='false', addon_id='script.trtv')
                del final_list[choice]
                del my_list[choice]
                counter += 1

# If still items in list offer to add more providers
                my_choice = 1
                while my_choice:
                    if len(final_list) > 1:
                        my_choice  = dialog.yesno(String(30264).upper(),String(30266))
                        if not my_choice:
                            break
                        choice     = dialog.select(String(30264),final_list)
                        koding.Addon_Setting(setting='offset%s'%counter, value=my_list[choice][3], addon_id='script.trtv')
                        koding.Addon_Setting(setting='xmlpath%s.url'%counter, value=my_list[choice][1], addon_id='script.trtv')
                        koding.Addon_Setting(setting='xmlpath%s.type'%counter, value='URL', addon_id='script.trtv')
                        if my_list[choice][2] in countries:
                            koding.Addon_Setting(setting='country%s'%counter, value=my_list[choice][2], addon_id='script.trtv')
                            koding.Addon_Setting(setting='usecountry%s'%counter, value='true', addon_id='script.trtv')
                        else:
                            koding.Addon_Setting(setting='usecountry%s'%counter, value='false', addon_id='script.trtv')
                        del final_list[choice]
                        del my_list[choice]
                        counter += 1