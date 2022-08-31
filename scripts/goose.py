from goose3 import Goose


url = "https://goose3.readthedocs.io/en/latest/index.html"
url = "https://en.wikipedia.org/wiki/Reinforcement_learning"
url = "https://medium.com/analytics-vidhya/abstractive-text-summarization-430901a602c0"
url = "https://arxiv.org/pdf/2108.03350.pdf"
url = "https://lilianweng.github.io/lil-log/contact.html"
url = "https://lilianweng.github.io/lil-log/contact.html"
url = "https://web.stanford.edu/group/pdplab/pdphandbook/handbookch10.html"
url = "https://medium.com/war-is-boring/the-u-s-air-force-once-sent-drones-on-daring-suicide-missions-over-vietnam-cd2895cc0c8b"
g = Goose()
article = g.extract(url=url)

print(f"Title: {article.title}")
#print(f"Description: {article.meta_description}")
print(f"Clean Text: {article.cleaned_text}")


