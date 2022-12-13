from goose3 import Goose


url = "https://goose3.readthedocs.io/en/latest/index.html"
url = "https://en.wikipedia.org/wiki/Reinforcement_learning"
url = "https://medium.com/analytics-vidhya/abstractive-text-summarization-430901a602c0"
url = "https://arxiv.org/pdf/2108.03350.pdf"
url = "https://lilianweng.github.io/lil-log/contact.html"
url = "https://web.stanford.edu/group/pdplab/pdphandbook/handbookch10.html"
url = "https://medium.com/war-is-boring/the-u-s-air-force-once-sent-drones-on-daring-suicide-missions-over-vietnam-cd2895cc0c8b"
url = "https://www.tutorialspoint.com/How-to-print-all-the-keys-of-a-dictionary-in-Python"
url = 'http://fox13now.com/2013/12/30/new-year-new-laws-obamacare-pot-guns-and-drones/'
g = Goose()
article = g.extract(url=url)

print(f"\nTitle:\n{article.title}")
#print(f"Description: {article.meta_description}")
print(f"\nClean Text:\n{article.cleaned_text}\n")


