[Skip to content](https://developers.llamaindex.ai/python/cloud/llamaparse/features/parse_region/#_top)
# Selecting what to parse
By default LlamaParse will extract all the visible content of every page of a document
## Parsing only some pages
[Section titled “Parsing only some pages”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/parse_region/#parsing-only-some-pages)
You can specify the pages you want to parse by passing specific page numbers as a comma-separated list in the `target_pages` argument. Pages are numbered starting at `0`.


```


parser =LlamaParse(




target_pages="0,1,2,22,33"



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'target_pages="0,1,2,22,33"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

The range syntax is also supported `target_pages=0-2,6-22,33`.
## Parsing only a targeted area of a document
[Section titled “Parsing only a targeted area of a document”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/parse_region/#parsing-only-a-targeted-area-of-a-document)
You can specify an area of a document that you want to parse. This can be helpful to remove headers and footers.
To do so you need to provide the bounding box margin expressed as a ratio compare to the page size between 0 and 1 in `bbox_left`, `bbox_right`, `bbox_top` and `bbox_bottom`.
Examples:
  * To not parse the top 10% of a document: `bbox_top=0.1`
  * To not parse the top 10% and bottom 20% of a document: `bbbox_top=0.1` and `bbox_bottom=0.2`,




```


parser =LlamaParse(




bbox_left=0.2



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'bbox_left=0.2'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## Bounding box (legacy)
[Section titled “Bounding box (legacy)”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/parse_region/#bounding-box-legacy)
We support a deprecated way of doing so where it is possible to provide the bounding box margin in clockwise order from the top in a comma separated string in the `bounding_box` arguments. The margins are expressed as a ratio compare to the page size between 0 and 1.
Examples:
  * To not parse the top 10% of a document: `bounding_box="0.1,0,0,0"`
  * To not parse the top 10% and bottom 20% of a document: `bounding_box="0.1,0,0.2,0"`




```


parser =LlamaParse(




bounding_box="0.1,0.4,0.2,0.3"



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'bounding_box="0.1,0.4,0.2,0.3"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## Limiting number of page to parse
[Section titled “Limiting number of page to parse”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/parse_region/#limiting-number-of-page-to-parse)
If you want to limit the maximum amount of pages to parse you can use the parameter `max_pages`. LlamaParse will stop parsing the document after the specified pages.


```


parser =LlamaParse(




max_pages=25



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'max_pages=25'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

