[Skip to content](https://developers.llamaindex.ai/python/cloud/llamaparse/features/metadata/#_top)
# Metadata
In JSON mode, LlamaParse will return a data structure representing the parsed object. This is useful for further processing or analysis.
To use this mode, set the result type to “json”.
Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/job/<job_id>/result/json'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"


```

## Result format
[Section titled “Result format”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/metadata/#result-format)
```



"pages": [




..pageobjects..





"job_metadata": {




"job_pages": int,




"job_is_cache_hit": boolean




```

## Page objects
[Section titled “Page objects”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/metadata/#page-objects)
Within page objects, the following keys may be present depending on your document.
  * `page`: The page number of the document.
  * `text`: The text extracted from the page.
  * `md`: The markdown version of the extracted text.
  * `images`: Any images extracted from the page.
  * `items`: An array of `heading`, `text` and `table` objects in the order they appear on the page.


## Retrieving images
[Section titled “Retrieving images”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/metadata/#retrieving-images)
Images are returned as an array of image objects, of the form:
```



"name": "img_p2_5.png",




"height": 718,




"width": 251



```

You can retrieve the image extracted directly using the value of the `name`, like this:
Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/job/<job_id>/result/image/<name>'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--output"file.png"


```

Note the additional `--output` argument to curl to get the binary saved to a file.
## Slide speaker notes
[Section titled “Slide speaker notes”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/metadata/#slide-speaker-notes)
For certain presentation formats, if a slide contains speaker notes, the speaker notes will be extracted and returned in the `slideSpeakerNotes` entry for the page:
```




"page": 1,




"text": "Hello\nSlide with notes",




"slideSpeakerNotes": "This is a speaker note",





...

```

Currently supported formats for slide speaker notes extraction:
  * `.pptx` (PowerPoint 2007+)


For these formats, slide speaker notes extraction is supported in all parse modes except `parse_page_with_lvm`.
