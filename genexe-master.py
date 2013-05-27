#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import logging
import logging.handlers


def getConf() :
	
	global 

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
		script_py = os.path.basename(sys.argv[1])
		script_nom = os.path.splitext(script_py)[0]
		if sys.platform == "win32" : executable = script_nom + ".exe"
		else : executable = script_nom + ".run"
		
	except ConfigParser.Error, e :
		log.critical(u"Error in configuration file ({})".format(e))
		quit(1)








def quit(code = 0) :
	log.debug("\\\\ End in {} with code {} ".format(os.path.abspath(os.curdir), code))
	sys.exit(code)


######################################################################
# Main
######################################################################

if __name__ == "__main__":
	os.system("cls")

	# Variables 
	g_version="1.0.0"
	g_maintainer = "p.audebert@astellia.com"
	if "--debug" in sys.argv : g_Debug = True
	else : g_Debug = False
	g_path_complete = os.path.abspath(sys.argv[0])
	g_exe = os.path.basename(g_path_complete)
	g_path = os.path.dirname(g_path_complete)
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
	
	if "--all" in sys.argv : sys.argv[1:] = ["--lin_x86", "--lin_x64", "--win_x86", "--win_x64"]
	
	# Linux 32bit
	if "--lin_x86" in sys.argv :
		if lin_x86.active :
			
			# On lance la VM si besoin
			if lin_x86.type == "virtualbox" : os.system("\"C:\Program Files\Oracle\VirtualBox\VBoxManage\" startvm \"{}\"".format(lin_x86.nomvm))
			
			# On attend que la machine de compilation soit up
			if sys.platform == "win32" : cmd = "ping /n 1 " + lin_x86.ip
			else : cmd = "ping -c1 " + lin_x86.ip
			ping = False
			while not ping :
				ping = commands.command(
				
			
			
			
			
		else :
			log.critical("Configuration invalide pour Linux x86")
	
	# Linux 64bit
	if "--lin_x64" in sys.argv :
	
	# Windows 32bit
	if "--win_x86" in sys.argv :

	# Windows 64bit
	if "--win_x64" in sys.argv :

	# Fin
	quit(0)
