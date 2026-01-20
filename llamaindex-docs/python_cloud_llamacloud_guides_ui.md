[Skip to content](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/ui/#_top)
# Index No-code UI Guide
Core workflows for Index via the no-code UI.
## Create new index
[Section titled “Create new index”](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/ui/#create-new-index)
Navigate to `Index` feature via the left navbar. 
Click `Create a new pipeline` button. You should see a index configuration form. 
### Configure data source
[Section titled “Configure data source”](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/ui/#configure-data-source)
Click `Select a data source` dropdown and select desired data source. 
Specify data source credentials and configurations (or upload files). 
See [full list of supported data sources](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources)
#### Scheduled sync
[Section titled “Scheduled sync”](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/ui/#scheduled-sync)
If you are using an external data source, you can schedule regular syncs to update changed files and ensure your index is always up to date. The syncs start from the index creation date. To enable scheduled sync, click on the dropdown under the data source details and select a frequency. Only `no scheduled sync`, `6 hours`, `12 hours` and `24 hours` are available. Please contact us if you need more granular syncing options.
### Configure data sink
[Section titled “Configure data sink”](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/ui/#configure-data-sink)
Click `Select a data sink` dropdown and select desired data sink. 
See [full list of supported data sinks](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks)
### Configure embedding model
[Section titled “Configure embedding model”](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/ui/#configure-embedding-model)
Select `OpenAI Embedding` and put in your API key. 
See [full list of supported embedding models](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/embedding_models/)
### Configure parsing & transformation settings
[Section titled “Configure parsing & transformation settings”](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/ui/#configure-parsing--transformation-settings)
Toggle to enable or disable `Llama Parse`.
Select `Auto` mode for best default transformation setting (specify desired chunks size & chunk overlap as necessary.)
`Manual` mode is coming soon, with additional customizability.
See [parsing & transformation details](https://developers.llamaindex.ai/python/cloud/llamacloud/parsing_transformation/)
### Deploy index
[Section titled “Deploy index”](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/ui/#deploy-index)
After configuring the ingestion pipeline, click `Deploy Index` to kick off ingestion. 
You should see an index overview with the latest ingestion status. 
## Manage existing index
[Section titled “Manage existing index”](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/ui/#manage-existing-index)
### Update files
[Section titled “Update files”](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/ui/#update-files)
Navigate to `Data Sources` tab to manage your connected data sources.
You can upsert, delete, download, and preview uploaded files.
### Sync index
[Section titled “Sync index”](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/ui/#sync-index)
Click `Sync` button on the top right to pull upstream changes (data sources & files) and refresh index with the latest content.
### Edit index
[Section titled “Edit index”](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/ui/#edit-index)
Click `Edit` to open up modal for configuring ingestion settings. 
### Delete index
[Section titled “Delete index”](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/ui/#delete-index)
Click `Delete` button to remove the index.
Note that this will not delete the uploaded files and previously registered data sources.
### Configure scheduled sync frequency
[Section titled “Configure scheduled sync frequency”](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/ui/#configure-scheduled-sync-frequency)
You can configure the scheduled sync frequency of your data source by going to the `Data Sources`, then scrolling down to the `Connectors` section, and clicking on the `Settings` icon on the right of the data source details.
Then, on the modal that pops up, you can select the desired sync frequency.
For more details on scheduled sync, including how the sync timing works, refer to the [Scheduled sync section](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/ui/#scheduled-sync) earlier in this page.
## Observe ingestion status & history
[Section titled “Observe ingestion status & history”](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/ui/#observe-ingestion-status--history)
Navigate to index overview tab. You should see:
  * the latest ingestion status on the `Index Information` card (top right), and
  * ingestion job history on the `Activity` card (bottom left). 


## Test retrieval endpoint
[Section titled “Test retrieval endpoint”](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/ui/#test-retrieval-endpoint)
Navigate to `Playground` tab to test your retrieval endpoint.
Select between `Fast`, `Accurate`, and `Advanced` retrieval modes.
  * `Fast`: Only dense retrieval
  * `Accurate`: Use hybrid search with dense & sparse retrieval and re-ranking
  * `Advanced`: Full customizability for tuning hybrid search and re-ranking


Input test query and specify retrieval configurations (e.g. base retrieval and top n after re-ranking) and click `Run` button to see preview for retrieved nodes. 
Click `Copy` from bottom left panel to make direct REST API calls to the retrieval endpoint.
