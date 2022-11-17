# ElasticSearch Document Store (Custom Module)

import json
import re
import os
from tqdm import tqdm
from typing import List, Optional, Type, Union, Dict
import numpy as np

from alexandria_utils.data import *

try:
    from elasticsearch import Elasticsearch
    from elasticsearch.client import IndicesClient
    from elasticsearch.helpers import scan
    from elasticsearch.exceptions import RequestError
except (ImportError, ModuleNotFoundError) as ie:
    print(f"Error in `elasticsearch` imports: {ie}")
    print("if Elasticsearch not installed or Not in current Env, install with `pip install elasticsearch`")
    exit(1) #break execution, install the module


# Connector if running a cluster -- from the haystack folks
def prepare_hosts(host, port):
    """
    Create a list of host(s) + port(s) to allow direct client connections to multiple nodes,
    in the format expected by the client.
    """
    if isinstance(host, list):
        if isinstance(port, list):
            if not len(port) == len(host):
                raise ValueError("Length of list `host` must match length of list `port`")
            hosts = [{"host": h, "port": p} for h, p in zip(host, port)]
        else:
            hosts = [{"host": h, "port": port} for h in host]
    else:
        hosts = [{"host": host, "port": port}]
    return hosts


# Custom ES Class -- wrappers for search, connection, insertion, etc.
class ES_Controller(Elasticsearch):
    def __init__(
            self,
            host: Union[str, List[str]] = "localhost",
            port: Union[int, List[int]] = 9200,
            username: str = "",
            password: str = "",
            api_key_id: Optional[str] = None,
            api_key: Optional[str] = None,
            aws4auth=None,
            index: str = "document",
            scheme: str = "http",       # or "https"
            ca_certs: Optional[str] = None,
            verify_certs: bool = True,
            timeout: int = 30,          #time to wait before exiting, if no response from ES
            use_system_proxy: bool = False,
        ):
        
        # Initialize the ES Client (same as in- https://elasticsearch-py.readthedocs.io/en/v8.5.0/api.html#module-elasticsearch)
        super().__init__(
            host=host, #typically "elasticsearch" or "localhost" (depending on if running inside container or locally)
            port=port, #9200
            username=username,
            password=password,
            api_key=api_key,
            api_key_id=api_key_id,
            aws4auth=aws4auth,
            scheme=scheme,
            ca_certs=ca_certs,
            verify_certs=verify_certs,
            timeout=timeout,
            use_system_proxy=use_system_proxy,)

        # Create the Index Manager (and `elasticsearch.client.IndicesClient()`) from- https://elasticsearch-py.readthedocs.io/en/v8.5.0/api.html#indices
        # self.index_manager = Elasticsearch.client.IndicesClient(self)
        self.index_manager = IndicesClient(self)
        self.index = index


    # Healthcheck
    @classmethod
    def alive(cls):
        status = cls().ping()
        print("STATUS: {}".format("Online" if status else "Offline"))
        return


    # Maybe don't need, idea here is to init obj with an index and use that specified one as default for funcs where not provided...
    def current_index(self):
        print(f"Currently using the {self.index}")
        return


    # Get a list of all the Indices available
    def list_indices(self) -> List[str]:
        info = self.indices.get(index="*")
        return list(info.keys()) #list of the index names, passable to self.indicies.get("<NAME>") to work w index


    # Make a New or Overwrite an Existing Index, given a name ()
    def create_index(self, index_name: str, headers: Optional[Dict[str, str]] = None):
        """
        Create a new index for storing documents. In case if an index with the name already exists, prints out that index name and exits
          - Favor Large indices as opposed to creating many Small indcies- https://www.elastic.co/blog/index-vs-type 
        """
        overwrite = False

        # Check if index_name refers to an alias
        if self.indices.exists(index_name):
            ans = input(f"Index: '{index_name}' already exists, would you like to overwrite it? [y/n]: ")
            if (ans == "y") | (ans == "yes") | (ans == "Yes"):
                print("overwriting")
                overwrite = True
                pass
            else:
                print("Exiting w/o overwriting")
                exit(1)

        # Create or Overwrite the Specified Index
        if overwrite:
            # at the moment, here we DELETE and Recreate that same index... perhaps a more elegant way to do this?
            self.index_manager.delete(index=index_name)
            # self.index_manager.create(index=index_name) #old call, using below method for creating instead
            self.indices.create(index=index_name, body=headers)
        else:
            # self.index_manager.create(index=index_name) #old call, using below method for creating instead
            self.indices.create(index=index_name, body=headers)

            return


    # Remove an Index from the DB
    def delete_index(self, index_name: str):
        """
        Delete an existing index. If index name doesn't exist, exit out
        """
        # Check if index_name refers to an alias
        if self.indices.exists(index_name):
            self.index_manager.delete(index_name)
        else:
            print(f"No Index named {index_name}, exiting...")
            exit(1)
        return


    # Upload Index Templates (match any index based on REGEX of their respective names)
    def upload_index_templates(self):
        """
        Uploads all index templates in the "data" directory to ES (will be template backend for any newly created indices)
            - Assumes names of Templates follow pattern: '<NAME>-<TYPE>-template.json'
        """

        # TODO: update this function to handle any EXISTING Templates (give option to overwrite, del existing and add new w same name)

        # Find the Template Files in Data Dir
        contents = os.listdir("data")
        content_string = "\n".join(contents)
        template_files = re.findall("[A-z]*-[A-z]*-template.json", content_string) #all of the template files in the dir dir
        paths = ["data/"+f"{i}" for i in template_files]

        # Upload the Files to ES as Templates -- uses self.index_manager
        for template in paths:
            template_name = template.split("/")[1].split(".")[0].replace("-template", "") #name for storage in ES
            template = get_data(template) #actual template to upload
            self.index_manager.put_index_template(name=template_name, body=template, create=True) #will replace existing templates if same name!
            print("Uploaded {}".format(template_name))

        return


    # Remove all the current templates from ES (stored in "URL_PATH/_index_template")
    def delete_index_templates(self, template_name="*"):
        """
        Clears out all of the index_templates in ES by default, specific deletion if `template_name` provided
        """
        self.index_manager.delete_index_template(template_name)
        print("Index Templates Removed")

        return


    # Util to check what Templates Exist or their Contents
    def list_index_templates(self, template_name="*", names_only=True):
        """
        Prints out a list of all the index templates currently in ES, or if `template_name` specified will check for existence of a specific template name

        Parameters:
            template_name: str, the name of a specified template to check for, else will operate on all (can get the schema with specific name)
            names_only: bool, will return a list of template names if true, else the actual templates themselves (can review)
        """
        # res = self.index_manager.exists_index_template(template_name) #this is just a boolean check
        res = self.index_manager.get_index_template(template_name) #this returns actual templates (can parse)
        print(res)

        # Return a List of Names
        if names_only:
            names_lst = []
            for t in res["index_templates"]:
                # print(t)
                names_lst.append(t["name"])
            return names_lst

        # Return the Whole Documents
        else: 
            return res["index_templates"]


    # Upload Single Content JSON Wrapper
    def upload_document(self, index_name: str, document: Dict, page_type=None):
        """
        Given an Index and a Document (content dict) --> add document to index for search
        """
        if page_type == None:
            print("No 'page_type' given, please provide label for content schema")
            return #exit 

        # Map Content to ES Expected Values
        uid = document["UID"]
        main_content = {
            # "URL": list(document.keys())[0], #adding url as key to the doc dict when adding this way (in function that calls this func)
            "URL": document["URL"],
            "SUMMARY": "\n".join(document["SUMMARY"]),
            "TITLE": document["TITLE"],
            "TIMESTAMP": document["TIMESTAMP"],
            "PAGE_TYPE": page_type,
        }

        self.create(index=index_name, id=uid, body=main_content) #body contains the content we want to store in ES 
        return


    # Upload a Batch of Documents (a full Content JSON)
    def upload_content_json(self, index_name: str, json_path: str, page_type=None):
        """
        Util to upload a batch of Content JSONs to a specified index, wraps the 'upload_document()' function
        
        Parameters:
            index_name: str, name of the index to upload to -- must be specified
            json_path: str, path to the Content JSON to upload (assuming this follows the Alexandria Schema for JSONs)
            page_type: str, one of the supported types: ['application/pdf', 'text/html']
        """
        if page_type == None:
            print("No 'page_type' given, please provide label for content schema")
            return #exit 

        if not self.indices.exists(index_name):
            print(f"No Index: {index_name} -- will create index and add in documents")

        # Iter over Content JSON file & Upload
        docs = get_data(json_path) #get data from local file

        print(f"Uploading contents of '{json_path}' to {index_name}")
        for uid in tqdm(docs):
            doc = docs[uid] #work with one content entry at a time --> UID is now the main key for each entry
            # doc["URL"] = url #below func expects url as a key in the Doc (not as the unique ind) --> url no longer main key, is an attribute
            self.upload_document(index_name, doc, page_type)
        print("Document Uploads complete, saved in {}".format(index_name))
        return


    # Get all the documents in an index
    def list_documents(self, index: str) -> List[str]:
        resp = scan(self, index=index, query={"query": { "match_all" : {}}} )
        docs = [json.dumps(item) for item in resp]
        return docs


    # Search Functions -- utils to format the Query DSL and return results (defaults anchored around Alexandria datastruct)
    #presumably these could get wrapped into a single function, but for now keeping separate (since sep usage + kwarg mappings)
    #this is effectively a custom version of the High-Level ES_DSL Library- https://elasticsearch-dsl.readthedocs.io/en/latest/
    # All Search Funcs call the `.search()` func under the hood- https://elasticsearch-py.readthedocs.io/en/v8.5.0/api.html#elasticsearch.Elasticsearch.search

    # Match Search
    def search_match(self, query="", index="", field="SUMMARY", **kwargs):
        """
        This function does `match` search on a specified field in the ES Index
        See-https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html for more info on match searching

        Parameters:
            query: str, search terms to check for in ES
            index: str, specified index to search, if empty string will search ALL the available indices
            field: str, the field to filter search query on, one of ['SUMMARY', 'TITLE', 'URL']
        
        Sample Kwargs:
            fuzziness: int, value for allowed levenshtein distance between query terms and result matches
        """

        # Set up Search JSON w Base Params
        search_body = {
                "query" : {
                    # This looks for the existence of Tokens in a Field (if multi tokens, will match on out of order stuff)
                    "match" : {
                        field : {
                            "query" : query,
                        }
                    }
                }
        }

        # Add Additional Kwargs to the Query DSL -- must follow name/value conventions in upstream docs
        for name, value in kwargs.items():
            search_body["query"]["match"][field][name] = value

        # POST Query DSL to ES
        results = self.search(index=index, body=search_body, size=250)

        return results

    # Match Phrase Search
    def search_matchphrase(self, query="", index="", field="SUMMARY", **kwargs):
        """
        Match_Phrase search matches a Contiguous string (set of tokens), see- https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query-phrase.html for more info

        Parameters:
            query: str, search terms to check for in ES
            index: str, specified index to search, if empty string will search ALL the available indices
            field: str, the field to filter search query on, one of ['SUMMARY', 'TITLE', 'URL']

        Sample Kwargs:
            slop: int, number of 'out of order' tokens to accept (allowance for tokens that break the contiguous string) -- think of this as levenshtein distance for words in a sentence
        """

        # Set up Search JSON w Base Params
        search_body = {
                "query" : {
                    # This looks for CONTIGUOUS spans of tokens that match our phrase
                    "match_phrase" : {
                        field : {
                            "query" : query,
                        }
                    }
                }
        }

        # Add Additional Kwargs to the Query DSL -- must follow name/value conventions in upstream docs
        for name, value in kwargs.items():
            search_body["query"]["match"][field][name] = value

        # POST Query DSL to ES
        results = self.search(index=index, body=search_body, size=250)

        return results

    # Wildcard Searching
    def search_wildcard(self, query="", index="", field="SUMMARY", **kwargs):
        """
        This function does wildcard search on the specified field in ES, the query needs to be formatted like- https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-wildcard-query.html

        Parameters:
            query: str, search terms to check for in ES
            index: str, specified index to search, if empty string will search ALL the available indices
            field: str, the field to filter search query on, one of ['SUMMARY', 'TITLE', 'URL']

        Sample Kwargs:
        boost: float, number to adjust the relevance scores of the wildcard query
        case_insensitive: boolean, whether or not to make the wildcard matching boolean based
        rewrite: str, one of the valid values for Apache Lucene methods, listed in- https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-multi-term-rewrite.html
        """

        # Set up Search JSON w Base Params
        search_body = {
                "query" : {
                    "wildcard" : {
                        field : {
                            "value" : query,
                        }
                    }
                }
        }

        # Add Additional Kwargs to the Query DSL -- must follow name/value conventions in upstream docs
        for name, value in kwargs.items():
            search_body["query"]["match"][field][name] = value

        # POST Query DSL to ES
        results = self.search(index=index, body=search_body, size=250)

        return results


    # Util to Format the Output of any of the above Search Functions (same-ish return types, can standardize)
    def format_results(self, results=None, title_only=False, relevant_content=False, trimmed_results=False):
        if results == None:
            print("No results provided to parse, exiting...")
            return

        if title_only:
            return [i["_source"]["TITLE"] for i in results["hits"]["hits"]] #parse out just the entry titles
        
        elif relevant_content: 
            # Returns a Tuple of; (doc_title, summarized_content, source_url, relevancy_score)
            return [(i["_source"]["TITLE"], i["_source"]["SUMMARY"], i["_source"]["URL"], i["_score"]) for i in results["hits"]["hits"]]

        elif trimmed_results:
            # Sliced Content String (easier to view long summaries in terminal)
            return [(i["_source"]["TITLE"], i["_source"]["SUMMARY"][0:150], i["_score"]) for i in results["hits"]["hits"]]
