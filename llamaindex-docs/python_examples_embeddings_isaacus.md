[Skip to content](https://developers.llamaindex.ai/python/examples/embeddings/isaacus/#_top)
# Isaacus Embeddings 
The `llama-index-embeddings-isaacus` package contains LlamaIndex integrations for building applications with Isaacus’ legal AI embedding models. This integration allows you to easily connect to and use the **Kanon 2 Embedder** - the world’s most accurate legal embedding model on the [Massive Legal Embedding Benchmark (MLEB)](https://isaacus.com/blog/introducing-mleb).
Isaacus embeddings support task-specific optimization:
  * `task="retrieval/query"`: Optimize embeddings for search queries
  * `task="retrieval/document"`: Optimize embeddings for documents to be indexed


In this notebook, we will demonstrate using Isaacus Embeddings for legal document retrieval.
## Installation
[Section titled “Installation”](https://developers.llamaindex.ai/python/examples/embeddings/isaacus/#installation)
Install the necessary integrations.
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
```


%pip install llama-index-embeddings-isaacus




%pip install llama-index-llms-openai


```

```


%pip install llama-index


```

## Setup
[Section titled “Setup”](https://developers.llamaindex.ai/python/examples/embeddings/isaacus/#setup)
### Get your Isaacus API key
[Section titled “Get your Isaacus API key”](https://developers.llamaindex.ai/python/examples/embeddings/isaacus/#get-your-isaacus-api-key)
  1. Create an account at [Isaacus Platform](https://platform.isaacus.com/accounts/signup/)
  2. Add a [payment method](https://platform.isaacus.com/billing/) to claim your [free credits](https://docs.isaacus.com/pricing/credits)
  3. Create an [API key](https://platform.isaacus.com/users/api-keys/)


```


import os




# Set your Isaacus API key



isaacus_api_key ="YOUR_ISAACUS_API_KEY"




os.environ["ISAACUS_API_KEY"] = isaacus_api_key


```

## Basic Usage
[Section titled “Basic Usage”](https://developers.llamaindex.ai/python/examples/embeddings/isaacus/#basic-usage)
### Get a Single Embedding
[Section titled “Get a Single Embedding”](https://developers.llamaindex.ai/python/examples/embeddings/isaacus/#get-a-single-embedding)
```


from llama_index.embeddings.isaacus import IsaacusEmbedding




# Initialize the Isaacus Embedding model



embed_model =IsaacusEmbedding(




api_key=isaacus_api_key,




model="kanon-2-embedder",





# Get a single embedding



embedding = embed_model.get_text_embedding(




"This agreement shall be governed by the laws of Delaware."






print(f"Embedding dimension: (embedding)}")




print(f"First 5 values: {embedding[:5]}")


```

### Get Batch Embeddings
[Section titled “Get Batch Embeddings”](https://developers.llamaindex.ai/python/examples/embeddings/isaacus/#get-batch-embeddings)
```

# Get embeddings for multiple legal texts



legal_texts =[




"The parties agree to binding arbitration.",




"Confidential information shall not be disclosed.",




"This contract may be terminated with 30 days notice.",






embeddings = embed_model.get_text_embedding_batch(legal_texts)





print(f"Number of embeddings: (embeddings)}")




print(f"Each embedding has (embeddings[0])} dimensions")


```

## Task-Specific Embeddings
[Section titled “Task-Specific Embeddings”](https://developers.llamaindex.ai/python/examples/embeddings/isaacus/#task-specific-embeddings)
Isaacus embeddings support different tasks for optimal performance:
  * **`retrieval/document`**: For documents to be indexed
  * **`retrieval/query`**: For search queries


Using the appropriate task improves retrieval accuracy.
```

# For documents (use when indexing)



doc_embed_model =IsaacusEmbedding(




api_key=isaacus_api_key,




task="retrieval/document",






doc_embedding = doc_embed_model.get_text_embedding(




"The Company has the right to terminate this agreement."






print(f"Document embedding dimension: (doc_embedding)}")


```

```

# For queries (automatically used by get_query_embedding)



query_embedding = embed_model.get_query_embedding(




"What are the termination conditions?"






print(f"Query embedding dimension: (query_embedding)}")


```

## Dimensionality Reduction
[Section titled “Dimensionality Reduction”](https://developers.llamaindex.ai/python/examples/embeddings/isaacus/#dimensionality-reduction)
You can reduce the embedding dimensionality for faster search and lower storage costs:
```

# Use reduced dimensions (default is 1792)



embed_model_512 =IsaacusEmbedding(




api_key=isaacus_api_key,




dimensions=512,






embedding_512 = embed_model_512.get_text_embedding("Legal text example")





print(f"Reduced embedding dimension: (embedding_512)}")


```

## Full RAG Example with Legal Documents
[Section titled “Full RAG Example with Legal Documents”](https://developers.llamaindex.ai/python/examples/embeddings/isaacus/#full-rag-example-with-legal-documents)
Now let’s build a complete RAG pipeline using Isaacus embeddings with a legal document (Uber’s 10-K SEC filing).
```


import logging




import sys





logging.basicConfig(stream=sys.stdout,level=logging.INFO)




logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))





from llama_index.core import VectorStoreIndex, SimpleDirectoryReader




from llama_index.llms.openai import OpenAI




from llama_index.core.response.notebook_utils import display_source_node




from IPython.display import Markdown, display


```

### Download Legal Document Data
[Section titled “Download Legal Document Data”](https://developers.llamaindex.ai/python/examples/embeddings/isaacus/#download-legal-document-data)
We’ll use Uber’s 10-K SEC filing, which contains legal and regulatory information - perfect for demonstrating Kanon 2’s legal domain expertise.
```


!mkdir -p 'data/10k/'




!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/10k/uber_2021.pdf'-O 'data/10k/uber_2021.pdf'


```

### Load the Legal Document
[Section titled “Load the Legal Document”](https://developers.llamaindex.ai/python/examples/embeddings/isaacus/#load-the-legal-document)
```


documents =SimpleDirectoryReader("./data/10k/").load_data()




print(f"Loaded (documents)} document(s)")


```

### Build Index with Document Task
[Section titled “Build Index with Document Task”](https://developers.llamaindex.ai/python/examples/embeddings/isaacus/#build-index-with-document-task)
We use `task="retrieval/document"` when building the index to optimize embeddings for document storage.
```

# Initialize embedding model for documents



embed_model =IsaacusEmbedding(




api_key=isaacus_api_key,




model="kanon-2-embedder",




task="retrieval/document",





# Build the index



index = VectorStoreIndex.from_documents(




documents=documents,




embed_model=embed_model,



```

### Query with Legal Questions
[Section titled “Query with Legal Questions”](https://developers.llamaindex.ai/python/examples/embeddings/isaacus/#query-with-legal-questions)
Now we’ll query the index with legal-specific questions. Note that `get_query_embedding` automatically uses `task="retrieval/query"` for optimal query performance.
```

# Create a retriever



retriever = index.as_retriever(similarity_top_k=3)




# Query about risk factors



retrieved_nodes = retriever.retrieve(




"What are the main risk factors mentioned in the document?"






print(f"Retrieved (retrieved_nodes)} nodes\n")





for i, node inenumerate(retrieved_nodes):




print(f"\n--- Node {i+1} (Score: {node.score:.4f}) ---")




display_source_node(node,source_length=500)


```

### Query about Legal Proceedings
[Section titled “Query about Legal Proceedings”](https://developers.llamaindex.ai/python/examples/embeddings/isaacus/#query-about-legal-proceedings)
```

# Query about legal proceedings



retrieved_nodes = retriever.retrieve(




"What legal proceedings or litigation is the company involved in?"






print(f"Retrieved (retrieved_nodes)} nodes\n")





for i, node inenumerate(retrieved_nodes):




print(f"\n--- Node {i+1} (Score: {node.score:.4f}) ---")




display_source_node(node,source_length=500)


```

### Build a Query Engine with LLM
[Section titled “Build a Query Engine with LLM”](https://developers.llamaindex.ai/python/examples/embeddings/isaacus/#build-a-query-engine-with-llm)
Combine Isaacus embeddings with an LLM for complete question answering:
```


import os




# Set your OpenAI API key



openai_api_key ="YOUR_OPENAI_API_KEY"




os.environ["OPENAI_API_KEY"] = openai_api_key


```

```

# Set up LLM



llm =OpenAI(model="gpt-4o-mini",temperature=0)




# Create query engine



query_engine = index.as_query_engine(




llm=llm,




similarity_top_k=5,





# Ask a legal question



response = query_engine.query(




"What are the company's main regulatory and legal risks?"






display(Markdown(f"**Answer:** {response}"))


```

### Another Legal Query
[Section titled “Another Legal Query”](https://developers.llamaindex.ai/python/examples/embeddings/isaacus/#another-legal-query)
```


response = query_engine.query(




"What intellectual property does the company rely on?"






display(Markdown(f"**Answer:** {response}"))


```

## Async Usage
[Section titled “Async Usage”](https://developers.llamaindex.ai/python/examples/embeddings/isaacus/#async-usage)
Isaacus embeddings also support async operations for better performance in async applications:
```


import asyncio






asyncdefget_embeddings_async():




embed_model =IsaacusEmbedding(




api_key=isaacus_api_key,






# Get async single embedding




embedding =await embed_model.aget_text_embedding(




"Async legal document text"






# Get async batch embeddings




embeddings =await embed_model.aget_text_embedding_batch(




["Text 1", "Text 2", "Text 3"]






return embedding, embeddings





# Run async function



embedding, embeddings =awaitget_embeddings_async()





print(f"Async single embedding dimension: (embedding)}")




print(




f"Async batch: (embeddings)} embeddings of (embeddings[0])} dimensions each"



```

## Summary
[Section titled “Summary”](https://developers.llamaindex.ai/python/examples/embeddings/isaacus/#summary)
In this notebook, we demonstrated:
  1. **Basic usage** - Getting single and batch embeddings
  2. **Task-specific optimization** - Using `retrieval/document` for indexing and `retrieval/query` for searching
  3. **Dimensionality reduction** - Reducing embedding size for efficiency
  4. **Legal RAG pipeline** - Building a complete retrieval system with legal documents (Uber 10-K)
  5. **Async operations** - Using async methods for better performance


The Kanon 2 Embedder excels at legal document understanding and retrieval, making it ideal for legal tech applications, compliance tools, contract analysis, and more.
## Additional Resources
[Section titled “Additional Resources”](https://developers.llamaindex.ai/python/examples/embeddings/isaacus/#additional-resources)
  * [Isaacus Documentation](https://docs.isaacus.com)
  * [Kanon 2 Embedder Announcement](https://isaacus.com/blog/introducing-kanon-2-embedder)
  * [Massive Legal Embedding Benchmark (MLEB)](https://isaacus.com/blog/introducing-mleb)
  * [Isaacus Platform](https://platform.isaacus.com)


