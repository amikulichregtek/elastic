import elasticsearch
import os

os.system('cls' if os.name == 'nt' else 'clear')

indexName = 'test_index'
indexNewName = 'test_index_new'

mapping = {
    "settings": {
        "number_of_shards": 2
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

res = es.indices.delete(index=indexName, ignore = [404])
res = es.indices.delete(index=indexNewName, ignore = [404])


# creating source index
es.indices.create(index=indexName, body=mapping, ignore = [400])

res=es.indices.get_settings( index=indexName )
print("Source index:", res)

es.indices.put_settings(index=indexName, body = {
  "settings": {
    "index.blocks.write": False 
  }
})

#uploading some data
list(map(lambda x: es.index(index=indexName,id=x, body= {
    "boolField":True,
    "textField":"text" + str(x),
    "intField":x
}, refresh=True), range(1,3)))

print('Content of original index', es.search(index=indexName, body='''{"query": {"match_all": {}}}''', size=100)['hits']['hits'])

es.indices.put_settings(index=indexName, body = {
  "settings": {
    "index.number_of_replicas": 0,                                
    "index.blocks.write": True                                    
  }
})

res = es.indices.shrink(index=indexName, target = indexNewName, body = {
  "settings": {
    "index.number_of_shards": 1
  }
})
print(res)

es.indices.put_settings(index=indexNewName, body = {
  "settings": {
    "index.blocks.write": False 
  }
})

res=es.indices.get_settings( index=indexNewName )
print("Destination index:", res)

es.indices.put_settings(index=indexName, body = {
  "settings": {
    "index.blocks.write": False 
  }
})

res = es.indices.delete(index=indexName, ignore = [404])
res = es.indices.delete(index=indexNewName, ignore = [404])

