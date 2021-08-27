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
  "description" : "rename field name",
  "processors" : [
    {
      "rename" : {
        "field": "textField",
        "target_field": "renamedTextField"
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
print(res)

#uploading some data
res = es.index(index=indexName,id=1, body=data, refresh=True)
print(res)

res=es.get(index=indexName, id=1)
print(res)

#creating pipeline with renaming processor
res = ic.put_pipeline(body=pipeline, id=pipelineName)
print(res)

#reindexing with pipleine
res = es.reindex(body = reindexBody)
print(res)

if not es.indices.exists(index=indexNewName):
    print('Reindexing error')
    exit()

# original field textField renamed to renamedTextField
res=es.get(index=indexNewName, id=1)
print(res)

res = es.indices.delete(index=indexNewName, ignore = [404])
res = es.indices.delete(index=indexName, ignore = [404])

