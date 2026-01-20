[Skip to content](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/advanced/#_top)
# Advanced
LlamaCloud comes with a few advanced retrieval techniques that allow you to improve the accuracy of the retrieval.
## Hybrid Search
[Section titled “Hybrid Search”](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/advanced/#hybrid-search)
Hybrid search combines the strengths of both vector search and keyword search to improve retrieval accuracy. By leveraging the advantages of both methods, hybrid search can provide more relevant results.
**Note:** Hybrid search is currently only supported by a few vector databases. See [data sinks](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks) for a list of databases that support this feature.
### How Hybrid Search Works
[Section titled “How Hybrid Search Works”](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/advanced/#how-hybrid-search-works)
  1. **Vector Search** : This method uses vector embeddings to find documents that are semantically similar to the query. It is particularly useful for capturing the meaning and context of the query, even if the exact keywords are not present in the documents.
  2. **Keyword Search** : This method looks for exact matches of the query keywords in the documents. It is effective for finding documents that contain specific terms.


By combining these two methods, hybrid search can return results that are both contextually relevant and contain the specific keywords from the query.
Here’s how you can include hybrid search in your Retrieval API requests:
  * [ Python Framework ](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/advanced/#tab-panel-48)
  * [ TypeScript Framework ](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/advanced/#tab-panel-49)


```


import os




os.environ[



"LLAMA_CLOUD_API_KEY"




] ="llx-..."# can provide API-key in env or in the constructor later on





from llama_cloud_services import LlamaCloudIndex




# connect to existing index



index =LlamaCloudIndex("my_first_index",project_name="Default")




# configure retriever



retriever = index.as_retriever(




dense_similarity_top_k=3,




sparse_similarity_top_k=3,




alpha=0.5,




enable_reranking=False,





nodes = retriever.retrieve("Example query")


```

TODO: TypeScript 🐱
## Re-ranking
[Section titled “Re-ranking”](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/advanced/#re-ranking)
Re-ranking is a technique used to improve the order of search results by applying ranking models to the initial set of retrieved document chunks. This can help in presenting the most relevant chunks at the top of the search results. One common technique is to set a high top-k value, then use re-ranking to improve the order of the results, and then choose the first few results from the re-ranked results as the basis for your final response.
Here’s how you can include re-ranking in your Retrieval API requests:
  * [ Python Framework ](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/advanced/#tab-panel-50)
  * [ TypeScript Framework ](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/advanced/#tab-panel-51)


```


import os




os.environ[



"LLAMA_CLOUD_API_KEY"




] ="llx-..."# can provide API-key in env or in the constructor later on





from llama_cloud_services import LlamaCloudIndex




# connect to existing index



index =LlamaCloudIndex("my_first_index",project_name="Default")




# configure retriever



retriever = index.as_retriever(




dense_similarity_top_k=3,




sparse_similarity_top_k=3,




alpha=0.5,




enable_reranking=True,




rerank_top_n=3,





nodes = retriever.retrieve("Example query")


```

```

import { LlamaCloudIndex } from "llama-cloud-services";



// connect to existing index


const index = new LlamaCloudIndex({



name: "example-pipeline",




projectName: "Default",




apiKey: process.env.LLAMA_CLOUD_API_KEY, // can provide API-key in the constructor or in the env



});



// configure retriever


const retriever = index.asRetriever({



similarityTopK: 3,




sparseSimilarityTopK: 3,




alpha: 0.5,




enableReranking: true,




rerankTopN: 3,



});



const nodes = retriever.retrieve({



query: "Example Query"



});

```

## Metadata Filtering
[Section titled “Metadata Filtering”](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/advanced/#metadata-filtering)
Metadata filtering allows you to narrow down your search results based on specific attributes or tags associated with the documents. This can be particularly useful when you have a large dataset and want to focus on a subset of documents that meet certain criteria.
Here are a few use cases where metadata filtering would be useful:
  * Only retrieve chunks from a set of specific files
  * Implement access control by filtering by User IDs or User Group IDs that each document is associated with
  * Filter documents based on their creation or modification date to retrieve the most recent or relevant information.
  * Apply metadata filtering to focus on documents that contain specific tags or categories, such as “financial reports” or “technical documentation.”


Here’s how you can include metadata filtering in your Retrieval API requests:
  * [ Python Framework ](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/advanced/#tab-panel-52)
  * [ TypeScript Framework ](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/advanced/#tab-panel-53)


```


import os




os.environ[



"LLAMA_CLOUD_API_KEY"




] ="llx-..."# can provide API-key in env or in the constructor later on





from llama_cloud_services import LlamaCloudIndex




from llama_index.core.vector_stores import (




MetadataFilter,




MetadataFilters,




FilterOperator,





# connect to existing index



index =LlamaCloudIndex("my_first_index",project_name="Default")




# create metadata filter



filters =MetadataFilters(




filters=[




MetadataFilter(




key="theme",operator=FilterOperator.EQ,value="Fiction"







# configure retriever



retriever = index.as_retriever(




dense_similarity_top_k=3,




sparse_similarity_top_k=3,




alpha=0.5,




enable_reranking=True,




rerank_top_n=3,




filters=filters,





nodes = retriever.retrieve("Example query")


```

```

import { LlamaCloudIndex } from "llama-cloud-services";



// connect to existing index


const index = new LlamaCloudIndex({



name: "example-pipeline",




projectName: "Default",




apiKey: process.env.LLAMA_CLOUD_API_KEY, // can provide API-key in the constructor or in the env



});



// create metadata filter


const filters = {



filters: [





key: "theme",




operator: "==",




value: "Fiction",







// configure retriever


const retriever = index.asRetriever({



similarityTopK: 3,




sparseSimilarityTopK: 3,




alpha: 0.5,




enableReranking: true,




rerankTopN: 3,



});



const nodes = retriever.retrieve({



query: "Example Query"




preFilters: filters



});

```

## Metadata Filter Inference
[Section titled “Metadata Filter Inference”](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/advanced/#metadata-filter-inference)
Metadata Filter Inference automatically infers search filters from a query using a metadata schema. This can help improve search precision by leveraging metadata attributes without manual filter specification.
This is very similar to Auto-Retrieval from the [LlamaIndex framework](https://docs.llamaindex.ai/en/stable/examples/vector_stores/elasticsearch_auto_retriever/).
Here are a few use cases where metadata filter inference would be useful:
  * Automatically filter documents based on inferred criteria from the query.
  * Account for temporal context in the query. 
    * e.g. a user’s query for “What are the latest updates from the past year?” should be filtered to only include documents from the past year.


Using the `search_filters_inference_schema` parameter, you can specify a [Pydantic](https://docs.pydantic.dev/latest/) model that will be used to infer the filters from the query. You will need to carefully craft the docstring & field descriptions to ensure the model can infer the correct filters.
Here’s how you can include metadata filter inference in your Retrieval API requests:
  * [ Python Framework ](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/advanced/#tab-panel-47)


```


import os




from pydantic import BaseModel, Field




from llama_cloud_services import LlamaCloudIndex




# Set your API key



os.environ["LLAMA_CLOUD_API_KEY"] ="llx-..."# Replace with your actual API key




# Define a Pydantic model for the metadata schema


# The docstring & field description are used to describe the schema to the model.



classMetadataSchema(BaseModel):





Metadata schema for the index.





theme: str=Field(description="The theme of the document. Starts with a uppercase letter.")




author: str=Field(description="The author of the document. First name only, starts with a uppercase letter.")




# Connect to an existing index



index =LlamaCloudIndex("my_first_index",project_name="Default")




# Configure retriever with metadata filter inference



retriever = index.as_retriever(




dense_similarity_top_k=3,




sparse_similarity_top_k=3,




alpha=0.5,




enable_reranking=True,




rerank_top_n=3,




search_filters_inference_schema=MetadataSchema,





# Perform retrieval with inferred filters



nodes = retriever.retrieve("Find documents about Fiction by Alice")



# all returned nodes will have metadata where theme="Fiction" and author="Alice"

```

### Crafting the Schema
[Section titled “Crafting the Schema”](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/advanced/#crafting-the-schema)
The schema descriptions, docstrings, and types need to be described very deliberately as they are provided to the model to infer the filters from the query.
Here are some tips for crafting the schema for metadata filter inference:
  * Fill in the docstring on the Pydantic model to describe the schema to the model.
  * Use the `description` field to describe the schema to the model.
  * Use a granular `type` annotation on the field.
  * Specify any casing requirements in the `description` field.
  * When describing a date/datetime field, use the `date` or `datetime` type. Descirbe the format of the date/datetime in the `description` field.
  * When a field is a string from a constrained set of values, use an `Enum` type.


