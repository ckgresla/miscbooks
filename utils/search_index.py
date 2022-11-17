# Util to Construct, Update and Query a User's (inverted) Search Index -- brain stuff


import time
import json
import nltk
from collections import defaultdict


class SearchIndex():

    inverse_index = None

    # Write Webpage Content to JSON
    def write_content(self, url=None, title=None, summary=None, token_counts=None, embedding=None, webpage_content_type=None):
        """
        Assuming PDF & TextWebpage JSONs look like:
        { "http://<THE-URL-FOR-THE-CONTENT>" : {
            "TIMESTAMP" : utc timestamp,                        #rounded ms since epoch
            "TITLE" : webpage_title,                            #title as per DOM/url if no title tags or PDF tags
            "SUMMARY" : ["summary1", ...],                      #array of summary strings
            "TOKEN_COUNTS" : token_counts,                      #Dict of {token : count} -- for unique tokens in article (stops removed)
            "EMBEDDING" : [0.1, 2.65, -0.9, ....]   #Document Level embedding
            }
        }
        """

        if url==None:
            print("No URL Provided, Need URL to Create Entry")
            return

        # user_data_json = "articles.json"
        timestamp = int(time.time()*1000) #UTC time in ms

        # content = url : {timestamp, title, summary, keyphrases} #need finalize for dict

        # Map Content to Schema/Collection of Same Files
        if webpage_content_type == "application/pdf":
           user_data_json = "pdfs.json"
        elif webpage_content_type == "text/html":
            user_data_json = "webpages.json"

        # Open Article Content JSON
        with open(user_data_json, "r") as f:
            file = json.load(f)
            # print(f"current time = {timestamp}")
            # print(file)
            # print(type(file)) #dict
            f.close()

        file[url] = {"TIMESTAMP" : timestamp,
                     "TITLE" : title,
                     "SUMMARY" : summary,
                     "TOKEN_COUNTS" : token_counts,
                     "EMBEDDING" : [1, 2, 3], #testing Embedding models
                    }

        # Save Article JSON after Update
        with open(user_data_json, "w") as f:
            file = json.dumps(file, indent=4)
            f.write(file)
            f.close()

        return

    # Clean Up input summary statements
    def tokenize_sequence(self, input_text):
        tokenized_text = nltk.tokenize.word_tokenize(input_text)
        tokenized_text = [token.lower() for token in tokenized_text if token.isalpha()] #make lowercase & remove punctuation
        return tokenized_text

    # Assemble Inverse Index from List of Strings (Corpus)
    def create_inverse_index(self, corpus):
        inv_ind = defaultdict(dict) #word-level inverse index
        stops = set(nltk.corpus.stopwords.words("english"))
        tokenized_docs = []
    
        for i, doc in enumerate(corpus):
            # print(doc)
            # doc = [i.strip() for i in doc.split("-") if i != ""]
            # doc = " ".join(doc)
            doc = self.tokenize_sequence(doc) #returns list of tokens as they appear in original text (stops, lowercased and punctuation removed)
            tokenized_docs.append(doc)
    
            # print(doc)
    
            for j, token in enumerate(doc):
                if token in stops:
                    continue
                if (token in inv_ind) & (i in inv_ind[token]):
                    inv_ind[token][i].append(j) #which doc in corpus and which token in that document (positional info required)
                else:
                    inv_ind[token][i] = []
                    inv_ind[token][i].append(j)

        # Set Created Index to Class Default
        self.inverse_index = inv_ind
        return

    def record_level_query(self, query):
        result = set() #list of sequences (document & token occurence) matches for the query
        query = query.lower().split()

        for token in query:
            if token in self.inverse_index:
                if len(result) == 0:
                    result.update(self.inverse_index[token].keys())
                else:
                    result.intersection_update(self.inverse_index[token].keys())

        if len(result) != 0:
            return result
        else:
            return "No Matches"



# Test Case
if __name__ == "__main__":
    import json 

    # Read in Sample Data -- testing w text/html corpora
    with open("webpages.json", "r") as f:
        data = json.load(f)

    corpus = []
    for i in data.keys():
        corpus.append(" ".join(data[i]["SUMMARY"]))
    
    si = SearchIndex()
    si.create_inverse_index(corpus) #assemble an inverted index from a given corpus

    # Make a Query
    query_string = "optimization"
    res = si.record_level_query(query_string)
    print(f"Relevant Documents for Query: {query_string}")
    print(res)
