import pickle
import sys
import requests
from getpass import getpass
from bs4 import BeautifulSoup
import itertools
import os
import sqlite3
import hashlib
from pathlib import Path

fullpath = sys.argv[0]
pathspc = os.path.dirname(fullpath)
data = dict()


dirpath = sys.argv[1]  # Gives the absolutepath of directory
obsdirpathlist = dirpath.split('/')[:-1]
obsdirpath = str()
for i in obsdirpathlist:
    obsdirpath = obsdirpath + i + '/'  # this is observing dir full path it includes slash at the end and beginning
observing_dir = dirpath.split("/")[-1]  # this is observing directory eg.outlab30

try:
    print("Reading User information ...", end="      ")
    f = open(pathspc+'/spc_user_data', 'rb')
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
        f = open(pathspc+'/spc_user_data','wb')
        pickle.dump(data,f)
        print("User credentials updated")
        f.close()
        
base_url = data['url']
url = base_url + 'login/'



def md5sum(filename, blocksize=65536):
    hash = hashlib.md5()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            hash.update(block)
    return hash.hexdigest()

def listsmd5unequal(ldict,sdict):  # dicts of filenames and md5s
    unequalmd5s=[]
    for i in ldict:
        if ldict[i] != sdict[i] :
            unequalmd5s.append(i)
    return unequalmd5s 

def ifstr1startswithstr2(str1,str2):
    if(str1.split('/')[0]==str2):
        return True
    else:
        return False        

def falselist(n):
    l = []
    for i in range(0,n):
        l.append("False")
    return l

def truelist(n):
    l = []
    for i in range(0,n):
        l.append("True")
    return l        
insync = str()
empty = []
red = '\033[91m'
green = '\033[92m'
end_c = '\033[0m'
files=dict()
var3 = str()
list777 = []
list77 = []
boollist=[]
for path, subdirs, files in os.walk(dirpath):
   for filename in files:
     f2 = os.path.join(path, filename)
     list777.append(f2) 
for i in list777:
    serpath = i.replace(obsdirpath,"")
    list77.append(serpath)
      #this list consists of filepaths same as that of in server   


list7 = []
data = dict()
try:
    print("Reading User information ...", end="      ")
    f = open(pathspc+'/spc_user_data', 'rb')
    data = pickle.load(f)
    print("done")
except IOError:
    print("Authentication credentials not found")
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
        f = open(pathspc+'/spc_user_data','wb')
        pickle.dump(data,f)
        print("User credentials updated")
        f.close()

base_url = data['url']
url = base_url+'login/'
client = requests.session()
try:
    print("connecting to server ...", end="      ")
    client.get(url)
    print("done")
except requests.ConnectionError as e:
    print("The following error occured connecting to the server: {}\n Please try again".format(e))
    client.close()
    sys.exit()

try:
    csrf = client.cookies['csrftoken']
except():
    print("Error obtaining csrf token")
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
            print("User authentication failed. Please try again")
            client.close()
            sys.exit()
        print("Reading files ...")
        r1 = client.get(base_url)
        soup = BeautifulSoup(r1.text, 'html.parser')
        productDivs = soup.findAll(attrs = {"id" : "filepath"})
        productDivs2 = soup.findAll('a', attrs = {"id" : "filename"})
        productDivs3 = soup.findAll(attrs = {"id" : "md5sum"})
        productDivs5 = soup.findAll(attrs = {"id" : "deletefile"})
        productDivs6 = soup.findAll('a', attrs = {"id" : "startsync"})
        productDivs7 = soup.findAll('a', attrs = {"id" : "stopsync"})

        md5list={}

        for link,l in zip(productDivs5,productDivs3):
            pathinserver = link.string
            if(ifstr1startswithstr2(pathinserver,observing_dir)==True):
                list7.append(pathinserver)
                md5list[pathinserver] = l.string.split()[1] #dict of filenames and md5sums of all files in server
        insync = productDivs6[0].string
        if insync=="True":
            print(red+"Sync is going on in some other device.Please wait for sometime."+end_c)
            sys.exit()    
        elif insync=="False": 
            try:   
                var = base_url+productDivs6[0]['href']
                client.get(var,allow_redirects=True)
            except() as e:
                print("Error connecting: {}".format(e))

except() as e:
    print("Error connecting: {}".format(e))

def download(listoffiles):
    for lit in listoffiles:
        for link,li in zip(productDivs2,productDivs):   
            if (li.string.split()[2]+link.string == lit):
                var = base_url[:-1] + link['href']
                try:
                    r2 = client.get(var, allow_redirects=True)
                    filep = str()
                    filen = obsdirpath+lit  #absolute file path in local 
                    l = filen.split('/')[1:-1]
                    for i in l:
                        filep = filep + '/' + i
                    path = Path(filep)
                    path.mkdir(parents=True, exist_ok=True)    
                    f1 = open(filen, 'wb')
                    f1.write(r2.content)
                    f1.close()
                except() as e:
                    print("Error connecting: {}".format(e))   

