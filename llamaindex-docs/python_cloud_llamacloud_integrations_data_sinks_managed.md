[Skip to content](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks/managed/#_top)
# Managed Data Sink
Use LlamaCloud managed index as data sink.
## Configure via UI
[Section titled “Configure via UI”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks/managed/#configure-via-ui)
## Configure via API / Client
[Section titled “Configure via API / Client”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks/managed/#configure-via-api--client)
Simply set `data_sink_id` to None when creating a pipeline
  * [ TypeScript Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks/managed/#tab-panel-78)


```


pipeline = {




'name': 'test-pipeline',




'transform_config': {...},




'embedding_config': {...},




'data_sink_id': None






pipeline = client.pipelines.upsert_pipeline(request=pipeline)


```

```


const pipeline = {




'name': 'test-pipeline',




'transform_config': {...},




'embedding_config': {...},




'dataSinkId': null






pipeline=awaitclient.pipelines.upsertPipeline(pipeline)


```

