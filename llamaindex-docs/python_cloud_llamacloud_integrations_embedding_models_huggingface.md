[Skip to content](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/embedding_models/huggingface/#_top)
# HuggingFace Embedding
Embed data using HuggingFace’s Inference API.
## Configure via UI
[Section titled “Configure via UI”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/embedding_models/huggingface/#configure-via-ui)
  1. Select `HuggingFace Embedding` from the `Embedding Model` dropdown.
  2. Enter your HuggingFace API key.
  3. Enter your HuggingFace model name or URL, e.g. `BAAI/bge-small-en-v1.5`.


## Configure via API / Client
[Section titled “Configure via API / Client”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/embedding_models/huggingface/#configure-via-api--client)
```python pipeline = { 'name': 'test-pipeline', 'transform_config': {...}, 'embedding_config': { 'type': 'HUGGINGFACE_API_EMBEDDING', 'component': { 'token': 'hf_...', 'model_name': 'BAAI/bge-small-en-v1.5', }, }, 'data_sink_id': data_sink.id } 
pipeline = client.pipelines.upsert_pipeline(request=pipeline)
```

</TabItem>


<TabItem value="typescript" label="TypeScript Client" default>


```Typescript


const pipeline = {



'name': 'test-pipeline',




'transform_config': {...},




'embedding_config': {




'type': 'HUGGINGFACE_API_EMBEDDING',




'component': {




'token': 'hf_...',




'model_name': 'BAAI/bge-small-en-v1.5',






'dataSinkId': data_sink.id





await client.pipelines.upsertPipeline({


projectId: projectId,


body: pipeline


```

