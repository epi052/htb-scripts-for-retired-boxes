# Simple Brute Force of Tomcat Login via Basic Auth

## Build 

I demonstrate installing [requests](http://docs.python-requests.org/en/master/) here using [pipenv](https://pipenv.readthedocs.io/en/latest/).  If you're running this on Kali, you almost certainly already have requests installed and can skip ahead.

```
git clone https://github.com/epi052/htb-scripts-for-retired-boxes.git
cd htb-scripts-for-retired-boxes/jerry
pipenv --three install requests 
```

## Execution

```
pipenv shell

python tomcat-login-brute.py
[+] Found credentials: tomcat:s3cret
```

