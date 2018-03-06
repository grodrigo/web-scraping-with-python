#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import getpass
import sys, os

from app import *

if __name__ == "__main__":
    initialSetup.Check()

    parser = argparse.ArgumentParser(
        description      = 'Download courses with scraping',
        epilog           = "*** Change settings.py to make your life easier ***",
        argument_default = argparse.SUPPRESS
        )

    parser.add_argument('-u','--user', required=False)
    parser.add_argument('-p','--password', required=False)
    parser.add_argument('-lg','--login_url', required=False)

    group = parser.add_mutually_exclusive_group()

    group.add_argument('-C','--career', help='NOT implemented')
    group.add_argument('-c','--course',)
    group.add_argument('-m','--material')

    args = vars(parser.parse_args())

    if 'user' in args:
        if not 'password' in args:
            args['password'] = getpass.getpass("Password: ")
        session = login(args['user'], args['password'],args.get('login_url'))
    else:
        session = login(login_url = args.get('login_url'))

    #select your download
    if 'career' in args:
        ## TODO ##
        print("Not implemented yet")
    elif 'course' in args:
        download_course(session, args['course'])
    elif 'material' in args:
        download_material_from_url(session, material=args['material'])
    else:
        if settings.GeneralConfig.COURSE:
            download_course(session, settings.GeneralConfig.COURSE)
        if settings.GeneralConfig.MATERIAL:
            download_material_from_url(session, settings.GeneralConfig.MATERIAL)
