import sys
import requests
import pickle
from getpass import getpass
import os.path
fullpath = sys.argv[0]
path = os.path.dirname(fullpath)
data = dict()
base_url = input('Enter Server URL:')
if base_url[len(base_url)-1] != '/':
    base_url = base_url + '/'
url = base_url + 'signup/'
err = "A user with that username already exists"
err2 = "Enter a valid username"
client = requests.session()
try:
    print("connecting to server ...")
    client.get(url)
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

Username = input("Please enter Username :")
print("Please keep the following things in mind while choosing a password:")
print("1. Your password can't be too similar to your other personal information")
print("2. Your password must contain at least 8 characters")
print("3. Your password can't be a commonly used password")
print("4. Your password can't be entirely numeric")
Password = getpass("Enter Password:")
Password2 = getpass("Confirm Password:")
if Password != Password2:
    while Password != Password2:
        print("Your Password does not match. Please try again")
        Password = getpass("Enter Password:")
        Password2 = getpass("Confirm Password:")

payload = {'username': Username, 'password1': Password, 'password2': Password2, 'csrfmiddlewaretoken': csrf}

try:
    print("Sending request ...")
    r = client.post(url, data=payload, headers=dict(Referer=url))
    r.raise_for_status()
    if r.status_code == 200:
        print("Request sent ...")
    if r.url == base_url+'login/':
        print("Registration successful")
        client.close()
        ans = input("Would you like to save your username and password?[y/n]:")
        if ans == 'n' or ans == 'N'or ans == 'no' or ans == 'No':
            sys.exit()
        elif ans == 'y' or ans == 'Y'or ans == 'yes' or ans == 'Yes':
            data = dict(username=Username, password=Password, url=base_url)
            f = open(path+'/spc_user_data', 'wb')
            pickle.dump(data, f)
            print("User credentials saved")
            f.close()
            sys.exit()
        else:
            print("Invalid input. You can save password by running '$spc config edit'")
            sys.exit()
    else:
        while r.url != base_url+'login/':
            if r.url != url:
                print('Unknown error occured. Please try again')
                client.close()
                sys.exit()
            elif str(r.text).find(err2) != -1:
                print("Username is invalid. Username can contain max.150 characters, letters digits and @/./+/-/_ only")
                client.close()
                client = requests.session()
                try:
                    client.get(url)
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

                Username = input("Username :")
                Password = getpass("Enter Password:")
                Password2 = getpass("Confirm Password:")
                if Password != Password2:
                    while Password != Password2:
                        print("Your Password does not match. Please try again")
                        Password = getpass("Enter Password:")
                        Password2 = getpass("Confirm Password:")
                payload = {'username': Username, 'password1': Password, 'password2': Password2,
                           'csrfmiddlewaretoken': csrf}
                print("Sending request ...")
                r = client.post(url, data=payload, headers=dict(Referer=url))
                r.raise_for_status()
                if r.status_code == 200:
                    print("Request sent ...")
            elif str(r.text).find(err) == -1:
                print("Your password does not meet the required conditions. Please choose another one")
                client.close()
                client = requests.session()
                try:
                    client.get(url)
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

                Password = getpass("Enter Password:")
                Password2 = getpass("Confirm Password:")
                if Password != Password2:
                    while Password != Password2:
                        print("Your Password does not match. Please try again")
                        Password = getpass("Enter Password:")
                        Password2 = getpass("Confirm Password:")
                payload = {'username': Username, 'password1': Password, 'password2': Password2,
                           'csrfmiddlewaretoken': csrf}
                print("Sending request ...")
                r = client.post(url, data=payload, headers=dict(Referer=url))
                r.raise_for_status()
                if r.status_code == 200:
                    print("Request sent ...")
            else:
                client.close()
                print("The username is already used. Please choose another one")
                client = requests.session()
                try:
                    client.get(url)
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

                Username = input("Username :")
                Password = getpass("Enter Password:")
                Password2 = getpass("Confirm Password:")
                if Password != Password2:
                    while Password != Password2:
                        print("Your Password does not match. Please try again")
                        Password = getpass("Enter Password:")
                        Password2 = getpass("Confirm Password:")
                payload = {'username': Username, 'password1': Password, 'password2': Password2, 'csrfmiddlewaretoken': csrf}
                print("Sending request ...")
                r = client.post(url, data=payload, headers=dict(Referer=url))
                r.raise_for_status()
                if r.status_code == 200:
                    print("Request sent ...")
    print("Registration successful")
    ans = input("Would you like to save your username and password?[y/n]:")
    if ans == 'n' or ans == 'N' or ans == 'no' or ans == 'No':
        sys.exit()
    elif ans == 'y' or ans == 'Y' or ans == 'yes' or ans == 'Yes':
        data = dict(username=Username, password=Password, url=base_url)
        f = open(path+'/spc_user_data', 'wb')
        pickle.dump(data, f)
        print("User credentials saved")
        f.close()
        client.close()
        sys.exit()
    else:
        print("Invalid input. You can save password by running '$spc config edit'")
        client.close()
        sys.exit()


except requests.exceptions.HTTPError as e:
    print('HTTP error: {}'.format(e))
except requests.exceptions.RequestException as e:
    print('Connection Error: {}'.format(e))
    client.close()
    sys.exit()
