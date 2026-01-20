[Skip to content](https://developers.llamaindex.ai/python/cloud/llamaparse/features/parsing_instructions/#_top)
# Parsing instructions (deprecated)
Parsing instruction still work by are deprecated. Use [Prompts](https://developers.llamaindex.ai/python/cloud/llamaparse/features/prompts) instead.
LlamaParse can use LLMs under the hood, allowing you to give it natural-language instructions about what it’s parsing and how to parse. This is an incredibly powerful feature!
We support 3 different types of instruction, that can be used in combination of each other (it is possible to set all 3 of them)
## content_guideline_instruction (deprecated)
[Section titled “content_guideline_instruction (deprecated)”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/parsing_instructions/#content_guideline_instruction-deprecated)
If you want to change / transform the content with LlamaParse, you should use `content_guideline_instruction`.


```


parser =LlamaParse(




content_guideline_instruction="If output is not in english, translate it in english."



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'>content_guideline_instruction="If output is not in english, translate it in english."'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## complemental_formatting_instruction (deprecated)
[Section titled “complemental_formatting_instruction (deprecated)”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/parsing_instructions/#complemental_formatting_instruction-deprecated)
If you need to change the way LlamaParse format the output document in some way, and want to keep the markdown output formatting, you should use `complemental_formatting_instruction`. Doing so will not override our formatting system, and will allow you to improve on our formatting.


```


parser =LlamaParse(




complemental_formatting_instruction="For headings, do not output level 1 heading, start at level 2 (##)"



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'complemental_formatting_instruction="For headings, do not output level 1 heading, start at level 2 (##)"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## formatting_instruction (deprecated)
[Section titled “formatting_instruction (deprecated)”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/parsing_instructions/#formatting_instruction-deprecated)
This allow you to override any formatting instruction done by llamaParse. If you do not want the model to output Markdown and want to output something else, use it. However be mindful that it is easy to degrade LlamaParse performances with `formating_instruction` as this override our formatting and formatting correction (like table extractions).


```


parser =LlamaParse(




formatting_instruction="Output the document as a Latex page. For table use HTML"



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'formatting_instruction="Output the document as a Latex page. For table use HTML"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

