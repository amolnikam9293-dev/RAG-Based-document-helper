[Skip to content](https://developers.llamaindex.ai/python/examples/llm/vercel-ai-gateway/#_top)
# Vercel AI Gateway 
The AI Gateway is a proxy service from Vercel that routes model requests to various AI providers. It offers a unified API to multiple providers and gives you the ability to set budgets, monitor usage, load-balance requests, and manage fallbacks. You can find out more from their [docs](https://vercel.com/docs/ai-gateway)
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
```


%pip install llama-index-llms-vercel-ai-gateway


```

```


!pip install llama-index


```

```


from llama_index.llms.vercel_ai_gateway import VercelAIGateway




from llama_index.core.llms import ChatMessage





llm =VercelAIGateway(




model="anthropic/claude-4-sonnet",




max_tokens=64000,




context_window=200000,




api_key="your-api-key",




default_headers={




"http-referer": "https://myapp.com/"# Optional: Your app URL




"x-title": "My App"# Optional: Your app name







print(llm.model)


```

## Call `chat` with ChatMessage List
[Section titled “Call chat with ChatMessage List”](https://developers.llamaindex.ai/python/examples/llm/vercel-ai-gateway/#call-chat-with-chatmessage-list)
You need to either set env var `VERCEL_AI_GATEWAY_API_KEY` or `VERCEL_OIDC_TOKEN` or set api_key in the class constructor
```

# import os


# os.environ['VERCEL_AI_GATEWAY_API_KEY'] = '<your-api-key>'




llm =VercelAIGateway(




api_key="pBiuCWfswZCDxt8D50DSoBfU",




max_tokens=64000,




context_window=200000,




model="anthropic/claude-4-sonnet",



```

```


message =ChatMessage(role="user",content="Tell me a joke")




resp = llm.chat([message])




print(resp)


```

### Streaming
[Section titled “Streaming”](https://developers.llamaindex.ai/python/examples/llm/vercel-ai-gateway/#streaming)
```


message =ChatMessage(role="user",content="Tell me a story in 250 words")




resp = llm.stream_chat([message])




forin resp:




print(r.delta,end="")


```

## Call `complete` with Prompt
[Section titled “Call complete with Prompt”](https://developers.llamaindex.ai/python/examples/llm/vercel-ai-gateway/#call-complete-with-prompt)
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
[Section titled “Model Configuration”](https://developers.llamaindex.ai/python/examples/llm/vercel-ai-gateway/#model-configuration)
```

# This example uses Anthropic's Claude 4 Sonnet (models are specified as `provider/model`):



llm =VercelAIGateway(




model="anthropic/claude-4-sonnet",




api_key="pBiuCWfswZCDxt8D50DSoBfU",



```

```


resp = llm.complete("Write a story about a dragon who can code in Rust")




print(resp)


```

