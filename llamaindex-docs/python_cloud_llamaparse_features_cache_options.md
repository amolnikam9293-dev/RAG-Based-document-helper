[Skip to content](https://developers.llamaindex.ai/python/cloud/llamaparse/features/cache_options/#_top)
# Cache options
## About cache
[Section titled “About cache”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/cache_options/#about-cache)
By default LlamaParse caches parsed documents for 48 hours before permanently deleting them. The cache takes into account the parsing parameters that can have an impact on the output (such as parsing_instructions, language, and page_separators).
## Cache invalidation
[Section titled “Cache invalidation”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/cache_options/#cache-invalidation)
You can invalidate the cache for a specific document by setting the `invalidate_cache` option to `True`. The cache will be cleared, the document will be re-parsed and the new parsed document will be stored in the cache.


```


parser =LlamaParse(




invalidate_cache=True



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'invalidate_cache="true"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## Do not cache
[Section titled “Do not cache”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/cache_options/#do-not-cache)
You can specify that you do not want a specific job to be cached by setting the `do_not_cache` option to `True`. In this case the document will not be added in the cache, so if you re-upload the document it will be re-processed.


```


parser =LlamaParse(




do_not_cache=True



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'do_not_cache="true"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

