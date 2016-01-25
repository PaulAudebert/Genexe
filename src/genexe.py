#!/usr/bin/python
# -*- coding: utf-8 -*-

import platform, os, sys, shutil
import logging
import logging.handlers
import ConfigParser
import urllib
import zipfile, tarfile, bz2


def getConf() :
	
	global pyinstaller_url, pyinstaller_zip, pyinstaller_rep, input_file, script_nom, executable, output_file

	config = ConfigParser.RawConfigParser()
	config.read(os.path.join(g_path_base, g_conf_file))
	log.debug(u"{} {} = {}".format(g_conf_file, type(os.path.join(g_path_base, g_conf_file)), os.path.join(g_path_base, g_conf_file)))
	
	try :
		pyinstaller_url = config.get("pyinstaller", "url")
		pyinstaller_zip = os.path.basename(pyinstaller_url)
		if ".tar" in pyinstaller_zip :
			pyinstaller_rep = '.' + os.path.splitext(os.path.splitext(pyinstaller_zip)[0])[0]
		else :
			pyinstaller_rep = '.' + os.path.splitext(pyinstaller_zip)[0]
		input_file = os.path.basename(sys.argv[1])
		if not input_file.endswith(".py") : quit(1)
		
		script_nom = os.path.splitext(input_file)[0]
		
		if sys.platform == "win32" :
			executable = script_nom + ".exe"
		else :
			executable = script_nom
		
		if sys.platform == "win32" :
			if platform.architecture()[0] == "32bit" : output_file = executable
			else : output_file = script_nom + "_x64.exe"
		else :
			if platform.architecture()[0] == "32bit" : output_file = executable + ".run"
			else : output_file = script_nom + "_x64.run"
		
	except ConfigParser.Error, e :
		log.critical(u"Error in configuration file ({})".format(e))
		quit(1)


def download() :
	urllib.urlretrieve(pyinstaller_url, '.' + pyinstaller_zip)


def decompression() :
	zip_type = os.path.splitext(pyinstaller_zip)[1]
	if zip_type == ".zip" :
		log.debug(u"Archive zip")
		with zipfile.ZipFile('.' + pyinstaller_zip, 'r') as archive :
			for fichier in archive.namelist():
				log.debug("fichier {} = {}".format(type(fichier), fichier))
				data = archive.read(fichier)
				log.debug("data {} = {}".format(type(data), data[:50]))
				with open(fichier, 'wb') as f : f.write(data)
		
		# On renome le repertoire de Pyinstaller avec un '.' pour le cacher
		shutil.move(pyinstaller_rep[1:], pyinstaller_rep)
		
		return 0
		
	elif zip_type == ".bz2" :
		log.debug(u"Archive bz2")
		with tarfile.open('.' + pyinstaller_zip, 'r:bz2') as archive :
			for fichier in archive : archive.extract(fichier)
		
		# On renome le repertoire de Pyinstaller avec un '.' pour le cacher
		shutil.move(pyinstaller_rep[1:], pyinstaller_rep)
		
		return 0
		
	else :
		log.error(u"Archive non gérée")
		return 1


def quit(code = 0) :
	log.debug("\\\\ End in {} with code {} ".format(os.path.abspath(os.curdir), code))
	sys.exit(code)


######################################################################
# Main
######################################################################

if __name__ == "__main__":
	if sys.platform == "win32" : os.system("cls")
	else : os.system("clear")
	
	# Variables globales
	g_version = "1.0.0"
	g_maintainer = "paul.audebert@gmail.com"
	if "--debug" in sys.argv : g_Debug = True
	else : g_Debug = False
	g_path_complete = os.path.abspath(sys.argv[0])
	g_path_base = os.path.dirname(g_path_complete) + "\\"
	g_exe = os.path.basename(g_path_complete)
	g_conf_file = os.path.splitext(g_exe)[0] + ".conf"
	g_log_file = os.path.splitext(g_exe)[0] + ".log"
	g_log_maxsize = 20 * 1024 * 1024  # 20 Mo
	g_log_backup = 1
	
	# Log
	log = logging.getLogger()
	log.setLevel(logging.DEBUG)
	outputSdt = logging.StreamHandler()
	if g_Debug : outputSdt.setLevel(logging.DEBUG)
	else : outputSdt.setLevel(logging.INFO)
	outputSdt.setFormatter(logging.Formatter(datefmt = "%H:%M:%S", fmt = "%(asctime)s %(levelname)s : %(message)s"))
	log.addHandler(outputSdt)
	log.debug(u"DEBUG MODE")

	# Début
	#os.chdir(g_path_base)
	log.debug(u"// Load in " + os.path.abspath(os.curdir))
	print('#'*80)
	print('#' + ' '*78 + '#')
	print('#' + u"{} {}".format(os.path.splitext(g_exe)[0], g_version).center(78,' ') + '#')
	print('#' + ' '*78 + '#')
	print('#'*80)
	
	# Récupération des paramêtres
	log.info(u"Launch parametres")
	getConf()
	
	# Téléchargement & Décompression de pyinstaller
	if not os.path.isdir(pyinstaller_rep) :
		
		# Téléchargement
		if not os.path.isfile('.' + pyinstaller_zip) :
			log.info(u"Téléchargement de Pyinstaller")
			if download() : quit(1)
			log.info(u"100%")
		else :
			log.info(u"Pyinstaller déjà téléchargé")
		
		# Décompression
		log.info(u"Extraction de Pyinstaller")
		if decompression() : quit(1)
		log.info(u"100%")
		
		# Supression de l'archive
		log.info(u"Nettoyage")
		os.remove('.' + pyinstaller_zip)
		log.info(u"100%")
		
	else :
		log.info(u"Pyinstaller déjà décompressé")
	
	# Execution de Pyinstaller
	log.info(u"Génération de l'executable standalone")
	os.chdir(pyinstaller_rep)
	log.debug("Enter in " + os.path.abspath(os.curdir))
	if g_Debug : os.system("python pyinstaller.py -F ../" + input_file)
	else : os.popen("python pyinstaller.py -F ../" + input_file)
	#os.spawnl(os.P_WAIT, "python pyinstaller.py -F ../" + input_file)  # reste à tester
	os.chdir(os.path.pardir)
	log.debug("Enter in " + os.path.abspath(os.curdir))
	
	# On déplace l'executable généré juste à côté du script source
	emplacement = os.path.join(pyinstaller_rep, script_nom, "dist", executable)
	log.debug("emplacement {} = {}".format(type(emplacement), emplacement))
	try : os.remove(output_file)
	except WindowsError : pass
	os.rename(emplacement, output_file)
	log.info(u"100%")
	
	# Fin
	quit(0)