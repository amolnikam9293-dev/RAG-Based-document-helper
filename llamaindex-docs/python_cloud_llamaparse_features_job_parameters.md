[Skip to content](https://developers.llamaindex.ai/python/cloud/llamaparse/features/job_parameters/#_top)
# Job predictability
LlamaParse let you set your own Quality or Time SLA for a given job. This will reject job that do not meet the conditions. It is useful when you know you need the result before a certain date and do not need them after, or to better fine tune the type of job LlamaParse reject.
## Timeouts
[Section titled “Timeouts”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/job_parameters/#timeouts)
By default LlamaParse timeout a job after 30 minutes of parsing (not including time spent waiting in queue).
LlamaParse expose 2 parameters to allow you to let a job expire early `job_timeout_in_seconds` and `job_timeout_extra_time_per_page_in_seconds`
#### job_timeout_in_seconds
[Section titled “job_timeout_in_seconds”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/job_parameters/#job_timeout_in_seconds)
`job_timeout_in_seconds` allow you to specify a timeout for your job, inclusive of time spent in the LlamaParse queue. The timeout counter start as soon as a `job_id` is return after upload of the file to parse is complete. If the job is not complete in time, it will be failed, and it’s status set to `ERROR: "EXPIRED"`.
The minimum value is 2 minutes (120 seconds)


```


parser =LlamaParse(




job_timeout_in_seconds=300



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'job_timeout_in_seconds=300'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

#### job_timeout_extra_time_per_page_in_seconds
[Section titled “job_timeout_extra_time_per_page_in_seconds”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/job_parameters/#job_timeout_extra_time_per_page_in_seconds)
`job_timeout_extra_time_per_page_in_seconds` allow you to allocate more time for `job_timeout_in_seconds` based on the number of pages in the document. It need to be used alongside with `job_timeout_in_seconds`.


```


parser =LlamaParse(




job_timeout_extra_time_per_page_in_seconds=10



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'job_timeout_extra_time_per_page_in_seconds=10'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## Job Quality
[Section titled “Job Quality”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/job_parameters/#job-quality)
A lot of thing can go wrong when parsing document, and LlamaParse will try to address / correct them. By default LlamaParse try to return the most data possible given extraction error to not block downstream process. This can in some case lead to some lower quality result (like a page not extracted as structured in the middle of a document).
If the default behavior of trying to return data at all cost is not the expected one for your application you can use the strict options to force failure of job on some error or warnings.
#### strict_mode_image_extraction
[Section titled “strict_mode_image_extraction”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/job_parameters/#strict_mode_image_extraction)
`strict_mode_image_extraction=true` will force LlamaParse to fail the job if an image can not be extracted from the document. Typical reason why an image extraction will fail are malformed or buggy image embedded in the document.


```


parser =LlamaParse(




strict_mode_image_extraction=true



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'strict_mode_image_extraction=true'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

#### strict_mode_image_ocr
[Section titled “strict_mode_image_ocr”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/job_parameters/#strict_mode_image_ocr)
`strict_mode_image_ocr=true` will force LlamaParse to fail the job if an image can not be extracted OCR from the document. Typical reason why OCR will fail is when image are corrupted, issue with our OCR servers, …


```


parser =LlamaParse(




strict_mode_image_ocr=true



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'strict_mode_image_ocr=true'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

#### strict_mode_reconstruction
[Section titled “strict_mode_reconstruction”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/job_parameters/#strict_mode_reconstruction)
`strict_mode_reconstruction=true` will force LlamaParse to fail the job if it is not able to convert the document to structured markdown. This could happen in case of buggy table, or reconstruction model failing. The default behavior when the reconstruction fail on a page is to return the extracted text instead of the markdown for the page.


```


parser =LlamaParse(




strict_mode_reconstruction=true



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'strict_mode_reconstruction=true'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

#### strict_mode_buggy_font
[Section titled “strict_mode_buggy_font”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/job_parameters/#strict_mode_buggy_font)
`strict_mode_buggy_font=true` will force LlamaParse to fail the job if it is not able to extract a font. PDF in particular can contain really buggy font, and if llamaParse is not able to identify a glyph from a font, this will fail the job.


```


parser =LlamaParse(




strict_mode_buggy_font=true



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'strict_mode_buggy_font=true'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

