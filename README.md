# WEB SCRAPING WITH PYTHON

## Description ##
This is a project to do web scrapping for testing and backup purpose.

It only works with a specific site, which is not mentioned here for legal reasons,
but its approach I think is applicable to future projects.

The process is simple: login to a page, walk over the site structure and download its videos and html material.

## Notes ##
The idea was to put together in a project: command line usage, session handling and site analysis.  
The modules mainly used are requests (or mechanize.Browser in the old code), BeautifulSoup and json.  

To debug was useful the pdb module, remember to put the sentence pdb.set_trace() few lines before you want.  
Commands: n for next, c for continue, p for print a variable, pp for pretty print, !statement to execute a
statement (e.g. to declare a variable), j line to jump (e.g. to avoid known errors).  
python -m pdb -c continue myscript.py # for python2.7 -c isn't present.

## Configuration ##
It's advisable to create an isolated workspace with virtualenv for example.  
```bash
virtualenv venv
source venv/bin/activate
# to deactivate just do wherever you want: deactivate
```
Install the requirements  
```bash
pip install -r requirements.txt
```

**settings.py and headers.txt**  

In the app directory is placed the whole application, and in Downloads the downloads organized by material.
Copy settings_example.py to settings.py and put your own configuration if you want.

While the project was ending, the site implemented ReCaptcha, and that brought
many problems to the very necessary first stage: the login.  
After a day of thinking how to bypass the trouble, I found that stealing the headers
from an active browser session browser worked well.  
I couldn't find if it was only due the ReCaptcha or anything else, so some other login
examples were moved to "another_login_examples.py" for future review.  

## Conclusion ##
Copy the correct headers in 'app/headers.txt' and everything gonna be all right.  
Set the correct settings in 'app/settings.py' and everything gonna be all right.  
Avoid this steps, and you'll get in trouble with me.  
                ─╤╦︻3=(◣_◢)=Ƹ︻╦╤─
