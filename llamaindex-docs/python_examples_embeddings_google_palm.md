[Skip to content](https://developers.llamaindex.ai/python/examples/embeddings/google_palm/#_top)
# Google PaLM Embeddings 
**NOTE:** This example is deprecated. Please use the `GoogleGenAIEmbedding` class instead, detailed [here](https://github.com/run-llama/llama_index/blob/main/docs/examples/embeddings/google_genai.ipynb).
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
```


%pip install llama-index-embeddings-google


```

```


!pip install llama-index


```

```

# imports



from llama_index.embeddings.google import GooglePaLMEmbedding


```

```

# get API key and create embeddings




model_name ="models/embedding-gecko-001"




api_key ="YOUR API KEY"





embed_model =GooglePaLMEmbedding(model_name=model_name,api_key=api_key)





embeddings = embed_model.get_text_embedding("Google PaLM Embeddings.")


```

```

/opt/homebrew/lib/python3.11/site-packages/tqdm/auto.py:21: TqdmWarning: IProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/stable/user_install.html



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

[0.028517298, -0.0028859433, -0.035110522, 0.021982985, -0.0039763353]

```

