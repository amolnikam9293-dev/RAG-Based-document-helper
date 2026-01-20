[Skip to content](https://developers.llamaindex.ai/python/cloud/llamacloud/parsing_transformation/#_top)
# Parsing & Transformation
Once data is loaded from a Data Source, it is pre-processed before being sent to the Data Sink. There are many pre-processing parameters that can be tweaked to optimize the downstream retrieval performance of your index. While Index sets you up with reasonable defaults, you can dig deeper and customize them as you see fit for your specific use case.
## Parser Settings
[Section titled “Parser Settings”](https://developers.llamaindex.ai/python/cloud/llamacloud/parsing_transformation/#parser-settings)
A key step of any RAG pipeline is converting your input file into a format that can be used to generate a vector embedding. There are many parameters that can be used to tweak this conversion process to optimize for your use case. Index sets you up from the start with reasonable defaults for your parsing configurations, but also allows you to dig deeper and customize them as you see fit for your specific application.
## Transformation Settings
[Section titled “Transformation Settings”](https://developers.llamaindex.ai/python/cloud/llamacloud/parsing_transformation/#transformation-settings)
The transform configuration is used to define the transformation of the data before it is ingested into the Index. it is a JSON object which you can choose between two modes `auto` and `advanced` and as the name suggests, the `auto` mode is handled by Index which uses a set of default configurations and the `advanced` mode is handled by the user with the ability to define their own transformation.
### Auto Mode
[Section titled “Auto Mode”](https://developers.llamaindex.ai/python/cloud/llamacloud/parsing_transformation/#auto-mode)
You can set the mode by passing the `transform_config` as below on index creation or update.
```


transform_config = {




"mode": "auto"



```

Also when using the `auto` mode, you can configure the chunk size being used for the transformation by passing the `chunk_size` and `chunk_overlap` parameter as below.
```


transform_config = {




"mode": "auto",




"chunk_size": 1000,




"chunk_overlap": 100



```

### Advanced Mode
[Section titled “Advanced Mode”](https://developers.llamaindex.ai/python/cloud/llamacloud/parsing_transformation/#advanced-mode)
The advanced mode provides a variation of configuration options for the user to define their own transformation. The advanced mode is defined by the `mode` parameter as `advanced` and the `segmentation_config` and `chunking_config` parameters are used to define the segmentation and chunking configuration respectively.
```


transform_config = {




"mode": "advanced",




"segmentation_config": {




"mode": "page",




"page_separator": "\n---\n"





"chunking_config": {




"mode": "sentence",




"separator": "",




"paragraph_separator": "\n"




```

### Segmentation Configuration
[Section titled “Segmentation Configuration”](https://developers.llamaindex.ai/python/cloud/llamacloud/parsing_transformation/#segmentation-configuration)
The segmentation configuration uses the document structure and/or semantics to divide the documents into smaller parts following natural segmentation boundaries. The `segmentation_config` parameter include three modes `none`, `page` and `element`.
##### None Segmentation Configuration
[Section titled “None Segmentation Configuration”](https://developers.llamaindex.ai/python/cloud/llamacloud/parsing_transformation/#none-segmentation-configuration)
The `none` segmentation configuration is used to define no segmentation.
```


transform_config = {




"mode": "advanced",




"segmentation_config": {




"mode": "none"




```

##### Page Segmentation Configuration
[Section titled “Page Segmentation Configuration”](https://developers.llamaindex.ai/python/cloud/llamacloud/parsing_transformation/#page-segmentation-configuration)
The `page` segmentation configuration is used to define the segmentation by page and the `page_separator` parameter is used to define the separator, which will split your document into pages.
```


transform_config = {




"mode": "advanced",




"segmentation_config": {




"mode": "page",




"page_separator": "\n---\n"




```

##### Element Segmentation Configuration
[Section titled “Element Segmentation Configuration”](https://developers.llamaindex.ai/python/cloud/llamacloud/parsing_transformation/#element-segmentation-configuration)
The `element` segmentation configuration is used to define the segmentation by element which identifies the elements from the document as title, paragraph, list, table, etc.
```


transform_config = {




"mode": "advanced",




"segmentation_config": {




"mode": "element"




```

### Chunking Configuration
[Section titled “Chunking Configuration”](https://developers.llamaindex.ai/python/cloud/llamacloud/parsing_transformation/#chunking-configuration)
Chunking configuration is mainly used to deal with context window limitaitons of embeddings model and LLMs. Conceptually, it’s the step after segmenting, where segments are further broken down into smaller chunks as necessary to fit into the context window. It include a few modes `none`, `character`, `token`, `sentence` and `semantic`.
Also all chunk config modes allow the user to define the `chunk_size` and `chunk_overlap` parameters. In the examples below we are not always defining the chunk_size and chunk_overlap parameters but you can always define them.
#### None Chunking Configuration
[Section titled “None Chunking Configuration”](https://developers.llamaindex.ai/python/cloud/llamacloud/parsing_transformation/#none-chunking-configuration)
The `none` chunking configuration is used to define no chunking.
```


transform_config = {




"mode": "advanced",




"chunking_config": {




"mode": "none"




```

#### Character Chunking Configuration
[Section titled “Character Chunking Configuration”](https://developers.llamaindex.ai/python/cloud/llamacloud/parsing_transformation/#character-chunking-configuration)
The `character` chunking configuration is used to define the chunking by character and the `chunk_size` parameter is used to define the size of the chunk.
```


transform_config = {




"mode": "advanced",




"chunking_config": {




"mode": "character",




"chunk_size": 1000




```

#### Token Chunking Configuration
[Section titled “Token Chunking Configuration”](https://developers.llamaindex.ai/python/cloud/llamacloud/parsing_transformation/#token-chunking-configuration)
The `token` chunking configuration is used to define the chunking by token and uses [OpenAI tokenizer](https://developers.llamaindex.ai/python/cloud/llamacloud/parsing_transformation/%22https:/github.com/openai/tiktoken%22) behind the hood. Also`chunk_size` and `chunk_overlap` parameters are used to define the size of the chunk and the overlap between the chunks.
```


transform_config = {




"mode": "advanced",




"chunking_config": {




"mode": "token",




"chunk_size": 1000,




"chunk_overlap": 100




```

#### Sentence Chunking Configuration
[Section titled “Sentence Chunking Configuration”](https://developers.llamaindex.ai/python/cloud/llamacloud/parsing_transformation/#sentence-chunking-configuration)
The `sentence` chunking configuration is used to define the chunking by sentence and the `separator` and `paragraph_separator` parameters are used to define the separator between the sentences and paragraphs.
```


transform_config = {




"mode": "advanced",




"chunking_config": {




"mode": "sentence",




"separator": "",




"paragraph_separator": "\n"




```

## Embedding Model
[Section titled “Embedding Model”](https://developers.llamaindex.ai/python/cloud/llamacloud/parsing_transformation/#embedding-model)
The embedding model allows you to construct a numerical representation of the text within your files. This is a crucial step in allowing you to search for specific information within your files. There are a wide variety of embedding models to choose from, and we support quite a few with Index.
## Sparse Model Configuration
[Section titled “Sparse Model Configuration”](https://developers.llamaindex.ai/python/cloud/llamacloud/parsing_transformation/#sparse-model-configuration)
The sparse model configuration enables hybrid search by combining dense embeddings with sparse embeddings for improved retrieval accuracy. This configuration is particularly useful for scenarios where you want to leverage both semantic similarity (dense) and keyword matching (sparse) capabilities.
### Available Sparse Models
[Section titled “Available Sparse Models”](https://developers.llamaindex.ai/python/cloud/llamacloud/parsing_transformation/#available-sparse-models)
Index supports three sparse model types:
  * **`auto`**(default): Automatically selects the appropriate sparse model (Default: Splade)
  * **`splade`**: Uses SPLADE model for learned sparse representations
  * **`bm25`**: Uses Qdrant’s FastEmbed BM25 model for traditional keyword-based sparse embeddings


### Configuration
[Section titled “Configuration”](https://developers.llamaindex.ai/python/cloud/llamacloud/parsing_transformation/#configuration)
You can configure the sparse model when creating or updating a pipeline:
```


from llama_cloud import LlamaCloudClient





client =LlamaCloudClient(api_key="your_api_key")




# Create pipeline with sparse model configuration



pipeline = client.pipelines.create_pipeline(




name="my-hybrid-pipeline",




# ... other pipeline configuration ...




sparse_model_config={




"model_type": "splade"# or "bm25", "auto"




```

### Usage in Retrieval
[Section titled “Usage in Retrieval”](https://developers.llamaindex.ai/python/cloud/llamacloud/parsing_transformation/#usage-in-retrieval)
When using hybrid search with configured sparse models, you can control the balance between dense and sparse retrieval:
```


from llama_cloud_services import LlamaCloudIndex




# Connect to your pipeline



index =LlamaCloudIndex("my-hybrid-pipeline",project_name="Default")




# Configure retriever for hybrid search



retriever = index.as_retriever(




dense_similarity_top_k=5,# Number of results from dense search




sparse_similarity_top_k=5,# Number of results from sparse search




alpha=0.5,# Balance between dense (0.0) and sparse (1.0)




enable_reranking=True,# Optional reranking for better results




rerank_top_n=10# Number of results to rerank






nodes = retriever.retrieve("your search query")


```

After Pre-Processing, your data is ready to be sent to the Data Sink ➡️
