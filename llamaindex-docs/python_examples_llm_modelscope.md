[Skip to content](https://developers.llamaindex.ai/python/examples/llm/modelscope/#_top)
# ModelScope LLMS 
In this notebook, we show how to use the ModelScope LLM models in LlamaIndex. Check out the [ModelScope site](https://www.modelscope.cn/).
If you’re opening this Notebook on colab, you will need to install LlamaIndex 🦙 and the modelscope.
```


!pip install llama-index-llms-modelscope


```

## Basic Usage
[Section titled “Basic Usage”](https://developers.llamaindex.ai/python/examples/llm/modelscope/#basic-usage)
```


import sys




from llama_index.llms.modelscope import ModelScopeLLM





llm =ModelScopeLLM(model_name="qwen/Qwen3-8B",model_revision="master")





rsp = llm.complete("Hello, who are you?")




print(rsp)


```

#### Use Message request
[Section titled “Use Message request”](https://developers.llamaindex.ai/python/examples/llm/modelscope/#use-message-request)
```


from llama_index.core.base.llms.types import MessageRole, ChatMessage





messages =[




ChatMessage(




role=MessageRole.SYSTEM,content="You are a helpful assistant."





ChatMessage(role=MessageRole.USER,content="How to make cake?"),





resp = llm.chat(messages)




print(resp)


```

