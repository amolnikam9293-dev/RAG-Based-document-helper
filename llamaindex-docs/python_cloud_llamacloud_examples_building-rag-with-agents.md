[Skip to content](https://developers.llamaindex.ai/python/cloud/llamacloud/examples/building-rag-with-agents/#_top)
# Building RAG Applications with Index & Agents
Index is an enterprise service from LlamaIndex which makes it easy to load, parse, index and retrieve data and then use it in AI Agents built in our LlamaIndex open source framework.
This notebook is part of a [video tutorial](https://youtu.be/fx4SeNc3RZE?feature=shared) showing you how to get started with Index by creating your first index, loading data into it, setting up some configuration parameters, and then plugging that data into an agent.
To do that, we’ll walk you through a very simple agent built in LlamaIndex open source using our Workflows abstraction. This isn’t intended to be a full workflows tutorial, but we’ll provide you with some links to dive deeper.
The dataset we’ll be using today is a set of deposit account and rate agreements from JP Morgan Chase, a set of very dense and technical PDFs, perfect for getting an LLM to do the work of reading and understanding. If you want to create your own index, you can get the documents from Chase’s website or right here:
  * [Deposit account agreement](https://www.dropbox.com/scl/fi/b96krxnp0vqzd46i9a27h/chase-deposit-account-agreement.pdf?rlkey=702xiqbe4g24739v31iengfxj&dl=0)
  * [Additional banking services fees](https://www.dropbox.com/scl/fi/835lauu0qa45vq37y62a5/chase-additional-banking-services-and-fees.pdf?rlkey=emy2k2qvelzdshvhuk57zz4wl&dl=0)


## Video Tutorial
[Section titled “Video Tutorial”](https://developers.llamaindex.ai/python/cloud/llamacloud/examples/building-rag-with-agents/#video-tutorial)
Watch the video tutorial for this notebook:
As always, we’ll need to install our dependencies:
```


!pip install llama-cloud-services llama-index-llms-anthropic llama-index-core


```

To get started, we’ll need two API keys:
  * A `LLAMACLOUD_API_KEY` to access our index
  * An `ANTHROPIC_API_KEY` to access the LLM we’ll use to power our agent


```


from google.colab import userdata




LLAMACLOUD_API_KEY= userdata.get('llamacloud-demo-video')




ANTHROPIC_API_KEY= userdata.get('anthropic-key')


```

Let’s bring in our LlamaCloud Index:
```


from llama_cloud_services import LlamaCloudIndex





index =LlamaCloudIndex(




name="demo-video-index-1",




project_name="Demo Project",




organization_id="your-organization-id",




api_key=LLAMACLOUD_API_KEY



```

We’ll smoke-test our index to make sure there’s data in it by running a basic retrieval:
```


query ="What is the monthly service fee for Chase Total Checking"




nodes = index.as_retriever().retrieve(query)





print("Found "+(len(nodes))+" nodes")





for node in nodes:




print(f"Node ID: {node.node.id_}")




print(f"Score: {node.score}")




print(f"File Name: {node.node.metadata.get('file_name')}")




print(f"Page Label: {node.node.metadata.get('page_label')}")




print("-"*20)


```

```


Found 6 nodes




Node ID: 8703fd46-ae91-4542-b46b-f3bf95190693




Score: 0.9446333




File Name: chase additional banking services and fees.pdf




Page Label: 3




--------------------




Node ID: 0f226f14-384a-45c7-9d34-1fccfcb71f9a




Score: 0.8812988




File Name: chase additional banking services and fees.pdf




Page Label: 8




--------------------




Node ID: 877d22f0-711c-4817-a487-0084ef4dff71




Score: 0.82560414




File Name: chase additional banking services and fees.pdf




Page Label: 7




--------------------




Node ID: 9d31640a-b561-47b5-a518-0844c9855672




Score: 0.81524754




File Name: chase additional banking services and fees.pdf




Page Label: 5




--------------------




Node ID: 279cfd9c-bdd9-4b73-9791-96aa6bc32528




Score: 0.79732054




File Name: chase additional banking services and fees.pdf




Page Label: 2




--------------------




Node ID: f5c0df7c-b16d-4bcc-85aa-b79211b527e3




Score: 0.79675186




File Name: chase additional banking services and fees.pdf




Page Label: 6




--------------------


```

Great! Our index is returning the raw nodes for our query. If we want, we can even get a basic answer to our question by creating a query engine from the index.
First we’ll need to instantiate an LLM for the query engine to use:
```


from llama_index.llms.anthropic import Anthropic





llm =Anthropic(




api_key=ANTHROPIC_API_KEY,




model="claude-sonnet-4-20250514",



```

Now we create a query engine and ask the question:
```


engine = index.as_query_engine=llm)




response = engine.query(query)




print(response)


```

```


The monthly service fee for Chase Total Checking is **$12** (increasing to $15, effective August 24, 2025).





However, you can avoid this monthly service fee by meeting any ONE of the following requirements during each monthly statement period:





- Electronic deposits totaling $500 or more (such as payroll or government benefits through ACH, Real Time Payment, FedNow networks, or third-party services using Visa/Mastercard networks)




- **OR** maintain a daily balance of $1,500 or more in the account




- **OR** maintain an average beginning day balance of $5,000 or more across the account and any linked qualifying deposits/investments


```

But we can do more! These engines work by naively sending the entire query to the retriever in a single shot, and hoping the retrieved chunks are sufficient to answer the question. We can make an agent that can query the index and use the data in concert with tools to answer complex, multi-part questions.
To get started, let’s create the simplest possible tool: a function that can add two numbers.
```


defadd(a: float, b: float) -> float:




"""Add two numbers and returns the sum"""




return+ b


```

Now we’ll create a second tool, this one created from the query engine we made earlier.
```


from llama_index.core.tools import QueryEngineTool





jpmorgan = QueryEngineTool.from_defaults(




query_engine=engine,




name="JPMorganChaseTool",




description="Query documents about JP Morgan Chase bank rates, fees and procedures",



```

Now we’ll instantiate a FunctionAgent and give it these two tools. To learn more about creating agents, check out our [agent tutorial](https://docs.llamaindex.ai/en/stable/understanding/agent/).
```


from llama_index.core.agent.workflow import FunctionAgent





workflow =FunctionAgent(




tools=[add,jpmorgan],




llm=llm,




system_prompt="You are an expert in JP Morgan Chase banking fees and procedures"



```

Now we’re ready to ask a really complicated question! To show what’s happening under the hood, we’ll be streaming our tool calls and the results of those tool calls from the agent as it happens. Check out our [streaming documentation](https://docs.llamaindex.ai/en/stable/understanding/agent/streaming/) for more on how this works.
```


from llama_index.core.agent.workflow import (




AgentOutput,




ToolCallResult,






handler = workflow.run("""You have a Chase Total Checking account with $25 in your balance on



Monday morning. Throughout Monday, you make a $15 grocery purchase (debit card),


write a $20 check that gets cashed, and have a $25 automatic utility bill payment (ACH)


that processes. On Tuesday, you request a rush replacement for your lost debit card and


place a stop payment on another check over the phone with a banker. What is the total



amount in fees you would be charged, and when would each fee be assessed?""")




# handle streaming output



asyncfor event in handler.stream_events():




ifisinstance(event, AgentOutput):




for tool_call in event.tool_calls:




print("-"*20)




print("Tool called: "+ tool_call.tool_name)




print("Tool arguments:")




# Print all keys and values in tool_call.tool_kwargs




for key, value in tool_call.tool_kwargs.items():




print(f{key}: {value}")




print("-"*10)




elifisinstance(event, ToolCallResult):




print("Tool output: ", event.tool_output# the tool output


```

```


--------------------




Tool called: JPMorganChaseTool




Tool arguments:




input: Chase Total Checking overdraft fees NSF fees when transactions cause negative balance




----------




Tool output:  For Chase Total Checking accounts, here are the overdraft fees when transactions cause a negative balance:





## Overdraft Fees




Chase charges a **$34 Overdraft Fee per transaction** during nightly processing, beginning with the first transaction that overdraws your account balance by more than $50. There is a maximum of 3 fees per business day, up to $102 total.





## When Overdraft Fees Won't Be Charged




You won't be charged an Overdraft Fee in these situations:





- **Chase Overdraft Assist**: No fee if you're overdrawn by $50 or less at the end of the business day, OR if you're overdrawn by more than $50 but bring your account balance to overdrawn by $50 or less by the end of the next business day (you have until 11 p.m. ET/8 p.m. PT to make a deposit or transfer)





- **Small transactions**: No fee for transactions that are $5 or less





- **Authorized transactions**: No fee if your debit card transaction was authorized when there was sufficient available balance in your account





## What's Covered by Standard Overdraft Practice




The Standard Overdraft Practice covers:




- Checks and other transactions using your checking account number




- Recurring debit card transactions (like subscriptions or gym memberships)




- Automatic payments (recurring bills)





## What's NOT Covered




Everyday debit card transactions (groceries, gas, dining) are NOT covered unless you specifically enroll in Chase Debit Card Coverage.





Chase pays overdrafts at their discretion and does not guarantee they will always authorize or pay overdraft transactions. If they don't pay an overdraft, the transaction will be declined or returned.




--------------------




Tool called: JPMorganChaseTool




Tool arguments:




input: Chase debit card replacement fee rush delivery cost




----------




Tool output:  The cost for rush delivery of a replacement Chase debit card is **$15 per card, upon request**.





This fee applies when you request express shipping of a replacement debit or ATM card. You can avoid this fee by requesting standard shipping instead.





This rush delivery fee applies to most Chase account types, including Chase First Checking accounts. However, some premium account types like Chase Sapphire Checking and Chase Private Client Checking waive this fee as part of their benefits.




--------------------




Tool called: JPMorganChaseTool




Tool arguments:




input: Chase stop payment fee cost phone banker




----------




Tool output:  The stop payment fee when you contact Chase and a banker places your stop payment request on a check or ACH is $30 per request.





If you use chase.com, Chase Mobile, or the automated phone system to place a stop payment on a check, the fee is $25 per request. However, only some types of stop payments are available through these online and automated channels.




--------------------




Tool called: add




Tool arguments:




a: 15




b: 30




----------




Tool output:  45


```

```


print(str(await handler))


```

```


Based on the Chase Total Checking fee structure, here's what would happen in your scenario:





## Monday Transactions Analysis:




**Starting balance:** $25





1. **$15 grocery purchase (debit card)** - This would likely be **declined** since everyday debit card transactions are NOT covered by Chase's Standard Overdraft Practice unless you specifically enrolled in Chase Debit Card Coverage.





2. **$20 check cashed** - Balance becomes $5 ($25 - $20)





3. **$25 automatic utility bill payment (ACH)** - Balance becomes -$20 ($5 - $25)





## Overdraft Fee Assessment:




Since your account would be overdrawn by only $20 (which is less than $50), **Chase Overdraft Assist applies** - you would **NOT be charged the $34 overdraft fee** as long as the overdraft is $50 or less.





## Tuesday Fees:




1. **Rush debit card replacement:** $15




2. **Stop payment via phone with banker:** $30





## Total Fees: $45





**Fee Assessment Timeline:**




- **Monday:** $0 in overdraft fees (protected by Chase Overdraft Assist)




- **Tuesday:** $45 total ($15 for rush card replacement + $30 for stop payment)





The key factor here is that Chase Overdraft Assist protects you from overdraft fees when you're overdrawn by $50 or less, which saves you from what would otherwise be a $34 overdraft fee on the utility payment.


```

