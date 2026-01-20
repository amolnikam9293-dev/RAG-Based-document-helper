[Skip to content](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/jira/#_top)
# Jira Data Source
Load data from Jira
## Configure via UI
[Section titled “Configure via UI”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/jira/#configure-via-ui)
We can load data by using three different types of authentication methods:
## 1. OAuth2 Authentication Mechanism
[Section titled “1. OAuth2 Authentication Mechanism”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/jira/#1-oauth2-authentication-mechanism)
## 2. PAT Authentication Mechanism
[Section titled “2. PAT Authentication Mechanism”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/jira/#2-pat-authentication-mechanism)
## 3. Basic Authentication Mechanism
[Section titled “3. Basic Authentication Mechanism”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/jira/#3-basic-authentication-mechanism)
## Configure via API / Client
[Section titled “Configure via API / Client”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/jira/#configure-via-api--client)
#### 1. OAuth2 Authentication Mechanism
[Section titled “1. OAuth2 Authentication Mechanism”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/jira/#1-oauth2-authentication-mechanism-1)
  * [ TypeScript Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/jira/#tab-panel-102)


```


from llama_cloud.types import CloudJiraDataSource





ds = {




'name': '<your-name>',




'source_type': 'JIRA',




'component': CloudJiraDataSource(




api_token: '<api_token>',# Access token in this case




cloud_id: '<cloud_id>',




authentication_mechanism: 'oauth2',




query: '<query>',






data_source = client.data_sources.create_data_source(request=ds)


```

```


const ds = {




'name': '<your-name>',




'sourceType': 'JIRA',




'component': {




'api_token': '<api_token>', // Access token in this case




'cloud_id': '<cloud_id>',




'authentication_mechanism': 'oauth2',




'query': '<query>',







const dataSource = await client.dataSources.createDataSource({




body: ds



```

#### 2. PAT Authentication Mechanism
[Section titled “2. PAT Authentication Mechanism”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/jira/#2-pat-authentication-mechanism-1)
  * [ TypeScript Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/jira/#tab-panel-104)


```


from llama_cloud.types import CloudJiraDataSource





ds = {




'name': '<your-name>',




'source_type': 'JIRA',




'component': CloudJiraDataSource(




api_token: '<api_token>',# Personal Access Token (PAT) in this case




server_url: '<server_url>',




authentication_mechanism: 'pat',




query: '<query>',






data_source = client.data_sources.create_data_source(request=ds)


```

```


const ds = {




'name': '<your-name>',




'sourceType': 'JIRA',




'component': {




'api_token': '<api_token>', // Personal Access Token (PAT) in this case




'server_url': '<server_url>',




'authentication_mechanism': 'pat',




'query': '<query>',







const dataSource = await client.dataSources.createDataSource({




body: ds



```

#### 3. Basic Authentication Mechanism
[Section titled “3. Basic Authentication Mechanism”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/jira/#3-basic-authentication-mechanism-1)
  * [ TypeScript Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/jira/#tab-panel-106)


```


from llama_cloud.types import CloudJiraDataSource





ds = {




'name': '<your-name>',




'source_type': 'JIRA',




'component': CloudJiraDataSource(




email: '<email>',




api_token: '<api_token>',




server_url: '<server_url>',




authentication_mechanism: 'basic',




query: '<query>',






data_source = client.data_sources.create_data_source(request=ds)


```

```


const ds = {




'name': '<your-name>',




'sourceType': 'JIRA',




'component': {




'email': '<email>',




'api_token': '<api_token>',




'server_url': '<server_url>',




'authentication_mechanism': 'basic',




'query': '<query>',







const dataSource = await client.dataSources.createDataSource({




body: ds



```

