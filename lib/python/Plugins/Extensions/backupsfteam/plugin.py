from Plugins.Plugin import PluginDescriptor
from Screens.Console import Console

cmd = "/usr/lib/enigma2/python/Plugins/Extensions/Backup-sfteam-USB/backup.sh /media/usb"

def main(session, **kwargs):
    	session.open(Console,_("Backup-sfteam-USB"),[cmd])
    	
def Plugins(**kwargs):
    	return [PluginDescriptor(name="Backup-sfteam-USB", description=_("BACKUP/SFTEAM en USB Imagen Gigablue"), where = PluginDescriptor.WHERE_PLUGINMENU, icon = "pluginLogo.png", fnc=main),
            	PluginDescriptor(name="Backup-sfteam-USB", description=_("BACKUP/SFTEAM en USB Imagen Gigablue"), where = PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=main)]


