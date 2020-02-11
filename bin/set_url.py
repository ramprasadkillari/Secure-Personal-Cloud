import pickle
import sys
import os.path
fullpath = sys.argv[0]
path = os.path.dirname(fullpath)
data = dict()
url = input("Enter URL:")
if url[len(url)-1] != '/':
        url = url + '/'
try:
    f = open(path+'/spc_user_data', 'rb')
    data = pickle.load(f)
    f.close()
except IOError:
    data = dict()

data['url'] = url
f = open(path+'/spc_user_data', 'wb')
pickle.dump(data,f)
f.close()
print("URL saved")