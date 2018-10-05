import requests
from bs4 import BeautifulSoup
import shutil
import datetime
import os.path
from appscript import app, mactypes

nasa_apod_base_url = 'https://apod.nasa.gov/apod/'
nasa_apod_html_url = nasa_apod_base_url + 'astropix.html'

image_download_path = 'images/'

"""
Downloads image from http url
@param image_url: HTTP url image path
@param image_name: Name to be used for saving images
"""
def download_image_from_path(image_url, image_name):
    image_response = requests.get(image_url, stream=True)
    with open(image_download_path + image_name, 'wb') as out_file:
        shutil.copyfileobj(image_response.raw, out_file)
    del image_response

"""
Sets image as mac desktop wallpaper
@param image_path: Path of image on disk
"""
def set_mac_desktop_wallpaper(image_path):
    app('Finder').desktop_picture.set(mactypes.File(image_path))

"""
Create uniue image name using timestamp
"""
def get_image_name_for_today():
    date_string = datetime.datetime.now().strftime("%Y_%m_%d")
    image_name = 'img_' + date_string + '.png'
    return image_name

"""
Extracts image HTTP url from from nasa_apod_base_url
"""
def get_image_path_from_html():
    r = requests.get(url=nasa_apod_html_url)
    if r.status_code == 200:
        html_doc = r.text
        soup = BeautifulSoup(html_doc, 'html.parser')
        image_url = nasa_apod_base_url + soup.find('img')['src']
        return image_url
    else:
        return ''


def main():
    image_name = get_image_name_for_today()
    if not os.path.exists(image_download_path + image_name):
        image_url = get_image_path_from_html()
        download_image_from_path(image_url, image_name)
    set_mac_desktop_wallpaper(image_download_path + image_name)
    print datetime.datetime.now() ,"=> Wallpaper Changed:", image_name


if __name__ == '__main__':
    main()
