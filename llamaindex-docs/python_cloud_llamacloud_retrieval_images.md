[Skip to content](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/images/#_top)
# Image Retrieval
In addition to retrieving text content from your indexed documents, LlamaCloud also supports retrieving images sourced from these documents.
This is particularly useful for applications that require visual context, such as presentations, reports, or any other document type that includes images.
## Image sources
[Section titled “Image sources”](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/images/#image-sources)
Images are extracted from Files attached to an index in the following ways:
  * Page Screenshots 
    * A screenshot of each page in a file is taken and stored as an image.
    * This screenshot image data can be downloaded from the [Page Screenshots API](https://api.cloud.llamaindex.ai/docs#/Files/get_file_page_screenshot_api_v1_files__id__page_screenshots__page_index__get)
  * Page Figures 
    * If a file contains figures embedded in its pages, these figures are extracted and stored as images.
    * This figure image data can be downloaded from the [Page Figures API](https://api.cloud.llamaindex.ai/docs#/Files/get_file_page_figure_api_v1_files__id__page_figures__page_index___figure_name__get)
    * **Important Note:** Please note that Page Figure extraction is currently not supported for self-hosted (aka BYOC) deployments of LlamaCloud. We will be adding support for this environment in the near future!


## Enabling Image Indexing
[Section titled “Enabling Image Indexing”](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/images/#enabling-image-indexing)
To enable image retrieval in your index, you need to have the correct parsing parameters setup on your index.
### Setting up via LlamaCloud UI
[Section titled “Setting up via LlamaCloud UI”](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/images/#setting-up-via-llamacloud-ui)
When creating a new index or editing an existing one, simply ensure you’ve toggled **Enable Multi-modal retrieval** under the Multi-Modal Indexing section.
### Setting up via API
[Section titled “Setting up via API”](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/images/#setting-up-via-api)
To enable image retrieval programmatically, you need to toggle the correct flags under the `llama_parse_parameters` on your index.
For enabling Page Screenshot indexing & retrieval, set the `llama_parse_parameters.take_screenshot` flag to `true`. For enabling Page Figure indexing & retrieval, set the `llama_parse_parameters.extract_layout` flag to `true`.
Here is an example of setting this up using the [`LlamaCloudIndex` class](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/framework_integration):
```


from llama_cloud import LlamaParseParameters




from llama_cloud_services import LlamaCloudIndex





index = LlamaCloudIndex.create_index(




name="my_image_index",




project_name="Default",




api_key="llx-...",




llama_parse_parameters=LlamaParseParameters(




take_screenshot=True,




extract_layout=True,




```

## Retrieving Images
[Section titled “Retrieving Images”](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/images/#retrieving-images)
Once your index is set up to support image indexing, you can retrieve images using the retriever interface on your `LlamaCloudIndex`. Image retrieval works similarly to text retrieval, but you must specify which types of images you want to retrieve: page screenshots and/or page figures.
### Retrieving Page Screenshots
[Section titled “Retrieving Page Screenshots”](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/images/#retrieving-page-screenshots)
To retrieve page screenshots (full-page images for each page in your indexed files), use the `as_retriever` method with the `retrieve_page_screenshot_nodes=True` parameter:
```


from llama_cloud import LlamaParseParameters




from llama_cloud_services import LlamaCloudIndex




# Assume you have already created and ingested files into your index



index =LlamaCloudIndex(




name="my_image_index",




project_name="Default",




api_key="llx-...",




llama_parse_parameters=LlamaParseParameters(




take_screenshot=True,






# Wait for ingestion to complete if needed



index.wait_for_completion()




# Get a retriever that will return page screenshot images



retriever = index.as_retriever(retrieve_page_screenshot_nodes=True)




# Retrieve images relevant to your query



nodes = retriever.retrieve("What color is the company's logo?")




# Filter for image nodes (optional)



from llama_index.core.schema import ImageNode




image_nodes =[n.node forin nodes ifisinstance(n.node, ImageNode)]




# Each ImageNode contains a base64-encoded image and metadata



for img_node in image_nodes:




print(img_node.metadata# e.g., file_id, page_index, file_name




# img_node.image is a base64-encoded image string


```

### Retrieving Page Figures
[Section titled “Retrieving Page Figures”](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/images/#retrieving-page-figures)
To retrieve figures (e.g., charts, diagrams, images) extracted from your documents, use the `retrieve_page_figure_nodes=True` parameter:
```

from llama_cloud import LlamaParseParameters


from llama_cloud_services import LlamaCloudIndex



# Assume you have already created and ingested files into your index


index = LlamaCloudIndex(



name="my_image_index",




project_name="Default",




api_key="llx-...",




llama_parse_parameters=LlamaParseParameters(




extract_layout=True,






# Wait for ingestion to complete if needed


index.wait_for_completion()



# Get a retriever that will return page figure images


retriever = index.as_retriever(retrieve_page_figure_nodes=True)



nodes = retriever.retrieve("Describe the chart showing future growth projections")



image_nodes = [n.node for n in nodes if isinstance(n.node, ImageNode)]


for img_node in image_nodes:



print(img_node.metadata)  # includes file_id, page_index, figure_name, file_name


```

Of course, to retrieve both page screenshots and figures, you can set both `retrieve_page_screenshot_nodes=True` & `retrieve_page_figure_nodes=True`.
Just ensure you’ve also set `take_screenshot=True` and `extract_layout=True` in your index’s `llama_parse_parameters` to enable the necessary image extraction.
## Conclusion
[Section titled “Conclusion”](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/images/#conclusion)
**That’s it!** You can now retrieve images (screenshots and figures) from your indexed documents using LlamaCloud.
For more advanced use cases, such as [composite retrieval](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/retrieval/composite) or async usage, refer to the [framework integration guide](https://developers.llamaindex.ai/python/cloud/llamacloud/guides/framework_integration) and [the API reference](https://developers.llamaindex.ai/cloud-api-reference/llama-platform/).
