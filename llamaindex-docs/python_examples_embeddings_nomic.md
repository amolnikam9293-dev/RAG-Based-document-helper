[Skip to content](https://developers.llamaindex.ai/python/examples/embeddings/nomic/#_top)
# Nomic Embedding 
Nomic has released v1.5 🪆🪆🪆 is capable of variable sized embeddings with matryoshka learning and an 8192 context, embedding dimensions between 64 and 768.
In this notebook, we will explore using Nomic v1.5 embedding at different dimensions.
### Installation
[Section titled “Installation”](https://developers.llamaindex.ai/python/examples/embeddings/nomic/#installation)
```


%pip install -U llama-index llama-index-embeddings-nomic


```

### Setup API Keys
[Section titled “Setup API Keys”](https://developers.llamaindex.ai/python/examples/embeddings/nomic/#setup-api-keys)
```


nomic_api_key ="<NOMIC API KEY>"


```

```


import nest_asyncio





nest_asyncio.apply()





from llama_index.embeddings.nomic import NomicEmbedding


```

#### With dimension at 128
[Section titled “With dimension at 128”](https://developers.llamaindex.ai/python/examples/embeddings/nomic/#with-dimension-at-128)
```


embed_model =NomicEmbedding(




api_key=nomic_api_key,




dimensionality=128,




model_name="nomic-embed-text-v1.5",






embedding = embed_model.get_text_embedding("Nomic Embeddings")


```

```


print(len(embedding))


```

```


embedding[:5]


```

```

[0.05569458, 0.057922363, -0.30126953, -0.09832764, 0.05947876]

```

#### With dimension at 256
[Section titled “With dimension at 256”](https://developers.llamaindex.ai/python/examples/embeddings/nomic/#with-dimension-at-256)
```


embed_model =NomicEmbedding(




api_key=nomic_api_key,




dimensionality=256,




model_name="nomic-embed-text-v1.5",






embedding = embed_model.get_text_embedding("Nomic Embeddings")


```

```


print(len(embedding))


```

```


embedding[:5]


```

```

[0.044708252, 0.04650879, -0.24182129, -0.07897949, 0.04776001]

```

#### With dimension at 768
[Section titled “With dimension at 768”](https://developers.llamaindex.ai/python/examples/embeddings/nomic/#with-dimension-at-768)
```


embed_model =NomicEmbedding(




api_key=nomic_api_key,




dimensionality=768,




model_name="nomic-embed-text-v1.5",






embedding = embed_model.get_text_embedding("Nomic Embeddings")


```

```


print(len(embedding))


```

```


embedding[:5]


```

```

[0.027282715, 0.028381348, -0.14758301, -0.048187256, 0.029144287]

```

#### You can still use v1 Nomic Embeddings
[Section titled “You can still use v1 Nomic Embeddings”](https://developers.llamaindex.ai/python/examples/embeddings/nomic/#you-can-still-use-v1-nomic-embeddings)
It has 768 fixed embedding dimensions
```


embed_model =NomicEmbedding(




api_key=nomic_api_key,model_name="nomic-embed-text-v1"






embedding = embed_model.get_text_embedding("Nomic Embeddings")


```

```


print(len(embedding))


```

```


embedding[:5]


```

```

[0.0059013367, 0.03744507, 0.0035305023, -0.047180176, 0.0154418945]

```

### Let’s Build end to end RAG pipeline with Nomic v1.5 Embedding.
[Section titled “Let’s Build end to end RAG pipeline with Nomic v1.5 Embedding.”](https://developers.llamaindex.ai/python/examples/embeddings/nomic/#lets-build-end-to-end-rag-pipeline-with-nomic-v15-embedding)
We will use OpenAI for Generation step.
#### Set Embedding model and llm.
[Section titled “Set Embedding model and llm.”](https://developers.llamaindex.ai/python/examples/embeddings/nomic/#set-embedding-model-and-llm)
```


from llama_index.core import settings




from llama_index.core import VectorStoreIndex, SimpleDirectoryReader




from llama_index.llms.openai import OpenAI





import os





os.environ["OPENAI_API_KEY"] ="<YOUR OPENAI API KEY>"





embed_model =NomicEmbedding(




api_key=nomic_api_key,




dimensionality=128,




model_name="nomic-embed-text-v1.5",






llm =OpenAI(model="gpt-3.5-turbo")





settings.llm = llm




settings.embed_model = embed_model


```

#### Download Data
[Section titled “Download Data”](https://developers.llamaindex.ai/python/examples/embeddings/nomic/#download-data)
```


!mkdir -p 'data/paul_graham/'




!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt'-O 'data/paul_graham/paul_graham_essay.txt'


```

```

--2024-02-16 18:37:03--  https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt


Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 2606:50c0:8001::154, 2606:50c0:8003::154, 2606:50c0:8000::154, ...


Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|2606:50c0:8001::154|:443... connected.


HTTP request sent, awaiting response... 200 OK


Length: 75042 (73K) [text/plain]


Saving to: 'data/paul_graham/paul_graham_essay.txt'



data/paul_graham/pa 100%[===================>]  73.28K  --.-KB/s    in 0.02s



2024-02-16 18:37:03 (3.87 MB/s) - 'data/paul_graham/paul_graham_essay.txt' saved [75042/75042]

```

#### Load data
[Section titled “Load data”](https://developers.llamaindex.ai/python/examples/embeddings/nomic/#load-data)
```


documents =SimpleDirectoryReader("./data/paul_graham").load_data()


```

#### Index creation
[Section titled “Index creation”](https://developers.llamaindex.ai/python/examples/embeddings/nomic/#index-creation)
```


index = VectorStoreIndex.from_documents(documents)


```

#### Query Engine
[Section titled “Query Engine”](https://developers.llamaindex.ai/python/examples/embeddings/nomic/#query-engine)
```


query_engine = index.as_query_engine()


```

```


response = query_engine.query("what did author do growing up?")




print(response)


```

```

The author, growing up, worked on writing and programming. They wrote short stories and also tried writing programs on an IBM 1401 computer. Later, they got a microcomputer and started programming more extensively, writing simple games and a word processor.

```

