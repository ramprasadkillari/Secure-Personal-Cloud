import requests
import pickle
import os.path
import sys
fullpath = sys.argv[0]
path = os.path.dirname(fullpath)
data = dict()
try:
    print("Reading Server information ...")
    f = open(path+'/spc_user_data', 'rb')
    data = pickle.load(f)
except IOError:
    print("Server details not found. Use the command $spc set_url to configure server details")
    
url = data['url']
r = requests.get(url)
print(r.headers['Server'])
