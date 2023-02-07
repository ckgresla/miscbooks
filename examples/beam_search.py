# Simple Beam Search (decoding Tokens/Words from the output of a LLM)
# Taken from- https://machinelearningmastery.com/beam-search-decoder-natural-language-processing/

from math import log
import numpy as np


# beam search --> simple magic for tracking likely sequences of text and using the most likely as the "model output" (more like generation)
def beam_search_decoder(data, k):
    """
    Given an array of arrays (model output) and k sequences to evaluate, run beam search to find the best sequence from the set of model outputs

    """
    sequences = [[list(), 0.0]] #k sequences of words, @ start of process we have nothing to really work with (or no seqs. to evaluate between so it gets initialized as an empty list )
    # For Each Network Output (forward pass's outputed logits = row in the array of arrays that is data)
    for row in data:
        all_candidates = list() #possible & likely continuations of the sequence
        # expand each current candidate
        for i in range(len(sequences)):
            seq, score = sequences[i] #select a sequence from list of possible & likely seqs
            for j in range(len(row)):
                candidate = [seq + [j], score - log(row[j])] #check continuing the sequence with each word in output vec (only most likely get kept)
                all_candidates.append(candidate) 
        # order all candidates by score --> take the top k best tokens (that are continuations of the sequence of tokens)
        ordered = sorted(all_candidates, key=lambda tup:tup[1])
        # select k best
        sequences = ordered[:k]

    return sequences




# Sample Data --> a "Sequence" of Model Outputs (one vector of "Vocab" probs per generation, model predicts next token occurence)  
data = [
        [0.1, 0.2, 0.3, 0.4, 0.5],
        [0.5, 0.4, 0.3, 0.2, 0.1],
        [0.1, 0.2, 0.3, 0.4, 0.5],
        [0.5, 0.4, 0.3, 0.2, 0.1],
        [0.1, 0.2, 0.3, 0.4, 0.5],
        [0.1, 0.2, 0.3, 0.2, 0.2],
        [0.1, 0.2, 0.3, 0.4, 0.5],
        [0.5, 0.4, 0.3, 0.2, 0.1],
        [0.1, 0.2, 0.3, 0.4, 0.5],
        [0.5, 0.4, 0.3, 0.2, 0.1]
        # Output Logits, greedy decoding just takes argmax from each "row" in the outputs from the net
]

results = beam_search_decoder(data, 3)


for reasonable_sequence in results:
    print(reasonable_sequence)
