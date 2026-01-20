[Skip to content](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/embedding_models/bedrock/#_top)
# Bedrock Embedding
Embed data using AWS Bedrock’s API.
## Configure via UI
[Section titled “Configure via UI”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/embedding_models/bedrock/#configure-via-ui)
  1. Select `Bedrock Embedding` from the `Embedding Model` dropdown.
  2. Enter your AWS Region, AWS access key ID and AWS secret access key.
  3. Select your preferred model:


  * `Titan Embedding` (Default)
  * `Titan Embedding G1 Text 02`
  * `Cohere Embed English V3`
  * `Cohere Embed Multilingual V3`


## Configure via API / Client
[Section titled “Configure via API / Client”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/embedding_models/bedrock/#configure-via-api--client)
For API / Client, use the model IDs:
  * `amazon.titan-embed-text-v1`
  * `amazon.titan-embed-g1-text-02`
  * `cohere.embed-english-v3`
  * `cohere.embed-multilingual-v3`

```python pipeline = { 'name': 'test-pipeline', 'transform_config': {...}, 'embedding_config': { 'type': 'BEDROCK_EMBEDDING', 'component': { 'region_name': 'us-east-1', 'aws_access_key_id': '', 'aws_secret_access_key': '', 'model': 'amazon.titan-embed-text-v1', }, }, 'data_sink_id': data_sink.id } 
pipeline = client.pipelines.upsert_pipeline(request=pipeline)
```

</TabItem>


<TabItem value="typescript" label="TypeScript Client" default>


```Typescript


const pipeline = {



'name': 'test-pipeline',




'transform_config': {...},




'embedding_config': {




'type': 'BEDROCK_EMBEDDING',




'component': {




'region_name': 'us-east-1',




'aws_access_key_id': '<aws_access_key_id>',




'aws_secret_access_key': '<aws_secret_access_key>',




'model': 'amazon.titan-embed-text-v1',






'dataSinkId': data_sink.id





await client.pipelines.upsertPipeline({


projectId: projectId,


body: pipeline


```

