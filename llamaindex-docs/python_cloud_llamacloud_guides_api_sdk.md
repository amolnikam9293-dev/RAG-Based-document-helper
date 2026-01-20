[Skip to content](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#_top)
# Index API & Clients Guide
This guide highlights the core workflow for working with Index programmatically.
### App setup
[Section titled “App setup”](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#app-setup)
  * [ Python Sync Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#tab-panel-8)
  * [ Python Async Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#tab-panel-9)
  * [ TypeScript Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#tab-panel-10)


Install API client package
```


pip install llama-cloud


```

Import and configure client
```


from llama_cloud.client import LlamaCloud





client =LlamaCloud(token='<llama-cloud-api-key>')


```

Install API client package
```


pip install llama-cloud


```

Import and configure client
```


from llama_cloud.client import AsyncLlamaCloud





async_client =AsyncLlamaCloud(token='<llama-cloud-api-key>')


```

Install API client package
```

npm install llama-cloud-services

```

## Create new index
[Section titled “Create new index”](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#create-new-index)
### Upload files
[Section titled “Upload files”](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#upload-files)
  * [ Python Sync Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#tab-panel-11)
  * [ Python Async Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#tab-panel-12)
  * [ TypeScript Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#tab-panel-13)


```


withopen('test.pdf','rb') as f:




file= client.files.upload_file(upload_file=f)


```

```


withopen('test.pdf','rb') as f:




file=await async_client.files.upload_file(upload_file=f)


```

```

import fs from "fs";


import { uploadFileApiV1FilesPost } from "llama-cloud-services/api";



const fileBlob = new Blob([fs.createReadStream("./test.pdf")]);



const file = await uploadFileApiV1FilesPost({



headers: {




Authorization:




"Bearer llx-...",





query: {




project_id: "...",





body: {




upload_file: fileBlob,




});



console.log(file.data?.id);

```

### Configure data sources
[Section titled “Configure data sources”](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#configure-data-sources)
  * [ Python Sync Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#tab-panel-14)
  * [ Python Async Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#tab-panel-15)
  * [ TypeScript Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#tab-panel-16)


```


from llama_cloud.types import CloudS3DataSource





ds = {




'name': 's3',




'source_type': 'S3',




'component': CloudS3DataSource(bucket='test-bucket')





data_source = client.data_sources.create_data_source(request=ds)


```

```


from llama_cloud.types import CloudS3DataSource





ds = {




'name': 's3',




'source_type': 'S3',




'component': CloudS3DataSource(bucket='test-bucket')





data_source =await async_client.data_sources.create_data_source(request=ds)


```

```

import { createDataSourceApiV1DataSourcesPost } from "llama-cloud-services/api";



const data_source = await createDataSourceApiV1DataSourcesPost({



headers: {




Authorization:




"Bearer llx-...",





query: {




project_id: "...",





body: {




name: "s3",




source_type: "S3",




component: {




bucket: "test-bucket",





});



console.log(data_source.data?.id);

```

### Configure data sinks
[Section titled “Configure data sinks”](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#configure-data-sinks)
  * [ Python Sync Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#tab-panel-17)
  * [ Python Async Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#tab-panel-18)
  * [ TypeScript Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#tab-panel-19)


```


from llama_cloud.types import CloudPineconeVectorStore





ds = {




'name': 'pinecone',




'sink_type': 'PINECONE',




'component': CloudPineconeVectorStore(api_key='test-key',index_name='test-index')





data_sink = client.data_sinks.create_data_sink(request=ds)


```

```


from llama_cloud.types import CloudPineconeVectorStore





ds = {




'name': 'pinecone',




'sink_type': 'PINECONE',




'component': CloudPineconeVectorStore(api_key='test-key',index_name='test-index')





data_sink =await async_client.data_sinks.create_data_sink(request=ds)


```

```

import { createDataSinkApiV1DataSinksPost } from "llama-cloud-services/api";



const data_sink = await createDataSinkApiV1DataSinksPost({



headers: {




Authorization:




"Bearer llx-...",





query: {




project_id: "...",





body: {




name: "pinecone",




sink_type: "PINECONE",




component: {




api_key: "...",




index_name: "my-index-in-pinecone",





});



console.log(data_sink.data?.id);

```

### Setup transformation and embedding config
[Section titled “Setup transformation and embedding config”](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#setup-transformation-and-embedding-config)
```

# Embedding config



embedding_config = {




'type': 'OPENAI_EMBEDDING',




'component': {




'api_key': '<YOUR_API_KEY_HERE>', # editable




'model_name': 'text-embedding-ada-002'# editable






# Transformation auto config



transform_config = {




'mode': 'auto',




'config': {




'chunk_size': 1024, # editable




'chunk_overlap': 20# editable




```

### Create index (i.e. pipeline)
[Section titled “Create index (i.e. pipeline)”](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#create-index-ie-pipeline)
  * [ Python Sync Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#tab-panel-20)
  * [ Python Async Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#tab-panel-21)
  * [ TypeScript Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#tab-panel-22)


```


pipeline = {




'name': 'test-pipeline',




'embedding_config': embedding_config,




'transform_config': transform_config,




'data_sink_id': data_sink.id






pipeline = client.pipelines.upsert_pipeline(request=pipeline)


```

```


pipeline = {




'name': 'test-pipeline',




'embedding_config': embedding_config,




'transform_config': transform_config,




'data_sink_id': data_sink.id






pipeline =await async_client.pipelines.upsert_pipeline(request=pipeline)


```

```

import { upsertPipelineApiV1PipelinesPut } from "llama-cloud-services/api";



const pipeline = await upsertPipelineApiV1PipelinesPut({



headers: {




Authorization:




"Bearer llx-...",





query: {




project_id: "...",





body: {




name: "pipeline",




embedding_config: { ...},




transform_config: { ...},




data_sink_id: data_sink.data?.id,




});



console.log(pipeline.data?.id);

```

### Add files to index
[Section titled “Add files to index”](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#add-files-to-index)
  * [ Python Sync Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#tab-panel-23)
  * [ Python Async Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#tab-panel-24)
  * [ TypeScript Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#tab-panel-25)


```


files =[





'file_id': file.id,




'custom_metadata': {




'document_type': 'INVOICE'# Optioal, an example on how to add custom metadata to your files








pipeline_files = client.pipeline_files.add_files_to_pipeline(pipeline.id,request=files)


```

```


files =[





'file_id': file.id,




'custom_metadata': {




'document_type': 'INVOICE'# Optioal, an example on how to add custom metadata to your files








pipeline_files =await async_client.pipeline_files.add_files_to_pipeline(pipeline.id,request=files)


```

```

import { addFilesToPipelineApiApiV1PipelinesPipelineIdFilesPut } from "llama-cloud-services/api";




const files = await addFilesToPipelineApiApiV1PipelinesPipelineIdFilesPut({



headers: {




Authorization:




"Bearer llx-...",





path: {




pipeline_id: "...",





body: [





file_id: file.data?.id,




custom_metadata: {




document_type: 'INVOICE' // Optioal, an example on how to add custom metadata to your files






});



console.log(files.data?.length);

```

### Add data sources to index
[Section titled “Add data sources to index”](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#add-data-sources-to-index)
  * [ Python Sync Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#tab-panel-26)
  * [ Python Async Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#tab-panel-27)
  * [ TypeScript Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#tab-panel-28)


```


data_sources =[





'data_source_id': data_source.id,




'sync_interval': 43200.0# Optional, scheduled sync frequency in seconds. In this case, every 12 hours.







pipeline_data_sources = client.pipelines.add_data_sources_to_pipeline(pipeline.id,request=data_sources)


```

```


data_sources =[





'data_source_id': data_source.id,




'sync_interval': 43200.0# Optional, scheduled sync frequency in seconds. In this case, every 12 hours.







pipeline_data_sources =await async_client.pipelines.add_data_sources_to_pipeline(pipeline.id,request=data_sources)


```

```

import { addDataSourcesToPipelineApiV1PipelinesPipelineIdDataSourcesPut } from "llama-cloud-services/api";




const data_sources = await addDataSourcesToPipelineApiV1PipelinesPipelineIdDataSourcesPut({



headers: {




Authorization:




"Bearer llx-...",





path: {




pipeline_id: "...",





body: [





data_source_id: data_source.data?.id,




sync_interval: 43200.0 // Optional, scheduled sync frequency in seconds. In this case, every 12 hours.





});



console.log(data_sources.data?.length);

```

### Add documents to index
[Section titled “Add documents to index”](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#add-documents-to-index)
  * [ Python Sync Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#tab-panel-29)
  * [ Python Async Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#tab-panel-30)
  * [ TypeScript Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#tab-panel-31)


```


from llama_cloud.types import CloudDocumentCreate





documents =[




CloudDocumentCreate(




text='test-text',




metadata={




'test-key': 'test-val'








documents = client.pipelines.create_batch_pipeline_documents(pipeline.id,request=documents)


```

```


from llama_cloud.types import CloudDocumentCreate





documents =[




CloudDocumentCreate(




text='test-text',




metadata={




'test-key': 'test-val'








documents =await async_client.pipelines.create_batch_pipeline_documents(pipeline.id,request=documents)


```

```

import { createBatchPipelineDocumentsApiV1PipelinesPipelineIdDocumentsPost } from "llama-cloud-services/api";



const documents = await createBatchPipelineDocumentsApiV1PipelinesPipelineIdDocumentsPost({



headers: {




Authorization:




"Bearer llx-...",





path: {




pipeline_id: "...",





body: [





text: "test-text",




metadata: {




text_key: 'text_val'






});



console.log(documents.data?.length);

```

## Observe ingestion status & history
[Section titled “Observe ingestion status & history”](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#observe-ingestion-status--history)
### Get index status
[Section titled “Get index status”](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#get-index-status)
  * [ Python Sync Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#tab-panel-32)
  * [ Python Async Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#tab-panel-33)
  * [ TypeScript Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#tab-panel-34)


```


status = client.pipelines.get_pipeline_status(pipeline.id)


```

```


status =await async_client.pipelines.get_pipeline_status(pipeline.id)


```

```

import { getPipelineStatusApiV1PipelinesPipelineIdStatusGet } from "llama-cloud-services/api";




const status = await getPipelineStatusApiV1PipelinesPipelineIdStatusGet({



headers: {




Authorization:




"Bearer llx-...",





path: {




pipeline_id: "...",




});



console.log(status.data?.status);

```

### Get ingestion job history
[Section titled “Get ingestion job history”](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#get-ingestion-job-history)
  * [ Python Sync Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#tab-panel-35)
  * [ Python Async Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#tab-panel-36)
  * [ TypeScript Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#tab-panel-37)


```


jobs = client.pipelines.list_pipeline_jobs(pipeline.id)


```

```


jobs =await async_client.pipelines.list_pipeline_jobs(pipeline.id)


```

```

import { listPipelineJobsApiV1PipelinesPipelineIdJobsGet } from "llama-cloud-services/api";



const jobs = await listPipelineJobsApiV1PipelinesPipelineIdJobsGet({



headers: {




Authorization:




"Bearer llx-...",





path: {




pipeline_id: "...",




});



console.log(jobs.data?.length);

```

## Run search (i.e. retrieval endpoint)
[Section titled “Run search (i.e. retrieval endpoint)”](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#run-search-ie-retrieval-endpoint)
  * [ Python Sync Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#tab-panel-38)
  * [ Python Async Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#tab-panel-39)
  * [ TypeScript Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/#tab-panel-40)


```


results = client.pipelines.run_search(pipeline.id,query='test-query')


```

```


results =await async_client.pipelines.run_search(pipeline.id,query='test-query')


```

```

import { runSearchApiV1PipelinesPipelineIdRetrievePost } from "llama-cloud-services/api";



const results = await runSearchApiV1PipelinesPipelineIdRetrievePost({



headers: {




Authorization:




"Bearer llx-...",





path: {




pipeline_id: "...",





body: {




query: "text-query",




});



console.log(results.data?.retrieval_nodes?.length);

```

