[Skip to content](https://developers.llamaindex.ai/python/examples/observability/langfusecallbackhandler/#_top)
# Langfuse Callback Handler 
⚠️ This integration is deprecated. We recommend using the new instrumentation-based integration with Langfuse as described [here](https://langfuse.com/docs/integrations/llama-index/get-started).
This cookbook shows you how to use the Langfuse callback handler to monitor LlamaIndex applications.
## What is Langfuse?
[Section titled “What is Langfuse?”](https://developers.llamaindex.ai/python/examples/observability/langfusecallbackhandler/#what-is-langfuse)
[Langfuse](https://langfuse.com/docs) is an open source LLM engineering platform to help teams collaboratively debug, analyze and iterate on their LLM Applications. Langfuse offers a simple integration for automatic capture of [traces](https://langfuse.com/docs/tracing) and metrics generated in LlamaIndex applications.
## How does it work?
[Section titled “How does it work?”](https://developers.llamaindex.ai/python/examples/observability/langfusecallbackhandler/#how-does-it-work)
The `LangfuseCallbackHandler` is integrated with Langfuse and empowers you to seamlessly track and monitor performance, traces, and metrics of your LlamaIndex application. Detailed traces of the LlamaIndex context augmentation and the LLM querying processes are captured and can be inspected directly in the Langfuse UI.
## Setup
[Section titled “Setup”](https://developers.llamaindex.ai/python/examples/observability/langfusecallbackhandler/#setup)
### Install packages
[Section titled “Install packages”](https://developers.llamaindex.ai/python/examples/observability/langfusecallbackhandler/#install-packages)
```


%pip install llama-index llama-index-callbacks-langfuse


```

### Configure environment
[Section titled “Configure environment”](https://developers.llamaindex.ai/python/examples/observability/langfusecallbackhandler/#configure-environment)
If you haven’t done yet, [sign up on Langfuse](https://cloud.langfuse.com/auth/sign-up) and obtain your API keys from the project settings.
```


import os




# Get keys for your project from the project settings page https://cloud.langfuse.com



os.environ["LANGFUSE_SECRET_KEY"] ="sk-lf-..."




os.environ["LANGFUSE_PUBLIC_KEY"] ="pk-lf-..."




os.environ["LANGFUSE_HOST"] ="https://cloud.langfuse.com"# 🇪🇺 EU region



# os.environ["LANGFUSE_HOST"] = "https://us.cloud.langfuse.com" # 🇺🇸 US region



# OpenAI



os.environ["OPENAI_API_KEY"] ="sk-..."


```

### Register the Langfuse callback handler
[Section titled “Register the Langfuse callback handler”](https://developers.llamaindex.ai/python/examples/observability/langfusecallbackhandler/#register-the-langfuse-callback-handler)
#### Option 1: Set global LlamaIndex handler
[Section titled “Option 1: Set global LlamaIndex handler”](https://developers.llamaindex.ai/python/examples/observability/langfusecallbackhandler/#option-1-set-global-llamaindex-handler)
```


from llama_index.core import global_handler, set_global_handler





set_global_handler("langfuse")




langfuse_callback_handler = global_handler


```

#### Option 2: Use Langfuse callback directly
[Section titled “Option 2: Use Langfuse callback directly”](https://developers.llamaindex.ai/python/examples/observability/langfusecallbackhandler/#option-2-use-langfuse-callback-directly)
```


from llama_index.core import Settings




from llama_index.core.callbacks import CallbackManager




from langfuse.llama_index import LlamaIndexCallbackHandler





langfuse_callback_handler =LlamaIndexCallbackHandler()




Settings.callback_manager =CallbackManager([langfuse_callback_handler])


```

### Flush events to Langfuse
[Section titled “Flush events to Langfuse”](https://developers.llamaindex.ai/python/examples/observability/langfusecallbackhandler/#flush-events-to-langfuse)
The Langfuse SDKs queue and batches events in the background to reduce the number of network requests and improve overall performance. Before exiting your application, make sure all queued events have been flushed to Langfuse servers.
```

# ... your LlamaIndex calls here ...




langfuse_callback_handler.flush()


```

Done!✨ Traces and metrics from your LlamaIndex application are now automatically tracked in Langfuse. If you construct a new index or query an LLM with your documents in context, your traces and metrics are immediately visible in the Langfuse UI. Next, let’s take a look at how traces will look in Langfuse.
## Example
[Section titled “Example”](https://developers.llamaindex.ai/python/examples/observability/langfusecallbackhandler/#example)
Fetch and save example data.
```


!mkdir -p 'data/'




!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt'-O 'data/paul_graham_essay.txt'


```

Run an example index construction, query, and chat.
```


from llama_index.core import SimpleDirectoryReader, VectorStoreIndex




# Create index



documents =SimpleDirectoryReader("data").load_data()




index = VectorStoreIndex.from_documents(documents)




# Execute query



query_engine = index.as_query_engine()




query_response = query_engine.query("What did the author do growing up?")




print(query_response)




# Execute chat query



chat_engine = index.as_chat_engine()




chat_response = chat_engine.chat("What did the author do growing up?")




print(chat_response)




# As we want to immediately see result in Langfuse, we need to flush the callback handler



langfuse_callback_handler.flush()


```

Done!✨ You will now see traces of your index and query in your Langfuse project.
Example traces (public links):


## 📚 More details
[Section titled “📚 More details”](https://developers.llamaindex.ai/python/examples/observability/langfusecallbackhandler/#-more-details)
Check out the full [Langfuse documentation](https://langfuse.com/docs) for more details on Langfuse’s tracing and analytics capabilities and how to make most of this integration.
## Feedback
[Section titled “Feedback”](https://developers.llamaindex.ai/python/examples/observability/langfusecallbackhandler/#feedback)
If you have any feedback or requests, please create a GitHub [Issue](https://github.com/orgs/langfuse/discussions) or share your idea with the community on [Discord](https://discord.langfuse.com/).
