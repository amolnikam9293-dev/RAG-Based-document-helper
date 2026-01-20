[Skip to content](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#_top)
# LlamaParse API v2 Guide
This comprehensive guide covers the new v2 API endpoint for LlamaParse, which introduces a structured configuration approach for better organization and validation.
> ⚠️ **Alpha Version Warning** : The v2 endpoint is currently in alpha (`v2alpha1`) and is subject to breaking changes until the stable release. We recommend testing thoroughly and being prepared for potential API changes during development.
## Quick Start
[Section titled “Quick Start”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#quick-start)
### Basic Usage
[Section titled “Basic Usage”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#basic-usage)
**File ID Parsing (recommended):**
Terminal window```


curl-XPOST\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




-H"Content-Type: application/json"\





"file_id": "existing-file-id",




"parse_options": {




"tier": "agentic",




"version": "latest"






"https://api.cloud.llamaindex.ai/api/v2alpha1/parse"


```

**URL Parsing:**
Terminal window```


curl-XPOST\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




-H"Content-Type: application/json"\





"source_url": "https://example.com/document.pdf",




"parse_options": {




"tier": "cost_effective",




"version": "latest"






"https://api.cloud.llamaindex.ai/api/v2alpha1/parse/url"


```

**Multipart File Upload:**
Terminal window```


curl-XPOST\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




-F"file=@document.pdf"\




-F'configuration={




"parse_options": {




"tier": "fast",




"version": "latest"






"https://api.cloud.llamaindex.ai/api/v2alpha1/parse/upload"


```

### What’s Different from v1
[Section titled “What’s Different from v1”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#whats-different-from-v1)
  * **Tier-based** : Instead of parse modes, choose from LlamaParse tiers (`fast`, `cost_effective`, `agentic`, `agentic_plus`)
  * **Specialized endpoints** : Three separate endpoints for different input methods (`/`, `/url`, `/upload`)
  * **Better validation** : Structured JSON schema with clear error messages
  * **Hierarchical organization** : Related settings are grouped logically


## Endpoint Details
[Section titled “Endpoint Details”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#endpoint-details)
v2 provides three specialized endpoints for different input methods:
### File ID Parsing (Recommended)
[Section titled “File ID Parsing (Recommended)”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#file-id-parsing-recommended)
  * **URL** : `https://api.cloud.llamaindex.ai/api/v2alpha1/parse`
  * **Method** : `POST`
  * **Content-Type** : `application/json`
  * **Use case** : Parse an already uploaded file


### URL Parsing
[Section titled “URL Parsing”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#url-parsing)
  * **URL** : `https://api.cloud.llamaindex.ai/api/v2alpha1/parse/url`
  * **Method** : `POST`
  * **Content-Type** : `application/json`
  * **Use case** : Parsing documents directly from web URLs


### Multipart File Upload
[Section titled “Multipart File Upload”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#multipart-file-upload)
  * **URL** : `https://api.cloud.llamaindex.ai/api/v2alpha1/parse/upload`
  * **Method** : `POST`
  * **Content-Type** : `multipart/form-data`
  * **Use case** : Traditional file uploads from client applications


**Required Headers** : `Authorization: Bearer YOUR_API_KEY` (all endpoints)
## Choosing the Right Endpoint
[Section titled “Choosing the Right Endpoint”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#choosing-the-right-endpoint)
Select the appropriate endpoint based on your use case:
Endpoint | Use When | Input Method | Content-Type  
---|---|---|---  
**Recommended** : Parse an already uploaded file | File ID reference | `application/json`  
`/url` | Parsing documents directly from web URLs, shared links, or public documents | URL reference | `application/json`  
`/upload` | Uploading new files from client applications, web forms, or file pickers | Multipart form data | `multipart/form-data`  
**Key Differences:**
  * **URL fields** : Only the `/url` endpoint accepts `source_url` and `http_proxy` fields
  * **File handling** : `/upload` uses traditional file uploads, `/` references existing files, `/url` fetches remotely
  * **Configuration location** : `/upload` uses form data with a `configuration` parameter, others embed configuration in the JSON body


## Configuration Structure
[Section titled “Configuration Structure”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#configuration-structure)
The configuration structure varies by endpoint, with each endpoint accepting only the parameters relevant to its input method:
### File ID Parsing (`/`) - Recommended
[Section titled “File ID Parsing (/) - Recommended”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#file-id-parsing----recommended)
**JSON Request Body:**
```



"file_id": "existing-file-id (required)",




"parse_options": {




"tier": "fast|cost_effective|agentic|agentic_plus",




"version": "latest|2025-12-11",




// Tier-specific options





"webhook_configurations": [...],




"input_options": {...},




"crop_box": {...},




"page_ranges": {...},




"disable_cache": "boolean (optional)",




"output_options": {...},




"processing_control": {...}



```

### URL Parsing (`/url`)
[Section titled “URL Parsing (/url)”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#url-parsing-url)
**JSON Request Body:**
```



"source_url": "https://example.com/document.pdf (required)",




"http_proxy": "https://proxy.example.com (optional)",




"parse_options": {




"tier": "fast|cost_effective|agentic|agentic_plus",




"version": "latest|2025-12-11",




// Tier-specific options





"webhook_configurations": [...],




"input_options": {...},




"crop_box": {...},




"page_ranges": {...},




"disable_cache": "boolean (optional)",




"output_options": {...},




"processing_control": {...}



```

### Multipart Upload (`/upload`)
[Section titled “Multipart Upload (/upload)”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#multipart-upload-upload)
**Form Parameters:**
  * `file` (required): The document file to upload
  * `configuration` (required): JSON string containing parsing options


**Configuration JSON Structure:**
```



"parse_options": {




"tier": "fast|cost_effective|agentic|agentic_plus",




"version": "latest|2025-12-11",




// Tier-specific options





"webhook_configurations": [...],




"input_options": {...},




"crop_box": {...},




"page_ranges": {...},




"disable_cache": "boolean (optional)",




"output_options": {...},




"processing_control": {...}



```

## Tier-Based Parsing
[Section titled “Tier-Based Parsing”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#tier-based-parsing)
The new v2 API uses a simplified tier-based system instead of complex parse modes. The `tier` field determines how your document is processed, with automatic model selection and optimized settings for each tier.
### Agentic Plus Tier (`"agentic_plus"`)
[Section titled “Agentic Plus Tier ("agentic_plus")”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#agentic-plus-tier-agentic_plus)
**Best for** : Most complex documents requiring maximum accuracy (financial reports, dense layouts, scientific papers).
**Available Versions** :
  * `"latest"` - Always uses the most recent stable version
  * `"2025-12-11"` - Specific version for reproducible results
  * `"2025-12-18"` - Specific version for reproducible results
  * `"2025-12-31"` - Specific version for reproducible results


**Configuration example** :
```



"parse_options": {




"tier": "agentic_plus",




"version": "latest",




"agentic_options": {




"ignore": {




"ignore_diagonal_text": true,





"ocr_parameters": {




"languages": ["en", "fr"]






```

### Agentic Tier (`"agentic"`)
[Section titled “Agentic Tier ("agentic")”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#agentic-tier-agentic)
**Best for** : Complex documents requiring high accuracy with intelligent reasoning.
**Available Versions** :
  * `"latest"` - Always uses the most recent stable version
  * `"2025-12-11"` - Specific version for reproducible results
  * `"2025-12-18"` - Specific version for reproducible results
  * `"2025-12-31"` - Specific version for reproducible results
  * `"2026-01-08"` - Specific version for reproducible results


**Configuration example** :
```



"parse_options": {




"tier": "agentic",




"version": "latest",




"agentic_options": {




"ignore": {




"ignore_diagonal_text": true





"ocr_parameters": {




"languages": ["en"]






```

### Cost Effective Tier (`"cost_effective"`)
[Section titled “Cost Effective Tier ("cost_effective")”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#cost-effective-tier-cost_effective)
**Best for** : Documents with mixed content requiring structured output while maintaining cost efficiency.
**Available Versions** :
  * `"latest"` - Always uses the most recent stable version
  * `"2025-12-11"` - Specific version for reproducible results
  * `"2025-12-18"` - Specific version for reproducible results
  * `"2025-12-31"` - Specific version for reproducible results


**Configuration example** :
```



"parse_options": {




"tier": "cost_effective",




"version": "2025-12-11",




"agentic_options": {




"ignore": {




"ignore_diagonal_text": true,





"ocr_parameters": {




"languages": ["en", "fr"]






```

### Fast Tier (`"fast"`)
[Section titled “Fast Tier ("fast")”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#fast-tier-fast)
**Best for** : Quick text extraction from simple documents where speed is prioritized over advanced formatting.
**Available Versions** :
  * `"latest"` - Always uses the most recent stable version
  * `"2025-12-11"` - Specific version for reproducible results


**Configuration example** :
```



"parse_options": {




"tier": "fast",




"version": "latest",




"fast_options": {




"ignore": {




"ignore_diagonal_text": true,





"ocr_parameters": {




"languages": ["de"]






```

## Input Options
[Section titled “Input Options”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#input-options)
Configure how different file types are processed:
```



"input_options": {




"html": {




"make_all_elements_visible": true,




"remove_fixed_elements": true,




"remove_navigation_elements": true





"spreadsheet": {




"detect_sub_tables_in_sheets": true,




"force_formula_computation_in_sheets": true





"presentation": {




"out_of_bounds_content": true,





```

### HTML Options
[Section titled “HTML Options”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#html-options)
  * `make_all_elements_visible`: Forces hidden elements to be visible during parsing
  * `remove_fixed_elements`: Removes fixed-position elements (headers, sidebars)
  * `remove_navigation_elements`: Removes navigation menus


### Spreadsheet Options
[Section titled “Spreadsheet Options”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#spreadsheet-options)
  * `detect_sub_tables_in_sheets`: Find and extract sub-tables within spreadsheet cells
  * `force_formula_computation_in_sheets`: Force re-computation of spreadsheet cells containing formulas


### Presentation Options
[Section titled “Presentation Options”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#presentation-options)
  * `out_of_bounds_content`: Extract out of bounds content in presentation slides


## Page Ranges
[Section titled “Page Ranges”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#page-ranges)
Control which pages to process:
```



"page_ranges": {




"max_pages": 10,




"target_pages": "1,3,5-10"




```

  * `max_pages`: Maximum number of pages to process
  * `target_pages`: Specific pages using **1-based indexing** (e.g., “1,3,5-10” for pages 1, 3, and 5 through 10)


> **Important** : v2 uses 1-based page indexing, unlike v1 which used 0-based indexing.
## Crop Box
[Section titled “Crop Box”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#crop-box)
Define a specific area of each page to parse:
```



"crop_box": {




"top": 0.1,




"right": 0.1,




"bottom": 0.1,




"left": 0.1




```

Values are ratios (0.0 to 1.0) of the page dimensions. Example above crops 10% margin on all sides.
## Output Options
[Section titled “Output Options”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#output-options)
Customize the output format and structure:
### Markdown Options
[Section titled “Markdown Options”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#markdown-options)
```



"output_options": {




"markdown": {




"annotate_links": true,




"pages": {




"merge_tables_across_pages_in_markdown": false,





"tables": {




"compact_markdown_tables": false,




"output_tables_as_markdown": false,




"markdown_table_multiline_separator": ""






```

### Spatial Text Options
[Section titled “Spatial Text Options”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#spatial-text-options)
```



"output_options": {




"spatial_text": {




"preserve_layout_alignment_across_pages": true,




"preserve_very_small_text": false,




"do_not_unroll_columns": false





```

### Export Options
[Section titled “Export Options”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#export-options)
```



"output_options": {




"tables_as_spreadsheet": {




"enable": true




// Note: guess_sheet_name is always true in v2





"embedded_images": {




"enable": true





"screenshots": {




"enable": true





"export_pdf": {




"enable": false





```

## Webhook Configuration
[Section titled “Webhook Configuration”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#webhook-configuration)
Set up notifications for job completion:
```



"webhook_configurations": [





"webhook_url": "https://your-app.com/webhook",




"webhook_headers": {




"X-Custom-Header": "value"





"webhook_events": ["parse.done"]





```

> **Note** : Currently only the first webhook configuration is used.
## Processing Control
[Section titled “Processing Control”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#processing-control)
Configure timeouts and error handling:
```



"processing_control": {




"timeouts": {




"base_in_seconds": 300,




"extra_time_per_page_in_seconds": 30





"job_failure_conditions": {




"allowed_page_failure_ratio": 0.1,




"fail_on_image_extraction_error": false,




"fail_on_image_ocr_error": false,




"fail_on_markdown_reconstruction_error": true,




"fail_on_buggy_font": false





```

## Cache Control
[Section titled “Cache Control”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#cache-control)
Disable caching for fresh results:
```



"disable_cache": true



```

When `true`, this both invalidates any existing cache and prevents caching of new results.
## Always-Enabled Features
[Section titled “Always-Enabled Features”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#always-enabled-features)
The following features are **always enabled** in v2 across all tiers and cannot be disabled:
  * `adaptive_long_table`: Adaptive long table detection
  * `high_res_ocr`: High-resolution OCR processing
  * `merge_tables_across_pages_in_markdown`: Table merging across pages
  * `outlined_table_extraction`: Outlined table extraction
  * `guess_sheet_name`: Automatic sheet naming for spreadsheet exports


These were made default because they improve results for most documents and simplify the API.
## Complete Configuration Examples
[Section titled “Complete Configuration Examples”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#complete-configuration-examples)
### File ID Parsing Example (Recommended)
[Section titled “File ID Parsing Example (Recommended)”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#file-id-parsing-example-recommended)
Terminal window```


curl-XPOST\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




-H"Content-Type: application/json"\





"file_id": "existing-file-id",




"parse_options": {




"tier": "agentic_plus",




"version": "latest",




"agentic_options": {




"ignore": {




"ignore_diagonal_text": true,




"ignore_text_in_image": false





"ocr_parameters": {




"languages": ["en", "es"]







"page_ranges": {




"max_pages": 20,




"target_pages": "1-5,10,15-20"





"crop_box": {




"top": 0.05,




"bottom": 0.95,




"left": 0.05,




"right": 0.95





"output_options": {




"markdown": {




"annotate_links": true,




"tables": {




"output_tables_as_markdown": true






"screenshots": {




"enable": true






"webhook_configurations": [





"webhook_url": "https://example.com",




"webhook_events": ["parse.done"]






"processing_control": {




"timeouts": {




"base_in_seconds": 600





"job_failure_conditions": {




"allowed_page_failure_ratio": 0.05






"disable_cache": false





"https://api.cloud.llamaindex.ai/api/v2alpha1/parse"


```

### URL Parsing Example
[Section titled “URL Parsing Example”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#url-parsing-example)
Terminal window```


curl-XPOST\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




-H"Content-Type: application/json"\





"source_url": "https://example.com/report.pdf",




"http_proxy": "https://proxy.example.com",




"parse_options": {




"tier": "cost_effective",




"version": "latest",




"agentic_options": {




"ocr_parameters": {




"languages": ["en"]







"page_ranges": {




"max_pages": 20





"output_options": {




"webhook_configurations": [{




"webhook_url": "https://example.com/webhook",




"webhook_events": ["parse.done"]






"https://api.cloud.llamaindex.ai/api/v2alpha1/parse/url"


```

### Multipart Upload Example
[Section titled “Multipart Upload Example”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#multipart-upload-example)
Terminal window```


curl-XPOST\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




-F"file=@document.pdf"\




-F'configuration={




"parse_options": {




"tier": "agentic",




"version": "latest",




"agentic_options": {




"ignore": {




"ignore_diagonal_text": true,




"ignore_text_in_image": false





"ocr_parameters": {




"languages": ["en", "es"]







"page_ranges": {




"max_pages": 20,




"target_pages": "1-5,10,15-20"





"crop_box": {




"top": 0.05,




"bottom": 0.95,




"left": 0.05,




"right": 0.95





"output_options": {




"markdown": {




"annotate_links": true,




"tables": {




"output_tables_as_markdown": true






"screenshots": {




"enable": true






"webhook_configurations": [





"webhook_url": "https://example.com/webhook",




"webhook_events": ["parse.done"]






"processing_control": {




"timeouts": {




"base_in_seconds": 600





"job_failure_conditions": {




"allowed_page_failure_ratio": 0.05






"disable_cache": false





"https://api.cloud.llamaindex.ai/api/v2alpha1/parse/upload"


```

### File ID Parsing Example
[Section titled “File ID Parsing Example”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#file-id-parsing-example)
Terminal window```


curl-XPOST\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




-H"Content-Type: application/json"\





"file_id": "existing-file-id",




"parse_options": {




"tier": "agentic_plus",




"version": "latest"





"output_options": {




"markdown": {




"annotate_links": true







"https://api.cloud.llamaindex.ai/api/v2alpha1/parse"


```

## Error Handling
[Section titled “Error Handling”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#error-handling)
v2 provides detailed validation errors:
```



"detail": [





"type": "value_error",




"loc": ["parse_options", "tier"],




"msg": "Unsupported tier: invalid_tier. Must be one of: fast, cost_effective, agentic, agentic_plus",




"input": {...}





```

## Response Format
[Section titled “Response Format”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#response-format)
The response structure remains the same as v1, returning a `ParsingJob` object with job details and status.
## Migration from v1
[Section titled “Migration from v1”](https://developers.llamaindex.ai/python/cloud/llamaparse/api-v2-guide/#migration-from-v1)
If you’re migrating from v1, see our [detailed migration guide](https://developers.llamaindex.ai/python/cloud/llamaparse/migration-v1-to-v2/) for parameter mapping and breaking changes.
