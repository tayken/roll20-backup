#!/usr/bin/env python3

import base64
import os
import re
import requests

from bs4 import BeautifulSoup
from dotenv import dotenv_values
from markdownify import markdownify as md


config = dotenv_values('.env')
campaign_id = config['CAMPAIGN_ID']
output_folder = config['OUTPUT_FOLDER']

base_url = 'https://app.roll20.net'
forum_url = f'{base_url}/campaigns/forum/{campaign_id}/'

if not os.path.isdir(output_folder):
    print("Output folder doesn\'t exist, creating.")
    os.mkdir(output_folder)

forum = requests.get(forum_url)
soup = BeautifulSoup(forum.content, 'html.parser')
posts = soup.find(class_='postlistings').find_all('a')

for post in posts:
    post_url = f'{base_url}{post.get("href")}'
    post_id = post_url.split('/')[-2]
    post_title = post.get_text()
    filename = f'{post_id} - {post_title}.md'
    file_path = f'{output_folder}/{filename}'
    if os.path.exists(file_path):
        print(f'{post_title} already downloaded, skipping.')
    else:
        print(f'Downloading -> {post_title}')

        post_req = requests.get(post_url)
        base = re.findall(r'decode\(\".*\"\)', post_req.text)[0]
        base = re.sub(r'\"\).*$', '', base.replace('decode("', ''))
        decoded = base64.b64decode(base)

        with open(file_path, 'w') as f:
            f.write(md(decoded))
