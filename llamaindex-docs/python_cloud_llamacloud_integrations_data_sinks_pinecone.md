[Skip to content](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks/pinecone/#_top)
# Pinecone
Configure your own Pinecone instance as data sink.
## Configure via UI
[Section titled “Configure via UI”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks/pinecone/#configure-via-ui)
## Configure via API / Client
[Section titled “Configure via API / Client”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks/pinecone/#configure-via-api--client)
  * [ TypeScript Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks/pinecone/#tab-panel-84)


```


from llama_cloud.types import CloudPineconeVectorStore





ds = {




'name': '<your-name>',




'sink_type': 'PINECONE',




'component': CloudPineconeVectorStore(




api_key='<api_key>',




index_name='<index_name>',




name_space='<name_space>',# optional




insert_kwargs='<insert_kwargs>'# optional






data_sink = client.data_sinks.create_data_sink(request=ds)


```

```


const ds = {




'name': 'pinecone',




'sinkType': 'PINECONE',




'component': {




'api_key': '<api_key>',




'index_name': '<index_name>',




'name_space': '<name_space>'// optional




'insert_kwargs': '<insert_kwargs>'// optional







data_sink=awaitclient.dataSinks.createDataSink({




projectId: projectId,




body: ds



```

## Filter Syntax
[Section titled “Filter Syntax”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks/pinecone/#filter-syntax)
When using Pinecone as a data sink, you can apply filters using the following syntax:
Filter Operator | Pinecone Equivalent | Description  
---|---|---  
`$eq` | Equals  
`$ne` | Not equal  
`$gt` | Greater than  
`$lt` | Less than  
`$gte` | Greater than or equal  
`$lte` | Less than or equal  
`$in` | Value is in a list  
`nin` | `$nin` | Value is not in a list  
These filters can be applied to metadata fields when querying your Pinecone index to refine search results based on specific criteria.
