from pickle import *
from User import *

f = open('users.bin', 'wb')

userList = []
dump(userList, file = f)

f.close()