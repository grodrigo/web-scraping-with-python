# -*- coding: utf-8 -*-

"""Set the configuration to be used in the program.
    Take this example file and copy to app/settings.py

    AbstractConfig only provides a basic configuration, like the ROOT_DIR.

    You can use the program by command line, providing the necessary information,
    or setting your own configuration in GeneralConfig.

    Note that not all the parameters must be inicialized, for example you can pass
    the material url by command line.
"""
import os,sys

class AbstractConfig:
    BASEURL = ''
    LOGIN_PAGE = ''
    reg_lecture = '<section class="DiscusionDetail".*?)<!-- <script src="' #not used
    reg_video  = '"hls": "(.*?)\"' # not used
    USER = ''
    PASSWORD = ''
    ROOT_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
    COURSE = ''
    MATERIAL = ''

class GeneralConfig(AbstractConfig):
    # overwrite with your configurations
    BASEURL = 'http://example.com'
    LOGIN_PAGE = 'https://example.com/login'
    USER = 'username'
    PASSWORD = 'password'
    COURSE = 'http://example.com/course/acoursename'
