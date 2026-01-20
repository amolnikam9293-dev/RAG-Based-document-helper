[Skip to content](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks/milvus/#_top)
# Milvus
Configure your own Milvus Vector DB instance as data sink.
## Configure via UI
[Section titled “Configure via UI”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks/milvus/#configure-via-ui)
## Configure via API / Client
[Section titled “Configure via API / Client”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks/milvus/#configure-via-api--client)
  * [ TypeScript Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks/milvus/#tab-panel-76)


```


from llama_cloud.types import CloudMilvusVectorStore





ds = {




'name': '<your-name>',




'sink_type': 'MILVUS',




'component': CloudMilvusVectorStore(




uri='<uri>',




collection_name='<collection_name>',




token='<token>',# optional




# embedding dimension




dim='<dim>'# optional






data_sink = client.data_sinks.create_data_sink(request=ds)


```

```


const ds = {




'name': 'milvus',




'sinkType': 'MILVUS',




'component': {




'uri': '<uri>',




'collection_name': '<collection_name>',




'token': '<token>'// optional




// embedding dimension




'dim': '<dim>'// optional







data_sink=awaitclient.dataSinks.createDataSink({




projectId: projectId,




body: ds



```

