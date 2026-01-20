[Skip to content](https://developers.llamaindex.ai/python/examples/llm/bedrock_converse/#_top)
# Bedrock Converse 
## Basic Usage
[Section titled “Basic Usage”](https://developers.llamaindex.ai/python/examples/llm/bedrock_converse/#basic-usage)
#### Call `complete` with a prompt
[Section titled “Call complete with a prompt”](https://developers.llamaindex.ai/python/examples/llm/bedrock_converse/#call-complete-with-a-prompt)
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
```


%pip install llama-index-llms-bedrock-converse


```

```


!pip install llama-index


```

```


from llama_index.llms.bedrock_converse import BedrockConverse





profile_name ="Your aws profile name"




resp =BedrockConverse(




model="anthropic.claude-3-haiku-20240307-v1:0",




profile_name=profile_name,




).complete("Paul Graham is ")


```

```


print(resp)


```

#### Call `chat` with a list of messages
[Section titled “Call chat with a list of messages”](https://developers.llamaindex.ai/python/examples/llm/bedrock_converse/#call-chat-with-a-list-of-messages)
```


from llama_index.core.llms import ChatMessage




from llama_index.llms.bedrock_converse import BedrockConverse





messages =[




ChatMessage(




role="system",content="You are a pirate with a colorful personality"





ChatMessage(role="user",content="Tell me a story"),






resp =BedrockConverse(




model="anthropic.claude-3-haiku-20240307-v1:0",




profile_name=profile_name,




).chat(messages)


```

```


print(resp)


```

## Streaming
[Section titled “Streaming”](https://developers.llamaindex.ai/python/examples/llm/bedrock_converse/#streaming)
Using `stream_complete` endpoint
```


from llama_index.llms.bedrock_converse import BedrockConverse





llm =BedrockConverse(




model="anthropic.claude-3-haiku-20240307-v1:0",




profile_name=profile_name,





resp = llm.stream_complete("Paul Graham is ")


```

```


forin resp:




print(r.delta,end="")


```

Using `stream_chat` endpoint
```


from llama_index.llms.bedrock_converse import BedrockConverse





llm =BedrockConverse(




model="anthropic.claude-3-haiku-20240307-v1:0",




profile_name=profile_name,





messages =[




ChatMessage(




role="system",content="You are a pirate with a colorful personality"





ChatMessage(role="user",content="Tell me a story"),





resp = llm.stream_chat(messages)


```

```


forin resp:




print(r.delta,end="")


```

## Configure Model
[Section titled “Configure Model”](https://developers.llamaindex.ai/python/examples/llm/bedrock_converse/#configure-model)
```


from llama_index.llms.bedrock_converse import BedrockConverse





llm =BedrockConverse(




model="anthropic.claude-3-haiku-20240307-v1:0",




profile_name=profile_name,



```

```


resp = llm.complete("Paul Graham is ")


```

```


print(resp)


```

## Connect to Bedrock with Access Keys
[Section titled “Connect to Bedrock with Access Keys”](https://developers.llamaindex.ai/python/examples/llm/bedrock_converse/#connect-to-bedrock-with-access-keys)
```


from llama_index.llms.bedrock_converse import BedrockConverse





llm =BedrockConverse(




model="us.amazon.nova-lite-v1:0",




aws_access_key_id="AWS Access Key ID to use",




aws_secret_access_key="AWS Secret Access Key to use",




aws_session_token="AWS Session Token to use",




region_name="AWS Region to use, eg. us-east-1",






resp = llm.complete("Paul Graham is ")


```

```


print(resp)


```

## Function Calling
[Section titled “Function Calling”](https://developers.llamaindex.ai/python/examples/llm/bedrock_converse/#function-calling)
Claude, Command and Mistral Large models supports native function calling through AWS Bedrock Converse. There’s a seamless integration with LlamaIndex tools, through the `predict_and_call` function on the `llm`.
This allows the user to attach any tools and let the LLM decide which tools to call (if any).
If you wish to perform tool calling as part of an agentic loop, check out our [agent guides](https://docs.llamaindex.ai/en/latest/module_guides/deploying/agents/) instead.
**NOTE** : Not all models from AWS Bedrock support function calling and the Converse API. [Check the available features of each LLM here](https://docs.aws.amazon.com/bedrock/latest/userguide/models-features.html).
```


from llama_index.llms.bedrock_converse import BedrockConverse




from llama_index.core.tools import FunctionTool






defmultiply(a: int, b: int) -> int:




"""Multiple two integers and returns the result integer"""




return* b






defmystery(a: int, b: int) -> int:




"""Mystery function on two integers."""




return*++ b






mystery_tool = FunctionTool.from_defaults=mystery)




multiply_tool = FunctionTool.from_defaults=multiply)





llm =BedrockConverse(




model="anthropic.claude-3-haiku-20240307-v1:0",




profile_name=profile_name,



```

```


response = llm.predict_and_call(




[mystery_tool, multiply_tool],




user_msg="What happens if I run the mystery function on 5 and 7",



```

```


print(str(response))


```

```


response = llm.predict_and_call(




[mystery_tool, multiply_tool],




user_msg=(




"""What happens if I run the mystery function on the following pairs of numbers? Generate a separate result for each row:



- 1 and 2


- 8 and 4


- 100 and 20




NOTE: you need to run the mystery function for all of the pairs above at the same time \



"""




allow_parallel_tool_calls=True,



```

```


print(str(response))


```

```


forin response.sources:




print(f"Name: {s.tool_name}, Input: {s.raw_input}, Output: (s)}")


```

## Async
[Section titled “Async”](https://developers.llamaindex.ai/python/examples/llm/bedrock_converse/#async)
```


from llama_index.llms.bedrock_converse import BedrockConverse





llm =BedrockConverse(




model="anthropic.claude-3-haiku-20240307-v1:0",




aws_access_key_id="AWS Access Key ID to use",




aws_secret_access_key="AWS Secret Access Key to use",




aws_session_token="AWS Session Token to use",




region_name="AWS Region to use, eg. us-east-1",





resp =await llm.acomplete("Paul Graham is ")


```

```


print(resp)


```

