[Skip to content](https://developers.llamaindex.ai/python/examples/vector_stores/dashvectorindexdemo/#_top)
# DashVector Vector Store 
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
```


%pip install llama-index-vector-stores-dashvector


```

```


!pip install llama-index


```

```


import logging




import sys




import os





logging.basicConfig(stream=sys.stdout,level=logging.INFO)




logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


```

#### Creating a DashVector Collection
[Section titled “Creating a DashVector Collection”](https://developers.llamaindex.ai/python/examples/vector_stores/dashvectorindexdemo/#creating-a-dashvector-collection)
```


import dashvector


```

```


api_key = os.environ["DASHVECTOR_API_KEY"]




client = dashvector.Client(api_key=api_key)


```

```

# dimensions are for text-embedding-ada-002



client.create("llama-demo",dimension=1536)


```

```

{"code": 0, "message": "", "requests_id": "82b969d2-2568-4e18-b0dc-aa159b503c84"}

```

```


dashvector_collection = client.get("quickstart")


```

#### Download Data
[Section titled “Download Data”](https://developers.llamaindex.ai/python/examples/vector_stores/dashvectorindexdemo/#download-data)
```


!mkdir -p 'data/paul_graham/'




!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt'-O 'data/paul_graham/paul_graham_essay.txt'


```

#### Load documents, build the DashVectorStore and VectorStoreIndex
[Section titled “Load documents, build the DashVectorStore and VectorStoreIndex”](https://developers.llamaindex.ai/python/examples/vector_stores/dashvectorindexdemo/#load-documents-build-the-dashvectorstore-and-vectorstoreindex)
```


from llama_index.core import VectorStoreIndex, SimpleDirectoryReader




from llama_index.vector_stores.dashvector import DashVectorStore




from IPython.display import Markdown, display


```

```

INFO:numexpr.utils:Note: NumExpr detected 12 cores but "NUMEXPR_MAX_THREADS" not set, so enforcing safe limit of 8.


Note: NumExpr detected 12 cores but "NUMEXPR_MAX_THREADS" not set, so enforcing safe limit of 8.


INFO:numexpr.utils:NumExpr defaulting to 8 threads.


NumExpr defaulting to 8 threads.

```

```

# load documents



documents =SimpleDirectoryReader("./data/paul_graham").load_data()


```

```

# initialize without metadata filter



from llama_index.core import StorageContext





vector_store =DashVectorStore(dashvector_collection)




storage_context = StorageContext.from_defaults(vector_store=vector_store)




index = VectorStoreIndex.from_documents(




documents,storage_context=storage_context



```

#### Query Index
[Section titled “Query Index”](https://developers.llamaindex.ai/python/examples/vector_stores/dashvectorindexdemo/#query-index)
```

# set Logging to DEBUG for more detailed outputs



query_engine = index.as_query_engine()




response = query_engine.query("What did the author do growing up?")


```

```


display(Markdown(f"<b>{response}</b>"))


```

**The author worked on writing and programming outside of school. They wrote short stories and tried writing programs on the IBM 1401 computer. They also built a microcomputer and started programming on it, writing simple games and a word processor.**
