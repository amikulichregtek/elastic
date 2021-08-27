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
print("OriginaliIndex:", res)

#uploading some data
res = es.index(index=indexName,id=1, body={
    "textField":"text",
    "intField":10
}, refresh=True)

res=es.get(index=indexName, id=1)
#print("Payload:", res)

#uploading some data
res = es.index(index=indexName,id=2, body={
    "textField":"text",
    "intField":10,
    "newField":True   
}, refresh=True)

res=es.get(index=indexName, id=2)
print("Payload with new field:", res)

res=es.indices.get_mapping( indexName )
print("New mapping:", res)

res = es.indices.delete(index=indexName, ignore = [404])

