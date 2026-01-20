[Skip to content](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/framework_integration/#_top)
# Index Framework Integration
Index works seamlessly with our open source [python framework](https://github.com/run-llama/llama_index) and [typescript framework](https://github.com/run-llama/LlamaIndexTS).
You can use `LlamaCloudIndex` as a drop-in replace of the `VectorStoreIndex`. It offers better performance out-of-the-box, while simplifying the setup & maintenance.
You can either create an index via the framework, or connect to an existing index (e.g. created via the no-code UI).
## Create new index
[Section titled “Create new index”](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/framework_integration/#create-new-index)
In comparison to [creating new index via the no-code UI](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/ui/), you can create index from `Document` objects via the framework integration. This gives you more low level control over:
  1. how you want to pre-process your data, and
  2. using any data loaders from [LlamaHub](https://llamahub.ai).


Note that in this case, the data loading will be run locally (i.e. along with the framework code). For larger scale ingestion, it’s better to create the index via [no-code UI](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/ui/) or use the files or data sources API via [REST API & Clients](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/api_sdk/).
  * [ Python Framework ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/framework_integration/#tab-panel-41)
  * [ TypeScript Framework ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/framework_integration/#tab-panel-42)


Load documents
```


from llama_index.core import SimpleDirectoryReader





documents =SimpleDirectoryReader("data").load_data()


```

Create `LlamaCloudIndex`
```


import os




from llama_cloud_services import LlamaCloudIndex




os.environ[



"LLAMA_CLOUD_API_KEY"




] ="llx-..."# can provide API-key in env or in the constructor later on





index = LlamaCloudIndex.from_documents(




documents,




"my_first_index",




project_name="Default",




api_key="llx-...",




verbose=True,



```

Load documents
```

import { SimpleDirectoryReader } from "llamaindex";



const documents = await new SimpleDirectoryReader().loadData({



directoryPath: "node_modules/llamaindex/examples"



});

```

Create `LlamaCloudIndex`
```

import { LlamaCloudIndex } from "llama-cloud-services";



const index = await LlamaCloudIndex.fromDocuments({



documents: documents,




name: "example-pipeline",




projectName: "Default",




apiKey: "llx-..."



});

```

You may also optionally supply an `organization_id` string parameter to the `.from_documents` method. This may be useful if you have multiple projects with the same name under different organizations that you are a part of ([more info](https://developers.llamaindex.ai/python/cloud/general/organizations)). In general, it is recommended to supply this parameter if your account belongs to more than one organization to ensure your code continues to work as more projects are created in the organizations you are a member of.
## Connect to existing index
[Section titled “Connect to existing index”](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/framework_integration/#connect-to-existing-index)
  * [ Python Framework ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/framework_integration/#tab-panel-43)
  * [ TypeScript Framework ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/framework_integration/#tab-panel-44)


Connect to an existing index
```


import os




os.environ[



"LLAMA_CLOUD_API_KEY"




] ="llx-..."# can provide API-key in env or in the constructor later on





from llama_cloud_services import LlamaCloudIndex





index =LlamaCloudIndex("my_first_index",project_name="Default")


```

Connect to an existing index
```

const index = new LlamaCloudIndex({



name: "example-pipeline",




projectName: "Default",




apiKey: process.env.LLAMA_CLOUD_API_KEY, // can provide API-key in the constructor or in the env



});

```

## Use index in RAG/agent application
[Section titled “Use index in RAG/agent application”](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/framework_integration/#use-index-in-ragagent-application)
  * [ Python Framework ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/framework_integration/#tab-panel-45)
  * [ TypeScript Framework ](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/framework_integration/#tab-panel-46)


```


retriever = index.as_retriever()




nodes = retriever.retrieve("Example query")



...




query_engine = index.as_query_engine()




answer = query_engine.query("Example query")



...




chat_engine = index.as_chat_engine()




message = chat_engine.chat("Example query")



...

```

See [full framework documentation](https://docs.llamaindex.ai/)
```

// query engine


const queryEngine = index.asQueryEngine({



similarityTopK: 5,



});



const answer = await queryEngine.query({



query: "Example query",



});



// retrieval


const retriever = index.asRetriever({



similarityTopK: 5,



});



const nodes = await retriever.retrieve({



query: "Example query",



});



// chat


import { ContextChatEngine } from "llamaindex";



const retriever = index.asRetriever({



similarityTopK: 5,



});



const chatEngine = new ContextChatEngine({ retriever });



const responder = await chatEngine.chat({ message: query });

```

