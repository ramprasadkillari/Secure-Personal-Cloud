import pickle
import sys
import requests
from lxml import html
from getpass import getpass
from tabulate import tabulate
import numpy as np
import os.path

red = '\033[91m'
green = '\033[92m'
end_c = '\033[0m'


fullpath = sys.argv[0]
path = os.path.dirname(fullpath)
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

url = data['url'] + "login/"
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
payload = dict(username=data['username'], password=data['password'], csrfmiddlewaretoken=csrf, next='/')
try:
    print("Sending request ...")
    r = client.post(url, data=payload, headers=dict(Referer=url))
    r.raise_for_status()
    files = []
    paths = []
    times = []
    md5sums = []
    if r.status_code == 200:
        print("Request sent ...")
        if r.url == url:
            print(red+"User authentication failed. Please try again"+end_c)
            client.close()
            sys.exit()
        tree = html.fromstring(r.content)
        print("Reading files ...")
        files = tree.xpath('//a[@id="filename"]/text()')
        paths = tree.xpath('//div[@id="filepath"]/text()')
        times = tree.xpath('//div[@id="uploadtime"]/text()')
        md5sums = tree.xpath('//div[@id="md5sum"]/text()')
        if len(files) == 0:
            print("No files/directories uploaded")
            print("Use '$spc uploadfile <file_name> <file_path>' or '$spc uploaddir <dir_path>' to upload files/directories")
            sys.exit()
    Files = np.array(files)
    Paths = np.array(paths)
    Times = np.array(times)
    Md5sums = np.array(md5sums)
    table = np.column_stack((Files, Paths, Times,Md5sums))
    print(tabulate(table, headers=['File Name', 'File Path', 'Upload time','Md5sum']))
except requests.exceptions.HTTPError as e:
    print(red+'HTTP error: {}'.format(e)+end_c)
except requests.exceptions.RequestException as e:
    print(red+'Connection Error: {}'.format(e)+end_c)
    client.close()
    sys.exit()


client.close()
