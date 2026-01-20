[Skip to content](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/confluence/#_top)
# Confluence Data Source
Load data from Confluence
## Configure via UI
[Section titled “Configure via UI”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/confluence/#configure-via-ui)
#### Basic Authentication
[Section titled “Basic Authentication”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/confluence/#basic-authentication)
## Configure via API / Client
[Section titled “Configure via API / Client”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/confluence/#configure-via-api--client)
  * [ TypeScript Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/confluence/#tab-panel-96)


```


from llama_cloud.types import CloudConfluenceDataSource





ds = {




'name': '<your-name>',




'source_type': 'CONFLUENCE',




'component': CloudConfluenceDataSource(




server_url: '<server_url>',




user_name: '<user_name>',




api_token: '<api_token>',




space_key: '<space_key>',# Optional




page_ids: '<page_ids>',# Optional




cql: '<cql>',# Optional




label: '<label>',# Optional






data_source = client.data_sources.create_data_source(request=ds)


```

```


const ds = {




'name': '<your-name>',




'sourceType': 'CONFLUENCE',




'component': {




'server_url': 'server_url',




'user_name': '<user_name>',




'api_token': '<api_token>',




'space_key': '<space_key>', // Optional




'page_ids': '<page_ids>', // Optional




'cql': '<cql>'// Optional




'label': '<label>', // Optional







const dataSource = await client.dataSources.createDataSource({




body: ds



```

## Guide to create an OAuth 2.0 token:
[Section titled “Guide to create an OAuth 2.0 token:”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/confluence/#guide-to-create-an-oauth-20-token)
A step-by-step guide to creating an OAuth 2.0 token and using it to fetch data from a Confluence space. It includes instructions on setting up an OAuth 2.0 app in the Atlassian Developer Console, obtaining an access token, and making API requests using the token.
#### 1. Prerequisites
[Section titled “1. Prerequisites”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/confluence/#1-prerequisites)
  1. An Atlassian account.
  2. Access to the Atlassian Developer Console.
  3. Basic knowledge of OAuth 2.0 and API requests.
  4. A Confluence account with the necessary permissions.


#### 2. Setting Up the OAuth 2.0 App
[Section titled “2. Setting Up the OAuth 2.0 App”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/confluence/#2-setting-up-the-oauth-20-app)
  1. Go to the Atlassian Developer Console.
  2. Log in with your Atlassian account.
  3. Click on your profile icon in the top-right corner and select `Developer console`.
  4. Click on `Create app`.
  5. Enter the app name and click `Create`.
  6. In your app’s settings, go to `Authorization` in the left menu.
  7. Next to OAuth 2.0 (3LO), click `Configure https://auth.atlassian.com/oauth/token`.
  8. Enter the Callback URL (this is the URL that will handle the OAuth callback).
  9. Click `Save changes`.
  10. Go to `Permissions` in the left menu.
  11. Next to the Confluence API, click `Add`.
  12. Select the necessary scopes (e.g., read:confluence-space.summary).


#### 3. Implementing OAuth 2.0 (3LO) in Your App
[Section titled “3. Implementing OAuth 2.0 (3LO) in Your App”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/confluence/#3-implementing-oauth-20-3lo-in-your-app)
  1. Direct the User to the Authorization URL:


```

https://auth.atlassian.com/authorize?audience=api.atlassian.com&client_id=YOUR_CLIENT_ID&scope=read:confluence-space.summary&redirect_uri=YOUR_APP_CALLBACK_URL&state=YOUR_USER_BOUND_VALUE&response_type=code&prompt=consent

```

  1. Replace the placeholders with the appropriate values:
    1. `YOUR_CLIENT_ID`: The client ID of your app.
    2. `YOUR_APP_CALLBACK_URL`: The callback URL configured in your app settings.
    3. `YOUR_USER_BOUND_VALUE`: A unique value to maintain state between the request and callback.
  2. Exchange the Authorization Code for an Access Token:
Once the user grants access, they will be redirected to your callback URL with an authorization code. Use this code to obtain an access token:
```

curl --request POST \



--url 'https://auth.atlassian.com/oauth/token' \




--header 'Content-Type: application/json' \




--data '{




"grant_type": "authorization_code",




"client_id": "YOUR_CLIENT_ID",




"client_secret": "YOUR_CLIENT_SECRET",




"code": "YOUR_AUTHORIZATION_CODE",




"redirect_uri": "YOUR_APP_CALLBACK_URL"



```

Replace the placeholders with the appropriate values:
    1. `YOUR_CLIENT_ID`: The client ID of your app.
    2. `YOUR_CLIENT_SECRET`: The client secret of your app.
    3. `YOUR_AUTHORIZATION_CODE`: The authorization code received from the callback.
    4. `YOUR_APP_CALLBACK_URL`: The callback URL configured in your app settings.


#### 4. Fetching Data Using the Access Token:
[Section titled “4. Fetching Data Using the Access Token:”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/confluence/#4-fetching-data-using-the-access-token)
  1. Get the Cloud ID: Use the access token to get the cloud ID for your Confluence site:
```

curl --request GET \



--url 'https://api.atlassian.com/oauth/token/accessible-resources' \




--header 'Authorization: Bearer YOUR_ACCESS_TOKEN' \




--header 'Accept: application/json'


```

Replace `YOUR_ACCESS_TOKEN` with the actual access token received in the previous step.
  2. Read the Space: Use the cloud ID and access token to make a request to read the space:
```

curl --request GET \



--url 'https://api.atlassian.com/ex/confluence/CLOUD_ID/rest/api/space' \




--header 'Authorization: Bearer YOUR_ACCESS_TOKEN' \




--header 'Accept: application/json'


```



**User Inputs:** Replace the placeholders with the appropriate values:•
  1. `CLOUD_ID` : The cloud ID of your Confluence site.
  2. `YOUR_ACCESS_TOKEN` : The actual access token received in the previous step.


