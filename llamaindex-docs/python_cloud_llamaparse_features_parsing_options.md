[Skip to content](https://developers.llamaindex.ai/python/cloud/llamaparse/features/parsing_options/#_top)
# Parsing options
## Set language
[Section titled “Set language”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/parsing_options/#set-language)
LlamaParse uses OCR to extract text from images. Our OCR supports a [long list of languages](https://github.com/run-llama/llama_cloud_services/blob/main/py/llama_cloud_services/parse/utils.py#L54). You can specify one or more languages by separating them with a comma. This only affects text extracted from images.


```


parser =LlamaParse(




language="fr"



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'language="fr"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## Disable OCR
[Section titled “Disable OCR”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/parsing_options/#disable-ocr)
By default, LlamaParse runs OCR on images embedded in the document. You can disable it with `disable_ocr=True`.


```


parser =LlamaParse(




disable_ocr=True



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'disable_ocr="true"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## Skip diagonal text
[Section titled “Skip diagonal text”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/parsing_options/#skip-diagonal-text)
By default, LlamaParse will attempt to parse text that is diagonal on the page. This can be useful for some documents, but also introduce noise and errors. To avoid parsing diagonal text, set `skip_diagonal_text=True`.


```


parser =LlamaParse(




skip_diagonal_text=True



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'skip_diagonal_text="true"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## Do not unroll columns
[Section titled “Do not unroll columns”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/parsing_options/#do-not-unroll-columns)
By default, LlamaParse tries to unroll columns into reading order. Set `do_not_unroll_columns=True` to prevent LlamaParse from doing so.


```


parser =LlamaParse(




do_not_unroll_columns=True



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'do_not_unroll_columns="true"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## Target pages
[Section titled “Target pages”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/parsing_options/#target-pages)
By default, all pages will be extracted. To parse specific pages only, use a comma-separated string. Page numbering starts at 0.


```


parser =LlamaParse(




target_pages="0,2,7"



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'target_pages="0,2,7"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## Page separator
[Section titled “Page separator”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/parsing_options/#page-separator)
By default, LlamaParse will separate pages in the markdown and text output by \n---\n. You can change this separator by setting page_separator to the desired string.
It’s also possible to include the page number within the separator using `{pageNumber}` in the string. It will be replaced by the page number of the next page.


```


parser =LlamaParse(




page_separator="\n=================\n",




# page_separator="\n== {pageNumber} ==\n" # Will transform to "\n== 4 ==\n" to separate page 3 and 4.



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'page_separator="\n== {pageNumber} ==\n"'\




--form'page_prefix="START OF PAGE: {pageNumber}\n"'\




--form'page_suffix="\nEND OF PAGE: {pageNumber}"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## Page prefix and suffix
[Section titled “Page prefix and suffix”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/parsing_options/#page-prefix-and-suffix)
It’s possible to specify a prefix or a suffix to be added to each page. These strings can contain `{pageNumber}` as well and will be replaced by the current page number. Both parameters are optional and empty by default.


```


parser =LlamaParse(




page_prefix="START OF PAGE: {pageNumber}\n"




page_suffix="\nEND OF PAGE: {pageNumber}"



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'page_prefix="START OF PAGE: {pageNumber}\n"




page_suffix="\nEND OF PAGE: {pageNumber}"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## Bounding box
[Section titled “Bounding box”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/parsing_options/#bounding-box)
Specify an area of a document that you want to parse. This can be helpful to remove headers and footers. To do so you need to provide the bounding box margin in clockwise order from the top in a comma-separated. The margins are expressed as a fraction of the page size, a number between 0 and 1.
Examples:
  * To exclude the top 10% of a document: bounding_box=“0.1,0,0,0”
  * To exclude the top 10% and bottom 20% of a document: bounding_box=“0.1,0,0.2,0”




```


parser =LlamaParse(




bounding_box="0.1,0,0.2,0"



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'bounding_box="0.1,0,0.2,0"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## Take screenshot
[Section titled “Take screenshot”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/parsing_options/#take-screenshot)
Take a screenshot of each page and add it to JSON output in the following format:
```



"images": [





"name": "page_1.jpg",




"height": 792,




"width": 612,




"x": 0,




"y": 0,




"type": "full_page_screenshot"





```



```


parser =LlamaParse(




take_screenshot=True



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'take_screenshot="true"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## Disable image extraction
[Section titled “Disable image extraction”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/parsing_options/#disable-image-extraction)
It is possible to disable the extraction of image for better performance using `disable_image_extraction=true`


```


parser =LlamaParse(




disable_image_extraction=True



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'disable_image_extraction="true"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## Extract multiple table per sheet in spreadsheet
[Section titled “Extract multiple table per sheet in spreadsheet”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/parsing_options/#extract-multiple-table-per-sheet-in-spreadsheet)
By default LlamaParse extract each sheet of a spreadsheet as one table. Using `spreadsheet_extract_sub_tables=true`, LlamaParse will try to identify spreadsheet sheet with multiple table and return them as separated tables.


```


parser =LlamaParse(




spreadsheet_extract_sub_tables=True



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'spreadsheet_extract_sub_tables="true"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## Force re-computation of cells containing formulas in spreadsheet
[Section titled “Force re-computation of cells containing formulas in spreadsheet”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/parsing_options/#force-re-computation-of-cells-containing-formulas-in-spreadsheet)
By default, for spreadsheet cells containing formulas, LlamaParse extracts cached (pre-computed) values if a cached cell value exists in the document. When `spreadsheet_force_formula_computation=true`, LlamaParse will re-compute values for all spreadsheet cells containing formulas.


```


parser =LlamaParse(




spreadsheet_force_formula_computation=True



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'spreadsheet_force_formula_computation="true"'\




-F'file=@/path/to/your/file.xlsx;type=application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


```

Note that using `spreadsheet_force_formula_computation=true` will have a negative performance impact when parsing spreadsheets containing formulas.
## Output table as HTML in markdown
[Section titled “Output table as HTML in markdown”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/parsing_options/#output-table-as-html-in-markdown)
A common issue with markdown table is that they do not handle merged cells well. It is possible to ask LlamaParse to return table as html with `colspan` and `rowspan` to get a better representation of the table. When `output_tables_as_HTML=true`, tables present in the markdown will be output as HTML tables.


```


parser =LlamaParse(




output_tables_as_HTML=True



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'output_tables_as_HTML="true"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## Preserve alignment across pages
[Section titled “Preserve alignment across pages”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/parsing_options/#preserve-alignment-across-pages)
If set to `preserve_layout_alignment_across_pages=True` will try to keep the text align in text mode accross pages. Useful for document with continuous table / alignment accross pages.


```


parser =LlamaParse(




preserve_layout_alignment_across_pages=True



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'preserve_layout_alignment_across_pages="true"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## Preserve very small text
[Section titled “Preserve very small text”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/parsing_options/#preserve-very-small-text)
If set to `preserve_very_small_text=True`, LlamaParse will try to preserve very small text lines. This can be useful for documents containing vector graphics with very small text lines that may not be recognized by OCR or a vision model (such as in CAD drawings).


```


parser =LlamaParse(




preserve_very_small_text=True



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'preserve_very_small_text="true"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## Hide headers
[Section titled “Hide headers”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/parsing_options/#hide-headers)
When set to true, LlamaParse will try to not output page headers in the Markdown output. The removed headers will be present in the JSON object inside the `pageHeaderMarkdown` field if needed.
LlamaParse will use different techniques to identify the headers of the page based on the chosen mode; headers will not be detected in Fast Mode.


```


parser =LlamaParse(




hide_headers=True



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'hide_headers="true"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## Hide footers
[Section titled “Hide footers”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/parsing_options/#hide-footers)
When set to true, LlamaParse will try to not output page footers in the Markdown output. The removed footers will be present in the JSON object inside the `pageFooterMarkdown` field if needed.
LlamaParse will use different techniques to identify the footers of the page based on the chosen mode; footers will not be detected in Fast Mode.


```


parser =LlamaParse(




hide_footers=True



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'hide_footers="true"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## Page header/footer prefix/suffix
[Section titled “Page header/footer prefix/suffix”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/parsing_options/#page-headerfooter-prefixsuffix)
LlamaParse allows you to prefix/suffix the headers/footers of a page’s Markdown with a string. This allows control of how headers/footers are displayed in the Markdown.
It is possible to set them using the following properties:
  * `page_header_prefix` : Allows you to define the prefix to put before the page header
  * `page_header_suffix` : Allows you to define the suffix to put after the page header
  * `page_footer_prefix` : Allows you to define the prefix to put before page footer
  * `page_footer_suffix` :Allows you to define the suffix to put after page footer


Note that headers and footers will not be detected in Fast Mode, so these parameters will have no effect.


```


parser =LlamaParse(




page_header_prefix="[Header]",




page_header_suffix="[/Header]",




page_footer_prefix="[Footer]",




page_footer_suffix="[/Footer]"



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'page_header_prefix=""[Header]"'\




--form'page_header_suffix=""[/Header]"'\




--form'page_footer_prefix=""[Footer]"'\




--form'page_footer_suffix=""[/Footer]"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

With such a query the markdown for a page where header and footer are detected will look like:
```

[Header]


Journal of computer science, April 3 2025 edition


[/Header]



Some content



[Footer]


All right reserved, Corp Inc.


Page 2


[/Footer]

```

## Merge tables across pages in markdown
[Section titled “Merge tables across pages in markdown”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/parsing_options/#merge-tables-across-pages-in-markdown)
When set to true, LlamaParse will try to merge table across pages in the output markdown when it make sense. As a result the markdown will not be paginated, and all footer and headers will be removed.


```


parser =LlamaParse(




merge_tables_across_pages_in_markdown=True



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'merge_tables_across_pages_in_markdown="true"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## Extract out of bounds content in presentation slides
[Section titled “Extract out of bounds content in presentation slides”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/parsing_options/#extract-out-of-bounds-content-in-presentation-slides)
When set to true, for supported presentation formats, LlamaParse will extract out of bounds content from slides. By default, out of bounds content is not extracted.


```


parser =LlamaParse(




presentation_out_of_bounds_content=True



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'presentation_out_of_bounds_content="true"'\




-F'file=@/path/to/your/file.pptx;type=application/vnd.openxmlformats-officedocument.presentationml.presentation'


```

Currently supported formats for out of bounds slide content extraction:
  * `.pptx` (PowerPoint 2007+)


