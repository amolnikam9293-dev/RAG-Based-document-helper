[Skip to content](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/embedding_models/gemini/#_top)
# Gemini Embedding
Embed data using Gemini’s API.
## Configure via UI
[Section titled “Configure via UI”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/embedding_models/gemini/#configure-via-ui)
  1. Select `Gemini Embedding` from the `Embedding Model` dropdown.
  2. Enter your Gemini API key.


## Configure via API / Client
[Section titled “Configure via API / Client”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/embedding_models/gemini/#configure-via-api--client)
```python pipeline = { 'name': 'test-pipeline', 'transform_config': {...}, 'embedding_config': { 'type': 'GEMINI_EMBEDDING', 'component': { 'api_key': '', # editable }, }, 'data_sink_id': data_sink.id } 
pipeline = client.pipelines.upsert_pipeline(request=pipeline)
```

</TabItem>


<TabItem value="typescript" label="TypeScript Client" default>


```Typescript


const pipeline = {



name': 'test-pipeline',




'transform_config': {...},




'embedding_config': {




'type': 'GEMINI_EMBEDDING',




'component': {




'api_key': '<YOUR_GEMINI_API_KEY>', # editable






'dataSinkId': data_sink.id





await client.pipelines.upsertPipeline({


projectId: projectId,


body: pipeline


```

