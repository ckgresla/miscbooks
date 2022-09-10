# Bloom Embeddings Post- https://explosion.ai/blog/bloom-embeddings
# Relates somewhat to the "Bloom Filter" concept in Probability– https://en.wikipedia.org/wiki/Bloom_filter
# Effectively the technique is a space efficient and reasonsably accurate method for creating Embeddings (probabilistic in nature, leverages multiple hashes to spread out semantic meaning across vectors, as opposed to having a single long vector per unique token)

import mmh3 #i.e. "MurmurHash3" an library used for creating hashes, quickly
import numpy as np
from pprint import pprint


# Random Mapping 10 Vectors out of 100 (Track 90 Uniques, all other knows get placed somewhere in last 10 vecs)
def get_row(word_id, number_vectors=100, number_oov=10):
    number_known = number_vectors - number_oov #`number_oov` refers to the number of vectors reserved for "Out Of Vocabulary" Words/Tokens
    if word_id < number_known:
        return word_id #case for a Known Word Token (in vocabulary)
    else:
        return number_known + (word_id % number_oov) #case for an unknown token, gets assigned to one of the randon Vectors
    # Bloom Embeddings are the above carried out in the limit, that is instead of saving a subset of the Vectors for unknown tokens we instead save ALL word vectors as randoms
    # The power or magic of this technique, comes from the fact that adding multiple hashes (mappings for unique tokens to vectors) leads to approximating all unique values/vecs for all tokens, even if we have less vectors than we have tokens (random assignments are less likely to overlap with each additional hash, approximating the Unique Vector in the limit whilst keeping space smaller)


# Main Functions
def allocate(n_vectors, n_dimensions):
    table = np.zeroes((n_vectors, n_dimensions), dtype="f") #dtype="f" just means floating point in np
    table += np.random.uniform(-0.1, 0.1, table.size).reshape(table.shape) #add random noise & keep same shape (instantiation step)
    return table

def get_vector(table, word):
    hash1 = mmh3.hash(word, seed=0)
    hash2 = mmh3.hash(word, seed=1)

    row1 = hash1 % table.shape[0]
    row2 = hash2 % table.shape[0]
    return table[row1] + table[row2] #returns the unique-ish vector for a word, probability of Uniqueness increases with number of hashes! (and therefore possible vecs)

def update_vector(table, word, d_vector):
    # Same Strat for the update step, same seeds & modulo operation lead to the same unique id (effectively)
    hash1 = mmh3.hash(word, seed=0)
    hash2 = mmh3.hash(word, seed=1)

    row1 = hash1 % table.shape[0]
    row2 = hash2 % table.shape[0]

    # Update Vector in Table, in-place (no return)
    table[row1] -= 0.001 * d_vector
    table[row2] -= 0.001 * d_vector




# Toy Example (20 words, embedding them in 2 dimensions) -- Vector Table Shape = (20, 2)
vocab = ['apple', 'strawberry', 'orange', 'juice', 'drink', 'smoothie',
         'eat', 'fruit', 'health', 'wellness', 'steak', 'fries', 'ketchup',
         'burger', 'chips', 'lobster', 'caviar', 'service', 'waiter', 'chef'] #len=20


# Normal Method -- canonical way of representing word embeddings
normal = np.random.uniform(-0.1, 0.1, (20, 2)) #table shape is (20, 2) -- all unique words map to unique vectors 

word2id = {}
def get_normal_vector(word, table):
    if word not in word2id:
        word2id[word] = len(word2id) #assign tokens to words based on number of keys at time of adding (all become unique IDs)
    return normal[word2id[word]]


# Bloom Method -- what we are doing here (only 1 hash value for 1st example)
hashed = np.random.uniform(-0.1, 0.1, (15, 2))
hashes1 = [mmh3.hash(w, 1) % 15 for w in vocab] #hash creates a arbitrary random int for each word in the vocab
assert hashes1 == [3, 6, 4, 13, 8, 3, 13, 1, 9, 12, 11, 4, 2, 13, 5, 10, 0, 2, 10, 13]

# Visualize Assignment made to Hash Dict
hash_dict = {}
for i in range(0, 15):
    hash_dict[i] = []

for j in range(0, len(hashes1)):
    hash_dict[hashes1[j]].append(vocab[j])

print(f"\nHash Dictionary 1:")
pprint(hash_dict)
#this method doesn't make use of all the indicies available in range(0, 15) and doubles up on a few (two words share a same index), can do better assignment w a second Hash! (leveraging a different seed!)

# Adding a Second Hash Value, w a different seed
from collections import Counter
hashes2 = [mmh3.hash(w, 2) % 15 for w in vocab]
print(len(Counter(hashes2).most_common())) #12 is the most common val!

for j in range(0, len(hashes2)):
    hash_dict[hashes2[j]].append(vocab[j])

print(f"\nHash Dictionary 2:")
pprint(hash_dict)

# Check Number of Uniques after second Hash
print(len(Counter(zip(hashes1, hashes2))) == 20) #number of unique combinations after 2 hashes equals the num of unique tokens! (using less vectors normal case!)


# Adding the Unique Vectors together results in a Unique Combination
print("\nUnique Vecs:")
for word in vocab:
    k1 = mmh3.hash(word, 0) % 15
    k2 = mmh3.hash(word, 1) % 15
    vector = hashed[k1] + hashed[k2] #unique combination of two randomized vecs per unique token!
    print(word, '%.3f %.3f' % tuple(vector))




# Learn Vectors that are closer to the "Actual" Semantic meaning (instead of randomized, for this toy example we Simulate reality but main idea holds)
print("\n\nGradient Descent to Learn Vectors: ")
np.random.seed(0)

nb_epoch = 200 #steps of update for learning "True" Vectors
learn_rate = 0.001
nr_hash_vector = 15 #adding more vecs increases loss in short term but makes for better long-term learning (if many more epochs can "learn" more about Truth)

words = [str(i) for i in range(20)] #20 unique "words"
true_vectors = np.random.uniform(-0.1, 0.1, (len(words), 2)) #twenty unique vecs, "Ground Truth" in this simulation
hash_vectors = np.random.uniform(-0.1, 0.1, (nr_hash_vector, 2)) #15 (specified in above) unique vecs, Bloom way of approximating the Ground Truth
examples = list(zip(words, true_vectors))

for epoch in range(nb_epoch):
    np.random.shuffle(examples)
    loss = 0.0
    for word, truth in examples:
        key1 = mmh3.hash(word, 0) % nr_hash_vector
        key2 = mmh3.hash(word, 1) % nr_hash_vector
        # key3 = mmh3.hash(word, 42) % nr_hash_vector

        # hash_vector = hash_vectors[key1] #case when key2 is ignored, loss tends to go up since not getting full unique combos!
        hash_vector = hash_vectors[key1] + hash_vectors[key2]
        # hash_vector = hash_vectors[key1] + hash_vectors[key2] + hash_vectors[key3] #additional key (3 dims not 2)

        diff = hash_vector - truth

        hash_vectors[key1] -= learn_rate * diff
        hash_vectors[key2] -= learn_rate * diff
        # hash_vectors[key3] -= learn_rate * diff
        loss += (diff**2).sum() #sum of squared errors, Euclidean
    print(epoch, loss)

