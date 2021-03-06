from Screens.Screen import Screen
from Components.ConfigList import ConfigListScreen, ConfigList
from Components.ActionMap import ActionMap
from Components.Sources.StaticText import StaticText
from Components.config import config, ConfigSubsection, ConfigBoolean, getConfigListEntry, ConfigSelection, ConfigYesNo, ConfigIP
from Components.Network import iNetwork
from Components.Ipkg import IpkgComponent
from enigma import eDVBDB

config.misc.installwizard = ConfigSubsection()
config.misc.installwizard.hasnetwork = ConfigBoolean(default = False)
config.misc.installwizard.ipkgloaded = ConfigBoolean(default = False)
config.misc.installwizard.channellistdownloaded = ConfigBoolean(default = False)


class InstallWizard(Screen, ConfigListScreen):

	STATE_UPDATE = 0
	STATE_CHOISE_CHANNELLIST = 1
	STATE_CHOISE_SOFTCAM = 2
	STATE_CHOISE_PICONS = 3
	STATE_CHOISE_TDT = 4
	STATE_CHOISE_EPG = 5
	STATE_CHOISE_CACHE = 6
	
	def __init__(self, session, args = None):
		Screen.__init__(self, session)

		self.index = args
		self.list = []
		ConfigListScreen.__init__(self, self.list)

		if self.index == self.STATE_UPDATE:
			config.misc.installwizard.hasnetwork.value = False
			config.misc.installwizard.ipkgloaded.value = False
			modes = {0: " "}
			self.enabled = ConfigSelection(choices = modes, default = 0)
			self.adapters = [(iNetwork.getFriendlyAdapterName(x),x) for x in iNetwork.getAdapterList()]
			is_found = False
			for x in self.adapters:
				if x[1] == 'eth0':
					if iNetwork.getAdapterAttribute(x[1], 'up'):
						self.ipConfigEntry = ConfigIP(default = iNetwork.getAdapterAttribute(x[1], "ip"))
						iNetwork.checkNetworkState(self.checkNetworkCB)
						if_found = True
					else:
						iNetwork.restartNetwork(self.checkNetworkLinkCB)
					break
			if is_found is False:
				self.createMenu()
		elif self.index == self.STATE_CHOISE_CHANNELLIST:
			self.enabled = ConfigYesNo(default = True)
			modes = {"19e": "Astra 1", "23e": "Astra 3", "19e-23e": "Astra 1 Astra 3", "19e-23e-28e": "Astra 1 Astra 2 Astra 3", "13e-19e-23e-28e": "Astra 1 Astra 2 Astra 3 Hotbird"}
			self.channellist_type = ConfigSelection(choices = modes, default = "19e")
			self.createMenu()

		elif self.index == self.STATE_CHOISE_PICONS:
			self.enabled = ConfigYesNo(default = True)
			modes = {"19e": "Astra 19e", "23e": "Astra 3", "19e-23e": "Astra 1 Astra 3", "19e-23e-28e": "Astra 1 Astra 2 Astra 3", "13e-19e-23e-28e": "Astra 1 Astra 2 Astra 3 Hotbird"}
			self.picons_type = ConfigSelection(choices = modes, default = "19e")
			self.createMenu()

		elif self.index == self.STATE_CHOISE_EPG:
			self.enabled = ConfigYesNo(default = True)
			modes = {"xmltvimport": "Xmltvimport", "crossepg": "CrossEPG"}
			self.epg_type = ConfigSelection(choices = modes, default = "xmltvimport")
			self.createMenu()
			
		elif self.index == self.STATE_CHOISE_TDT:
			self.enabled = ConfigYesNo(default = True)
			modes = {"siano": "Siano", "Volar Black": "Hauppauge"}
			self.tdt_type = ConfigSelection(choices = modes, default = "siano")
			self.createMenu()

		elif self.index == self.STATE_CHOISE_SOFTCAM:
			self.enabled = ConfigYesNo(default = True)
			modes = {"cccam": "CCcam", "oscam": "Oscam"}
			self.softcam_type = ConfigSelection(choices = modes, default = "cccam")
			self.createMenu()
			
		elif self.index == self.STATE_CHOISE_CACHE:
			self.enabled = ConfigYesNo(default = True)
			modes = {"multics": "MultiCS"}
			self.cache_type = ConfigSelection(choices = modes, default = "multics")
			self.createMenu()

	def checkNetworkCB(self, data):
		if data < 3:
			config.misc.installwizard.hasnetwork.value = True
		self.createMenu()

	def checkNetworkLinkCB(self, retval):
		if retval:
			iNetwork.checkNetworkState(self.checkNetworkCB)
		else:
			self.createMenu()

	def createMenu(self):
		try:
			test = self.index
		except:
			return
		self.list = []
		if self.index == self.STATE_UPDATE:
			if config.misc.installwizard.hasnetwork.value:
				self.list.append(getConfigListEntry(_("Your internet connection is working (ip: %s)") % (self.ipConfigEntry.getText()), self.enabled))
			else:
				self.list.append(getConfigListEntry(_("Your receiver does not have an internet connection"), self.enabled))
		elif self.index == self.STATE_CHOISE_CHANNELLIST:
			self.list.append(getConfigListEntry(_("Install channel list"), self.enabled))
			if self.enabled.value:
				self.list.append(getConfigListEntry(_("Channel list type"), self.channellist_type))

		elif self.index == self.STATE_CHOISE_PICONS:
			self.list.append(getConfigListEntry(_("Install picons"), self.enabled))
			if self.enabled.value:
				self.list.append(getConfigListEntry(_("Picons list type"), self.picons_type))
