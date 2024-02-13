#!/usr/bin/python3

from bs4 import BeautifulSoup
import re
import requests
from urllib.parse import urljoin,urlparse
import sys
import select
from argparse import ArgumentParser,RawTextHelpFormatter
import os


def validateJS(name: str) -> bool:
	"""
	returns True if the file extension is .js in URL
	"""
	if os.path.splitext(urlparse(name).path)[1].lower() == ".js": 
		return True
	else :
		return False


def isAbsolute(url:str ) -> bool:
	"""
	returns True if the URL be an absolute URL and it has a valid scheme
	"""
	schemes = ["http", "https"]
	if bool(urlparse(url).netloc): 
		if urlparse(url).scheme in schemes:
			return True
	return False


def extractUrls(html: str) -> list:
	"""
	extract URLs from an html file then returns a list contains URLs
	"""
	regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|(([^\s()<>]+|(([^\s()<>]+)))))+(?:(([^\s()<>]+|(([^\s()<>]+))))|[^\s`!()[]{};:'\".,<>?«»“”‘’]))"
	matches = re.findall(regex,html)
	return [url[0] for url in matches]


def htmlFetcher(url: str) -> str:
	"""
	send request to a URL then returns response body
	"""
	headers = {
		"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
	}
	response = requests.get(url,headers=headers)
	return response.content.decode()


def htmlParser(html: str,baseUrl=None):
	"""
	gets html and extracts the JS files
	baseUrl -> It used to convert a relative URL to an absolute URL
	"""
	jsFiles = set()
	bs = BeautifulSoup(html, 'html.parser')
	
	scripts = bs.findAll('script')
	for script in scripts :
		try :
			jsFiles.add(script['src'])
		except KeyError:
			pass

	links = bs.findAll('link')	
	for link in links :
		try :
			jsFiles.add(link['href']) if validateJS(link['href']) else None
		except KeyError: 
			pass

	extractedUrls = extractUrls(html)
	for i in extractedUrls :
		i = i.strip('"')
		i = i.strip("'")
		try :
			jsFiles.add(i) if validateJS(i) else None
		except KeyError:
			pass

	for jsPath in jsFiles :
		if isAbsolute(jsPath) :
			print(jsPath)
		else :
			print(urljoin(baseUrl,jsPath))


def main():

	parser = ArgumentParser(
		prog="jsCollector",
        description='JavaScript Collector Tool',
        epilog='Examples :\r\n\tjsCollector.py -u https://example.com\r\n\tjsCollector.py -u https://example.com/index.html,https://example.com/admin.html\r\n\tjsCollector.py -f index.html\r\n\tcat index.html | jsCollector.py',
        formatter_class=RawTextHelpFormatter
	)

	parser._optionals.title = 'Options'
	group = parser.add_mutually_exclusive_group()
	group.add_argument("-u", "--url", metavar="url", help="target URLs to fetch html(seperate by ,)")
	group.add_argument("-f", "--file", metavar="file", help="html file")
	parser.add_argument("-v", "--version", action="version", version='%(prog)s 1.0')
	args = parser.parse_args()

	if select.select([sys.stdin, ], [], [], 0.0)[0]:
	    htmlParser(sys.stdin.read())
	else :
		if args.url is not None:
			urls = args.url.split(',')
			for url in urls :
				htmlParser(htmlFetcher(url),url)
		elif args.file is not None:
			with open(args.file) as inputFile:
				content = inputFile.read()
				htmlParser(content)


if __name__ == "__main__":
	main()
 
