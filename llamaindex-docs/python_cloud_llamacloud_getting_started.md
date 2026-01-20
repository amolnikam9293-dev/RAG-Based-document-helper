[Skip to content](https://developers.llamaindex.ai/python/cloud/llamacloud/getting_started/#_top)
# Getting Started
## Overview
[Section titled “Overview”](https://developers.llamaindex.ai/python/cloud/llamacloud/getting_started/#overview)
Index is part of the LlamaCloud platform (which includes LlamaParse, LlamaExtract, LlamaAgents, and other products). It makes it easy to set up a highly scalable & customizable data ingestion pipeline for your RAG use case. No need to worry about scaling challenges, document management, or complex file parsing.
Index offers all of this through a no-code UI, REST API / clients, and seamless integration with our popular python & typescript framework.
Connect your index to your [data sources](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/), set your parse parameters & embedding model, and the index automatically handles syncing your data into your [vector databases](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks/). From there, we offer an easy-to-use interface to query your indexes and retrieve relevant ground truth information from your input documents.
## Prerequisites
[Section titled “Prerequisites”](https://developers.llamaindex.ai/python/cloud/llamacloud/getting_started/#prerequisites)
  1. [Sign up for an account](https://cloud.llamaindex.ai)
  2. Prepare an API key for your preferred embedding model service (e.g. OpenAI).


## Sign in
[Section titled “Sign in”](https://developers.llamaindex.ai/python/cloud/llamacloud/getting_started/#sign-in)
Sign in via <https://cloud.llamaindex.ai/>
You should see options to sign in via Google, Github, Microsoft, or email.
## Set up an index via UI
[Section titled “Set up an index via UI”](https://developers.llamaindex.ai/python/cloud/llamacloud/getting_started/#set-up-an-index-via-ui)
Navigate to `Index` feature via the left navbar. 
Click the `Create Index` button. You should see a index configuration form. 
Configure data source - file upload
Click `Select a data source` dropdown and select `Files`
Drag files into file pond or `click to browse`. 
[See full list of data sources and specifications](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/)
Configure data sink - managed
Select `Fully Managed` data sink. 
[See full list of data sinks and specifications](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks/)
Configure embedding model - OpenAI
Select `OpenAI Embedding` and put in your API key. 
See [full list of supported embedding models](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/embedding_models/)
Configure parsing & transformation settings
Toggle to enable or disable `Llama Parse`.
Select `Auto` mode for best default transformation setting (specify desired chunks size & chunk overlap as necessary.)
`Manual` mode is coming soon, with additional customizability.
[More details about parsing & transformation settings](https://developers.llamaindex.ai/python/cloud/llamacloud/parsing_transformation/).
After configuring the ingestion pipeline, click `Deploy Index` to kick off ingestion. 
## (Optional) Observe and manage your index via UI
[Section titled “(Optional) Observe and manage your index via UI”](https://developers.llamaindex.ai/python/cloud/llamacloud/getting_started/#optional-observe-and-manage-your-index-via-ui)
You should see an index overview with the latest ingestion status. 
(optional) Test retrieval via playground
Navigate to `Playground` tab to test your retrieval endpoint.
Select between `Fast`, `Accurate`, and `Advanced` retrieval modes. Input test query and specify retrieval configurations (e.g. base retrieval and top n after re-ranking). 
(optional) Manage connected data sources (or uploaded files)
Navigate to `Data Sources` tab to manage your connected data sources.
You can upsert, delete, download, and preview uploaded files.
## Integrate your retrieval endpoint into RAG/agent application
[Section titled “Integrate your retrieval endpoint into RAG/agent application”](https://developers.llamaindex.ai/python/cloud/llamacloud/getting_started/#integrate-your-retrieval-endpoint-into-ragagent-application)
After setting up the index, we can now integrate the retrieval endpoint into our RAG/agent application. Here, we will use a colab notebook as example.
Obtain LlamaCloud API key
Navigate to `API Key` page from left sidebar. Click `Generate New Key` button. 
Copy the API key to safe location. You will not be able to retrieve this again. [More detailed walkthrough](https://developers.llamaindex.ai/python/cloud/general/api_key/).
Setup your RAG/agent application - python notebook
Install latest python framework:
```

pip install llama-index

```

[See detail instructions](https://docs.llamaindex.ai/en/stable/getting_started/installation/)
Navigate to `Overview` tab. Click `Copy` button under `Retrieval Endpoint` card 
Now you have a minimal RAG application ready to use! 
You can find demo colab notebook [here](https://colab.research.google.com/drive/1yu2dFrJDHYDDiiWYcEuZNodJulg1-QZD?usp=sharing).
