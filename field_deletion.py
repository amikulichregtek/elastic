import elasticsearch
import time

indexName = 'test_index'

mapping = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 1
    },
    "mappings": {
        "properties": {
            "boolField": {
                "type": "boolean"
            },
            "intField": {
                "type": "integer"
            },
            "textField": {
                "type": "text"
            }
        }
    }
}


# configure elasticsearch
config = {
    'host': '127.0.0.1',
    'port': 9200
}
es = elasticsearch.Elasticsearch([config,], timeout=300)

# creating source index
res = es.indices.create(index=indexName, body=mapping, ignore = [400])
print(res)

#uploading some data
list(map(lambda x: es.index(index=indexName,id=x, body= {
    "boolField":True,
    "textField":"text" + str(x),
    "intField":x
}, refresh=True), range(1,3)))

print(res)

res = es.search(
    index=indexName, 
    body={ 
    "query" : { 
        "match_all" : {} 
    },
    "stored_fields": ['_id']
})

ids = [d['_id'] for d in res['hits']['hits']]

print('Before field deletion')
print(list(map(lambda x: es.get(index=indexName, id=x), ids)))
#delete field for all documents
list(map(lambda x: es.update(index=indexName, body={"script" : "ctx._source.remove('boolField')"}, id=x), ids))
print('After field deletion')
print(list(map(lambda x: es.get(index=indexName, id=x), ids)))


res = es.indices.delete(index=indexName, ignore = [404])

