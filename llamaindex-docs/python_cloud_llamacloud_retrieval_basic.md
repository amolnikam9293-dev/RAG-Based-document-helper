[Skip to content](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/basic/#_top)
# Basic
Data Retrieval is a key step in any RAG application. The most common use case is to retrieve relevant context from your data to help with a question.
Once data has been ingested into LlamaCloud, you can use the Retrieval API to retrieve relevant context from your data.
Our Retrieval API allows you to retrieve relevant ground truth text chunks that have been ingested into a Index for a given query. The following snippets show how to run this basic form of retrieval:
  * [ Python Framework ](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/basic/#tab-panel-54)
  * [ TypeScript Framework ](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/basic/#tab-panel-55)


```


import os




os.environ[



"LLAMA_CLOUD_API_KEY"




] ="llx-..."# can provide API-key in env or in the constructor later on





from llama_cloud_services import LlamaCloudIndex




# connect to existing index



index =LlamaCloudIndex("my_first_index",project_name="Default")




# configure retriever


# alpha=1.0 restricts it to vector search.



retriever = index.as_retriever(




dense_similarity_top_k=3,




alpha=1.0,




enable_reranking=False,





nodes = retriever.retrieve("Example query")


```

```

import { LlamaCloudIndex } from "llama-cloud-services";



// connect to existing index


const index = new LlamaCloudIndex({



name: "example-pipeline",




projectName: "Default",




apiKey: process.env.LLAMA_CLOUD_API_KEY, // can provide API-key in the constructor or in the env



});



// configure retriever


const retriever = index.asRetriever({



similarityTopK: 3,




sparseSimilarityTopK: 3,




alpha: 0.5,




enableReranking: true,




rerankTopN: 3,



});



const nodes = retriever.retrieve({



query: "Example Query"



});

```

We can build upon this basic form of retrieval by including things like hybrid search, reranking, and metadata filtering to improve the accuracy of the retrieval. These advanced retrieval parameters are described in greater detail in the next section ➡️
