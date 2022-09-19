# Text Parser for Websites- https://github.com/codelucas/newspaper
# need do a `pip3 install newspaper3k` to get it in the env (also need run w python3)
from newspaper import Article

url = 'https://en.wikipedia.org/wiki/Reinforcement_learning'
url = 'http://fox13now.com/2013/12/30/new-year-new-laws-obamacare-pot-guns-and-drones/'
url = 'https://brain.ai'


article = Article(url)

article.download()
article.parse()
info = [article.authors, article.title, article.text]

for i in info:
	print(i, "\n\n")


#print(dir(article))
