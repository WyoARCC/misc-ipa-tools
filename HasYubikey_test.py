import HasYubikey


print 'Input a user name:'
user = raw_input('>')
x = HasYubikey.hasYubikey(user)
print user, 'has Yubikey[s]:'
print x