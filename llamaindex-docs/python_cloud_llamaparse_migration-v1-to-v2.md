[Skip to content](https://developers.llamaindex.ai/python/cloud/llamaparse/migration-v1-to-v2/#_top)
# Migration Guide: Parse Upload Endpoint v1 to v2
This guide will help you migrate from the v1 Parse upload endpoint to the new v2 endpoint, which introduces a structured configuration approach and improved organization of parsing options.
> ⚠️ **Alpha Version Warning** : The v2 endpoint is currently in alpha (`v2alpha1`) and is subject to breaking changes until the stable release. We recommend testing thoroughly and being prepared for potential API changes during development.
## Overview of Changes
[Section titled “Overview of Changes”](https://developers.llamaindex.ai/python/cloud/llamaparse/migration-v1-to-v2/#overview-of-changes)
The v2 endpoint replaces **individual form parameters** with a **single JSON configuration string** , providing:
  * **Better organization** : Related options are grouped into logical sections
  * **Type safety** : Structured validation with clear schemas
  * **Extensibility** : Easier to add new features without endpoint bloat
  * **Validation** : Better error messages and configuration validation


## Key Differences
[Section titled “Key Differences”](https://developers.llamaindex.ai/python/cloud/llamaparse/migration-v1-to-v2/#key-differences)
### v1 Endpoint
[Section titled “v1 Endpoint”](https://developers.llamaindex.ai/python/cloud/llamaparse/migration-v1-to-v2/#v1-endpoint)
```

POST /api/v1/parsing/upload


Content-Type: multipart/form-data



- 70+ individual form parameters


- Flat parameter structure


- All parameters available regardless of parse mode

```

### v2 Endpoints
[Section titled “v2 Endpoints”](https://developers.llamaindex.ai/python/cloud/llamaparse/migration-v1-to-v2/#v2-endpoints)
```

POST /api/v2alpha1/parse            (existing file by ID)


POST /api/v2alpha1/parse/url        (fetch from URL)


POST /api/v2alpha1/parse/upload     (multipart file upload)



- Specialized endpoints for different input methods


- Single 'configuration' JSON parameter per endpoint


- Hierarchical, structured configuration


- Always-enabled optimizations


- Strict validation with clear error messages

```

## Migration Steps
[Section titled “Migration Steps”](https://developers.llamaindex.ai/python/cloud/llamaparse/migration-v1-to-v2/#migration-steps)
### 1. Update the Endpoint URL
[Section titled “1. Update the Endpoint URL”](https://developers.llamaindex.ai/python/cloud/llamaparse/migration-v1-to-v2/#1-update-the-endpoint-url)
**Before (v1):**
```

POST https://api.cloud.llamaindex.ai/api/v1/parsing/upload

```

**After (v2):** Choose the appropriate endpoint based on your input method:
Terminal window```

# For parsing existing files by ID (recommended)



POSThttps://api.cloud.llamaindex.ai/api/v2alpha1/parse




# For parsing files from URLs



POSThttps://api.cloud.llamaindex.ai/api/v2alpha1/parse/url




# For multipart file uploads



POSThttps://api.cloud.llamaindex.ai/api/v2alpha1/parse/upload


```

### 2. Choose the Appropriate Endpoint and Configuration
[Section titled “2. Choose the Appropriate Endpoint and Configuration”](https://developers.llamaindex.ai/python/cloud/llamaparse/migration-v1-to-v2/#2-choose-the-appropriate-endpoint-and-configuration)
v2 provides specialized endpoints for different input methods. Choose the one that matches how you’re providing the document:
#### Existing File by ID (Recommended)
[Section titled “Existing File by ID (Recommended)”](https://developers.llamaindex.ai/python/cloud/llamaparse/migration-v1-to-v2/#existing-file-by-id-recommended)
For parsing an already uploaded file, use `/parse` with the file ID in the request body. This is the most efficient method as it reuses existing files.
#### URL-based Parsing
[Section titled “URL-based Parsing”](https://developers.llamaindex.ai/python/cloud/llamaparse/migration-v1-to-v2/#url-based-parsing)
For parsing documents from web URLs, use `/parse/url` with the URL and proxy settings in the request body.
#### Multipart File Upload
[Section titled “Multipart File Upload”](https://developers.llamaindex.ai/python/cloud/llamaparse/migration-v1-to-v2/#multipart-file-upload)
For traditional file uploads, use `/parse/upload` with multipart form data and a `configuration` parameter.
### 3. Replace Form Parameters with Configuration JSON
[Section titled “3. Replace Form Parameters with Configuration JSON”](https://developers.llamaindex.ai/python/cloud/llamaparse/migration-v1-to-v2/#3-replace-form-parameters-with-configuration-json)
The configuration approach depends on your chosen endpoint:
  * : Uses JSON request body with `file_id` and configuration fields (recommended)
  * **`/url`**: Uses JSON request body with`source_url` , `http_proxy`, and configuration fields
  * **`/upload`**: Uses multipart form data with`file` and `configuration` parameters


### 4. Migration Checklist
[Section titled “4. Migration Checklist”](https://developers.llamaindex.ai/python/cloud/llamaparse/migration-v1-to-v2/#4-migration-checklist)
Before migrating, review this checklist:
  * **Choose the right endpoint** : Select `/upload`, `/`, or `/url` based on your input method
  * **Update request format** : Change from form parameters to endpoint-specific configuration
  * **Replace parse modes with tiers** : Use `tier` instead of `parse_mode` (`fast`, `cost_effective`, `agentic`, `agentic_plus`)
  * **Remove model selection** : Models are now automatically selected based on tier
  * **Remove prompts** : Custom prompts are no longer supported for API simplification
  * **Remove external provider configs** : Azure OpenAI and external API keys are no longer supported
  * **Check for always-enabled parameters** : `adaptive_long_table`, `high_res_ocr`, `merge_tables_across_pages_in_markdown`, `outlined_table_extraction` and others are always enabled in v2
  * **Update page indexing** : Change `target_pages` from 0-based to 1-based indexing
  * **Move language parameter** : Move `language` to tier-specific `ocr_parameters`
  * **Update cache parameters** : Replace `invalidate_cache` + `do_not_cache` with single `disable_cache`
  * **Convert webhooks** : Change from single `webhook_url` to `webhook_configurations` array
  * **Remove header/footer customization** : Header/footer handling is now automatic
  * **Remove URL fields from non-URL endpoints** : Only `/url` endpoint accepts `source_url` and `http_proxy`
  * **Test thoroughly** : The alpha API may have additional breaking changes


## Configuration Structure
[Section titled “Configuration Structure”](https://developers.llamaindex.ai/python/cloud/llamaparse/migration-v1-to-v2/#configuration-structure)
The v2 configuration structure varies by endpoint:
### File ID (`/`) - Recommended
[Section titled “File ID (/) - Recommended”](https://developers.llamaindex.ai/python/cloud/llamaparse/migration-v1-to-v2/#file-id----recommended)
```



"file_id": "existing-file-id",




"parse_options": {




"tier": "fast|cost_effective|agentic|agentic_plus",




"version": "latest|2025-12-11",




// Tier-specific options (see examples below)





"webhook_configurations": [...],




"input_options": {...},




"crop_box": {...},




"page_ranges": {...},




"disable_cache": "boolean (optional)",




"output_options": {...},




"processing_control": {...}



```

### URL Parsing (`/url`)
[Section titled “URL Parsing (/url)”](https://developers.llamaindex.ai/python/cloud/llamaparse/migration-v1-to-v2/#url-parsing-url)
```



"source_url": "https://example.com/document.pdf",




"http_proxy": "https://proxy.example.com (optional)",




"parse_options": {




"tier": "fast|cost_effective|agentic|agentic_plus",




"version": "latest|2025-12-11",




// Tier-specific options (see examples below)





"webhook_configurations": [...],




"input_options": {...},




"crop_box": {...},




"page_ranges": {...},




"disable_cache": "boolean (optional)",




"output_options": {...},




"processing_control": {...}



```

### Multipart Upload (`/upload`)
[Section titled “Multipart Upload (/upload)”](https://developers.llamaindex.ai/python/cloud/llamaparse/migration-v1-to-v2/#multipart-upload-upload)
```



"parse_options": {




"tier": "fast|cost_effective|agentic|agentic_plus",




"version": "latest|2025-12-11",




// Tier-specific options (see examples below)





"webhook_configurations": [...],




"input_options": {...},




"crop_box": {...},




"page_ranges": {...},




"disable_cache": "boolean (optional)",




"output_options": {...},




"processing_control": {...}



```

## Parameter Mapping Reference
[Section titled “Parameter Mapping Reference”](https://developers.llamaindex.ai/python/cloud/llamaparse/migration-v1-to-v2/#parameter-mapping-reference)
### Basic Options
[Section titled “Basic Options”](https://developers.llamaindex.ai/python/cloud/llamaparse/migration-v1-to-v2/#basic-options)
v1 Parameter | v2 Location | Notes  
---|---|---  
`input_url` |  `source_url` (URL endpoint only) | Moved to URL endpoint, renamed from nested structure  
`http_proxy` |  `http_proxy` (URL endpoint only) | Only available in URL endpoint  
`max_pages` | `page_ranges.max_pages` | Same functionality  
`target_pages` | `page_ranges.target_pages` |  **Breaking change** : Now uses 1-based indexing (user inputs “1,2,3” instead of “0,1,2”)  
`invalidate_cache` and `do_not_cache` | `disable_cache` |  **Breaking change** : Single boolean combines both v1 parameters  
`language` | `parse_options.{mode}_options.ocr_parameters.languages` | Same functionality  
> **Important** : In v1, `target_pages` used 0-based indexing (e.g., “0,1,2” for pages 1, 2, 3). In v2, it uses 1-based indexing (e.g., “1,2,3” for the same pages) to be homogenous with the rest of the platform.
### Always Enabled in v2 (Breaking Changes)
[Section titled “Always Enabled in v2 (Breaking Changes)”](https://developers.llamaindex.ai/python/cloud/llamaparse/migration-v1-to-v2/#always-enabled-in-v2-breaking-changes)
The following parameters are **always enabled** in v2 across all tiers and cannot be disabled. We’re doing this to simplify calling LlamaParse and because these options give better results:
v1 Parameter | v2 Behavior | Breaking Change  
---|---|---  
`adaptive_long_table` | Always `true` |  **Breaking** : Cannot be disabled in v2  
`high_res_ocr` | Always `true` |  **Breaking** : Cannot be disabled in v2  
`merge_tables_across_pages_in_markdown` | Always `true` |  **Breaking** : Cannot be disabled in v2  
`outlined_table_extraction` | Always `true` |  **Breaking** : Cannot be disabled in v2  
`guess_xlsx_sheet_name` | Always `true` |  **Breaking** : Cannot be disabled in v2  
### Tier-Based Parameter Migration
[Section titled “Tier-Based Parameter Migration”](https://developers.llamaindex.ai/python/cloud/llamaparse/migration-v1-to-v2/#tier-based-parameter-migration)
v1 Parameter | v2 Location | Notes  
---|---|---  
`parse_mode` | `parse_options.tier` |  **Breaking** : Now uses tier-based system  
`model` | Automatic selection |  **Breaking** : Model is selected automatically based on tier  
`parsing_instruction` | **Removed** |  **Breaking** : Prompts are no longer supported for simplification  
`formatting_instruction` | **Removed** |  **Breaking** : Prompts are no longer supported for simplification  
`system_prompt` | **Removed** |  **Breaking** : Prompts are no longer supported for simplification  
`user_prompt` | **Removed** |  **Breaking** : Prompts are no longer supported for simplification  
`language` | `parse_options.{tier}_options.ocr_parameters.languages` | Same functionality  
### Removed/Deprecated Parameters
[Section titled “Removed/Deprecated Parameters”](https://developers.llamaindex.ai/python/cloud/llamaparse/migration-v1-to-v2/#removeddeprecated-parameters)
The following v1 parameters are **not supported** in v2:
v1 Parameter | v2 Status | Migration Path  
---|---|---  
`use_vendor_multimodal_model` |  **Removed** (was deprecated) | Use appropriate tier instead  
`gpt4o_mode` | **Removed** | Use `tier: "cost_effective"` for GPT-4o-mini or `tier: "agentic_plus"` for premium  
`gpt4o_api_key` | **Removed** | External provider support removed for simplification  
`premium_mode` | **Removed** | Use `tier: "agentic_plus"` for highest quality  
`fast_mode` | **Removed** | Use `tier: "fast"` for fastest processing  
`continuous_mode` | **Removed** | No direct equivalent  
`vendor_multimodal_api_key` | **Removed** |  **Breaking** : External providers removed for simplification  
`azure_openai_*` | **Removed** |  **Breaking** : External providers removed for simplification  
`bounding_box` | **Renamed** | Use `crop_box` object instead  
`disable_image_extraction` | **Removed** |  **Breaking** : Image extraction is now always optimized automatically  
`hide_headers` | **Removed** |  **Breaking** : Header handling is now automatic  
`hide_footers` | **Removed** |  **Breaking** : Footer handling is now automatic  
`page_header_prefix` | **Removed** |  **Breaking** : Header formatting removed for simplification  
`page_footer_prefix` | **Removed** |  **Breaking** : Footer formatting removed for simplification  
`page_prefix` | **Removed** |  **Breaking** : Page prefix formatting removed for simplification  
`page_separator` | **Removed** |  **Breaking** : Custom page separators removed for simplification  
`keep_page_separator_when_merging_tables` | **Removed** |  **Breaking** : Table merging behavior is now optimized automatically  
`input_s3_path` and `input_s3_region` | **Removed** | Not supported in v2alpha1  
`output_s3_path_prefix` and `output_s3_region` | **Removed** | Not supported in v2alpha1  
### Webhook Configuration Breaking Changes
[Section titled “Webhook Configuration Breaking Changes”](https://developers.llamaindex.ai/python/cloud/llamaparse/migration-v1-to-v2/#webhook-configuration-breaking-changes)
v1 Parameter | v2 Location | Notes  
---|---|---  
`webhook_url` | `webhook_configurations[0].webhook_url` |  **Breaking** : Now an array, but only first entry is used at the moment  
`webhook_configurations` (string) |  `webhook_configurations` (array) |  **Breaking** : Format changed from JSON string to structured array  
### Not Yet Implemented in v2
[Section titled “Not Yet Implemented in v2”](https://developers.llamaindex.ai/python/cloud/llamaparse/migration-v1-to-v2/#not-yet-implemented-in-v2)
The following options exist in the v2 schema but are not yet implemented:
  * `ignore_strikethrough_text` (exists in schema but not processed)
  * `input_options.pdf.password` (placeholder for future implementation)


### Crop Box Options
[Section titled “Crop Box Options”](https://developers.llamaindex.ai/python/cloud/llamaparse/migration-v1-to-v2/#crop-box-options)
v1 Parameter | v2 Location  
---|---  
`bbox_top` | `crop_box.top`  
`bbox_bottom` | `crop_box.bottom`  
`bbox_left` | `crop_box.left`  
`bbox_right` | `crop_box.right`  
### Input Format Options
[Section titled “Input Format Options”](https://developers.llamaindex.ai/python/cloud/llamaparse/migration-v1-to-v2/#input-format-options)
v1 Parameter | v2 Location  
---|---  
`html_make_all_elements_visible` | `input_options.html.make_all_elements_visible`  
`html_remove_fixed_elements` | `input_options.html.remove_fixed_elements`  
`html_remove_navigation_elements` | `input_options.html.remove_navigation_elements`  
`disable_image_extraction` | `input_options.pdf.disable_image_extraction`  
`spreadsheet_extract_sub_tables` | `input_options.spreadsheet.detect_sub_tables_in_sheets`  
### Ignore Options
[Section titled “Ignore Options”](https://developers.llamaindex.ai/python/cloud/llamaparse/migration-v1-to-v2/#ignore-options)
v1 Parameter | v2 Location  
---|---  
`skip_diagonal_text` | `parse_options.{mode}_options.ignore.ignore_diagonal_text`  
`disable_ocr` | `parse_options.{mode}_options.ignore.ignore_text_in_image`  
### Output Options
[Section titled “Output Options”](https://developers.llamaindex.ai/python/cloud/llamaparse/migration-v1-to-v2/#output-options)
v1 Parameter | v2 Location  
---|---  
`annotate_links` | `output_options.markdown.annotate_links`  
`page_suffix` | **Removed**  
`hide_headers` | **Removed**  
`hide_footers` | **Removed**  
`compact_markdown_table` | `output_options.markdown.tables.compact_markdown_tables`  
`output_tables_as_HTML` |  `output_options.markdown.tables.output_tables_as_markdown` (inverted)  
`guess_xlsx_sheet_name` | `output_options.tables_as_spreadsheet.guess_sheet_name`  
`extract_layout` | **Removed**  
`take_screenshot` | `output_options.screenshots.enable`  
`output_pdf_of_document` | `output_options.export_pdf.enable`  
### Processing Control
[Section titled “Processing Control”](https://developers.llamaindex.ai/python/cloud/llamaparse/migration-v1-to-v2/#processing-control)
v1 Parameter | v2 Location  
---|---  
`job_timeout_in_seconds` | `processing_control.timeouts.base_in_seconds`  
`job_timeout_extra_time_per_page_in_seconds` | `processing_control.timeouts.extra_time_per_page_in_seconds`  
`page_error_tolerance` | `processing_control.job_failure_conditions.allowed_page_failure_ratio`  
## Error Handling
[Section titled “Error Handling”](https://developers.llamaindex.ai/python/cloud/llamaparse/migration-v1-to-v2/#error-handling)
API v2 provides more detailed error messages:
### v1 Errors:
[Section titled “v1 Errors:”](https://developers.llamaindex.ai/python/cloud/llamaparse/migration-v1-to-v2/#v1-errors)
```

400: Invalid parameter combination

```

### v2 Errors:
[Section titled “v2 Errors:”](https://developers.llamaindex.ai/python/cloud/llamaparse/migration-v1-to-v2/#v2-errors)
```



"detail": [





"type": "value_error",




"loc": ["parse_options", "tier"],




"msg": "Unsupported tier: invalid_tier. Must be one of: fast, cost_effective, agentic, agentic_plus",




"input": {...}





```

> The v1 endpoint will remain available for the foreseeable future, so you can migrate at your own pace. However, new features and improvements will be focused on the v2 endpoint structure.
