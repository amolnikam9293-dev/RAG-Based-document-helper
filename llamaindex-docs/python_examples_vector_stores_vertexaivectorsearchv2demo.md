[Skip to content](https://developers.llamaindex.ai/python/examples/vector_stores/vertexaivectorsearchv2demo/#_top)
# Google Vertex AI Vector Search v2.0 
This notebook demonstrates how to use **Vertex AI Vector Search v2.0** with LlamaIndex.
> [Vertex AI Vector Search v2.0](https://cloud.google.com/vertex-ai/docs/vector-search/overview) introduces a simplified **collection-based architecture** that eliminates the need for separate index creation and endpoint deployment.
## v2.0 vs v1.0
[Section titled “v2.0 vs v1.0”](https://developers.llamaindex.ai/python/examples/vector_stores/vertexaivectorsearchv2demo/#v20-vs-v10)
Feature | v1.0 | v2.0  
---|---|---  
Architecture | Index + Endpoint | Collection  
Setup Steps | Create index → Deploy to endpoint | Create collection  
GCS Bucket | Required for batch updates | Not needed  
**Note** : For v1.0 usage, see [VertexAIVectorSearchDemo.ipynb](https://developers.llamaindex.ai/python/examples/vector_stores/vertexaivectorsearchv2demo/VertexAIVectorSearchDemo.ipynb)
## Install Dependencies
[Section titled “Install Dependencies”](https://developers.llamaindex.ai/python/examples/vector_stores/vertexaivectorsearchv2demo/#install-dependencies)
Install LlamaIndex with v2 support:
> **Note** : V2 support requires `llama-index-vector-stores-vertexaivectorsearch` version that supports Vertex AI Vector Search v2.0 API.
```

# Install with v2 support (the [v2] extra installs google-cloud-vectorsearch)


# !pip install 'llama-index-vector-stores-vertexaivectorsearch[v2]' llama-index-embeddings-vertex llama-index-llms-vertex

```

### Authentication(if using Colab):
[Section titled “Authentication(if using Colab):”](https://developers.llamaindex.ai/python/examples/vector_stores/vertexaivectorsearchv2demo/#authenticationif-using-colab)
```

# Colab authentication.



import sys





if"google.colab"in sys.modules:




from google.colab import auth





auth.authenticate_user()




print("Authenticated")


```

## Configuration
[Section titled “Configuration”](https://developers.llamaindex.ai/python/examples/vector_stores/vertexaivectorsearchv2demo/#configuration)
Set your Google Cloud project details:
```

# Google Cloud Configuration



PROJECT_ID="your-project-id"# @param {type:"string"}




REGION="us-central1"# @param {type:"string"}




COLLECTION_ID="llamaindex-demo-collection"# @param {type:"string"}




# Embedding dimensions (768 for textembedding-gecko@003)



EMBEDDING_DIMENSION=768


```

## Create a v2 Collection
[Section titled “Create a v2 Collection”](https://developers.llamaindex.ai/python/examples/vector_stores/vertexaivectorsearchv2demo/#create-a-v2-collection)
Unlike v1.0 which requires creating an index and deploying it to an endpoint, v2.0 only requires creating a collection:
```


from google.cloud import vectorsearch_v1beta




# Initialize the client



client = vectorsearch_v1beta.VectorSearchServiceClient()




# Check if collection already exists



parent =f"projects/{PROJECT_ID}/locations/{REGION}"




collection_name =f"{parent}/collections/{COLLECTION_ID}"





try:




request = vectorsearch_v1beta.GetCollectionRequest(name=collection_name)




collection = client.get_collection(request=request)




print(f"Collection already exists: {collection.name}")




exceptExceptionas e:




if"404"instr(e) or"NotFound"instr(e):




print(f"Creating collection: {COLLECTION_ID}")




request = vectorsearch_v1beta.CreateCollectionRequest(




parent=parent,




collection_id=COLLECTION_ID,




collection={




"data_schema": {




"type": "object",




"properties": {




"text": {"type": "string"},




"ref_doc_id": {"type": "string"},




"price": {"type": "number"},




"color": {"type": "string"},




"category": {"type": "string"},






"vector_schema": {




"embedding": {




"dense_vector": {"dimensions": EMBEDDING_DIMENSION}








operation = client.create_collection(request=request)




collection = operation.result()




print(f"Collection created: {collection.name}")




else:




raise e


```

## Set Up LlamaIndex Components
[Section titled “Set Up LlamaIndex Components”](https://developers.llamaindex.ai/python/examples/vector_stores/vertexaivectorsearchv2demo/#set-up-llamaindex-components)
```

# Imports



from llama_index.core import Settings, StorageContext, VectorStoreIndex




from llama_index.core.schema import TextNode




from llama_index.core.vector_stores.types import (




MetadataFilters,




MetadataFilter,




FilterOperator,





from llama_index.embeddings.vertex import VertexTextEmbedding




from llama_index.llms.vertex import Vertex




from llama_index.vector_stores.vertexaivectorsearch import VertexAIVectorStore




# Authentication - get default credentials



import google.auth





credentials, project = google.auth.default()




print(f"Authenticated with project: {project}")


```

```

# Configure embedding model



embed_model =VertexTextEmbedding(




model_name="text-embedding-004",




project=PROJECT_ID,




location=REGION,




credentials=credentials,





# Configure LLM



llm =Vertex(




model="gemini-2.5-flash",




project=PROJECT_ID,




location=REGION,




credentials=credentials,





# Set as defaults



Settings.embed_model = embed_model




Settings.llm = llm





print("Embedding model and LLM configured successfully!")


```

## Create v2 Vector Store
[Section titled “Create v2 Vector Store”](https://developers.llamaindex.ai/python/examples/vector_stores/vertexaivectorsearchv2demo/#create-v2-vector-store)
Creating a v2 vector store is simple - just specify `api_version="v2"` and your `collection_id`:
```

# Create v2 vector store



vector_store =VertexAIVectorStore(




api_version="v2",# Use v2 API




project_id=PROJECT_ID,




region=REGION,




collection_id=COLLECTION_ID,




# No index_id, endpoint_id, or gcs_bucket_name needed!






print(f"Vector store created with api_version={vector_store.api_version}")


```

## Add Documents
[Section titled “Add Documents”](https://developers.llamaindex.ai/python/examples/vector_stores/vertexaivectorsearchv2demo/#add-documents)
### Simple Text Nodes
[Section titled “Simple Text Nodes”](https://developers.llamaindex.ai/python/examples/vector_stores/vertexaivectorsearchv2demo/#simple-text-nodes)
```

# Create some sample text nodes



texts =[




"LlamaIndex is a data framework for LLM applications.",




"Vertex AI Vector Search provides scalable vector similarity search.",




"RAG combines retrieval with generation for better AI responses.",




"Embeddings convert text into numerical vectors for similarity matching.",





# Create nodes with embeddings



nodes =[




TextNode(text=text,embedding=embed_model.get_text_embedding(text))




for text in texts





# Add to vector store



ids = vector_store.add(nodes)




print(f"Added (ids)} nodes to vector store")


```

### Nodes with Metadata
[Section titled “Nodes with Metadata”](https://developers.llamaindex.ai/python/examples/vector_stores/vertexaivectorsearchv2demo/#nodes-with-metadata)
```

# Sample product data with metadata



products =[





"description": "A versatile pair of dark-wash denim jeans. Made from durable cotton with a classic straight-leg cut.",




"price": 65.00,




"color": "blue",




"category": "pants",






"description": "A lightweight linen button-down shirt in crisp white. Perfect for keeping cool with breathable fabric.",




"price": 34.99,




"color": "white",




"category": "shirts",






"description": "A soft chunky knit sweater in vibrant forest green. Oversized fit and cozy wool blend.",




"price": 89.99,




"color": "green",




"category": "sweaters",






"description": "Classic crewneck t-shirt in heathered blue. Comfortable cotton jersey, a wardrobe essential.",




"price": 19.99,




"color": "blue",




"category": "shirts",






"description": "Tailored black trousers in comfortable stretch fabric. Perfect for work or dressy events.",




"price": 59.99,




"color": "black",




"category": "pants",






# Create nodes with metadata



product_nodes =[]




for product in products:




text = product.pop("description")




embedding = embed_model.get_text_embedding(text)




node =TextNode(




text=text,




embedding=embedding,




metadata=product,# remaining fields become metadata





product_nodes.append(node)




# Add to vector store



ids = vector_store.add(product_nodes)




print(f"Added (ids)} product nodes with metadata")


```

## Query the Vector Store
[Section titled “Query the Vector Store”](https://developers.llamaindex.ai/python/examples/vector_stores/vertexaivectorsearchv2demo/#query-the-vector-store)
### Simple Similarity Search
[Section titled “Simple Similarity Search”](https://developers.llamaindex.ai/python/examples/vector_stores/vertexaivectorsearchv2demo/#simple-similarity-search)
```

# Create index from vector store



storage_context = StorageContext.from_defaults(vector_store=vector_store)




index = VectorStoreIndex.from_vector_store(




vector_store=vector_store,embed_model=embed_model





# Create retriever



retriever = index.as_retriever(similarity_top_k=3)




# Query



results = retriever.retrieve("comfortable pants for work")





print("Search Results:")




print("-"*60)




for result in results:




print(f"Score: {result.get_score():.3f}")




print(f"Text: {result.get_text()[:100]}...")




print(f"Metadata: {result.metadata}")




print("-"*60)


```

### Search with Metadata Filters
[Section titled “Search with Metadata Filters”](https://developers.llamaindex.ai/python/examples/vector_stores/vertexaivectorsearchv2demo/#search-with-metadata-filters)
```

# Filter by color



filters =MetadataFilters(filters=[MetadataFilter="color",value="blue")])





retriever = index.as_retriever(filters=filters,similarity_top_k=3)




results = retriever.retrieve("casual clothing")





print("Blue items only:")




print("-"*60)




for result in results:




print(




f"Score: {result.get_score():.3f} | Color: {result.metadata.get('color')}"





print(f"Text: {result.get_text()[:80]}...")




print("-"*60)


```

```

# Filter by price range



filters =MetadataFilters(




filters=[




MetadataFilter="price",operator=FilterOperator.LT,value=50.0),







retriever = index.as_retriever(filters=filters,similarity_top_k=3)




results = retriever.retrieve("clothing")





print("Items under $50:")




print("-"*60)




for result in results:




print(




f"Score: {result.get_score():.3f} | Price: ${result.metadata.get('price')}"





print(f"Text: {result.get_text()[:80]}...")




print("-"*60)


```

## RAG Query with LLM
[Section titled “RAG Query with LLM”](https://developers.llamaindex.ai/python/examples/vector_stores/vertexaivectorsearchv2demo/#rag-query-with-llm)
Use the vector store with an LLM for retrieval-augmented generation:
```

# Create query engine



query_engine = index.as_query_engine(similarity_top_k=3)




# Ask a question



response = query_engine.query(




"What blue clothing items do you have and what are their prices?"






print(




"Question: What blue clothing items do you have and what are their prices?"





print("-"*60)




print(f"Answer: {response.response}")




print("-"*60)




print("Sources:")




for node in response.source_nodes:




print(f"  - {node.text[:60]}... (score: {node.score:.3f})")


```

## v2-Only Features
[Section titled “v2-Only Features”](https://developers.llamaindex.ai/python/examples/vector_stores/vertexaivectorsearchv2demo/#v2-only-features)
### Delete Specific Nodes
[Section titled “Delete Specific Nodes”](https://developers.llamaindex.ai/python/examples/vector_stores/vertexaivectorsearchv2demo/#delete-specific-nodes)
```

# Delete specific nodes by ID


# vector_store.delete_nodes(node_ids=["node_id_1", "node_id_2"])



print("delete_nodes() - Delete specific nodes by their IDs")


```

### Clear All Data (v2 only)
[Section titled “Clear All Data (v2 only)”](https://developers.llamaindex.ai/python/examples/vector_stores/vertexaivectorsearchv2demo/#clear-all-data-v2-only)
v2 supports clearing all data from a collection - this is NOT available in v1:
```

# Clear all data from the collection


# WARNING: This deletes ALL data in the collection!


# vector_store.clear()



print("clear() - Clears all data from collection (v2 only!)")


```

## Clean Up
[Section titled “Clean Up”](https://developers.llamaindex.ai/python/examples/vector_stores/vertexaivectorsearchv2demo/#clean-up)
Delete the collection when done to avoid charges:
```


CLEANUP=True# Set to True to delete the collection





ifCLEANUP:




from google.cloud import vectorsearch_v1beta





client = vectorsearch_v1beta.VectorSearchServiceClient()




collection_name = (




f"projects/{PROJECT_ID}/locations/{REGION}/collections/{COLLECTION_ID}"






print(f"Deleting collection: {collection_name}")




client.delete_collection(name=collection_name)




print("Collection deleted.")


```

## Summary
[Section titled “Summary”](https://developers.llamaindex.ai/python/examples/vector_stores/vertexaivectorsearchv2demo/#summary)
This notebook demonstrated:
  1. **Simple Setup** : v2 only requires a collection - no index/endpoint deployment
  2. **Easy Integration** : Just add `api_version="v2"` to use the new API
  3. **Same Interface** : All LlamaIndex operations (add, query, delete) work the same
  4. **New Features** : v2 adds `clear()` method not available in v1


### Migration from v1
[Section titled “Migration from v1”](https://developers.llamaindex.ai/python/examples/vector_stores/vertexaivectorsearchv2demo/#migration-from-v1)
```

# v1 (old)



vector_store =VertexAIVectorStore(




project_id="...",




region="...",




index_id="projects/.../indexes/123",




endpoint_id="projects/.../indexEndpoints/456",




gcs_bucket_name="my-bucket"





# v2 (new)



vector_store =VertexAIVectorStore(




api_version="v2",




project_id="...",




region="...",




collection_id="my-collection"



```

For detailed migration instructions, see [V2_MIGRATION.md](https://github.com/run-llama/llama_index/blob/main/llama-index-integrations/vector_stores/llama-index-vector-stores-vertexaivectorsearch/V2_MIGRATION.md)
