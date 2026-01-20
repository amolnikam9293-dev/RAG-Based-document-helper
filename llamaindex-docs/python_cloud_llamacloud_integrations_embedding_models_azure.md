[Skip to content](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/embedding_models/azure/#_top)
# Azure Embedding
Embed data using Azure’s API.
## Configure via UI
[Section titled “Configure via UI”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/embedding_models/azure/#configure-via-ui)
  1. Select `Azure Embedding` from the `Embedding Model` dropdown.
  2. Enter your Azure API key, deployment name, endpoint name and API version.


## Configure via API / Client
[Section titled “Configure via API / Client”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/embedding_models/azure/#configure-via-api--client)
```python pipeline = { 'name': 'test-pipeline', 'transform_config': {...}, 'embedding_config': { 'type': 'AZURE_EMBEDDING', 'component': { 'azure_deployment': '', # editable 'api_key': '', # editable 'azure_endpoint': '', # editable 'api_version': '', # editable }, } 'data_sink_id': data_sink.id } 
pipeline = client.pipelines.upsert_pipeline(request=pipeline)
```

</TabItem>


<TabItem value="typescript" label="TypeScript Client" default>


```Typescript


const pipeline = {



'name': 'test-pipeline',




'transform_config': {...},




'embedding_config': {




'type': 'AZURE_EMBEDDING',




'component': {




'deployment_name': '<YOUR_DEPLOYMENT_NAME>', # editable




'api_key': '<YOUR_AZUREOPENAI_API_KEY>', # editable




'azure_endpoint': '<YOUR AZURE_ENDPOINT>', # editable




'api_version': '<YOUR AZURE_API_VERSION>', # editable






'dataSinkId': data_sink.id





await client.pipelines.upsertPipeline({


projectId: projectId,


body: pipeline


```

