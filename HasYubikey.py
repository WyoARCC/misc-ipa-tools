#!/usr/bin/python

# HasYubiKey.py
# Jeremy Clay
# June 20, 2016

# Script that will search the server for a given user and return a list of all
# of the Yubikeys associated with their account.  If no Yubikeys have been
# assigned, an empty list will be returned.
#
# This is NOT a standalone script.  user must import HasYubikey.py into their
# script to be able to use the function 'hasYubikey(userName)'
# 
# The ipa client will determine which server to connect to in this order:
#
#       1. The server configured in /etc/ipa/default.conf in the xmlrpc_uri
#       directive.
#
#       2. An unordered list of servers from the ldap DNS SRV records.
#
#       If a kerberos error is raised by any of the requests then it will stop
#       processing and display the error message.
#
# the following package needs to be installed: 'ipa-admintools.x86_64' 

import subprocess


# function that takes a single parameter 'userName' that is a 'string'
# extracts the Yubikey('fax') numbers from the attributes associated with user
# and returns them as a 'list' named 'yubikeys' 
# if no keys are assigned to the user, 'yubikeys' will remain empty and an
# empty list will be returned
def hasYubikey(userName):
	# this try/except checks the validity of the given userName
	try:
		ipaResults = subprocess.check_output("ipa user-find --all --raw " + userName,\
		 shell=True)
	# if the given username is not in the system, error message will print and
	# program will exit with a return value of '1'
	except: 
		print "'%s' is not a valid user name" % userName
		exit(1)
	
	# assign the user and all of their attributes as a list
	user = ipaResults.split('\n')

	yubikeys =[] # list to hold the yubikey numbers

	# loop through all of the attributes of a user. If Yubikey is assigned, add
	# yubikey number[s] to the list 'yubikeys'
	for attribute in user:
		if attribute.find('facsimileTelephoneNumber') != -1:
			yubikeys.append(attribute.split(":")[1].strip())
	return yubikeys
