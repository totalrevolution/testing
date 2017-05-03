# -*- coding: utf-8 -*-

# plugin.program.tbs
# Total Revolution Maintenance (c) by whufclee (info@totalrevolution.tv)

# Total Revolution Maintenance is licensed under a
# Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.

# You should have received a copy of the license along with this
# work. If not, see http://creativecommons.org/licenses/by-nc-nd/4.0.

# IMPORTANT: If you choose to use the special noobsandnerds features which hook into their server
# please make sure you give approptiate credit in your add-on description (noobsandnerds.com)
# 
# Please make sure you've read and understood the license, this code can NOT be used commercially
# and it can NOT be modified and redistributed. Thank you.

import koding
import xbmc
import xbmcgui
import xbmcaddon
import shutil

try:
    AddonID = xbmcaddon.Addon().getAddonInfo('id')
except:
    AddonID = koding.Caller()
ADDON       =  xbmcaddon.Addon(id=AddonID)
   
def Wipe_Settings():
    path = xbmc.translatePath('special://profile/addon_data/'+AddonID)
    shutil.rmtree(path)   
    xbmcgui.Dialog().ok('Add-on Successfully Reset', 'Your add-on has now been reset to defaults. If you previously had login information entered in the settings don\'t forget to add the details back again.')


if __name__ == '__main__':
    koding.Busy_Dialog()
    Wipe_Settings()
    koding.Busy_Dialog(False)
    ADDON.openSettings()