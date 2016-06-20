import HasYubikey

user = 'ceastma2'
x = HasYubikey.hasYubikey(user)
print user, 'has Yubikey[s]:'
print x