def upload(listoffiles):
    for lit in listoffiles:
        l = lit.split('/')
        l.pop()
        fil = str()
        for i in l:
            fil = fil+i+"/"
        filepath = fil    
        files = {'document': open(obsdirpath+lit, 'rb')}
        try:
            r2 = client.post(base_url+'upload_file/', data={'filepath': filepath, 'csrfmiddlewaretoken': r.cookies['csrftoken']}, files=files)
            if r2.url == base_url:
                print("File upload successful")
            else:
                print("An error occured")            
        except() as e:
            print("error posting file: {}".format(e))

try:
    serverset = set(list7)
    localset = set(list77)
    localmd5list = {}        
    inser = list(serverset - localset)
    inloc = list(localset - serverset)
    inboth = list(localset.intersection(serverset))

    for i in inboth:
        localmd5list[i] = md5sum(i)
    inboth_difmd = listsmd5unequal(localmd5list,md5list)

    print()
    if (serverset == localset) and len(inboth_difmd) == 0:
        print(green+"The directory is same in both client and server"+end_c)
    else:
        print("The observed directory have some differences from the files in cloud")
        print(green+"Files in cloud not in the local directory :"+end_c)
        print(inser)
        print()
        print(green+"Files in the local directory that are not in the cloud :"+end_c)
        print(inloc)
        print()
        print("Choose one of the below options: ")
        print("1. Change the directory of local as that of in cloud")
        print("2. Change the files in cloud same as that of in local")
        print("3. Merge both the local and files in cloud")
        print("4. Don't change anything")
        x = input()

        if(int(x)==1):
            for lit in inloc:
                os.remove(obsdirpath+lit)
            download(inser+inboth_difmd) 
            print(green+"Done"+end_c)

        elif(int(x)==2):
            for lit in inser:
                for link in productDivs5:
                    if(link.string == lit):
                        var = base_url[:-1]+link['href']
                        try:
                            r2 = client.get(var, allow_redirects=True)
                            print("Deleting ...", end="      ")
                            print(green+"done"+end_c)
                        except() as e:
                            print(red+"Error connecting: {}".format(e)+end_c)                               
            upload(inloc+inboth_difmd)
            print(green+"Done"+end_c) 

        elif(int(x)==3):
            download(inser)
            upload(inloc)
            if len(inboth_difmd) != 0:
                print("There are some files in the server different from that of local files with same name.Please let us know what to do by choosing one of the three options:")
                print(green+"Files present in both cloud and local directory but with different file content :"+end_c)
                print(inboth_difmd)
                print()
                print("1.Download all the files from server")
                print("2.Upload all the local fles to server")
                print("3.Chose manually what to do with each file")
                inp = input()
                if inp == '1':
                    download(inboth_difmd)                           
                elif inp == '2':
                    upload(inboth_difmd)                         
                elif inp == '3':
                    for lit in inboth_difmd:
                        print("1.Download the file from server")
                        print("2.Upload the local file to server")
                        inp == input()
                        if inp == '1':
                            for link,li in zip(productDivs2,productDivs):   
                                if (li.string.split()[2]+link.string == lit):
                                    var = base_url[:-1] + link['href']
                                    try:
                                        r2 = client.get(var, allow_redirects=True)
                                        filep = str()
                                        filen = obsdirpath+lit  #absolute file path in local 
                                        l = filen.split('/')[1:-1]
                                        for i in l:
                                            filep = filep + '/' + i
                                        path = Path(filep)
                                        path.mkdir(parents=True, exist_ok=True)    
                                        f1 = open(filen, 'wb')
                                        f1.write(r2.content)
                                        f1.close()
                                    except() as e:
                                        print("Error connecting: {}".format(e))  
                        elif inp == '2':
                            l = lit.split('/')
                            l.pop()
                            for i in l:
                                fil = fil+i+"/"
                            filepath = fil    
                            files = {'document': open(obsdirpath+lit, 'rb')}
                            try:
                                r2 = client.post(base_url+'upload_file/', data={'filepath': filepath, 'csrfmiddlewaretoken': r.cookies['csrftoken']}, files=files)
                                if r2.url == base_url:
                                    print("File upload successful")
                                else:
                                    print("An error occured")            
                            except() as e:
                                print("error posting file: {}".format(e)) 
            print("Done")
        else:
            print("Nothing is changed") 
    try:
        var = base_url+productDivs7[0]['href']
        client.get(var,allow_redirects=True)
    except() as e:
            print("Error connecting: {}".format(e))

except requests.exceptions.HTTPError as e:
    print('HTTP Error: {}'.format(e))
except requests.exceptions.RequestException as e:
    print('Connection Error: {}'.format(e))
    client.close()
    sys.exit()
client.close()