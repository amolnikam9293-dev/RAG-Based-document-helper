[Skip to content](https://developers.llamaindex.ai/python/examples/vector_stores/existing_data/weaviate_existing_data/#_top)
# Guide: Using Vector Store Index with Existing Weaviate Vector Store 
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
```


%pip install llama-index-vector-stores-weaviate




%pip install llama-index-embeddings-openai


```

```


!pip install llama-index


```

```


import weaviate


```

```


client = weaviate.Client("https://test-cluster-bbn8vqsn.weaviate.network")


```

## Prepare Sample “Existing” Weaviate Vector Store
[Section titled “Prepare Sample “Existing” Weaviate Vector Store”](https://developers.llamaindex.ai/python/examples/vector_stores/existing_data/weaviate_existing_data/#prepare-sample-existing-weaviate-vector-store)
### Define schema
[Section titled “Define schema”](https://developers.llamaindex.ai/python/examples/vector_stores/existing_data/weaviate_existing_data/#define-schema)
We create a schema for “Book” class, with 4 properties: title (str), author (str), content (str), and year (int)
```


try:




client.schema.delete_class("Book")




except:




pass


```

```


schema = {




"classes": [





"class": "Book",




"properties": [




{"name": "title", "dataType": ["text"]},




{"name": "author", "dataType": ["text"]},




{"name": "content", "dataType": ["text"]},




{"name": "year", "dataType": ["int"]},









ifnot client.schema.contains(schema):




client.schema.create(schema)


```

### Define sample data
[Section titled “Define sample data”](https://developers.llamaindex.ai/python/examples/vector_stores/existing_data/weaviate_existing_data/#define-sample-data)
We create 4 sample books
```


books =[





"title": "To Kill a Mockingbird",




"author": "Harper Lee",




"content": (




"To Kill a Mockingbird is a novel by Harper Lee published in"




" 1960..."





"year": 1960,






"title": "1984",




"author": "George Orwell",




"content": (




"1984 is a dystopian novel by George Orwell published in 1949..."





"year": 1949,






"title": "The Great Gatsby",




"author": "F. Scott Fitzgerald",




"content": (




"The Great Gatsby is a novel by F. Scott Fitzgerald published in"




" 1925..."





"year": 1925,






"title": "Pride and Prejudice",




"author": "Jane Austen",




"content": (




"Pride and Prejudice is a novel by Jane Austen published in"




" 1813..."





"year": 1813,




```

### Add data
[Section titled “Add data”](https://developers.llamaindex.ai/python/examples/vector_stores/existing_data/weaviate_existing_data/#add-data)
We add the sample books to our Weaviate “Book” class (with embedding of content field
```


from llama_index.embeddings.openai import OpenAIEmbedding





embed_model =OpenAIEmbedding()


```

```


with client.batch as batch:




for book in books:




vector = embed_model.get_text_embedding(book["content"])




batch.add_data_object(




data_object=book,class_name="Book",vector=vector



```

## Query Against “Existing” Weaviate Vector Store
[Section titled “Query Against “Existing” Weaviate Vector Store”](https://developers.llamaindex.ai/python/examples/vector_stores/existing_data/weaviate_existing_data/#query-against-existing-weaviate-vector-store)
```


from llama_index.vector_stores.weaviate import WeaviateVectorStore




from llama_index.core import VectorStoreIndex




from llama_index.core.response.pprint_utils import pprint_source_node


```

You must properly specify a “index_name” that matches the desired Weaviate class and select a class property as the “text” field.
```


vector_store =WeaviateVectorStore(




weaviate_client=client,index_name="Book",text_key="content"



```

```


retriever = VectorStoreIndex.from_vector_store(vector_store).as_retriever(




similarity_top_k=1



```

```


nodes = retriever.retrieve("What is that book about a bird again?")


```

Let’s inspect the retrieved node. We can see that the book data is loaded as LlamaIndex `Node` objects, with the “content” field as the main text.
```


pprint_source_node(nodes[0])


```

```

Document ID: cf927ce7-0672-4696-8aae-7e77b33b9659


Similarity: None


Text: author: Harper Lee title: To Kill a Mockingbird year: 1960  To


Kill a Mockingbird is a novel by Harper Lee published in 1960......

```

The remaining fields should be loaded as metadata (in `metadata`)
```


nodes[0].node.metadata


```

```

{'author': 'Harper Lee', 'title': 'To Kill a Mockingbird', 'year': 1960}

```

