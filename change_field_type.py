import elasticsearch
import time

indexName = 'test_index'
indexNewName = 'test_index_new'
pipelineName = 'renamePipeline'

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

data = {
    "boolField":True,
    "textField":"text",
    "intField":10
}

pipeline = {
  "description" : "change field type",
  "processors" : [
    {
      "convert" : {
        "field" : "intField",
        "type": "long"
      }
    }
  ]
}

reindexBody = {
  "source": {
    "index": indexName
  },
  "dest": {
    "index": indexNewName,
    "pipeline": pipelineName
  }
} 


# configure elasticsearch
config = {
    'host': '127.0.0.1',
    'port': 9200
}
es = elasticsearch.Elasticsearch([config,], timeout=300)
ic = elasticsearch.client.IngestClient(es)

# creating source index
res = es.indices.create(index=indexName, body=mapping, ignore = [400])

res=es.indices.get_mapping( indexName )
print("Source mapping:", res)

#uploading some data
res = es.index(index=indexName,id=1, body=data, refresh=True)
print(res)

res=es.get(index=indexName, id=1)
print(res)

#creating pipeline with renaming processor
res = ic.put_pipeline(body=pipeline, id=pipelineName)
print(res)

#reindexing with pipleine
es.reindex(body = reindexBody)

if not es.indices.exists(index=indexNewName):
    print('Reindexing error')
    exit()

res=es.indices.get_mapping( indexNewName )
print("New mapping:", res)

res = es.indices.delete(index=indexNewName, ignore = [404])
res = es.indices.delete(index=indexName, ignore = [404])

