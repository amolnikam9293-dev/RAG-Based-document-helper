[Skip to content](https://developers.llamaindex.ai/python/cloud/llamaextract/features/performance_tips/#_top)
# Performance Tips
## Overall Performance Best Practices
[Section titled “Overall Performance Best Practices”](https://developers.llamaindex.ai/python/cloud/llamaextract/features/performance_tips/#overall-performance-best-practices)
For maximum extraction success:
  1. **Start with the best models for debugging** : When troubleshooting extraction issues, use `PREMIUM` mode with powerful parse/extract models. The choice of models can significantly impact extraction success—see [available models](https://developers.llamaindex.ai/python/cloud/llamaextract/features/options/#available-models-by-extraction-mode) for options. If the extraction succeeds with powerful models, you can then downgrade to identify which specific fields are causing issues on lower modes. For example, if `BALANCED` mode only extracts 5 out of 10 array elements, you might resolve this by changing the [extraction target](https://developers.llamaindex.ai/python/cloud/llamaextract/features/concepts#extraction-target). However, if extraction fails even with the best models, the issue is likely in your schema design (e.g., ambiguous field descriptions).
```

# Start debugging with a powerful configuration



extraction_config = {




"mode": "PREMIUM",




"parse_model": "anthropic-sonnet-4.5",




"extraction_model": "openai-gpt-5"



```

  2. **Start small and iterate** : Begin with a subset of your data or schema to validate your extraction approach and iterate on your schema description (e.g. adding examples, formatting instructions etc.) to get better accuracy before scaling.
  3. **Design clear, focused schemas** : Prefer precise short descriptions over verbose fields that try to do too much. See the [section on schema design](https://developers.llamaindex.ai/python/cloud/llamaextract/features/schema_design) and [avoiding complex transformations](https://developers.llamaindex.ai/python/cloud/llamaextract/features/performance_tips/#avoid-complex-field-transformations).
  4. **Leverage document structure** : Use page ranges, extraction targets, sections, and chunking strategies to optimize processing. See [options](https://developers.llamaindex.ai/python/cloud/llamaextract/features/options).
  5. **Combine tools strategically** : LlamaExtract excels at extracting information from documents. Focus on leveraging this strength while using complementary tools for computational tasks and validation (e.g., heavy calculations are better handled in a post-processing step).


## Extracting from Tables and Ordered Lists
[Section titled “Extracting from Tables and Ordered Lists”](https://developers.llamaindex.ai/python/cloud/llamaextract/features/performance_tips/#extracting-from-tables-and-ordered-lists)
**The situation:** When working with documents containing tables, spreadsheets (CSV/Excel), or ordered lists of entities, you want to ensure comprehensive and accurate extraction of each row or item.
**Use`PER_TABLE_ROW` extraction target**: If you are only interested in extracting or transforming data from a table or ordered list of entities, use the `PER_TABLE_ROW` extraction target. This processes each row individually for comprehensive coverage and accurate results.
```


from llama_cloud import ExtractionTarget




# Optimal: Use PER_TABLE_ROW for tabular data extraction



extraction_config = {




"extraction_target": ExtractionTarget.PER_TABLE_ROW



```

**When your schema has additional elements beyond the table:** If your schema includes fields that need to be extracted from outside the table (e.g., document metadata, headers, or summary information), you have two options:
  1. **Split your extraction task** : Run separate extractions for tabular data (using `PER_TABLE_ROW`) and non-tabular elements.
```

# First extraction: Get document-level metadata



metadata_result = agent.extract(




document,




schema=metadata_schema,




extraction_target=ExtractionTarget.PER_DOCUMENT





# Second extraction: Get table row data



table_result = agent.extract(




document,




schema=table_row_schema,




extraction_target=ExtractionTarget.PER_TABLE_ROW,




page_range="5-10"# Adjust these accordingly to send pages with the table



```

  2. **Use a reasoning model in PREMIUM mode** : If you need to extract both tabular and non-tabular elements in a single pass, use an extraction model like `gpt-5` or `gpt-5-mini` in `PREMIUM` mode. Note that this approach can be slower.
```


extraction_config = {




"extraction_model": "openai-gpt-5",




"mode": "PREMIUM"



```



## Avoid Complex Field Transformations
[Section titled “Avoid Complex Field Transformations”](https://developers.llamaindex.ai/python/cloud/llamaextract/features/performance_tips/#avoid-complex-field-transformations)
Don’t embed business logic in field descriptions. Extract clean data first, then compute in your application code.
```

# ❌ Problematic: Too much logic in the field description



problematic_field = {




"calculated_score": {




"type": "number",




"description": "If revenue > 1M, multiply by 0.8, else if revenue < 500K multiply by 1.2, otherwise use the base score from table 3, but only if the date is after 2020 and the category is not 'exempt'"






# ✅ Better: Simple extraction, handle logic separately



better_schema = {




"revenue": {"type": "number", "description": "Total revenue in dollars"},




"base_score": {"type": "number", "description": "Base score value from the scoring table"},




"date": {"type": "string", "description": "Date in YYYY-MM-DD format"},




"category": {"type": "string", "description": "Business category"}





# Then handle calculations in your application code:



defcalculate_final_score(extracted_data):




revenue = extracted_data["revenue"]




if revenue 1000000:




return extracted_data["base_score"] *0.8




elif revenue 500000:




return extracted_data["base_score"] *1.2




return extracted_data["base_score"]


```

