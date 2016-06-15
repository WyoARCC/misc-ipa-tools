#!/usr/bin/python

# IpaVsGetent.py
# Jeremy Clay
# June 6, 2016
# 
# script that compares the bash commands 'getent group mounmoran',
# and 'ipa group-show mountmoran'
#
# the following package needs to be installed:
# 'ipa-admintools.x86_64'

import subprocess

# run bash command 'getent group mountmoran'
# results stored as a string in variable getentResults
getentResults = subprocess.check_output("getent group mountmoran", shell=True)

# parse getentResults to extract the users
# the users are stored as a list in variable getentUsers
getentUsers = getentResults.split(':')[3].strip().split(',')

# for testing purposes only, uncomment the next two lines
#getentUsers.append('xtraUser1')
#getentUsers.append('xtraUser2')

getentUsers.sort()

# run bash command 'ipa group-show mountmoran'
# results stored as a string in variable ipaResults
ipaResults = subprocess.check_output("ipa group-show mountmoran", shell=True)

# results from 'ipa group-show mountmoran' reports two groups of users:
# 'Member users', and 'Indirect Member users'.  These two groups are parsed
# out of the ipaResults and combined into on list: 'ipaMembers'
ipaUsersNoNewLine = ipaResults.split('\n')

MemberUsers = ipaUsersNoNewLine[3]
MemberUsers = MemberUsers.strip().split(':')[1].strip()
MemberUsers = "".join(MemberUsers.split()).split(',')

IndirectMemberUsers = ipaUsersNoNewLine[6]
IndirectMemberUsers = IndirectMemberUsers.strip().split(':')[1].strip()
IndirectMemberUsers = "".join(IndirectMemberUsers.split()).split(',')

ipaMembers = MemberUsers + IndirectMemberUsers

# for testing purposes only, uncomment the following line
#ipaMembers.append('xtraUser3')

ipaMembers.sort()

print '-' * 20
# Print the number of users reported from the bash commands on the terminal
print 'There are', ipaMembers.__len__(), 'users reported in ipa results.'
print 'There are', getentUsers.__len__(), 'users reported in getent results.'

print '-' * 20

if getentUsers == ipaMembers: # both commands report the exact same users
	print "Results from ipa and getent are the same."
else: # results from bash commands vary
	print "Results from ipa and getent are NOT the same."

	# extract discrepancies from lists of users.  Store these discrepancies in
	# 2 new lists: 'uniqueGetentUsers', and 'uniqueIpaMembers'
	uniqueGetentUsers = list(set(getentUsers) - set(ipaMembers))
	uniqueGetentUsers.sort()
	uniqueIpaMembers = list(set(ipaMembers) - set(getentUsers))
	uniqueIpaMembers.sort()

	print '-' * 20

	# Print discrepancies to the terminal
	if uniqueGetentUsers.__len__() > 0:
		print "The users reported in getent results that do not show up in ipa results are:"
		for user in uniqueGetentUsers:
			print '\t', user

	else:
		print 'There are no users reported in getent results that do not show up in ipa results.'

	print '-' * 20

	if uniqueIpaMembers.__len__() > 0:
		print 'The users reported in ipa results that do not show up in getent results are:'
		for member in uniqueIpaMembers:
			print '\t', member
	else:
		print 'There are no users reported in ipa results that do not show up in getent results.'

print '-' * 20
exit(0)