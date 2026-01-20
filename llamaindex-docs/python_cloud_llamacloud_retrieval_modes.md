[Skip to content](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/modes/#_top)
# Retrieval Modes
There are 4 Retrieval modes to choose from when using Index for retrieval:
  * `chunks`
  * `files_via_metadata`
  * `files_via_content`
  * `auto_routed`


This mode can be specified via the `retrieval_mode` parameter on the `LlamaCloudIndex.as_retriever` instance method. The playground UI can also be configured to use each of these retrieval modes.
The following sections describe each mode in further detail.
##  `chunks` mode
[Section titled “chunks mode”](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/modes/#chunks-mode)
### What does it do?
[Section titled “What does it do?”](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/modes/#what-does-it-do)
When using this mode, retrieval queries will be fullfilled by finding semantically similar chunks from the documents that have been ingested into the index. This is done by embedding the retrieval query, and then searching within the connected data sink for document chunks whose embeddings are a short distance away from this query embedding.
### When to use it?
[Section titled “When to use it?”](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/modes/#when-to-use-it)
When you want to retrieve specific pieces of information from a large dataset, `chunks` mode is ideal. In particular, fact finding queries about specific sections about a document would be well suited for this retrieval mode.
##  `files_via_metadata` mode
[Section titled “files_via_metadata mode”](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/modes/#files_via_metadata-mode)
### What does it do?
[Section titled “What does it do?”](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/modes/#what-does-it-do-1)
In `files_via_metadata` mode, the retrieval process focuses on selecting files based on their metadata attributes. This mode leverages a language model to evaluate the relevance of file metadata to the query. The metadata can include file names, resource information, and custom metadata tags. The selected files are then processed to retrieve the relevant documents.
### When to use it?
[Section titled “When to use it?”](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/modes/#when-to-use-it-1)
Use `files_via_metadata` mode when your query is expected to match specific metadata attributes of files. This is particularly useful for queries that involve identifying files by their names or other metadata tags, such as when you need to retrieve documents based on specific file properties or when the metadata provides a clear indication of relevance to the query.
##  `files_via_content` mode
[Section titled “files_via_content mode”](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/modes/#files_via_content-mode)
### What does it do?
[Section titled “What does it do?”](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/modes/#what-does-it-do-2)
The `files_via_content` mode retrieves files by analyzing the content within the files. It ranks document chunks based on their relevance to the query and selects files accordingly. This mode is designed to understand and process the actual content of the files in their entirety, making it suitable for queries that require summarization of the document’s text.
### When to use it?
[Section titled “When to use it?”](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/modes/#when-to-use-it-2)
Choose `files_via_content` mode when your query requires a holistic analysis of the file’s content. This mode is ideal for summarization queries where the file that needs to be summarized is not known beforehand.
##  `auto_routed` mode
[Section titled “auto_routed mode”](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/modes/#auto_routed-mode)
### What does it do?
[Section titled “What does it do?”](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/modes/#what-does-it-do-3)
The `auto_routed` mode is a superset of the other retrieval modes, designed to automatically select the most appropriate retrieval strategy based on the query. It leverages a language model to evaluate the query and determine whether to use `chunks`, `files_via_metadata`, or `files_via_content` mode. This dynamic selection process ensures that the retrieval method aligns with the query’s requirements, optimizing the retrieval process.
### When to use it?
[Section titled “When to use it?”](https://developers.llamaindex.ai/python/cloud/llamacloud/retrieval/modes/#when-to-use-it-3)
Use `auto_routed` mode when the nature of the query is not predetermined, or when you want the system to intelligently choose the best retrieval strategy. This mode is particularly useful in scenarios where queries can vary widely in their requirements, such as a mix of fact-finding, summarization, and metadata-based queries. By automatically routing the query to the most suitable retriever, `auto_routed` mode provides a more flexible retrieval solution.
