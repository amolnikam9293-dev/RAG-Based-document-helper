[Skip to content](https://developers.llamaindex.ai/python/examples/embeddings/gemini/#_top)
# Google Gemini Embeddings 
**NOTE:** This example is deprecated. Please use the `GoogleGenAIEmbedding` class instead, detailed [here](https://github.com/run-llama/llama_index/blob/main/docs/examples/embeddings/google_genai.ipynb).
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
```


%pip install llama-index-embeddings-gemini


```

```


!pip install llama-index 'google-generativeai>=0.3.0' matplotlib


```

```


import os





GOOGLE_API_KEY=""# add your GOOGLE API key here




os.environ["GOOGLE_API_KEY"] =GOOGLE_API_KEY


```

```

# imports



from llama_index.embeddings.gemini import GeminiEmbedding


```

```

# get API key and create embeddings




model_name ="models/embedding-001"





embed_model =GeminiEmbedding(




model_name=model_name,api_key=GOOGLE_API_KEY,title="this is a document"






embeddings = embed_model.get_text_embedding("Google Gemini Embeddings.")


```

```

/Users/haotianzhang/llama_index/venv/lib/python3.11/site-packages/tqdm/auto.py:21: TqdmWarning: IProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/stable/user_install.html



from .autonotebook import tqdm as notebook_tqdm


```

```


print(f"Dimension of embeddings: (embeddings)}")


```

```

Dimension of embeddings: 768

```

```


embeddings[:5]


```

```

[0.028174246, -0.0290093, -0.013280814, 0.008629, 0.025442218]

```

```


embeddings = embed_model.get_query_embedding("Google Gemini Embeddings.")




embeddings[:5]


```

```

[0.028174246, -0.0290093, -0.013280814, 0.008629, 0.025442218]

```

```


embeddings = embed_model.get_text_embedding(




["Google Gemini Embeddings.", "Google is awesome."]



```

```


print(f"Dimension of embeddings: (embeddings)}")




print(embeddings[0][:5])




print(embeddings[1][:5])


```

```

Dimension of embeddings: 2


[0.028174246, -0.0290093, -0.013280814, 0.008629, 0.025442218]


[0.009427786, -0.009968997, -0.03341217, -0.025396815, 0.03210592]

```

```


embedding =await embed_model.aget_text_embedding("Google Gemini Embeddings.")




print(embedding[:5])


```

```

[0.028174246, -0.0290093, -0.013280814, 0.008629, 0.025442218]

```

```


embeddings =await embed_model.aget_text_embedding_batch(





"Google Gemini Embeddings.",




"Google is awesome.",




"Llamaindex is awesome.",






print(embeddings[0][:5])




print(embeddings[1][:5])




print(embeddings[2][:5])


```

```

[0.028174246, -0.0290093, -0.013280814, 0.008629, 0.025442218]


[0.009427786, -0.009968997, -0.03341217, -0.025396815, 0.03210592]


[0.013159992, -0.021570021, -0.060150445, -0.042500723, 0.041159637]

```

```


embedding =await embed_model.aget_query_embedding("Google Gemini Embeddings.")




print(embedding[:5])


```

```

[0.028174246, -0.0290093, -0.013280814, 0.008629, 0.025442218]

```

