[Skip to content](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks/qdrant/#_top)
# Qdrant
Configure your own Qdrant instance as data sink.
## Configure via UI
[Section titled “Configure via UI”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks/qdrant/#configure-via-ui)
## Configure via API / Client
[Section titled “Configure via API / Client”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks/qdrant/#configure-via-api--client)
  * [ TypeScript Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks/qdrant/#tab-panel-82)


```


from llama_cloud.types import CloudQdrantVectorStore





ds = {




'name': '<your-name>',




'sink_type': 'QDRANT',




'component': CloudQdrantVectorStore(




api_key='<api_key>',




collection_name='<collection_name>',




url='<url>',




max_retries='<max_retries>',# optional




client_kwargs='<client_kwargs>'# optional






data_sink = client.data_sinks.create_data_sink(request=ds)


```

```


const ds = {




'name': 'qdrant',




'sinkType': 'QDRANT',




'component': {




'api_key': '<api_key>',




'collection_name': '<collection_name>',




'url': '<url>',




'max_retries': '<max_retries>'// optional




'client_kwargs': '<client_kwargs>'// optional







data_sink=awaitclient.dataSinks.createDataSink({




projectId: projectId,




body: ds



```