#		self["config"].list = self.list
#		self["config"].l.setList(self.list)

		elif self.index == self.STATE_CHOISE_TDT:
			self.list.append(getConfigListEntry(_("Install usb tdt "), self.enabled))
			if self.enabled.value:
				self.list.append(getConfigListEntry(_("Tdt list type"), self.tdt_type))
				
		elif self.index == self.STATE_CHOISE_EPG:
			self.list.append(getConfigListEntry(_("Install epg manager"), self.enabled))
			if self.enabled.value:
				self.list.append(getConfigListEntry(_("Epg manager type"), self.epg_type))
				
		elif self.index == self.STATE_CHOISE_SOFTCAM:
			self.list.append(getConfigListEntry(_("Install softcam"), self.enabled))
			if self.enabled.value:
				self.list.append(getConfigListEntry(_("Softcam type"), self.softcam_type))

		elif self.index == self.STATE_CHOISE_CACHE:
			self.list.append(getConfigListEntry(_("Install cache server"), self.enabled))
			if self.enabled.value:
				self.list.append(getConfigListEntry(_("Cache Server type"), self.cache_type))
				
		self["config"].list = self.list
		self["config"].l.setList(self.list)

	def keyLeft(self):
		if self.index == 0:
			return
		ConfigListScreen.keyLeft(self)
		self.createMenu()

	def keyRight(self):
		if self.index == 0:
			return
		ConfigListScreen.keyRight(self)
		self.createMenu()

	def run(self):
		if self.index == self.STATE_UPDATE:
			if config.misc.installwizard.hasnetwork.value:
				self.session.open(InstallWizardIpkgUpdater, self.index, _('Please wait (updating packages)'), IpkgComponent.CMD_UPDATE)
		elif self.index == self.STATE_CHOISE_CHANNELLIST and self.enabled.value:
			self.session.open(InstallWizardIpkgUpdater, self.index, _('Please wait (downloading channel list)'), IpkgComponent.CMD_REMOVE, {'package': 'enigma2-plugin-settings-sfteam-' + self.channellist_type.value})

		elif self.index == self.STATE_CHOISE_PICONS and self.enabled.value:
			self.session.open(InstallWizardIpkgUpdater, self.index, _('Please wait (downloading picons)'), IpkgComponent.CMD_INSTALL, {'package': 'enigma2-plugin-picons-sfteam-' + self.picons_type.value})

		elif self.index == self.STATE_CHOISE_TDT and self.enabled.value:
			self.session.open(InstallWizardIpkgUpdater, self.index, _('Please wait (downloading driver)'), IpkgComponent.CMD_INSTALL, {'package': 'enigma2-plugin-drivers-dvb-usb-' + self.tdt_type.value})

		elif self.index == self.STATE_CHOISE_EPG and self.enabled.value:
			self.session.open(InstallWizardIpkgUpdater, self.index, _('Please wait (downloading epg manager)'), IpkgComponent.CMD_INSTALL, {'package': 'enigma2-plugin-extensions-' + self.epg_type.value})
			
		elif self.index == self.STATE_CHOISE_SOFTCAM and self.enabled.value:
			self.session.open(InstallWizardIpkgUpdater, self.index, _('Please wait (downloading softcam)'), IpkgComponent.CMD_INSTALL, {'package': 'enigma2-plugin-softcams-sfteam-' + self.softcam_type.value})

		elif self.index == self.STATE_CHOISE_CACHE and self.enabled.value:
			self.session.open(InstallWizardIpkgUpdater, self.index, _('Please wait (downloading cache server)'), IpkgComponent.CMD_INSTALL, {'package': 'enigma2-plugin-cache-sfteam-' + self.cache_type.value})
		return

class InstallWizardIpkgUpdater(Screen):
	skin = """
	<screen position="c-300,c-25" size="600,50" title=" ">
		<widget source="statusbar" render="Label" position="10,5" zPosition="10" size="e-10,30" halign="center" valign="center" font="Regular;22" transparent="1" shadowColor="black" shadowOffset="-1,-1" />
	</screen>"""

	def __init__(self, session, index, info, cmd, pkg = None):
		self.skin = InstallWizardIpkgUpdater.skin
		Screen.__init__(self, session)

		self["statusbar"] = StaticText(info)

		self.pkg = pkg
		self.index = index
		self.state = 0

		self.ipkg = IpkgComponent()
		self.ipkg.addCallback(self.ipkgCallback)

		if self.index == InstallWizard.STATE_CHOISE_CHANNELLIST:
			self.ipkg.startCmd(cmd, {'package': 'enigma2-plugin-settings-*'})
		else:
			self.ipkg.startCmd(cmd, pkg)

	def ipkgCallback(self, event, param):
		if event == IpkgComponent.EVENT_DONE:
			if self.index == InstallWizard.STATE_UPDATE:
				config.misc.installwizard.ipkgloaded.value = True
			elif self.index == InstallWizard.STATE_CHOISE_CHANNELLIST:
				if self.state == 0:
					self.ipkg.startCmd(IpkgComponent.CMD_INSTALL, self.pkg)
					self.state = 1
					return
				else:
					config.misc.installwizard.channellistdownloaded.value = True
					eDVBDB.getInstance().reloadBouquets()
					eDVBDB.getInstance().reloadServicelist()
			self.close()
