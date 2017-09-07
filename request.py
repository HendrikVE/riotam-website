#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgi, cgitb
import os
import subprocess
import logging
	
def main():
	
	cgitb.enable()
	
	logging.basicConfig(filename = "log/log.txt", format="%(asctime)s [%(levelname)s]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)

	print "Content-Type: text/html"
	print "\n\r"

	form = cgi.FieldStorage()

	selected_modules = form.getlist("selected_modules")
	device = form.getfirst("device")
	
	argument_modules = []
	argument_modules.append("--modules")
	for module in selected_modules:
		argument_modules.append(" " + module)

	arguments = "".join(argument_modules) + " " + "--device " + device
	
	os.chdir("../riotam-backend/")
	proc = subprocess.Popen(["python", "build.py",  arguments], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	print proc.communicate()[0]
	
if __name__ == "__main__":
	main()