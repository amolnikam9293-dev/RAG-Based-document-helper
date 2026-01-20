[Skip to content](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/azure_blob/#_top)
# Azure Blob Storage Data Source
Load data from Azure Blob Storage.
## Configure via UI
[Section titled “Configure via UI”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/azure_blob/#configure-via-ui)
We can load data by using two different types of authentication methods:
## 1. Account Key Authentication Mechanism
[Section titled “1. Account Key Authentication Mechanism”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/azure_blob/#1-account-key-authentication-mechanism)
## 2. Service Principal Authentication Mechanism
[Section titled “2. Service Principal Authentication Mechanism”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/azure_blob/#2-service-principal-authentication-mechanism)
## 3. SAS URL Authentication Mechanism
[Section titled “3. SAS URL Authentication Mechanism”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/azure_blob/#3-sas-url-authentication-mechanism)
## Configure via API / Client
[Section titled “Configure via API / Client”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/azure_blob/#configure-via-api--client)
#### 1. Account Key Authentication Mechanism
[Section titled “1. Account Key Authentication Mechanism”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/azure_blob/#1-account-key-authentication-mechanism-1)
  * [ TypeScript Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/azure_blob/#tab-panel-86)


```


from llama_cloud.types import CloudAzStorageBlobDataSource





ds = {




'name': '<your-name>',




'source_type': 'AZURE_STORAGE_BLOB',




'component': CloudAzStorageBlobDataSource(




container_name='<container_name>',




account_url='<account_url>',




blob='<blob>',# optional




prefix='<prefix>',# optional




account_name='<account_name>',




account_key='<account_key>',






data_source = client.data_sources.create_data_source(request=ds)


```

```

const ds = {



'name': '<your-name>',




'sourceType': 'AZURE_STORAGE_BLOB',




'component': {




'container_name': '<container_name>',




'account_url': '<account_url>',




'blob': '<blob>',  // optional




'prefix': '<prefix>',  // optional




'account_name': '<account_name>',




'account_key': '<account_key>',






data_source = await client.dataSources.createDataSource({



body: ds



```

#### 2. Service Principal Authentication Mechanism
[Section titled “2. Service Principal Authentication Mechanism”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/azure_blob/#2-service-principal-authentication-mechanism-1)
  * [ TypeScript Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/azure_blob/#tab-panel-88)


```


from llama_cloud.types import CloudAzStorageBlobDataSource





ds = {




'name': '<your-name>',




'source_type': 'AZURE_STORAGE_BLOB',




'component': CloudAzStorageBlobDataSource(




container_name='<container_name>',




account_url='<account_url>',




blob='<blob>',# optional




prefix='<prefix>',# optional




client_id='<client_id>',




client_secret='<client_secret>',




tenant_id='<tenant_id>',






data_source = client.data_sources.create_data_source(request=ds)


```

```

const ds = {



'name': '<your-name>',




'sourceType': 'AZURE_STORAGE_BLOB',




'component': {




'container_name'='<container_name>',




'account_url'='<account_url>',




'blob'='<blob>',  // optional




'prefix'='<prefix>',  // optional




'client_id'='<client_id>',




'client_secret'='<client_secret>',




'tenant_id'='<tenant_id>',






data_source = await client.dataSources.createDataSource({



body: ds



```

#### 3. SAS URL Authentication Mechanism
[Section titled “3. SAS URL Authentication Mechanism”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/azure_blob/#3-sas-url-authentication-mechanism-1)
  * [ TypeScript Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/azure_blob/#tab-panel-90)


```


from llama_cloud.types import CloudAzStorageBlobDataSource





ds = {




'name': '<your-name>',




'source_type': 'AZURE_STORAGE_BLOB',




'component': CloudAzStorageBlobDataSource(




container_name='<container_name>',




account_url='<account_url>/?<SAS_TOKEN>',




blob='<blob>',# optional




prefix='<prefix>',# optional






data_source = client.data_sources.create_data_source(request=ds)


```

```

const ds = {



'name': '<your-name>',




'sourceType': 'AZURE_STORAGE_BLOB',




'component': {




'container_name': '<container_name>',




'account_url': '<account_url>/?<SAS_TOKEN>',




'blob': '<blob>',  // optional




'prefix': '<prefix>',  // optional






data_source = await client.dataSources.createDataSource({



body: ds



```

