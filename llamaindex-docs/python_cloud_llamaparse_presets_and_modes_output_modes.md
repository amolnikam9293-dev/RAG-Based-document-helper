[Skip to content](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/output_modes/#_top)
# Output
LlamaParse supports the following output formats:
  * Text: A basic text representation of the parsed document
  * Markdown: A [Markdown](https://en.wikipedia.org/wiki/Markdown) representation of the parsed document
  * JSON : A JSON representation of the content of the document
  * XLSX: A spreadsheet containing all the tables found in the document
  * PDF: A PDF representation of the parsed document (note: this is not the same as the original document)
  * Images: All images contained in the document. Need to set `save_images=True` on the job parameters.
  * Page Screenshot: Screenshots of document pages
  * Structured: if structured output is required, a JSON object containing the required data.


## Parsing modes and output
[Section titled “Parsing modes and output”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/output_modes/#parsing-modes-and-output)
LlamaParse supports different output formats depending on the parsing mode:
Mode | `text` | `markdown` | `json` | `xlsx` | `pdf` | structured  | `images` | screenshots   
---|---|---|---|---|---|---|---|---  
default (accurate) mode | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅  
fast_mode | ✅ | 🚫 | ✅ | 🚫 | ✅ | 🚫 | ✅ | ✅  
vendor_multimodal_mode | 🚫 | ✅ | ✅ | ✅ | ✅ | 🚫 | 🚫 | ✅  
premium_mode | ✅ | ✅ | ✅ | ✅ | ✅ | 🚫 | ✅ | ✅  
auto_mode | ✅ | ✅ | ✅ | ✅ | ✅ | 🚫 | ✅ | ✅  
continuous_mode | ✅ | ✅ | ✅ | ✅ | ✅ | 🚫 | ✅ | ✅  
spreadsheet  | ✅ | ✅ | ✅ | ✅ | 🚫 | 🚫 | ✅ | 🚫  
audio files  | ✅ | 🚫 | 🚫 | 🚫 | 🚫 | 🚫 | 🚫 | 🚫  
## Result endpoint
[Section titled “Result endpoint”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/output_modes/#result-endpoint)
LlamaParse allows you to retrieve your job results in different ways using the result endpoint. The supported result formats are `text`, `markdown`, `json`, `xlsx`, `pdf`, or `structured`.
Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/job/{job_id}/result/markdown'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"


```

The return result is a json object containing the requested result and a `job_metadata` field. The `job_metadata` contain:
  * `job_pages` : How many pages (or for spreadsheet sheets) were in your document.
  * `job_auto_mode_triggered_pages` : How many pages where upgraded to `premium_mode` after triggering `auto_mode`
  * `job_is_cache_hit` : If the job was a cache hit (we do not bill cache hits).


```



"markdown": "Here the markdown of the document if you asked for markdown as the result type....",




"job_metadata": {




"job_pages": 5,




"job_auto_mode_triggered_pages": 0,




"job_is_cache_hit": false




```

## Raw endpoint
[Section titled “Raw endpoint”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/output_modes/#raw-endpoint)
Instead of returning a JSON object containing your parsed document, you can set LlamaParse to return the raw text extracted from the document by retrieving the data in “raw” mode. The raw result can be `text`, `markdown`, `json`, `xlsx`, or `structured`.
Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/job/{job_id}/raw/result/markdown'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"


```

## Images
[Section titled “Images”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/output_modes/#images)
Image (and screenshot) can be download using the `job/{job_id}/result/image/image_name.png` endpoint.
Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/job/{job_id}/result/image/image_name.png'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"


```

## Details endpoint
[Section titled “Details endpoint”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/output_modes/#details-endpoint)
It is possible to see the details of a job including eventual job error or warning (both at the document and page model), but also the original job parameter using the `job/{job_id}/details` endpoint.
Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/job/{job_id}/details'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"


```

## Status endpoint
[Section titled “Status endpoint”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/output_modes/#status-endpoint)
It is possible to see the status of a job using the `job/{job_id}` endpoint.
Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/job/{job_id}'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"


```

## Footnotes
[Section titled “Footnotes”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/output_modes/#footnote-label)
  1. structured output is only available if `structured_output=True` [↩](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/output_modes/#user-content-fnref-1)
  2. document screenshots are available when `take_screenshot=True` [↩](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/output_modes/#user-content-fnref-2)
  3. Spreadsheets have their own pipeline and are processed differently than other documents, independently of the selected mode. [↩](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/output_modes/#user-content-fnref-3)
  4. Audio file have their own pipeline and are processed differently than other documents, independently of the selected mode. [↩](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/output_modes/#user-content-fnref-4)


