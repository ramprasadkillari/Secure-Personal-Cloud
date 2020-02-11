import pickle
import sys
import requests
from getpass import getpass
from bs4 import BeautifulSoup

import os.path
fullpath = sys.argv[0]
path = os.path.dirname(fullpath)
data = dict()
filename = sys.argv[1]

red = '\033[91m'
green = '\033[92m'
end_c = '\033[0m'

try:
    print("Reading User information ...", end="      ")
    f = open(path+'/spc_user_data', 'rb')
    data = pickle.load(f)
    print("done")
except IOError:
    print(red+"Authentication credentials not found"+end_c)
    u = input("Enter Username:")
    p = getpass("Enter Password:")
    data['username'] = u
    data['password'] = p
    url = input("Enter Server URL:")
    if url[len(url)-1] != '/':
        url = url + '/'
    data['url'] = url
    save = input('Would you like to save the configuration? [y/n]:')
    if save == 'y' or save == 'Y':
        f = open(path+'/spc_user_data','wb')
        pickle.dump(data,f)
        print("User credentials updated")
        f.close()
        
base_url = data['url']
url = base_url + 'login/'

client = requests.session()
try:
    print("connecting to server ...", end="      ")
    client.get(url)
    print("done")
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

    if r.status_code == 200:
        print("Request sent ...")
        if r.url == url:
            print(red+"User authentication failed. Please try again"+end_c)
            client.close()
            sys.exit()
        print("Reading files ...")
    r1 = client.get(base_url)
    soup = BeautifulSoup(r1.text, 'html.parser')
    productDivs = soup.findAll('a', attrs = {"id" : "deletefile"})
    #print(productDivs[0].string)
    print("Searching for {} ...".format(filename))
    for link in productDivs:
        if link.string == filename:
            var = base_url[:-1] + link['href']
            try:
                r2 = client.get(var, allow_redirects=True)
                print("Deleting ...", end="      ")
                r2.raise_for_status()
                if r.status_code == 200:
                    print(green+"done"+end_c)
                else:
                    print(red+"failed"+end_c)
            except() as e:
                print(red+"Error connecting: {}".format(e)+end_c)


except requests.exceptions.HTTPError as e:
    print(red+'HTTP error: {}'.format(e)+end_c)
except requests.exceptions.RequestException as e:
    print(red+'Connection Error: {}'.format(e)+end_c)
    client.close()
    sys.exit()

client.close()
