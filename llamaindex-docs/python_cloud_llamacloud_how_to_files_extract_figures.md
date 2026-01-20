[Skip to content](https://developers.llamaindex.ai/python/cloud/llamacloud/how_to/files/extract_figures/#_top)
# Extracting Figures from Documents
LlamaCloud provides several API endpoints to help you extract and work with figures (images) from your documents, including charts, tables, and other visual elements. This guide will show you how to use these endpoints effectively.
These figures can be used for a variety of purposes, such as creating visual summaries, generating reports, chatbot responses, and more.
## Available Endpoints
[Section titled “Available Endpoints”](https://developers.llamaindex.ai/python/cloud/llamacloud/how_to/files/extract_figures/#available-endpoints)
  1. List All Figures: `/v1/files/{id}/page-figures`
  2. List Figures on a Specific Page: `/v1/files/{id}/page-figures/{page_index}`
  3. Get a Specific Figure: `/v1/files/{id}/page-figures/{page_index}/{figure_name}`


## How to Use
[Section titled “How to Use”](https://developers.llamaindex.ai/python/cloud/llamacloud/how_to/files/extract_figures/#how-to-use)
### App setup
[Section titled “App setup”](https://developers.llamaindex.ai/python/cloud/llamacloud/how_to/files/extract_figures/#app-setup)
  * [ Python Sync Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/how_to/files/extract_figures/#tab-panel-57)
  * [ Python Async Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/how_to/files/extract_figures/#tab-panel-58)
  * [ TypeScript Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/how_to/files/extract_figures/#tab-panel-59)


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

### 1. List All Figures in a Document
[Section titled “1. List All Figures in a Document”](https://developers.llamaindex.ai/python/cloud/llamacloud/how_to/files/extract_figures/#1-list-all-figures-in-a-document)
To get a list of all figures across all pages in a document:
  * [ Python Sync Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/how_to/files/extract_figures/#tab-panel-60)
  * [ Python Async Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/how_to/files/extract_figures/#tab-panel-61)
  * [ TypeScript Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/how_to/files/extract_figures/#tab-panel-62)


```

# Get all figures from a document



figures = client.files.list_file_pages_figures="your-file-id")


```

```

# Get all figures from a document



figures =await async_client.files.list_file_pages_figures="your-file-id")


```

```


import { listFilePagesFiguresApiV1FilesIdPageFiguresGet } from'llama-cloud-services/api';




// Get all figures from a document



const figures = await listFilePagesFiguresApiV1FilesIdPageFiguresGet({




headers: {




Authorization:




"Bearer llx-...",





query: {




project_id: "...",





path: {




id: "<file_id>"







console.log(figures.data?.length);


```

output:
```




"figure_name": "page_1_figure_1.jpg",




"file_id": "71370e55-0f32-4977-b347-460735079386",




"page_index": 1,




"figure_size": 87724,




"is_likely_noise": true,




"confidence": 0.423






"figure_name": "page_2_figure_1.jpg",




"file_id": "71370e55-0f32-4977-b347-460735079386",




"page_index": 2,




"figure_size": 87724,




"is_likely_noise": true,




"confidence": 0.423




```

### 2. List Figures on a Specific Page
[Section titled “2. List Figures on a Specific Page”](https://developers.llamaindex.ai/python/cloud/llamacloud/how_to/files/extract_figures/#2-list-figures-on-a-specific-page)
To get figures from a specific page in your document:
  * [ Python Sync Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/how_to/files/extract_figures/#tab-panel-63)
  * [ Python Async Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/how_to/files/extract_figures/#tab-panel-64)
  * [ TypeScript Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/how_to/files/extract_figures/#tab-panel-65)


```

# Get figures from a specific page



page_figures = client.files.list_file_page_figures(




id="your-file-id",




page_index=1# Page numbers start at 0



```

```

# Get figures from a specific page



page_figures =await async_client.files.list_file_page_figures(




id="your-file-id",




page_index=1# Page numbers start at 0



```

```


import { listFilePageFiguresApiV1FilesIdPageFiguresPageIndexGet } from'llama-cloud-services/api';




// Get figures from a specific page



const file_page_figures = await listFilePageFiguresApiV1FilesIdPageFiguresPageIndexGet({




headers: {




Authorization:




"Bearer llx-...",





query: {




project_id: "...",





path: {




id: "<file_id>",




page_index: 1,






console.log(file_page_figures.data?.length);


```

output:
```




"figure_name": "page_1_figure_1.jpg",




"file_id": "71370e55-0f32-4977-b347-460735079386",




"page_index": 1,




"figure_size": 87724,




"is_likely_noise": true,




"confidence": 0.423






"figure_name": "page_1_figure_2.jpg",




"file_id": "71370e55-0f32-4977-b347-460735079386",




"page_index": 1,




"figure_size": 47724,




"is_likely_noise": true,




"confidence": 0.423




```

### 3. Get a Specific Figure
[Section titled “3. Get a Specific Figure”](https://developers.llamaindex.ai/python/cloud/llamacloud/how_to/files/extract_figures/#3-get-a-specific-figure)
To retrieve a specific figure from your document:
  * [ Python Sync Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/how_to/files/extract_figures/#tab-panel-66)
  * [ Python Async Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/how_to/files/extract_figures/#tab-panel-67)
  * [ TypeScript Client ](https://developers.llamaindex.ai/python/cloud/llamacloud/how_to/files/extract_figures/#tab-panel-68)


```

# Get a specific figure



figure = client.files.get_file_page_figure(




id="your-file-id",




page_index=1,




figure_name="figure1"



```

```

# Get a specific figure



figure =await async_client.files.get_file_page_figure(




id="your-file-id",




page_index=1,




figure_name="figure1"



```

```


import { getFilePageFigureApiV1FilesIdPageFiguresPageIndexFigureNameGet } from"llama-cloud-services/api";




// Get a specific figure



const figure = await getFilePageFigureApiV1FilesIdPageFiguresPageIndexFigureNameGet({




headers: {




Authorization:




"Bearer llx-...",





query: {




project_id: "...",





path: {




id: "<file_id>",




page_index: 1,




figure_name: "<figure_name>"




```

output:
Terminal window```


thebase64encodedimage


```

