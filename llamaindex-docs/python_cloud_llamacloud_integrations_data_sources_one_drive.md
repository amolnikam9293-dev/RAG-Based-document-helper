[Skip to content](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/one_drive/#_top)
# Microsoft OneDrive Data Source
Load data from Microsoft OneDrive
## Configure via UI
[Section titled “Configure via UI”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/one_drive/#configure-via-ui)
## Configure via API / Client
[Section titled “Configure via API / Client”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/one_drive/#configure-via-api--client)
  * [ TypeScript Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/one_drive/#tab-panel-100)


```


from llama_cloud.types import CloudOneDriveDataSource





ds = {




'name': '<your-name>',




'source_type': 'MICROSOFT_ONEDRIVE',




'component': CloudOneDriveDataSource(




user_principal_name='<user_principal_name>',




folder_path='<folder_path>',# optional




folder_id='<folder_id>',# optional




client_id='<client_id>',




client_secret='<client_secret>',




tenant_id='<tenant_id>',






data_source = client.data_sources.create_data_source(request=ds)


```

```


const ds = {




name: '<your-name>',




sourceType: 'MICROSOFT_ONEDRIVE',




component: {




userPrincipalName: '<user_principal_name>',




folderPath: '<folder_path>'// optional




folderId: '<folder_id>'// optional




clientId: '<client_id>',




clientSecret: '<client_secret>',




tenantId: '<tenant_id>',







const dataSource = await client.dataSources.createDataSource({




body: ds



```

