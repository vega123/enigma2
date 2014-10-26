installdir = $(pkglibdir)/python/Plugins/Extensions

SUBDIRS = TuxboxPlugins CutListEditor PicturePlayer MediaScanner MediaPlayer GraphMultiEPG SocketMMI DVDBurn Modem 

if HAVE_LIBDDVD
SUBDIRS += DVDPlayer 
endif
if HAVE_ubifs
SUBDIRS += backupsfteam
endif

install_PYTHON =	\
	__init__.py
