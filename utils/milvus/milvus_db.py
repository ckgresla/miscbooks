# Utils to Spinup & Work with a Milvus Vector DB
# Milvus Documentation- https://pymilvus.readthedocs.io/en/latest/tutorial.html

import requests
import time
import numpy as np
from tqdm import tqdm
from milvus import Milvus, IndexType, MetricType, Status

from alexandria_utils.data import *


# Connect to the Server (running in Docker Presumably)
host = 'localhost'
port = '19530'

mlvs = Milvus(host=host, port=port)

# Embedding Model Endpoint
EMBEDDING_MODEL_URL = "http://192.168.1.26:5003/e-lf" #could settle this on SageMaker?




# Upload Single Instance of Data to Vector DB
def upload_text(collection_name: str=None, document_text: str=None, unique_id: int=None, norm_vec=False, partition_name: str=None):
    """
    Upload a single document string and UID to a Specified Collection/Partition in Milvus

    Parameters
        collection_name: str, the name of the collection to insert the vector into (presumably kept per User)
        document_text: str,  the text to compute an embedding for and then upload to MLVS
        unique_id: int, the 64bit unique Integer ID for the Document
        norm_vec: boolean, whether or not to normalize the vector, only normalize if the Milvus Metric is `Inner Product`
        partition_name: str, specific name of partition within the collection -- for Alexandria these might be the `doc_types`
    """
    assert collection_name != None and collection_name != "", "Collection Name must be Specified -- where would we put the Vector?"
    unique_id = int(unique_id) #confirm this is an int, will not place nice otherwise

    # Get the Embedding for the Text + Format for Milvus
    doc_vec = get_embedding(document_text, normalize=norm_vec)
    doc_vec = np.array(doc_vec, dtype=float)
    doc_vec = doc_vec.reshape(1, 768) #need to add 1 extra dim for milvus
    unique_id = [unique_id] #needs be a list of ints...


    # Add to Specific Partition within Collection
    if partition_name:
        start = time.monotonic()
        status_code, _ = mlvs.insert(collection_name=collection_name, records=doc_vec, ids=unique_id, partition_name=partition_name)
        print(f"Inserted 1 Vector into '{collection_name}' inside '{partition_name}'-- took {time.monotonic() - start : .2f}s")
    # Add to General Collection
    else:
        start = time.monotonic()
        status_code, _ = mlvs.insert(collection_name=collection_name, records=doc_vec, ids=unique_id) 
        print(f"Inserted 1 Vector into '{collection_name}' -- took {time.monotonic() - start : .2f}s")

    return status_code


# Upload a Batch of Vectors to the same Collection/Partition
def upload_batch_docs(collection_name: str=None, content_dict=None, norm_vec=False, partition_name: str=None):
    """
    Upload the documents of a schema specific Content JSON to the corresponding Collection/Partition in Milvus

    Parameters
        collection_name: str, the name of the collection to insert the vector into (presumably kept per User)
        content_dict: str or dict, the path to a content dict or the actual dictionary of values
        norm_vec: boolean, whether or not to normalize the vector, only normalize if the Milvus Metric is `Inner Product` 
        partition_name: str, specific name of partition within the collection -- for Alexandria these might be the `doc_types`
    """
    assert collection_name != None and collection_name != "", "Collection Name must be Specified -- where would we put the Vector?"

    # Get Data if Given Path
    if type(content_dict) == str:
        content_dict == get_data(content_dict) #will load in content dict if given a string

    content_dict_ids = list(content_dict.keys()) #the unique ids for each entry in the Content JSON

    # Compute Embeddings & Get UIDs for Upload
    embeddings, uids = [], []
    for uid in tqdm(content_dict_ids):
        txt = content_dict[uid]["SUMMARY"]
        txt = "\n".join(txt).replace("- ", "") #strip bullet points and convert into one long string
        vec = get_embedding(txt, normalize=norm_vec) #get embedding w or w/o unit normalization

        embeddings.append(vec)
        uids.append(content_dict[uid]["UID"]) #get specific UID for the Content, must be an int to play nice w Milvus dtypes
    
    # Convert into Milvus' dtypes --> np.array(of floats) for vecs, ints for uids
    embeddings = np.array(embeddings, dtype=float)
    uids = [int(uid) for uid in uids]
        # Assuming Positional correspondence between UIDs and Vecs

    # Add to Specific Partition within Collection
    if partition_name:
        start = time.monotonic()
        # status_code, _ = mlvs.insert(collection_name=collection_name, records=embeddings, partition_name=partition_name)
        status_code, _ = mlvs.insert(collection_name=collection_name, records=embeddings, ids=uids, partition_name=partition_name)
        print(f"Inserted {len(embeddings)} Vectors into '{collection_name}' inside '{partition_name}'-- took {time.monotonic() - start : .2f}s")
    # Add to General Collection
    else:
        start = time.monotonic()
        status_code, _ = mlvs.insert(collection_name=collection_name, records=embeddings, ids=uids) 
        print(f"Inserted {len(embeddings)} Vectors into '{collection_name}'-- took {time.monotonic() - start : .2f}")

    return status_code


