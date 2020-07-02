#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cached_url
from bs4 import BeautifulSoup
import yaml
import time
import os
from telegram_util import compactText

chapter_prefix = 'https://www.gongzicp.com/novel/getChapterList?nid='
detail_prefix = 'https://www.gongzicp.com/read-%s.html'
content_anchor = 'content: "'
novel_anchor = 'novelName: "'

with open('credential') as f:
	credential = yaml.load(f, Loader=yaml.FullLoader)

def getNid(url):
	return url.split('-')[-1].split('.')[0]

def getIds(content):
	for item in content['data']['list']:
		cid = item.get('id')
		if cid:
			yield cid

def getContent(raw_content, debug_info = None):
	try:
		content = raw_content.split(content_anchor)[1].split('",')[0]
	except Exception as e:
		print(debug_info)
		return ''
	soup = BeautifulSoup(content.replace('\/', '/'), 'html.parser')
	for item in soup.find_all('p'):
		if 'hidden' in str(item.attrs):
			item.decompose()
	content = soup.text.encode().decode('unicode-escape')
	return content.replace('\r', '\n')

def getNovelName(raw_content):
	novel_name = raw_content.split(novel_anchor)[1].split('",')[0]
	return novel_name.encode().decode('unicode-escape')

def download(url, force_cache = False):
	nid = getNid(url)
	content = cached_url.get(chapter_prefix + nid, force_cache = force_cache)
	content = yaml.load(content, Loader=yaml.FullLoader)
	novel_name = None
	result = []
	for cid in getIds(content):
		raw_content = cached_url.get(
			detail_prefix % cid, 
			force_cache = True,
			sleep = 1)
		if not novel_name:
			novel_name = getNovelName(raw_content)
			os.system('mkdir download > /dev/null 2>&1')
		result.append(getContent(raw_content, debug_info = detail_prefix % cid))
	with open('download/%s.txt' % novel_name, 'w') as f:
		f.write(compactText(''.join(result)))
	# TODO
	# if there is need, automatically send to kindle
	
if __name__ == "__main__":
	download('https://www.gongzicp.com/novel-22108.html', force_cache = True)