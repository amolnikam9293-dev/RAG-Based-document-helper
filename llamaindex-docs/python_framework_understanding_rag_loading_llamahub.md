[Skip to content](https://developers.llamaindex.ai/python/framework/understanding/rag/loading/llamahub/#_top)
# LlamaHub
Our data connectors are offered through [LlamaHub](https://llamahub.ai/) 🦙. LlamaHub contains a registry of open-source data connectors that you can easily plug into any LlamaIndex application (+ Agent Tools, and Llama Packs).
## Usage Pattern
[Section titled “Usage Pattern”](https://developers.llamaindex.ai/python/framework/understanding/rag/loading/llamahub/#usage-pattern)
Get started with:
```


from llama_index.core import download_loader





from llama_index.readers.google import GoogleDocsReader





loader =GoogleDocsReader()




documents = loader.load_data(document_ids=[...])


```

## Built-in connector: SimpleDirectoryReader
[Section titled “Built-in connector: SimpleDirectoryReader”](https://developers.llamaindex.ai/python/framework/understanding/rag/loading/llamahub/#built-in-connector-simpledirectoryreader)
`SimpleDirectoryReader`. Can support parsing a wide range of file types including `.md`, `.pdf`, `.jpg`, `.png`, `.docx`, as well as audio and video types. It is available directly as part of LlamaIndex:
```


from llama_index.core import SimpleDirectoryReader





documents =SimpleDirectoryReader("./data").load_data()


```

## Available connectors
[Section titled “Available connectors”](https://developers.llamaindex.ai/python/framework/understanding/rag/loading/llamahub/#available-connectors)
Browse [LlamaHub](https://llamahub.ai/) directly to see the hundreds of connectors available, including:
  * [Notion](https://developers.notion.com/) (`NotionPageReader`)
  * [Google Docs](https://developers.google.com/docs/api) (`GoogleDocsReader`)
  * [Slack](https://api.slack.com/) (`SlackReader`)
  * [Discord](https://discord.com/developers/docs/intro) (`DiscordReader`)
  * [Apify Actors](https://llamahub.ai/l/apify-actor) (`ApifyActor`). Can crawl the web, scrape webpages, extract text content, download files including `.pdf`, `.jpg`, `.png`, `.docx`, etc.


