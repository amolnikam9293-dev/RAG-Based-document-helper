[Skip to content](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/presets/#_top)
# Modes and Presets
LlamaParse supports different parsing modes and presets to adapt to your use case.
## Cost-effective
[Section titled “Cost-effective”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/presets/#cost-effective)
The cost-effective mode is great for everyday documents that include a mix of images, tables, and text. You get reliable formatting without any extra setup.
### Under the Hood
[Section titled “Under the Hood”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/presets/#under-the-hood)
Cost-effective has been designed for more standard documents, with simple layouts, and for huge batch of documents when the output accuracy isn’t critical. It allow you to get good overall results while keeping some credits for other tasks.
To use Cost-effective, set the following parameters:


```


parser =LlamaParse(




api_key="<you-api-key>",# See how to get your API key at https://developers.llamaindex.ai/python/cloud/general/api_key/




parse_mode="parse_page_with_llm",# The parsing mode




high_res_ocr=True,# Whether to use high resolution OCR (slower but more precise)




adaptive_long_table=True,# Adaptive long table. LlamaParse will try to detect long table and adapt the output




outlined_table_extraction=True,# Whether to try to extract outlined tables




output_tables_as_HTML=True,# Whether to output tables as HTML in the markdown output



```

Terminal window```


curl-XPOST'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'parse_mode="parse_page_with_llm"'\




--form'high_res_ocr="true"'\




--form'adaptive_long_table="true"'\




--form'outlined_table_extraction="true"'\




--form'output_tables_as_HTML="true"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## Agentic
[Section titled “Agentic”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/presets/#agentic)
Agentic mode has been designed for most documents with diagrams and images. It provides a great quality on the vast majority of documents at a reasonable price. It may struggle with complex layouts or charts.
### Under the Hood
[Section titled “Under the Hood”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/presets/#under-the-hood-1)
Agentic mode performs OCR, image extraction, and identifies structural elements such as tables and headings. It also outputs equations in LaTeX format and converts diagrams into Mermaid syntax for further analysis and visualization.
To use Agentic, set the following parameters:


```


parser =LlamaParse(




api_key="<you-api-key>",# See how to get your API key at https://developers.llamaindex.ai/python/cloud/general/api_key




parse_mode="parse_page_with_agent",# The parsing mode




model="gemini-2.5-flash",# The model to use




high_res_ocr=True,# Whether to use high resolution OCR (slower but more precise)




adaptive_long_table=True,# Adaptive long table. LlamaParse will try to detect long table and adapt the output




outlined_table_extraction=True,# Whether to try to extract outlined tables




output_tables_as_HTML=True,# Whether to output tables as HTML in the markdown output



```

Terminal window```


curl-XPOST'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'parse_mode="parse_page_with_agent"'\




--form'model="gemini-2.5-flash"'\




--form'high_res_ocr="true"'\




--form'adaptive_long_table="true"'\




--form'outlined_table_extraction="true"'\




--form'output_tables_as_HTML="true"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## Agentic Plus
[Section titled “Agentic Plus”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/presets/#agentic-plus)
Agentic Plus Mode is designed for complex, highly formatted documents—things like scanned financial reports, research papers, or anything with charts, tables, and diagrams. It gives you the most accurate and structured results.
### Under the Hood
[Section titled “Under the Hood”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/presets/#under-the-hood-2)
Agentic Plus combines all the capabilities of Agentic mode with enhanced processing power and a better model. It’s able to handle the most challenging document layouts, providing superior accuracy for complex tables, charts, and multi-column layouts.
To use Agentic Plus, set the following parameters:


```


parser =LlamaParse(




api_key="<you-api-key>",# See how to get your API key at https://developers.llamaindex.ai/python/cloud/general/api_key




parse_mode="parse_page_with_agent",# The parsing mode




model="anthropic-sonnet-4.0",# The model to use




high_res_ocr=True,# Whether to use high resolution OCR (slower but more precise)




adaptive_long_table=True,# Adaptive long table. LlamaParse will try to detect long table and adapt the output




outlined_table_extraction=True,# Whether to try to extract outlined tables




output_tables_as_HTML=True,# Whether to output tables as HTML in the markdown output



```

Terminal window```


curl-XPOST'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'parse_mode="parse_page_with_agent"'\




--form'model="anthropic-sonnet-4.0"'\




--form'high_res_ocr="true"'\




--form'adaptive_long_table="true"'\




--form'outlined_table_extraction="true"'\




--form'output_tables_as_HTML="true"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## Use Case Specific Presets
[Section titled “Use Case Specific Presets”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/presets/#use-case-specific-presets)
Use-case specific preset are versioned. You can get the last version of the preset by calling them with the `-latest` flag or directly without flags.
### Invoices
[Section titled “Invoices”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/presets/#invoices)
For Invoices and receipts. Set `preset="invoice"` on API. Current version is `invoice-v-1`.
### Scientific Paper
[Section titled “Scientific Paper”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/presets/#scientific-paper)
For Scientific papers. Set `preset="scientific"` on API. Current version is `scientific-v-1`.
### Technical Documentation
[Section titled “Technical Documentation”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/presets/#technical-documentation)
For technical documentation with schematics. Set `preset="technicalDocumentation"` on API. Current version is `technicalDocumentation-v-1`.
Output schematics in the present in the documentation using the following `XML` format in the markdown:
```

schematic



bbox0.1,0.1,0.9,0.9</bbox




captionCaption of the schematic (if present)</caption




schematic_elements




element




typeType of the element (e.g. resistor, capacitor, etc.)</type




valueValue of the element (e.g. 10k, 100uF, etc.)</value




positionx,y</position




labelLabel of the element (if present)</label




</element




<!-- Repeat for each element in the schematic -->




</schematic_elements



</schematic

```

### Forms
[Section titled “Forms”](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/presets/#forms)
For forms and questionnaires. Set `preset="forms"` on API. Current version is `forms-v-1`.
Output form field in the markdown as a table with the following columns `Field Name`, `Field Type`, `Field Value`.
```

| Field Name                     | Field Type   | Field Value                              |


| ------------------------------ | ------------ | ---------------------------------------- |


| A checkbox                     | Checkbox     | Unchecked                                |


| Another checkbox               | Checkbox     | Checked                                  |


| Number of Thin                 | Text         | 1                                        |


| Name of tool                   | Text         | LlamaParse                               |


| Date review                    | Date         | 24/06/2024                               |


| Contractor                     | Signature    | John Doe                                 |


| Available                      | Radio        | Yes                                      |

```

