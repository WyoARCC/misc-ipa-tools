#!/usr/bin/python

# UsersWithYubikey.py
# Jeremy Clay
# June 20, 2016
# 
# 
# script that searches the server and reports the uid and Yubikey numbers
# associated with any users that have Yubikeys associated to their accounts
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

# the following package needs to be installed: 'ipa-admintools.x86_64' 

import subprocess

# function that returns a list of all of the users
def getUserList():
	ipaResults = subprocess.check_output("ipa user-find --all --raw", shell=True)

	return ipaResults.split('\n\n')


# function that takes a list of users, and returns a list of 
# users that have Yubikeys associated with their accounts
def getUsersWithYubiList(list):
	usersWithKey = []

	for user in list:
		returnValue = user.find('facsimileTelephoneNumber')
		# a return value of -1 indicates that the user.find() function failed
		if returnValue != -1: # did NOT fail
			usersWithKey.append(user)

	return usersWithKey


# function that takes in a user and returns a string of the following form
# 	'<uid>: "<key#1>, <key#2>, ..."'
def getUsernameAndYubikey(user):
	user = user.split('\n')

	numFax = 0
	usernameAndKey = ""
	for attribute in user:
		if attribute.find('uid:') != -1:
			# append the user's unique id to the string 'usernameAndKey'
			usernameAndKey = usernameAndKey + attribute.split(":")[1].strip() + ':"'
		
		elif attribute.find('facsimileTelephoneNumber') != -1:
			# append the Yubikey number[s] to the string 'usernameAndKey'
			numFax += 1
			if numFax > 1:
				usernameAndKey = usernameAndKey + ',' + attribute.split(":")[1].strip()
			else:
				usernameAndKey = usernameAndKey + attribute.split(":")[1].strip()

	usernameAndKey = usernameAndKey + '"'

	return usernameAndKey


# function that creates the final list of uids and Yubikeys to be reported
def getFinalList(list):
	finalList = []

	for user in list:
		finalList.append(getUsernameAndYubikey(user))

	return finalList


# function that prints out the users in a list
def printList(list):
	for user in list:
		print user


# call function to create a list of all of the users on the server
users = getUserList()

# extract only the users with a Yubikey associated to them
usersWithYubikey = getUsersWithYubiList(users)

# create a final list with only the uids and Yubikeys
finalList = getFinalList(usersWithYubikey)

# display script results
print 'There are %s users with a Yubikey' % len(finalList)
printList(finalList)
