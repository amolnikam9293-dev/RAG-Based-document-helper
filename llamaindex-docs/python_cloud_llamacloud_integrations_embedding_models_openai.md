[Skip to content](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/embedding_models/openai/#_top)
# OpenAI Embedding
Embed data using OpenAI’s API.
## Configure via UI
[Section titled “Configure via UI”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/embedding_models/openai/#configure-via-ui)
  1. Select `OpenAI Embedding` from the `Embedding Model` dropdown.
  2. Enter your OpenAI API key.
  3. Select your preferred model:


  * `text-embedding-3-small` (Default)
  * `text-similarity-3-large`
  * `text-embedding-ada-002`


## Configure via API / Client
[Section titled “Configure via API / Client”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/embedding_models/openai/#configure-via-api--client)
```python pipeline = { 'name': 'test-pipeline', 'transform_config': {...}, 'embedding_config': { 'type': 'OPENAI_EMBEDDING', 'component': { 'api_key': '', # editable 'model_name': 'text-embedding-3-small' # editable }, }, 'data_sink_id': data_sink.id } 
pipeline = client.pipelines.upsert_pipeline(request=pipeline)
```

</TabItem>


<TabItem value="typescript" label="TypeScript Client" default>


```Typescript


const pipeline = {



'name': 'test-pipeline',




'transform_config': {...},




'embedding_config': {




'type': 'OPENAI_EMBEDDING',




'component': {




'api_key': '<YOUR_API_KEY_HERE>', # editable




'model_name': 'text-embedding-3-small' # editable






'dataSinkId': data_sink.id





await client.pipelines.upsertPipeline({


projectId: projectId,


body: pipeline


```

