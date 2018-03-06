# -*- coding: utf-8 -*-
import pdb
from settings import *
import re,sys,json,os

from slugify import slugify
from bs4 import BeautifulSoup
from download_material import download_material
import settings
import sys

def download_course(session, url):
    result = session.get(url)
    c = result.content
    soup_course = BeautifulSoup(c,'lxml')
    #print(soup_course.prettify())
    script_course = soup_course.find('script', text=re.compile('data ='))

    #get json data
    json_text = re.search(r'^\s*window\.data\s*=\s*({.*?})\s*;\s*$',
        script_course.string, flags=re.DOTALL | re.MULTILINE).group(1)
    course_data = json.loads(json_text)

    course = course_data['initialProps']['course']
    course_id = str(course['id'])
    course_url = course['url']
    course_title = course['name']
    course_slug = slugify(course_title)

    os.chdir('Downloads')

    # Save in the log that we are downloading a new course
    with open(settings.GeneralConfig.ROOT_DIR + '/Downloads/downloaded.json') as json_file:
            downloaded_courses = json.load(json_file)

    if not downloaded_courses.get(course_id):
        downloaded_courses[course_id] = {
                'title' : course_title,
                'slug'  : course_slug,
                'url'   : course_url,
                'materials' : {}
        }

        # Save in the log file the new course
        with open(settings.GeneralConfig.ROOT_DIR + '/Downloads/downloaded.json', 'w') as outfile:
            json.dump(downloaded_courses, outfile)


    print("  Downloading course", course_slug)
    if not(os.path.exists(course_slug)):
        os.system("mkdir " + course_slug)
    os.chdir(course_slug)

    # Save the html initial page of the course to see the content.
    if not(os.path.exists(course['slug']+'.html')):
        print("Creando html del curso")
        m = re.findall ('(<section id="wrapper".*?)<!-- <script src=', str(soup_course), re.DOTALL)[0]
        with open(course_slug + '.html', 'w') as f:
            f.write('<html><body>')
            f.write(m)
            f.write('</body></html>')

    # Walk over sections
    sections = course_data['initialProps']['concepts']
    for section in sections:
        section_slug = slugify(section['title'])
        print("      Descargando sección:",section_slug)

        if not(os.path.exists(section_slug)):
            os.system("mkdir " + section_slug)

        os.chdir(section_slug)
        for material in section['materials']:
            # Check it's a new download
            if (material['id'] not in downloaded_courses[course_id]['materials'].keys()
                or material['id'] not in downloaded_courses['singles'].keys()):
                download_material(session, material)

                #reload downloaded_courses and save the new material in the log
                with open(settings.GeneralConfig.ROOT_DIR + '/Downloads/downloaded.json') as json_file:
                        downloaded_courses = json.load(json_file)
                downloaded_courses[course_id]['materials'][material['id']] = {
                    "section" : material['concept'],
                    "name"  :   material['name'],
                    "slug"  :   section_slug,
                    "url"   :   material['url'],
                    "material_type" : material['material_type']
                }
                with open(settings.GeneralConfig.ROOT_DIR + '/Downloads/downloaded.json', 'w') as outfile:
                    json.dump(downloaded_courses, outfile)

        # Back to course directory
        os.chdir('../')
