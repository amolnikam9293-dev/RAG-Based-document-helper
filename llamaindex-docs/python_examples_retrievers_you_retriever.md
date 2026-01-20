[Skip to content](https://developers.llamaindex.ai/python/examples/retrievers/you_retriever/#_top)
# You.com Retriever 
This notebook walks you through how to setup a Retriever that can fetch from You.com
```


%pip install llama-index-retrievers-you


```

```


import os




from llama_index.retrievers.you import YouRetriever


```

### Retrieve from You.com’s Search API
[Section titled “Retrieve from You.com’s Search API”](https://developers.llamaindex.ai/python/examples/retrievers/you_retriever/#retrieve-from-youcoms-search-api)
```


you_api_key =""or os.environ["YDC_API_KEY"]





retriever =YouRetriever(endpoint="search",api_key=you_api_key# default


```

```


retrieved_results = retriever.retrieve("national parks in the US")




print(retrieved_results[0].get_content())


```

```

The beaches and underwater world off the coast of Florida provide endless opportunities of play in the ocean. ... Glacier Bay is a living laboratory with ongoing research and study by scientists on a wide range of ocean-related issues. ... A picture of coastal life, Fire Island offers rich biological diversity and the beautiful landscapes that draw us all to the ocean.


A military veteran, Jose Sarria also became a prominent advocate for Latinos, immigrants, and the LGBTQ community in San Francisco. ... Explore the history of the LGBTQ community on Governors Island and Henry Gurber's work in protecting gay rights.


Explore the history of the LGBTQ community on Governors Island and Henry Gurber's work in protecting gay rights. ... Sylvia Rivera was an advocate for transgender rights and LGBTQ+ communities, and was an active participant of the Stonewall uprising.

```

### Retrieve from You.com’s News API
[Section titled “Retrieve from You.com’s News API”](https://developers.llamaindex.ai/python/examples/retrievers/you_retriever/#retrieve-from-youcoms-news-api)
```


you_api_key =""or os.environ["YDC_API_KEY"]





retriever =YouRetriever(endpoint="news",api_key=you_api_key)


```

```


retrieved_results = retriever.retrieve("Fed interest rates")




print(retrieved_results[0].get_content())


```

```

But seven months after the October announcement, the Fed's key interest rate — the federal funds rate — is still stuck at 5.25% to 5.5%, where it has been since July 2023. U.S. interest rates are built with the fed funds rate as the foundation.

```

## Use in Query Engine
[Section titled “Use in Query Engine”](https://developers.llamaindex.ai/python/examples/retrievers/you_retriever/#use-in-query-engine)
```


from llama_index.core.query_engine import RetrieverQueryEngine





retriever =YouRetriever()




query_engine = RetrieverQueryEngine.from_args(retriever)


```

```


response = query_engine.query("Tell me about national parks in the US")




print(str(response))


```

```

There are 63 national parks in the United States, each established to preserve unique landscapes, wildlife, and historical sites for the enjoyment of present and future generations. These parks are managed by the National Park Service, which aims to conserve the scenery and natural and historic objects within the parks. National parks offer a wide range of activities such as hiking, camping, wildlife viewing, and learning about the natural world. Some of the most visited national parks include Great Smoky Mountains, Yellowstone, and Zion, while others like Gates of the Arctic see fewer visitors due to their remote locations. Each national park has its own distinct features and attractions, contributing to the diverse tapestry of protected lands across the country.

```

