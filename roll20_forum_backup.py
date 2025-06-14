#!/usr/bin/env python3

import base64
import os
import re
import requests

from bs4 import BeautifulSoup
from dotenv import dotenv_values
from markdownify import markdownify as md


base_url = 'https://app.roll20.net'


def download_post(post_url, file_path):
    post_req = requests.get(post_url)
    decoded = bytes()
    entries = re.findall(r'decode\(\".*\"\)', post_req.text)
    for entry in entries:
        entry = re.sub(r'\"\).*$', '', entry.replace('decode("', ''))
        decoded += base64.b64decode(entry)

    with open(file_path, 'w') as f:
        f.write(md(decoded))


def parse_forum_page(page_url, output_folder, min_post_id):
    forum_page = requests.get(page_url)
    soup = BeautifulSoup(forum_page.content, 'html.parser')
    posts = soup.find(class_='postlistings').find_all('a')

    next_page = None
    if soup.find(class_='nextpage'):
        next_page = soup.find(class_='nextpage').find_all('a')[0].get('href')

    for post in posts:
        post_url = f'{base_url}{post.get("href")}'
        post_id = post_url.split('/')[-2]
        post_title = post.get_text()

        filename = f'{post_id} - {post_title}.md'
        file_path = f'{output_folder}/{filename}'

        if int(post_id) < min_post_id:
            print('Reached earliest post, stopping.')
            next_page = None
            break
        elif os.path.exists(file_path):
            print(f'"{post_title}" is already downloaded, skipping.')
        else:
            print(f'Downloading -> {post_title}')
            download_post(post_url, file_path)

    if next_page:
        page_url = f'{base_url}{next_page}'
        parse_forum_page(page_url, output_folder, min_post_id)


def main():
    config = dotenv_values('.env')
    campaign_id = config.get('CAMPAIGN_ID')
    output_folder = config.get('OUTPUT_FOLDER')
    min_post_id = int(config.get('MIN_POST_ID', 0))

    if not os.path.isdir(output_folder):
        print("Output folder doesn\'t exist, creating.")
        os.mkdir(output_folder)

    forum_url = f'{base_url}/campaigns/forum/{campaign_id}/'
    parse_forum_page(forum_url, output_folder, min_post_id)


if __name__ == '__main__':
    main()
