[Skip to content](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/embedding_models/cohere/#_top)
# Cohere Embedding
Embed data using Cohere’s API.
## Configure via UI
[Section titled “Configure via UI”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/embedding_models/cohere/#configure-via-ui)
  1. Select `Cohere Embedding` from the `Embedding Model` dropdown.
  2. Enter your Cohere API key.


## Configure via API / Client
[Section titled “Configure via API / Client”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/embedding_models/cohere/#configure-via-api--client)
```python pipeline = { 'name': 'test-pipeline', 'transform_config': {...}, 'embedding_config': { 'type': 'COHERE_EMBEDDING', 'component': { 'api_key': '', # editable }, } 'data_sink_id': data_sink.id } 
pipeline = client.pipelines.upsert_pipeline(request=pipeline)
```

</TabItem>


<TabItem value="typescript" label="TypeScript Client" default>


```Typescript


const pipeline = {



'name': 'test-pipeline',




'transform_config': {...},




'embedding_config': {




'type': 'COHERE_EMBEDDING',




'component': {




'api_key': '<YOUR_COHERE_API_KEY>', # editable






'dataSinkId': data_sink.id





await client.pipelines.upsertPipeline({


projectId: projectId,


body: pipeline


```

