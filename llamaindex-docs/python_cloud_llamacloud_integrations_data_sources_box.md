[Skip to content](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/box/#_top)
# Box Storage Data Source
Load data from Box Storage.
## Configure via UI
[Section titled “Configure via UI”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/box/#configure-via-ui)
We can load data from Box using one of two different types of authentication, either a Developer Token or a Client Credential Grant.
## 1. Developer Token Authentication Mechanism
[Section titled “1. Developer Token Authentication Mechanism”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/box/#1-developer-token-authentication-mechanism)
Developer Tokens are short lived and can be created in the [Box Developer Console](https://developer.box.com/).
## 2. Client Credential Grant Authentication Mechanism
[Section titled “2. Client Credential Grant Authentication Mechanism”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/box/#2-client-credential-grant-authentication-mechanism)
These credentials can be used to access Box data for a specific user or an entire enterprise and are longer-lived than Developer Tokens. You can use either an Enterprise ID or a User ID to authenticate.
### Setting up Box CCG Credentials
[Section titled “Setting up Box CCG Credentials”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/box/#setting-up-box-ccg-credentials)
  1. Log in to your Box account / Create a Box developer account and navigate to the developer console.
  2. Create a new custom app.
  3. Select “Server Authentication (Client Credentials Grant)” as the authentication method.
  4. Under “App Access Level”, select `App + Enterprise Access`.
  5. We recommend giving your app all permissions, as shown: 
  6. Save your changes and submit the app for authorization.
  7. Open the [Box Admin console](https://app.box.com/master/custom-apps). As an admin, authorize the app in the Custom Apps Manager.
  8. Once the app is enabled, get your `User ID`, `Enterprise ID`, `Client ID` and `Client Secret` from app console in developer console.


### 1. Client Credential Grant Authentication Mechanism using an Enterprise ID
[Section titled “1. Client Credential Grant Authentication Mechanism using an Enterprise ID”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/box/#1-client-credential-grant-authentication-mechanism-using-an-enterprise-id)
Note that to access files via an Enterprise ID, they need to have been shared with that app. You can share files with an app by its email address, which can be found in the Developer Console under “Service Account Info”.
### 2. Client Credential Grant Authentication Mechanism using a User ID
[Section titled “2. Client Credential Grant Authentication Mechanism using a User ID”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/box/#2-client-credential-grant-authentication-mechanism-using-a-user-id)
If you are using a User ID, you can access files that have been shared with or created by that user. This will be the user ID of the person who created the app.
## Configure via API / Client
[Section titled “Configure via API / Client”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/box/#configure-via-api--client)
#### 1. Developer Token Authentication Mechanism
[Section titled “1. Developer Token Authentication Mechanism”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/box/#1-developer-token-authentication-mechanism-1)
  * [ TypeScript Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/box/#tab-panel-92)


```


from llama_cloud.types import CloudBoxDataSource





ds = {




'name': '<your-name>',




'source_type': 'BOX',




'component': CloudBoxDataSource(




folder_id='<folder_id>',# Optional




developer_token='<token>',# Developer Tokens are short lived






data_source = client.data_sources.create_data_source(request=ds)


```

```

const ds = {



'name': '<your-name>',




'sourceType': 'BOX',




'component': {




'folder_id'='<folder_id>', // Optional




'developer_token'='<token>', // Developer Tokens are short lived






data_source = await client.dataSources.createDataSource({



body: ds



```

#### 2. Client Credential Grant Authentication Mechanism
[Section titled “2. Client Credential Grant Authentication Mechanism”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/box/#2-client-credential-grant-authentication-mechanism-1)
  * [ TypeScript Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/box/#tab-panel-94)


```


from llama_cloud.types import CloudBoxDataSource





ds = {




'name': '<your-name>',




'source_type': 'BOX',




'component': CloudBoxDataSource(




folder_id='<folder_id>',# Optional




client_id='<client_id>',




client_secret='<client_secret>',




user_id='<user_id>',# Optional, if using enterprise_id




enterprise_id='<enterprise_id>'# Optional, if using user_id






data_source = client.data_sources.create_data_source(request=ds)


```

```

const ds = {



'name': '<your-name>',




'sourceType': 'BOX',




'component': {




'folder_id'='<folder_id>', // Optional




'client_id'='<client_id>',




'client_secret'='<client_secret>',




'user_id'='<user_id>', // Optional, if using enterprise_id




'enterprise_id'='<enterprise_id>' // Optional, if using user_id






data_source = await client.dataSources.createDataSource({



body: ds



```

