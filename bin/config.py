import pickle
import sys
import os.path
fullpath = sys.argv[0]
path = os.path.dirname(fullpath)

data = dict()
try:
    f = open(path+'/spc_user_data', 'rb')
    data = pickle.load(f)
except IOError:
    print("The file with user data is either missing or corrupted")
    print("You can use '$spc config edit' to reconfigure user data")
    sys.exit()
print("Server URL:" + str(data['url']))
print("Username:" + str(data['username']))
#print("Password:" + str(data['password']))
