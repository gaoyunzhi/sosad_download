#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cached_url
from bs4 import BeautifulSoup
from telegram_util import compactText

def findLinks(soup):
	for x in soup.find_all('a', class_='sosad-button'):
		yield x['href']

def getSoup(url, force_cache = True):
	return BeautifulSoup(cached_url.get(
		url, force_cache = force_cache), 'html.parser')

def getText(link):
	sub_soup = getSoup(link, force_cache = True)
	main_content = sub_soup.find('div', class_='main-text')
	if not main_content:
		print(link)
		return ''
	for att in ['font-4', 'text-left']:
		item = main_content.find('div', class_=att)
		if item:
			item.decompose()
	return sub_soup.find('div', class_='main-text').get_text(separator='\n')

def download(url, force_cache = False):
	soup = getSoup(url, force_cache = force_cache)
	novel_name = soup.find('title').text.split()[0]
	result = []
	for link in findLinks(soup):
		result.append(getText(link))
	with open('download/%s.txt' % novel_name, 'w') as f:
		f.write(compactText(''.join(result)))
	
if __name__ == "__main__":
	download('https://sosad.fun/threads/64040/profile', force_cache = True)