# Compute the Embedding with LongFormer (depending on Endpoint)
def get_embedding(txt, normalize=False):
    """
    Given as Model Endpoint, Compute the Embedding for a String --> presumably with Longformer

    Parameters
        txt: str | list[str], the input text to create an embedding for or the list of strings to get embeddings for (makes use of the batch method)
        normalize: boolean, whether or not to return the normalized embedding (euclidean/l2 norm, unit vector) --> required if using the `IP` distance metric in Milvus
    """
    # TODO: Make the Batch functionality work -- may or may not need depending on SageMaker/Model Deployment
    # if type(txt) == list:
        # request_body = {"batch_text": txt, "normalize_vecs": True}  #different name for data param if making use of the batch

    # If Not Batching, assume that `input_text` is always a single instance (if we did batch this is named differently, for CKG's API)
    if normalize:
        request_body = {"input_text": txt, "normalize_vecs": True} #will return Vectors of Unit Len (sum of output~=1)
    else:
        request_body = {"input_text": txt}

    payload = json.dumps(request_body) 
    headers = {'Content-Type': 'application/json'}

    # POST Text for Embedding Generation
    response = requests.request("POST", EMBEDDING_MODEL_URL, headers=headers, data=payload)
    if response.status_code != 200:
        print(f"Error, Code Given: {response.status_code}")

    # Reshape to nice Size for Output
    vec = np.array(response.json()) #get JSON from Endpoint
    vec = vec.reshape(768) #endpoint has support for batch requests, remove unnecessary dimensions

    return vec


# Search from Text-to-Vec
def text_to_vec(collection_name="", txt="", normalize=False, N=10, out_type="ids", partition_name=None):
    """
    Given a Query, compute the vector for it and find the most similar vectors inside Milvus

    Parameters
        collection_name: str, the name of the collection to insert the vector into (presumably kept per User)
        txt: str, text to find similar vectors for
        normalize: boolean, whether or not to normalize the vector for this Search (depends on the collection we are searching in!)
        N: int, maximum number of results to return
        out_type: str, what type of items to return -- one of; ['ids', 'full', 'res']
        partition_name: str, specific name of partition within the collection -- for Alexandria these might be the `doc_types`
    """
    assert collection_name != None and collection_name != "", "Collection Name must be Specified -- where would we put the Vector?"

    vec = get_embedding(txt, normalize=normalize)
    results = mlvs.search(collection_name, vec, N)

    # Search Milvus
    if partition_name:
        start = time.monotonic()
        results = mlvs.search(collection_name=collection_name, query_records=vec, top_k=N, partition_tags=[partition_name])
        print(f"Search took {time.monotonic - start : .2f}s -- returning {len(results[1][0])}") #using len of first segment of hits for printfo
    # Add to General Collection
    else:
        start = time.monotonic()
        results = mlvs.search(collection_name=collection_name, query_records=vec, top_k=N)
        print(f"Search took {time.monotonic - start : .2f}s -- returning {len(results[1][0])}") #using len of first segment of hits for printfo

    # Parse Return Items
    if out_type == "ids":
        return [results[1][i].id for i in results] #list of IDs per document (in best-first order)
    elif out_type == "full":
        return results #a tuple of (Milvus Status, Milvus Top Query Result)
    elif out_type == "res":
        return [(results[1][i].id, results[1][i].distance) for i in results] #list of Tuples; (id, distance) --> wrt the query embedding


def nuke_db():
    """
    DANGER: this removes everything in a Milvus Instance
    """

    status, values = mlvs.list_collections() 

    for c in values:
        mlvs.drop_collection(c)
    return
