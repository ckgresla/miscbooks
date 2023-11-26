"""
Calculating perplexity and entropy in python

Useful Sources
* Blog from which this math was taken- http://blog.echen.me/2021/12/23/a-laymans-introduction-to-perplexity-in-nlp/
* https://www3.nd.edu/~dchiang/teaching/nlp/2016/notes/chapter5v5.pdf
* Clean explanation of the Cross Entropy Loss- https://datascience.stackexchange.com/questions/20296/cross-entropy-loss-explanation
"""

import numpy as np


logits = np.random.normal(loc=-8, scale=8, size=(8)) #say vocab/output dist of 8 vals
# probs = np.array([1/6] * 6) 
softmax = lambda x: np.exp(x) / np.sum(np.exp(x), axis=0)
probs = softmax(logits)
print(sum(probs)) #probability distribution, since sum of probs = 1
print(probs)


surprisal = -np.log2(probs)
print(surprisal)

entropy = -np.sum(probs * np.log2(probs)) 
print(entropy)

perplexity = np.exp2(entropy)
print(perplexity)
