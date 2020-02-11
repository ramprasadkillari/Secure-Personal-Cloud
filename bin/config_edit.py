import pickle
from getpass import getpass
import os.path
import sys
fullpath = sys.argv[0]
path = os.path.dirname(fullpath)
Username = input("Enter Username:")
Password = getpass("Enter Password:")
Password2 = getpass("Confirm Password:")
if Password != Password2:
    while Password != Password2:
        print("Your Password does not match. Please try again")
        Password = getpass("Enter Password:")
        Password2 = getpass("Confirm Password:")
        print("Configure server URL using the command $spc set_url")
data = dict(username=Username, password=Password, url='http://127.0.0.1:8000/')
f = open(path+'/spc_user_data', 'wb')
pickle.dump(data, f)
print("User credentials updated")
f.close()
