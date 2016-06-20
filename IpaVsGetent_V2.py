#!/usr/bin/python

# IpaVsGetent.py
# Jeremy Clay
# June 6, 2016
# 
# script that takes 1 argument 'group name' and compares the bash commands 
# 'getent group <group name>',
# and 'ipa group-show <group name>'
#
# the following package needs to be installed:
# 'ipa-admintools.x86_64'

import subprocess
from sys import argv

script, groupName = argv

getentCommand = "getent group " + groupName
ipaCommand = "ipa group-show " + groupName

print '-' * 20
print "Running the script: '%s' on the group '%s'" % (script, groupName)

# run bash command 'getent group mountmoran'
# results stored as a string in variable getentResults
try:
	getentResults = subprocess.check_output(getentCommand, shell=True)
except:
	print "'%s' is not a valid groupname" % groupName
	exit(1)

# parse getentResults to extract the users
# the users are stored as a list in variable getentUsers
getentUsers = getentResults.split(':')[3].strip().split(',')

# for testing purposes only, uncomment the next two lines
#getentUsers.append('xtraUser1')
#getentUsers.append('xtraUser2')

getentUsers.sort()

# results from 'ipa group-show mountmoran' reports two groups of users:
# 'Member users', and 'Indirect Member users'.  Using 'grep' and appropriate
# options, these two groups are extracted, cleaned up, and combined into
# one list: 'ipaMembers'

# Extracting just the 'Member users' from the ipa command
MemberUsers = subprocess.check_output(ipaCommand + " | grep -i 'member users' | grep -iv 'indirect member users'", shell=True)

# Users are listed after "Member users:"
# String is split on the ':' and only the users are kept
MemberUsers = MemberUsers.split(':')[1].strip()
MemberUsers = "".join(MemberUsers.split()).split(',')

# Extracting just the 'Indirect Member users' from the ipa command
# If no Indirect Member users exist, 'ipaMembers' will only contain 'MemberUsers'
try:
	IndirectMemberUsers = subprocess.check_output(ipaCommand + " | grep -i 'indirect member users'", shell=True)

	# Users are listed after "Indirect Member users:"
	# String is split on the ':' and only the users are kept
	IndirectMemberUsers = IndirectMemberUsers.split(':')[1].strip()
	IndirectMemberUsers = "".join(IndirectMemberUsers.split()).split(',')

	# The lists containing the 'Member users' and 'Indirect Member users' are combined
	ipaMembers = MemberUsers + IndirectMemberUsers
except:
	ipaMembers = MemberUsers

# for testing purposes only, uncomment the following line
#ipaMembers.append('xtraUser3')

ipaMembers.sort()

print '-' * 20

if getentUsers == ipaMembers: # both commands report the exact same users
	print "Results from ipa and getent on the group '%s' are the same." % groupName
else: # results from bash commands vary
	print "Results from ipa and getent on the group '%s' are NOT the same." % groupName

	# extract discrepancies from lists of users.  Store these discrepancies in
	# 2 new lists: 'uniqueGetentUsers', and 'uniqueIpaMembers'
	uniqueGetentUsers = list(set(getentUsers) - set(ipaMembers))
	uniqueGetentUsers.sort()
	
	uniqueIpaMembers = list(set(ipaMembers) - set(getentUsers))
	uniqueIpaMembers.sort()

	print '-' * 20

	# Print discrepancies to the terminal
	if uniqueGetentUsers.__len__() > 0: # If the list is not empty
		print "The users reported in getent results that do not show up in ipa results are:"
		for user in uniqueGetentUsers:
			print '\t', user

	else: # The list is empty
		print 'There are no users reported in getent results that do not show up in ipa results.'

	print '-' * 20

	if uniqueIpaMembers.__len__() > 0: # If the list is not empty
		print 'The users reported in ipa results that do not show up in getent results are:'
		for member in uniqueIpaMembers:
			print '\t', member
	else: # The list is empty
		print 'There are no users reported in ipa results that do not show up in getent results.'

print '-' * 20
exit(0)