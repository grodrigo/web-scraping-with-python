import sys, os
import json

class Check:
    """
    Assert you have the Downloads folder and Singles folder inside to save your
    materials.
    Also check the downloaded.json file existence and basic structure.
    Made for run it once for script.
    """
    def __init__(self):
        if not(os.path.exists('Downloads')):
            os.system("mkdir " + 'Downloads')
        if not(os.path.exists('Downloads/Singles')):
            os.system("mkdir " + 'Downloads/Singles')

        #check structure of the json file
        try:
            with open('Downloads/downloaded.json') as json_file:
                downloaded_courses = json.load(json_file)
        except ValueError:
            raise ValueError("'Downloads/downloaded.json' isn't a valid json, check or remove it.")
        except IOError:  #the file doesn't exists
            downloaded_courses = {'singles':{}}
            with open('Downloads/downloaded.json', 'w') as outfile:
                json.dump(downloaded_courses, outfile)

        try:
            if not isinstance(downloaded_courses['singles'],type({})):
                raise ValueError("The 'single' key has to be a dict")
        except KeyError:
            raise KeyError("'Downloads/downloaded.json' needs the 'singles' key")
        print("initial test OK")
