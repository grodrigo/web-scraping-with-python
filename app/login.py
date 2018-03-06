# -*- coding: utf-8 -*-

"""
Login to the site and return the session

Now it only takes the stolen headers, due the captcha isn't possible to
login, just create a session, paste the headers and authentication and
return the session.
Remember: take the correct headers from the browser and paste them in a file
named 'headers.txt'

For how to do the login in other cases, take a look to the file
'another_login_examples.py'
"""
import pdb
import cookielib
import mechanize
import os
import requests

import settings
def login(user='', password='',login_url = ''):
    try:
        if not user:
            user = settings.GeneralConfig.USER
            password = settings.GeneralConfig.PASSWORD
        if not login_url:
            login_url = settings.GeneralConfig.LOGIN_PAGE
    except:
        print "Wrong settings"

    if not os.path.exists('app/headers.txt'):
        raise AssertionError("You need the file headers.txt")
    else:   # Cast the raw headers to a dict
        d = {}
        with open("app/headers.txt") as f:
            for line in f:
                line = line.strip()
                (key, val) = line.split(': ')
                d[key] = val

        s = requests.Session()
        s.auth = (user, password)
        s.headers.update(d)
        return s
