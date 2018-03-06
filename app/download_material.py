# -*- coding: utf-8 -*-
import sys,re,os,json
from subprocess import PIPE, Popen
from bs4 import BeautifulSoup
from slugify import slugify
import settings

def download_material(session, material):
    """Called from a course
    """
    result = session.get(settings.GeneralConfig.BASEURL + material['url'])
    c = result.content
    soup_material = BeautifulSoup(c,'lxml')
    title = material['name']
    slug = slugify(title)

    print("      ----Downloading material: ", title, material['material_type'])
    if material['material_type'] == 'video':
        download_material_video(session,soup_material,slug)
    else:
        download_material_html(session,soup_material,slug)
    print("Download complete")

def download_material_html(session, soup_material,slug):
    lecture = re.findall('(<section class="DiscusionDetail".*?)<!-- <script src="', str(soup_material), re.DOTALL)
    with open(slug + '.html', 'w') as f:
        f.write('<html><body>')
        f.write(lecture[0])
        f.write('</body></html>')

def download_material_video(session, soup_material,slug):
    script = soup_material.find('script', text=re.compile('data ='))
    m = re.findall ('"hls": "(.*?)\"', script.string, re.DOTALL)
    for video in m:
        cmd = 'ffmpeg -i {} -c copy -bsf:a aac_adtstoasc {}.mp4'.format(video, slug)
        process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        error_encontrado = process.stderr.read()
        process.stderr.close()
        listado = process.stdout.read()
        process.stdout.close()
        if not error_encontrado:
            break
        else:
            print('Error in the download. Check {}'.format(slug))
            # take note that there may exist a corrupted file, downloaded in half


###################################
def download_material_from_url(session, url):
    """Called directly from main
    """
    os.chdir('Downloads/Singles')
    with open(settings.GeneralConfig.ROOT_DIR + '/Downloads/downloaded.json') as json_file:
        downloaded_courses = json.load(json_file)
        for val in downloaded_courses['singles'].values():
            if val[2] == url:
                print "Material already downloaded"
                return

    result = session.get(url)
    c = result.content
    soup_material = BeautifulSoup(c,'lxml')
    #print(soup_material.prettify())
    material_title = soup_material.title.contents[0].encode('utf-8').strip()
    material_slug = slugify(material_title)

    # Find the material_id
    script_material = soup_material.find('script', text=re.compile('data ='))
    course_title = re.search(r'^\s*header: {\s*title: "(.*?)",$',script_material.string, flags=re.DOTALL | re.MULTILINE).group(1)
    material_id = re.search(r'^\s*material_id: (.*?),$',script_material.string, flags=re.DOTALL | re.MULTILINE).group(1)
    course_slug = slugify(course_title)

    #Let's see if it's a video or a lecture
    lecture = re.findall('(<section class="DiscusionDetail".*?)<!-- <script src="', str(soup_material), re.DOTALL)
    videos = re.findall('"hls": "(.*?)\"', str(soup_material), re.DOTALL)

    material_type = 'lecture' if lecture else 'videos'
    print("      ----Downloading material: ", material_title, material_type)
    if lecture:
        download_material_html(session,soup_material,material_slug)
    elif videos:
        download_material_video(session,soup_material,material_slug)
    print("Download complete.")

    # Save the download information
    try:
        with open(settings.GeneralConfig.ROOT_DIR + '/Downloads/downloaded.json') as json_file:
            downloaded_courses = json.load(json_file)
    except IOError:
        #creamos estructura vacía, con singles = materiales sueltos
        downloaded_courses = {'singles':{}}
        #    pass #aun no se creo descargados.json
    except ValueError:
        print 'json error, delete file "downloaded.json" and the downloads will restart.'
        sys.exit()

    downloaded_courses['singles'][material_id] = [course_slug, material_slug,url]
    with open(settings.GeneralConfig.ROOT_DIR + '/Downloads/downloaded.json', 'w') as outfile:
        json.dump(downloaded_courses, outfile)
