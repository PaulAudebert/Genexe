#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, shutil
import urllib
import tarfile, bz2


## Variables
pyinstaller_rep = ".pyinstaller-1.5.1"
pyinstaller_fic = "pyinstaller-1.5.1.tar.bz2"
pyinstaller_url = "https://github.com/downloads/pyinstaller/pyinstaller/" + pyinstaller_fic
script_py = sys.argv[1]
script_nom = os.path.splitext(script_py)[0]
if sys.platform == "win32" : executable = script_nom + ".exe"
else : executable = script_nom + ".run"


## Début
print(u" Téléchargement de Pyinstaller (si besoin) ".center(80,'#'))
if not os.path.isfile('.' + pyinstaller_fic) :
	urllib.urlretrieve(pyinstaller_url, '.' + pyinstaller_fic)
print(u"ok.\n")

print(u" Extraction de Pyinstaller (si besoin) ".center(80,'#'))
if not os.path.isdir(pyinstaller_rep) :
	with tarfile.open('.' + pyinstaller_fic,'r:bz2') as archive :
		for fichier in archive : archive.extract(fichier)
	shutil.move(pyinstaller_rep[1:], pyinstaller_rep)
print(u"ok.\n")

print(u" (Re)génération de l'executable standalone ".center(80,'#'))
os.chdir(pyinstaller_rep)
os.system(u"python pyinstaller.py -F -p ../biblio -p ~/Dropbox/Public/Git/Debogue ../" + script_py)
os.chdir(os.path.pardir)
source = os.path.join(os.path.curdir, pyinstaller_rep, script_nom, "dist", executable)
destination = os.path.curdir
if sys.platform.startswith("linux") : shutil.move(os.path.splitext(source)[0], source)
shutil.copy(source, destination)
print(u"ok.\n")

## Fin
