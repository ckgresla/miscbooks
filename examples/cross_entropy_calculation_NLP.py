# Example of Calculating the Cross Entropy in an NLP/Token Prediction sort of context
# Taken from- https://stackoverflow.com/questions/22933412/why-can-we-use-entropy-to-measure-the-quality-of-language-model
import random
from math import log


def cross_entropy(prediction_probabilities: list):
    """ Negative log likelihood """
    probs = list(prediction_probabilities)
    return -sum(log(p, 2) for p in probs) / len(probs)

def predictions(sequence, model):
    """ Forward Pass/Predictions on instances in a sequence """
    for item in sequence:
        yield model[item]

# n_instances = 2 #number of random characters to generate --> will return very wrong entropies!
n_instances = 100000 #number of random characters to generate  --> more correct entropy values, since more examples of generating distribution
# @ lower numbers of instances  we can get incorrect entropies, (i.e; incorrect token probabilities have lower entropy), but as n_samples increases entropy vals become correct
random_characters = [random.choice(['a', 'b']) for _ in range(n_instances)]

def print_entropy(m):
    print(f"Cross Entropy of {m}: {cross_entropy(predictions(random_characters, m))}")

# Evaluate the cross entropies of the prior probs
token_probs_1 = {"a": 0.5, "b": 0.5} #lower entropy, since probabilities of token are closer to the generating distribution!
print_entropy(token_probs_1)

token_probs_2 = {"a": 2./3, "b": 1./3} #higher entropy, token probabilities are farther from generating distribution (more confusion & more disorder)
print_entropy(token_probs_2)

token_probs_3 = {"a": 0.9, "b": 0.1} #higher entropy, token probabilities are farther from generating distribution (more confusion & more disorder)
print_entropy(token_probs_3)
