[Skip to content](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks/postgres/#_top)
# Postgres
Configure your own Postgres instance as data sink.
## Configure via UI
[Section titled “Configure via UI”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks/postgres/#configure-via-ui)
## Configure Parameters
[Section titled “Configure Parameters”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks/postgres/#configure-parameters)
To configure **Postgres** as a vector store for your LlamaCloud documents you will need the following:
Parameter | Description | Example  
---|---|---  
Database | Database name | `llamaindex`  
Host | Connection endpoint | `my-postgres-cluster.us-east-1.rds.amazonaws.com`  
User | Database username | `postgres`  
Password | Password for database user | `*****`  
Table Name | Table where embeddings will be stored | `llamaindex`  
Schema Name | Schema in which the database table will exist | `public`  
Embedding Dimension | Dimension size of embeddings | `1536`  
Port | Port where Postgres listens | `5432`  
## Configure via API / Client
[Section titled “Configure via API / Client”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks/postgres/#configure-via-api--client)
  * [ Typescript Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks/postgres/#tab-panel-121)


```


from llama_cloud.types import CloudPostgresVectorStore





ds = {




'name': '<your-data-sink-name>',




'sink_type': 'POSTGRES',




'component': CloudPostgresVectorStore(




database='<database-name>',




host='<database-host>',




user='<user>',




password='<password>',




port=5432,




embed_dim=1536,




schema_name='<schema>',




table_name='<table>'







data_sink = client.data_sinks.create_data_sink(request=ds)


```

```


const ds = {




'name': '<your-data-sink-name>',




'sinkType': 'POSTGRES',




'component': {




'database': '<database-name>',




'host': '<database-host>',




'user': '<user>',




'password': '<password>',




'port': 5432,




'embed_dim': 1536,




'schema_name': '<schema>',




'table_name': '<table>'







data_sink=awaitclient.dataSinks.createDataSink({



projectId: projectId,


body: ds


```

