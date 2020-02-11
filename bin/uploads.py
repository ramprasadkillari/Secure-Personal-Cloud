import pickle
import sys
import requests
from getpass import getpass
import os
from Crypto.Cipher import AES
from Crypto.Cipher import Blowfish
from Crypto.Cipher import ARC4
import tempfile




fullpath = sys.argv[0]
path = os.path.dirname(fullpath)
files = dict()
#AES key must be 16,24 or 32 bytes long and input string multiples of 16
#Blowfish key can be aby long but input string must be multiples of 8 
#ARC4 key and input string both can be anything

# from sjcl import SJCL

# cyphertext = SJCL().encrypt(b"secret message to encrypt", "shared_secret")

# print(cyphertext)
# print(SJCL().decrypt(cyphertext, "shared_secret"))



red = '\033[91m'
green = '\033[92m'
end_c = '\033[0m'

# try:
#     key = '0123456701234567'
#     chunk_size = 16
#     aes = AES.new(key)
#     with open(sys.argv[1], 'rb') as in_file:
#         temp = tempfile.NamedTemporaryFile("ab+")
#         temp.name = in_file.name
#         while True:
#             # chunk = in_file.read(chunk_size)
#             # if len(chunk) == 0:
#             #     break
#             # elif len(chunk) != chunk_size:
#             #     var = chunk_size-len(chunk)%chunk_size
#             #     chunk += var*chr(var)
#             #     chunk = aes.encrypt(chunk)
#             #     temp.write(chunk)
#             # else:
#             #     temp.write(aes.encrypt(chunk))
#
#             chunk = in_file.read()
#             chunk = chunSJCL().encrypt(chunk, key)
#             temp.write(chunk)
#         temp.seek(0)
#     #temp.name = "myu_name"
#         files = {'document': temp}
try:
    files = {'document' : open(sys.argv[1], 'rb')}
except IOError:
    print("file {} not found".format(sys.argv[1]))
    sys.exit()
print("Reading file {}".format(sys.argv[1]))
filepath = sys.argv[2]
data = dict()
try:
    print("Reading User information ...")
    f = open(path+'/spc_user_data', 'rb')
    data = pickle.load(f)
except IOError:
    print(red+"Authentication credentials not found"+end_c)
    u = input("Enter Username:")
    p = getpass("Enter Password:")
    url = input("Enter Server URL:")
    if url[len(url)-1] != '/':
        url = url + '/'
    data['username'] = u
    data['password'] = p
    data['url'] = url
    save = input('Would you like to save the configuration? [y/n]:')
    if save == 'y' or save == 'Y':
        f = open(path+'/spc_user_data','wb')
        pickle.dump(data,f)
        print("User credentials updated")
        f.close()

base_url = data['url']
url = base_url+'login/'
client = requests.session()
try:
    print("connecting to server ...")
    client.get(url)
except requests.ConnectionError as e:
    print(red+"The following error occured connecting to the server: {}\n Please try again".format(e)+end_c)
    client.close()
    sys.exit()

try:
    csrf = client.cookies['csrftoken']
except():
    print(red+"Error obtaining csrf token"+end_c)
    client.close()
    sys.exit()
payload = dict(username=data['username'], password=data['password'], csrfmiddlewaretoken=csrf, next='/upload_file/')
try:
    print("Sending request ...")
    r = client.post(url, data=payload, headers=dict(Referer=url))
    r.raise_for_status()
    if r.status_code == 200:
        print("Request sent ...")
        if r.url == url:
            print(red+"User authentication failed. Please try again"+end_c)
            client.close()
            sys.exit()
        else:
            try:
                print("Uploading file ...")
                r2 = client.post(base_url+'upload_file/', data={'filepath': filepath, 'csrfmiddlewaretoken': r.cookies['csrftoken']}, files=files )
                r2.raise_for_status()
                if r2.status_code != 200:
                    print(red+"An error occured . status_code = {}".format(r2.status_code)+end_c)
                    sys.exit()
                elif r2.url == base_url:
                    print(green+"File upload successful"+end_c)
                else:
                    print(red+"An error occured"+end_c)
            except() as e:
                print(red+"error posting file: {}".format(e)+end_c)
except requests.exceptions.HTTPError as e:
    print(red+'HTTP error: {}'.format(e)+end_c)
except requests.exceptions.RequestException as e:
    print(red+'Connection Error: {}'.format(e)+end_c)
    client.close()
    sys.exit()
