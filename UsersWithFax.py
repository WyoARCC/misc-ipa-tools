#!/usr/bin/python

# IpaVsGetent.py
# Jeremy Clay
# June 6, 2016
# 
# 
# script that searches the server and reports the uid and fax numbers
# associated with any users that have fax numbers associated to their accounts
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
# users that have facsimile numbers associated with their accounts
def getUsersWithFaxList(list):
	usersWithFax = []

	for user in list:
		returnValue = user.find('facsimileTelephoneNumber')
		
		if returnValue != -1:
			usersWithFax.append(user)

	return usersWithFax


# function that takes in a user and returns a string of the following form
# 	'<uid>: "<fax#1>, <fax#2>, ..."'
def getUsernameAndFax(user):
	user = user.split('\n')

	numFax = 0
	usernameAndFax = ""
	for attribute in user:
		if attribute.find('uid:') != -1:
			usernameAndFax = usernameAndFax + attribute.split(":")[1].strip() + ':"'
		
		elif attribute.find('facsimileTelephoneNumber') != -1:
			numFax += 1
			if numFax > 1:
				usernameAndFax = usernameAndFax + ',' + attribute.split(":")[1].strip()
			else:
				usernameAndFax = usernameAndFax + attribute.split(":")[1].strip()

	usernameAndFax = usernameAndFax + '"'

	return usernameAndFax


# function that creates the final list of uids and fax numbers to be reported
def getFinalList(list):
	finalList = []

	for user in list:
		finalList.append(getUsernameAndFax(user))

	return finalList


# function that prints out the users in a list
def printList(list):
	for user in list:
		print user


# call function to create a list of all of the users on the server
users = getUserList()

# extract only the users with a fax number associated to them
usersWithFax = getUsersWithFaxList(users)

# create a final list with only the uids and fax numbers
finalList = getFinalList(usersWithFax)

# display script results
print 'There are %s users with a fax number' % len(finalList)
printList(finalList)
