[Skip to content](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/composite/#_top)
# Composite Retrieval
## What is Composite Retrieval?
[Section titled “What is Composite Retrieval?”](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/composite/#what-is-composite-retrieval)
The Composite Retrieval API allows you to set up a `Retriever` entity that can do retrieval overal several indices at once. This allows you to query across several sources of information at once, further enhancing retrieval relevancy and breadth.
## When do you need to use this?
[Section titled “When do you need to use this?”](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/composite/#when-do-you-need-to-use-this)
A single index can ingest a variety of file or document types. These files can be formatted in various ways _(e.g. a SEC 10K filing may be formatted very differently to a PowerPoint slide show)_.
However, when all these various files/documents are ingested through the same single index, they will be subjected to the same parsing & chunking parameters, regardless of any individual differences in their formatting. This can be problematic as it can lead to sub-par downstream retrieval performance.
For example, a slideshow containing many images may require multi-modal parsing whereas an financial reports would be more concerned with accurate table and chart extraction. Ideally, your slideshows can be parsed and chunked differently than your financial reports are. To do so, you should put your slideshow files in an index named “Slide Shows” and your financial reports an an index named “Financial Reports”:
```


import os




from llama_cloud_services import LlamaCloudIndex




# Set your LlamaCloud API Key in LLAMA_CLOUD_API_KEY



assert os.environ.get("LLAMA_CLOUD_API_KEY")




project_name ="My Project"




# Setup your indices



slides_index = LlamaCloudIndex.from_documents(




documents=[],# leave documents empty since we will be uploading the raw files




name="Slides",




project_name=project_name,





# Add your slide files to the index



slides_directory ="./data/slides"




for file_name in os.listdir(slides_directory):




file_path = os.path.join(slides_directory, file_name)




# Add each file to the slides index




slides_index.upload_file(file_path,wait_for_ingestion=False)




# Do the same with your Financial Report files



financial_index = LlamaCloudIndex.from_documents(




documents=[],# leave documents empty since we will be uploading the raw files




name="Financial Reports",




project_name=project_name,






financial_reports_directory ="./data/financial_reports"




for file_name in os.listdir(financial_reports_directory):




file_path = os.path.join(financial_reports_directory, file_name)




# Add each file to the slides index




financial_index.upload_file(file_path,wait_for_ingestion=False)




# wait for both to finish ingestion



slides_index.wait_for_completion()




financial_index.wait_for_completion()


```

Now that you have these files in separate indicies, you can edit the parsing and chunking settings for these datasets independently either via the LlamaCloud UI or via the API.
However, when you want to retrieve data from these, you’re still only able to do so one index at a time via `index.as_retriever().retrieve("my query")`. Your application likely wants to use all of the information you’ve indexed across both of these indices. You can unify both of these retrievers by creating a _Composite_ Retriever:
```


from llama_cloud import CompositeRetrievalMode




from llama_cloud_services import LlamaCloudCompositeRetriever





composite_retriever =LlamaCloudCompositeRetriever(




name="My App Retriever",




project_name=project_name,




# If a Retriever named "My App Retriever" doesn't already exist, one will be created




create_if_not_exists=True,




# CompositeRetrievalMode.FULL will query each index individually and globally rerank results at the end




mode=CompositeRetrievalMode.FULL,




# return the top 5 results from all queried indices




rerank_top_n=5,





# Add the above indices to the composite retriever


# Carefully craft the description as this is used internally to route a query to an attached sub-index when CompositeRetrievalMode.ROUTING is used



composite_retriever.add_index(




slides_index,




description="Information source for slide shows presented during team meetings",





composite_retriever.add_index(




financial_index,




description="Information source for company financial reports",





# Start querying across both of these indices at once



nodes = retriever.retrieve("What was the key feature of the highest revenue product in 2024 Q4?")


```

With the above code, you can now query across all of your organizational knowledge, spread across a heterogenous dataset of files, _without_ having to sacrifice retrieval quality.
## Composite Retrieval Modes
[Section titled “Composite Retrieval Modes”](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/composite/#composite-retrieval-modes)
There are currently two Composite Retrieval Modes:
  * `full` - In this mode, all attached sub-indices will be queried and reranking will be executed across all nodes received from these sub-indices.
  * `routed` - In this mode, an agent determines which sub-indices are most relevant to the provided query _(based on the sub-index’s`name` & `description` you’ve provided)_ and only queries those indices that are deemed relevant. Only the nodes from that chosen subset of indices are then reranked before being returned in the retrieval response. 
    * Note: If you plan on using this mode, ensure that the `name` & `description` you give each sub-index in your Retriever is carefully crafted to assist the agent in accurately routing your queries.


