import hashlib
from elasticsearch import Elasticsearch
es = Elasticsearch()


def connection_is_available():
    if not es.ping():
        return False
    return True


def document_exists(es_index="posts", url=""):
    try:
        document_id = hashlib.md5(url.encode('utf-8')).hexdigest()
        res = es.get(index=es_index, id=document_id)
        found = res['found']
        return found
    except Exception as e:
        print(e)
        return False
    

def add_document(es_index="posts",data={}):
    print("INDEXING")
    print(data)
    document_id = hashlib.md5(data["url"].encode('utf-8')).hexdigest()
    try:
        res = es.index(index=es_index, id=document_id, body=data)
        print("Document added "+document_id)
        return True
    except Exception as e:
        print(e)
        return False
