[Skip to content](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/advance_parsing_modes/#_top)
# Advanced Parsing Modes
LlamaParse leverage Large Language Models (LLM) and Large Vision Models (LVM) to parse documents. By setting `parse_mode` it is possible to control of the parsing method used.
## Parse without AI
[Section titled “Parse without AI”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/advance_parsing_modes/#parse-without-ai)
Simple, text-only documents (aka Fast Mode)
#### Overview
[Section titled “Overview”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/advance_parsing_modes/#overview)
Parse without AI is the fastest way to extract plain text from documents. It’s ideal for PDFs that don’t require structure or formatting—just clean, raw content.
#### Under the Hood
[Section titled “Under the Hood”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/advance_parsing_modes/#under-the-hood)
This mode skips all AI-based reconstruction steps and does not use an LLM or LVM. Only layered text is extracted—no markdown is returned.
By default, it still performs OCR and image extraction to catch any non-layered content. However, you can disable both using `disable_ocr=True` and `disable_image_extraction=True` to maximize speed. This is equivalent to `fast_mode=True`.
To use this mode, set `parse_mode="parse_page_without_llm"`.


```


parser =LlamaParse(




parse_mode="parse_page_without_llm"



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'parse_mode="parse_page_without_llm"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## Parse with LLM
[Section titled “Parse with LLM”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/advance_parsing_modes/#parse-with-llm)
Documents with tables and images (aka Balanced Mode)
#### Overview
[Section titled “Overview”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/advance_parsing_modes/#overview-1)
Parse with LLM is the default parsing mode. It’s well-suited for documents that mix text with images, tables, and layout—like research papers or reports. No configuration is required to use it.
#### Under the Hood
[Section titled “Under the Hood”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/advance_parsing_modes/#under-the-hood-1)
This mode performs OCR, image extraction, and structural analysis. LlamaParse first extracts layered text from the page, then uses a Large Language Model to reconstruct the document layout and structure, producing a clean markdown output.
Documents are processed one page at a time, offering a balance of accuracy and cost-efficiency. The model is not configurable.
To use this mode explicitly, set `parse_mode="parse_page_with_llm"`.


```


parser =LlamaParse(




parse_mode="parse_page_with_llm"



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'parse_mode="parse_page_with_llm"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## Parse with LVM
[Section titled “Parse with LVM”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/advance_parsing_modes/#parse-with-lvm)
Best for rich visual content
#### Overview
[Section titled “Overview”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/advance_parsing_modes/#overview-2)
Parse with LVM is designed for visually complex documents like diagrams, charts, or design-heavy reports. It uses a vision model to interpret page images, returning only Markdown or structured JSON—no plain text.
#### Under the Hood
[Section titled “Under the Hood”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/advance_parsing_modes/#under-the-hood-2)
This mode transforms each page into an image and sends it to a Large Vision Model (LVM) for parsing. It does not extract layered text and does not return raw text output. Instead, the model produces structured markdown or JSON directly.
Equivalent to setting `use_vendor_multimodal_model=True`. The default model is `openai-gpt4o`, but you can specify others with `vendor_multimodal_model_name=<model_name>`.
Model | Model string  
---|---  
Open AI Gpt4o (Default) | `openai-gpt4o`  
Open AI Gpt4o Mini | `openai-gpt-4o-mini`  
OpenAI GPT-4.1 Nano | `openai-gpt-4-1-nano`  
OpenAI GPT-4.1 Mini | `openai-gpt-4-1-mini`  
OpenAI GPT-4.1 | `openai-gpt-4-1`  
Sonnet 3.5 (deprecated) | `anthropic-sonnet-3.5`  
Sonnet 3.7 | `anthropic-sonnet-3.7`  
Sonnet 4.0 | `anthropic-sonnet-4.0`  
Sonnet 4.5 (Preview) | `anthropic-sonnet-4.5`  
Haiku 4.5 (Preview) | `anthropic-haiku-4.5`  
Gemini 2.0 Flash | `gemini-2.0-flash`  
Gemini 2.5 Flash | `gemini-2.5-flash`  
Gemini 2.5 Pro | `gemini-2.5-pro`  
Gemini 1.5 Flash (discountinued) | `gemini-1.5-flash`  
Gemini 1.5 Pro (discountinued) | `gemini-1.5-pro`  
Custom Azure Model | `custom-azure-model`  
See [Multimodal](https://developers.llamaindex.ai/python/cloud/llamaparse/features/multimodal/) for more info.
To use this mode, set `parse_mode="parse_page_with_lvm"`.


```


parser =LlamaParse(




parse_mode="parse_page_with_lvm"



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'parse_mode="parse_page_with_lvm"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## Parse with Agent
[Section titled “Parse with Agent”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/advance_parsing_modes/#parse-with-agent)
Complex documents with tables and images (aka Premium Mode)
#### Overview
[Section titled “Overview”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/advance_parsing_modes/#overview-3)
Parse with Agent is our highest-performing mode, ideal for complex documents like financial reports, scanned forms, and visually dense layouts. It’s designed to extract structured content—including equations and diagrams—with maximum accuracy.
#### Under the Hood
[Section titled “Under the Hood”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/advance_parsing_modes/#under-the-hood-3)
This mode combines OCR, image extraction, and an agentic reasoning loop to deliver the most structured output possible. For each page, LlamaParse extracts layered text and a screenshot. Both are then passed to a Large Language Model and/or Large Vision Model through an agentic process to reconstruct layout and structure.
The output is high-fidelity markdown, including support for LaTeX-formatted equations and Mermaid-formatted diagrams.
This mode processes documents page by page. Equivalent to setting `premium_mode=True`.
To use this mode, set `parse_mode="parse_page_with_agent"`.


```


parser =LlamaParse(




parse_mode="parse_page_with_agent"



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'parse_mode="parse_page_with_agent"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## Parse with Layout Agent
[Section titled “Parse with Layout Agent”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/advance_parsing_modes/#parse-with-layout-agent)
Best for precise visual citations
#### Overview
[Section titled “Overview”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/advance_parsing_modes/#overview-4)
Parse with Layout Agent is optimized for layout-awareness, making it ideal when you need to preserve exact positioning—such as for visual citations, dense layouts, or precise text structure.
#### Under the Hood
[Section titled “Under the Hood”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/advance_parsing_modes/#under-the-hood-4)
This mode uses a mixture of vision-language models (VLMs) to parse each page while preserving layout fidelity. It supports LaTeX output for equations and Mermaid syntax for diagrams.
Parse with Layout Agent excels at transcribing tables, lists, headings, and body text with high accuracy—especially in dense, newspaper-like documents. Compared to other modes, this mode scales more efficiently as the complexity and density of the page increases.
To use this mode, set `parse_mode="parse_page_with_layout_agent"`.


```


parser =LlamaParse(




parse_mode="parse_page_with_layout_agent"



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'parse_mode="parse_page_with_layout_agent"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## Parse Document with LLM
[Section titled “Parse Document with LLM”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/advance_parsing_modes/#parse-document-with-llm)
Best for continuity between pages
#### Overview
[Section titled “Overview”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/advance_parsing_modes/#overview-5)
Parse Document with LLM is designed for documents where structure and context span across pages—like long tables or multi-section reports. It provides improved coherence by analyzing the document as a whole.
#### Under the Hood
[Section titled “Under the Hood”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/advance_parsing_modes/#under-the-hood-5)
This mode works like Parse Page with LLM but processes the entire document at once rather than page by page. By doing so, it ensures consistent heading hierarchy, better section continuity, and improved handling of tables that span multiple pages.
The model performs OCR, image extraction, and structure identification in a document-aware fashion. The output combines all content into a single response.
To use this mode, set `parse_mode="parse_document_with_llm"`.


```


parser =LlamaParse(




parse_mode="parse_document_with_llm"



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'parse_mode="parse_document_with_llm"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## Parse Document with Agent
[Section titled “Parse Document with Agent”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/advance_parsing_modes/#parse-document-with-agent)
Best for complex continuity between pages
#### Overview
[Section titled “Overview”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/advance_parsing_modes/#overview-6)
Parse Document with Agent is built for the most complex documents—those with dense layouts, long tables, or visual elements that span multiple pages. It maintains structural coherence across the entire file.
#### Under the Hood
[Section titled “Under the Hood”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/advance_parsing_modes/#under-the-hood-6)
This mode works like Parse Page with Agent, but instead of processing pages individually, it analyzes the full document in a single pass. This improves continuity in layouts, tables, and images across pages.
LlamaParse combines OCR, image extraction, and an agentic reasoning loop to deliver the most structured output possible. It extracts both layered text and screenshots across the entire document, then feeds them into a Large Language Model and/or Large Vision Model to reconstruct layout and structure.
To use this mode, set `parse_mode="parse_document_with_agent"`.


```


parser =LlamaParse(




parse_mode="parse_document_with_agent"



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'parse_mode="parse_document_with_agent"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## Deprecated Modes
[Section titled “Deprecated Modes”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/advance_parsing_modes/#deprecated-modes)
Depecrated modes - no longer maintained
#### Continuous Mode (Deprecated)
[Section titled “Continuous Mode (Deprecated)”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/advance_parsing_modes/#continuous-mode-deprecated)
Use `parse_mode="parse_document_with_llm"` instead.
