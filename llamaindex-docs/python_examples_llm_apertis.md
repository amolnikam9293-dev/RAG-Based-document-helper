[Skip to content](https://developers.llamaindex.ai/python/examples/llm/apertis/#_top)
# Apertis 
Apertis provides a unified API gateway to access multiple LLM providers including OpenAI, Anthropic, Google, and more through an OpenAI-compatible interface. You can find out more on their [documentation](https://docs.stima.tech).
**Supported Endpoints:**
  * `/v1/chat/completions` - OpenAI Chat Completions format (default)
  * `/v1/responses` - OpenAI Responses format compatible
  * `/v1/messages` - Anthropic format compatible


If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
```


%pip install llama-index-llms-apertis


```

```


!pip install llama-index


```

```


from llama_index.llms.apertis import Apertis




from llama_index.core.llms import ChatMessage


```

## Call `chat` with ChatMessage List
[Section titled “Call chat with ChatMessage List”](https://developers.llamaindex.ai/python/examples/llm/apertis/#call-chat-with-chatmessage-list)
You need to either set env var `APERTIS_API_KEY` or set api_key in the class constructor
```

# import os


# os.environ['APERTIS_API_KEY'] = '<your-api-key>'




llm =Apertis(




api_key="<your-api-key>",




max_tokens=256,




context_window=4096,




model="gpt-5.2",



```

```


message =ChatMessage(role="user",content="Tell me a joke")




resp = llm.chat([message])




print(resp)


```

### Streaming
[Section titled “Streaming”](https://developers.llamaindex.ai/python/examples/llm/apertis/#streaming)
```


message =ChatMessage(role="user",content="Tell me a story in 250 words")




resp = llm.stream_chat([message])




forin resp:




print(r.delta,end="")


```

## Call `complete` with Prompt
[Section titled “Call complete with Prompt”](https://developers.llamaindex.ai/python/examples/llm/apertis/#call-complete-with-prompt)
```


resp = llm.complete("Tell me a joke")




print(resp)


```

```


resp = llm.stream_complete("Tell me a story in 250 words")




forin resp:




print(r.delta,end="")


```

## Model Configuration
[Section titled “Model Configuration”](https://developers.llamaindex.ai/python/examples/llm/apertis/#model-configuration)
Apertis supports models from multiple providers:
Provider | Example Models  
---|---  
OpenAI |  `gpt-5.2`, `gpt-5-mini-2025-08-07`  
Anthropic | `claude-sonnet-4.5`  
Google | `gemini-3-flash-preview`  
```

# Using Claude



llm =Apertis(model="claude-sonnet-4.5")


```

```


resp = llm.complete("Write a story about a dragon who can code in Rust")




print(resp)


```

```

# Using Gemini



llm =Apertis(model="gemini-3-flash-preview")


```

```


resp = llm.complete("Explain quantum computing in simple terms")




print(resp)


```

