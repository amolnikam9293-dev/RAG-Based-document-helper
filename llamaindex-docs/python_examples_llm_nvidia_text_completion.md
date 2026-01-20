[Skip to content](https://developers.llamaindex.ai/python/examples/llm/nvidia_text_completion/#_top)
# NVIDIA's LLM Text Completion API 
Extending the NVIDIA class to support /completion API’s for below models:
  * bigcode/starcoder2-7b
  * bigcode/starcoder2-15b


## Installation
[Section titled “Installation”](https://developers.llamaindex.ai/python/examples/llm/nvidia_text_completion/#installation)
```


!pip install --force-reinstall llama_index-llms-nvidia


```

## Setup
[Section titled “Setup”](https://developers.llamaindex.ai/python/examples/llm/nvidia_text_completion/#setup)
**To get started:**
  1. Create a free account with [NVIDIA](https://build.nvidia.com/), which hosts NVIDIA AI Foundation models.
  2. Click on your model of choice.
  3. Under Input select the Python tab, and click `Get API Key`. Then click `Generate Key`.
  4. Copy and save the generated key as NVIDIA_API_KEY. From there, you should have access to the endpoints.


```


!which python


```

```


import getpass




import os




# del os.environ['NVIDIA_API_KEY']  ## delete key and reset



if os.environ.get("NVIDIA_API_KEY","").startswith("nvapi-"):




print("Valid NVIDIA_API_KEY already in environment. Delete to reset")




else:




nvapi_key = getpass.getpass("NVAPI Key (starts with nvapi-): ")




assert nvapi_key.startswith(




"nvapi-"




), f"{nvapi_key[:5]}... is not a valid key"




os.environ["NVIDIA_API_KEY"] = nvapi_key


```

```


os.environ["NVIDIA_API_KEY"]


```

```

# llama-parse is async-first, running the async code in a notebook requires the use of nest_asyncio



import nest_asyncio





nest_asyncio.apply()


```

## Working with NVIDIA API Catalog
[Section titled “Working with NVIDIA API Catalog”](https://developers.llamaindex.ai/python/examples/llm/nvidia_text_completion/#working-with-nvidia-api-catalog)
#### Usage of `use_chat_completions` argument:
[Section titled “Usage of use_chat_completions argument:”](https://developers.llamaindex.ai/python/examples/llm/nvidia_text_completion/#usage-of-use_chat_completions-argument)
Set None (default) to per-invocation decide on using /chat/completions vs /completions endpoints with query keyword arguments
  * set False to universally use /completions endpoint
  * set True to universally use /chat/completions endpoint


```


from llama_index.llms.nvidia importNVIDIA





llm =NVIDIA(model="bigcode/starcoder2-15b",use_chat_completions=False)


```

### Available Models
[Section titled “Available Models”](https://developers.llamaindex.ai/python/examples/llm/nvidia_text_completion/#available-models)
`is_chat_model` can be used to get available text completion models
```


print([model for model in llm.available_models if model.is_chat_model])


```

## Working with NVIDIA NIMs
[Section titled “Working with NVIDIA NIMs”](https://developers.llamaindex.ai/python/examples/llm/nvidia_text_completion/#working-with-nvidia-nims)
In addition to connecting to hosted [NVIDIA NIMs](https://ai.nvidia.com), this connector can be used to connect to local microservice instances. This helps you take your applications local when necessary.
For instructions on how to setup local microservice instances, see <https://developer.nvidia.com/blog/nvidia-nim-offers-optimized-inference-microservices-for-deploying-ai-models-at-scale/>
```


from llama_index.llms.nvidia importNVIDIA




# connect to an chat NIM running at localhost:8080, spcecifying a specific model



llm =NVIDIA(base_url="http://localhost:8080/v1")


```

### Complete: `.complete()`
[Section titled “Complete: .complete()”](https://developers.llamaindex.ai/python/examples/llm/nvidia_text_completion/#complete-complete)
We can use `.complete()`/`.acomplete()` (which takes a string) to prompt a response from the selected model.
Let’s use our default model for this task.
```


print(llm.complete("# Function that does quicksort:"))


```

As is expected by LlamaIndex - we get a `CompletionResponse` in response.
#### Async Complete: `.acomplete()`
[Section titled “Async Complete: .acomplete()”](https://developers.llamaindex.ai/python/examples/llm/nvidia_text_completion/#async-complete-acomplete)
There is also an async implementation which can be leveraged in the same way!
```


await llm.acomplete("# Function that does quicksort:")


```

#### Streaming
[Section titled “Streaming”](https://developers.llamaindex.ai/python/examples/llm/nvidia_text_completion/#streaming)
```


x = llm.stream_complete(prompt="# Reverse string in python:",max_tokens=512)


```

```


forin x:




print(t.delta,end="")


```

#### Async Streaming
[Section titled “Async Streaming”](https://developers.llamaindex.ai/python/examples/llm/nvidia_text_completion/#async-streaming)
```


x =await llm.astream_complete(




prompt="# Reverse program in python:",max_tokens=512



```

```


asyncforin x:




print(t.delta,end="")


```

