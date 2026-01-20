[Skip to content](https://developers.llamaindex.ai/python/cloud/llamaextract/features/options/#_top)
# Configuration Options
When creating a new Extraction Agent, the _schema_ is the most important part. However, there are a few other options that can significantly impact the extraction process.
## Schema Alignment and Extraction Target
[Section titled “Schema Alignment and Extraction Target”](https://developers.llamaindex.ai/python/cloud/llamaextract/features/options/#schema-alignment-and-extraction-target)
These options determine how your schema is applied to the document:
  * **Extraction Target** : Determines the scope and granularity of extraction. Available options:
    * `PER_DOC` (default): Schema is applied to the entire document, returns a single JSON object
    * `PER_PAGE`: Schema is applied to each page independently, returns an array of JSON objects (one per page)
    * `PER_TABLE_ROW`: Schema is applied to each entity in an ordered list (table rows, bulleted lists, etc.), returns an array of JSON objects (one per entity)
See the [Core Concepts](https://developers.llamaindex.ai/python/cloud/llamaextract/features/concepts#extraction-target) page for detailed guidance on when to use each mode.


## Important Settings
[Section titled “Important Settings”](https://developers.llamaindex.ai/python/cloud/llamaextract/features/options/#important-settings)
### Model Settings
[Section titled “Model Settings”](https://developers.llamaindex.ai/python/cloud/llamaextract/features/options/#model-settings)
  * **Extraction Mode** : The mode of extraction to use. Can be either `FAST`, `BALANCED`, `MULTIMODAL`, or `PREMIUM`. The default is `MULTIMODAL`. `FAST` mode is suitable for simple documents with OCR but no AI-based parsing - it is the fastest mode. `BALANCED` mode provides a good balance between speed and accuracy for most documents. `MULTIMODAL` mode (default) is suitable for visually rich documents with a mix of text, simple tables, and images. `PREMIUM` mode should be used for extracting data from complex tables and information-dense documents - it provides the highest accuracy with advanced OCR, complex table/header and layout detection.
  * **Parse Model** : The model to use for document parsing. If not provided, uses the default for the extraction mode. Parse models are only configurable in `MULTIMODAL` and `PREMIUM` modes. See table below for available models per mode.
  * **Extract Model** : The model to use for data extraction. If not provided, uses the default for the extraction mode. Extract models are only configurable in `PREMIUM` mode. See table below for available models.


#### Available Models by Extraction Mode
[Section titled “Available Models by Extraction Mode”](https://developers.llamaindex.ai/python/cloud/llamaextract/features/options/#available-models-by-extraction-mode)
Extraction Mode | Model Type | Models Available | Additional Credits | Description | Default  
---|---|---|---|---|---  
**FAST** | - | _Not configurable_  
**BALANCED** | - | _Not configurable_  
**MULTIMODAL** | _Parse Model_ | `gemini-2.0-flash` | None | Fast processing on medium complexity documents without dense tables | ✓  
`gemini-2.5-flash-lite` | None | Fast and small model similar to Gemini 2.0 Flash  
`gemini-2.5-flash` | +15 cred. / page | Successor to Gemini 2.0 Flash with improved performance  
`openai-gpt-4-1` | +25 cred. | -  
`gemini-2.5-pro` | +55 cred. | Ideal for visually complex documents  
_Extract Model_ | _Not configurable_  
**PREMIUM** | _Parse Model_ | `gemini-2.5-pro` | None | Ideal for visually complex documents, dense tables etc.  
`openai-gpt-4-1` | None | -  
`anthropic-haiku-4.5` | +25 cred. / page | Ideal for visually complex documents | ✓  
`anthropic-sonnet-4.5` | +45 cred. / page | High-performance parsing for complex layouts  
_Extract Model_ | `openai-gpt-4-1` | None | - | ✓  
`openai-gpt-5-mini` | None | Longer context retention and reasoning  
`openai-gpt-5` | +30 cred. | Longer context retention and reasoning (++)  
### System Prompt
[Section titled “System Prompt”](https://developers.llamaindex.ai/python/cloud/llamaextract/features/options/#system-prompt)
  * **System Prompt** : Any additional system level instructions for the extraction agent. Note that you should use the schema descriptions to pass field-level instructions, few-shot examples, formatting instructions, etc.


### Page Range and Context Window
[Section titled “Page Range and Context Window”](https://developers.llamaindex.ai/python/cloud/llamaextract/features/options/#page-range-and-context-window)
  * **Page Range** : Specify which pages to extract from by providing comma-separated page numbers or ranges (1-based indexing). For example, use `1,3,5-7,9` to extract pages 1, 3, pages 5 through 7, and page 9. You can also use ranges like `1-3,8-10` to extract the first three pages and pages 8 through 10. Page numbers are 1-based, meaning the first page is page 1. This option is useful when you only need to extract data from specific sections of large documents.
  * **Context Window** : Number of pages to pass as context for long document extraction. This is useful when extracting from large documents where you need context from surrounding pages. Use the `ExtractConfig.num_pages_context` argument from the SDK to configure this option. Larger values keep more of the surrounding document intact, which helps when you need to see multi-page tables or invoices in one pass. Smaller values advance through the file more aggressively and are better when you need exhaustive coverage of dense lists.


## Metadata Extensions
[Section titled “Metadata Extensions”](https://developers.llamaindex.ai/python/cloud/llamaextract/features/options/#metadata-extensions)
For additional extraction features that provide enhanced metadata and insights, see the [**Metadata Extensions**](https://developers.llamaindex.ai/python/cloud/llamaextract/features/extensions) page which covers:
  * **Citations** : Source tracing for extracted fields
  * **Reasoning** : Explanations for extraction decisions
  * **Confidence Scores** : Quantitative confidence measures


These extensions return additional metadata in the `extraction_metadata` field but may impact processing time.
## Other Advanced Options
[Section titled “Other Advanced Options”](https://developers.llamaindex.ai/python/cloud/llamaextract/features/options/#other-advanced-options)
These features are currently available under `Advanced Settings` in the UI.
  * **Chunk Mode** : Controls how the document is split for processing when dealing with large documents that exceed context limits. Choose between:
    * `PAGE`: Each page becomes a separate chunk for processing (default)
    * `SECTION`: Document is split into semantic sections based on content structure like headers and natural boundaries Use the `ExtractConfig.chunk_mode` argument from the SDK to configure this option.
  * **High Resolution Mode** : Enable high resolution processing for better accuracy on small text and fine details. This option improves OCR quality and uses higher resolution for document pages. Use the `ExtractConfig.high_resolution_mode` argument from the SDK to enable this feature. **Warning: This can slow down extraction processing time, use only when needed.**
  * **Invalidate Cache** : Purge cached results and rerun the full extraction. By default, LlamaExtract caches parsing results for 48 hours. Enable this option to bypass the cache and ensure fresh processing, which will incur fresh billing charges. Use the `ExtractConfig.invalidate_cache` argument from the SDK to enable cache invalidation.


## Setting Configuration Options
[Section titled “Setting Configuration Options”](https://developers.llamaindex.ai/python/cloud/llamaextract/features/options/#setting-configuration-options)
You can configure these options when creating an extraction agent using either the REST API or Python SDK.
### Python SDK
[Section titled “Python SDK”](https://developers.llamaindex.ai/python/cloud/llamaextract/features/options/#python-sdk)
First, install the Python SDK:
Terminal window```


pipinstallllama-cloud-services


```

Here’s how to set various configuration options:
```


from llama_cloud_services import LlamaExtract




from llama_cloud import ExtractConfig, ExtractMode, ChunkMode, ExtractTarget




# Initialize the client



extract =LlamaExtract(api_key="YOUR_API_KEY")




# Define your schema



schema = {




"type": "object",




"properties": {




"company_name": {"type": "string", "description": "Name of the company"},




"revenue": {"type": "number", "description": "Annual revenue in USD"}






# Create extraction configuration



config =ExtractConfig(




# Schema alignment




extraction_target=ExtractTarget.PER_DOC,# PER_DOC, PER_PAGE





# Model settings




extraction_mode=ExtractMode.MULTIMODAL,# FAST, BALANCED, MULTIMODAL, PREMIUM




parse_model=None,# Optional: override parse model




extract_model=None,# Optional: override extract model





# System prompt




system_prompt="Focus on the most recent financial data",





# Page range and context




page_range="1-5,10-15",# Extract from specific pages




num_pages_context=3,# Number of context pages for long docs





# Metadata extensions (see Metadata Extensions page for details)




cite_sources=True,# Enable citations




use_reasoning=True,# Enable reasoning (not available in FAST mode)




confidence_scores=True,# Enable confidence scores (MULTIMODAL/PREMIUM only)





# Advanced options




chunk_mode=ChunkMode.PAGE,# PAGE, SECTION




high_resolution_mode=True,# Enable for better OCR




invalidate_cache=False,# Set to True to bypass cache





# Create extraction agent with configuration



agent = extract.create_agent(




name="Financial Data Extractor",




data_schema=schema,




config=config





# Extract from a document



result = agent.extract("your-document.pdf")




print(result.data)


```

### REST API
[Section titled “REST API”](https://developers.llamaindex.ai/python/cloud/llamaextract/features/options/#rest-api)
You can also configure these options using the REST API when creating an extraction agent:
Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/extraction/extraction-agents'\




-H'accept: application/json'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




-H'Content-Type: application/json'\





"name": "Financial Data Extractor",




"data_schema": {




"type": "object",




"properties": {




"company_name": {"type": "string", "description": "Name of the company"},




"revenue": {"type": "number", "description": "Annual revenue in USD"}






"config": {




"extraction_target": "PER_DOC",




"extraction_mode": "MULTIMODAL",




"parse_model": null,




"extract_model": null,




"system_prompt": "Focus on the most recent financial data",




"page_range": "1-5,10-15",




"num_pages_context": 3,




"cite_sources": true,




"use_reasoning": true,




"confidence_scores": true,




"chunk_mode": "PAGE",




"high_resolution_mode": true,




"invalidate_cache": false




```

### Configuration Reference
[Section titled “Configuration Reference”](https://developers.llamaindex.ai/python/cloud/llamaextract/features/options/#configuration-reference)
Option | Type | Default | Description  
---|---|---|---  
**Schema Alignment**  
`extraction_target` | string | `"PER_DOC"` | Extraction scope: `PER_DOC`, `PER_PAGE`, `PER_TABLE_ROW`  
**Model Settings**  
`extraction_mode` | string | `"MULTIMODAL"` | Processing mode: `FAST`, `BALANCED`, `MULTIMODAL` (default), `PREMIUM`  
`parse_model` | string | `null` | Parse model override (optional)  
`extract_model` | string | `null` | Extract model override (optional)  
**System Prompt**  
`system_prompt` | string | `null` | Additional system-level instructions  
**Page Range and Context**  
`page_range` | string | `null` | Page numbers/ranges to extract (1-based, e.g., "1,3,5-7")  
`num_pages_context` | integer | `null` | Number of pages to pass as context for long documents  
**Metadata Extensions**  
`cite_sources` | boolean | `false` | Enable source citations  
`use_reasoning` | boolean | `false` | Enable extraction reasoning (not available in FAST mode)  
`confidence_scores` | boolean | `false` | Enable confidence scores (MULTIMODAL/PREMIUM only)  
**Advanced Options**  
`chunk_mode` | string | `"PAGE"` | Document chunking strategy: `PAGE`, `SECTION`  
`high_resolution_mode` | boolean | `false` | Enable high-resolution processing  
`invalidate_cache` | boolean | `false` | Bypass cached results  
**Note** : Some options like `confidence_scores` are only available in specific extraction modes. See the individual option descriptions above for details.
