[Skip to content](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/google_drive/#_top)
# Google Drive Data Source
Load data from Google Drive.
Make sure to setup the [Google Drive API](https://support.google.com/googleapi/answer/6158841?hl=en) before using this data source.
This setup involves creating a Service Account and configuring domain-wide delegation to allow the service account to access files within the Google Workspace team.
To create a service account key, follow these [instructions](https://developers.google.com/workspace/guides/create-credentials#service-account).
The service account must be granted access to files according to the following [instructions](https://support.google.com/a/answer/162106) (preferred), or through sharing the folders / files with the service account
## Configure via UI
[Section titled “Configure via UI”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/google_drive/#configure-via-ui)
## Configure via API / Client
[Section titled “Configure via API / Client”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/google_drive/#configure-via-api--client)
  * [ TypeScript Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/google_drive/#tab-panel-98)


```


from llama_cloud.types import (




CloudGoogleDriveDataSource,




ConfigurableDataSourceNames,




DataSourceCreate,





ds =DataSourceCreate(




name="<your-name>",




source_type=ConfigurableDataSourceNames.GOOGLE_DRIVE,




component=CloudGoogleDriveDataSource(




folder_id="<your-folder-id>",




service_account_key={




"type": "service_account",




"project_id": "<your-project-id>",




"private_key": "<your-private-key>",








data_source = client.data_sources.create_data_source(request=ds)


```

```

const ds = {



'name': '<your-name>',




'sourceType': 'GOOGLE_DRIVE',




'component': {




'folderId': '<your-folder-id>',




'serviceAccountKey': {




'type': 'service_account',




'project_id': '<your-project-id>',




'private_key': '<your-private-key>',







data_source = await client.dataSources.createDataSource({



body: ds



```

