[Skip to content](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks/astradb/#_top)
# AstraDB
Configure your own AstraDB instance as data sink.
## Configure via UI
[Section titled “Configure via UI”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks/astradb/#configure-via-ui)
## Configure via API / Client
[Section titled “Configure via API / Client”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks/astradb/#configure-via-api--client)
  * [ TypeScript Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks/astradb/#tab-panel-70)


```


from llama_cloud.types import CloudAstraDBVectorStore





ds = {




'name': '<your-name>',




'sink_type': 'ASTRA_DB',




'component': CloudAstraDBVectorStore(




token='<astra-db-application-token>',




api_endpoint='<astra-db-api-endpoint>',




collection_name='<collection-name>',




embedding_dimension=1536,# Length of embedding vectors




keyspace='<keyspace-name>',# optional (default: 'default_keyspace')







data_sink = client.data_sinks.create_data_sink(request=ds)


```

```


const ds = {




'name': 'astradb',




'sinkType': 'ASTRA_DB',




'component': {




'token': '<astra-db-application-token>',




'api_endpoint': '<astra-db-api-endpoint>',




'collection_name': '<collection-name>',




'embedding_dimension': 1536// Length of embedding vectors




'keyspace': '<keyspace-name>'// optional (default: 'default_keyspace')







data_sink=awaitclient.dataSinks.createDataSink({




projectId: projectId,




body: ds



```

## Configuration Parameters
[Section titled “Configuration Parameters”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks/astradb/#configuration-parameters)
Parameter | Type | Required | Description  
---|---|---|---  
`token` | string | Yes | The Astra DB Application Token to use for authentication  
`api_endpoint` | string | Yes | The Astra DB JSON API endpoint for your database  
`collection_name` | string | Yes | Collection name to use. If not existing, it will be created  
`embedding_dimension` | integer | Yes | Length of the embedding vectors in use (e.g., 1536 for OpenAI)  
`keyspace` | string | No | The keyspace to use. If not provided, ‘default_keyspace’ will be used  
## Prerequisites
[Section titled “Prerequisites”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks/astradb/#prerequisites)
Before configuring AstraDB as a data sink, ensure you have:
  1. **AstraDB Database** : A running AstraDB database instance
  2. **Application Token** : An AstraDB Application Token with appropriate permissions
  3. **API Endpoint** : The JSON API endpoint URL for your database
  4. **Keyspace** : A keyspace in your database (optional, will use ‘default_keyspace’ if not specified)


## Getting Started with AstraDB
[Section titled “Getting Started with AstraDB”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks/astradb/#getting-started-with-astradb)
### 1. Create an AstraDB Database
[Section titled “1. Create an AstraDB Database”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks/astradb/#1-create-an-astradb-database)
  * Visit the [AstraDB Console](https://astra.datastax.com)
  * Create a new database or use an existing one
  * Note down your database’s API endpoint


### 2. Generate an Application Token
[Section titled “2. Generate an Application Token”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks/astradb/#2-generate-an-application-token)
  * In the AstraDB Console, navigate to your database
  * Go to the “Connect” tab
  * Generate an Application Token with the necessary permissions
  * Save the token securely


### 3. Configure the Data Sink
[Section titled “3. Configure the Data Sink”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks/astradb/#3-configure-the-data-sink)
Use the token and API endpoint in your data sink configuration as shown in the examples above.
## Filter Syntax
[Section titled “Filter Syntax”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks/astradb/#filter-syntax)
When using AstraDB as a data sink, you can apply filters using standard MongoDB-style query operators:
Filter Operator | Description  
---|---  
`$eq` | Equals  
`$ne` | Not equal  
`$gt` | Greater than  
`$lt` | Less than  
`$gte` | Greater than or equal  
`$lte` | Less than or equal  
`$in` | Value is in a list  
`$nin` | Value is not in a list  
These filters can be applied to metadata fields when querying your AstraDB collection to refine search results based on specific criteria.
