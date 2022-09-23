# Script for Getting the DOM's Text for a URL w Beautiful Soup

import urllib.request
from bs4 import BeautifulSoup

url = 'http://www.google.com'
url = 'https://brain.ai/#/'
url = 'https://github.com/codelucas/newspaper'

if __name__ == "__main__":
	site = urllib.request.urlopen(url).read()
	soup = BeautifulSoup(site, "html.parser")
	print("PAGE TITLE:\n", soup.title.string)
	print("SOUP PRETTIFIED:\n", soup.prettify())
	print("TEXT:\n", soup.get_text())


