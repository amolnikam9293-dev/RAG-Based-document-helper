[Skip to content](https://developers.llamaindex.ai/python/cloud/llamaextract/features/schema_design/#_top)
# Schema Design and Restrictions
At the core of LlamaExtract is the schema, which defines the structure of the data you want to extract from your documents.
## Schema Restrictions
[Section titled “Schema Restrictions”](https://developers.llamaindex.ai/python/cloud/llamaextract/features/schema_design/#schema-restrictions)
_LlamaExtract only supports a subset of the JSON Schema specification._ While limited, it should be sufficient for a wide variety of use-cases.
  * If you are specifying the schema as a JSON, there are two ways you can mark optional fields: 
    * not including them in the containing object’s `required` array
    * explicilty marking them as nullable fields using `anyOf` with a `null` type. See `"start_date"` field in the [example schema](https://developers.llamaindex.ai/python/cloud/llamaextract/getting_started/api).
  * If you are using Pydantic for specifying the schema in the Python SDK, you can use the `Optional` annotation for marking optional fields.
  * Root node must be of type `object`.
  * Schema nesting must be limited to within 7 levels.
  * The important fields are key names/titles, type and description. Fields for formatting, default values, etc. are **not supported**. If you need these, you can add the restrictions to your field description and/or use a post-processing step. e.g. default values can be supported by making a field optional and then setting `"null"` values from the extraction result to the default value.
  * Additional schema restrictions: 
    * **Maximum properties** : 5,000 total properties across the entire schema.
    * **Maximum total string content** : 120,000 characters for all strings (field names, descriptions, enum values, etc.) combined.
    * **Maximum raw JSON schema size** : 150,000 characters for the raw JSON schema string.
  * If you hit these limits for complex extraction use cases, consider restructuring your extraction workflow to fit within these constraints, e.g. by extracting subsets of fields and later merging them together.


## Tips & Best Practices
[Section titled “Tips & Best Practices”](https://developers.llamaindex.ai/python/cloud/llamaextract/features/schema_design/#tips--best-practices)
  * Try to limit schema nesting to 3-4 levels.
  * Make fields optional when data might not always be present (specially `boolean` and `int` fields where defaults for missing values could cause confusion).
  * When you want to extract a variable number of entities, use an `array` type. However, note that you cannot use an `array` type for the root node.
  * Use descriptive field names and detailed descriptions. Use descriptions to pass formatting instructions or few-shot examples.
  * Above all, start simple and iteratively build your schema to incorporate requirements.


## Automatic Schema Generation
[Section titled “Automatic Schema Generation”](https://developers.llamaindex.ai/python/cloud/llamaextract/features/schema_design/#automatic-schema-generation)
Instead of manually defining schemas, you can use LlamaExtract’s automatic schema generation feature. The system can generate a schema based on:
  * **A natural language prompt** : Describe what data you want to extract
  * **A sample file** : Upload a document and let the system infer the schema from its structure
  * **An existing schema to refine** : Provide a base schema and let the system improve or extend it


You can combine these inputs — for example, provide both a sample file and a prompt to guide the generation.
### Using the REST API
[Section titled “Using the REST API”](https://developers.llamaindex.ai/python/cloud/llamaextract/features/schema_design/#using-the-rest-api)
Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/extraction/extraction-agents/schema/generate'\




-H'accept: application/json'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




-H'Content-Type: application/json'\





"prompt": "Extract invoice details including invoice number, date, vendor name, line items with descriptions and amounts, and total amount",




"file_id": "optional-file-id-for-sample-document"



```

For the full API documentation, see the [LlamaExtract API Reference](https://developers.llamaindex.ai/cloud-api-reference/category/llama-extract).
## Defining Schemas (Python SDK)
[Section titled “Defining Schemas (Python SDK)”](https://developers.llamaindex.ai/python/cloud/llamaextract/features/schema_design/#defining-schemas-python-sdk)
The Python SDK can be installed using
Terminal window```


pipinstallllama-cloud-services


```

Schemas can be defined using either Pydantic models or JSON Schema:
### Using Pydantic (Recommended)
[Section titled “Using Pydantic (Recommended)”](https://developers.llamaindex.ai/python/cloud/llamaextract/features/schema_design/#using-pydantic-recommended)
```


from pydantic import BaseModel, Field




from typing import List, Optional




from llama_cloud_services import LlamaExtract





classExperience(BaseModel):




company: str=Field(description="Company name")




title: str=Field(description="Job title")




start_date: Optional[str] =Field(description="Start date of employment")




end_date: Optional[str] =Field(description="End date of employment")





classResume(BaseModel):




name: str=Field(description="Candidate name")




experience: List[Experience] =Field(description="Work history")


```

### Using JSON Schema
[Section titled “Using JSON Schema”](https://developers.llamaindex.ai/python/cloud/llamaextract/features/schema_design/#using-json-schema)
```


schema = {




"type": "object",




"properties": {




"name": {"type": "string", "description": "Candidate name"},




"experience": {




"type": "array",




"description": "Work history",




"items": {




"type": "object",




"properties": {




"company": {




"type": "string",




"description": "Company name",





"title": {"type": "string", "description": "Job title"},




"start_date": {




"anyOf": [{"type": "string"}, {"type": "null"}],




"description": "Start date of employment",





"end_date": {




"anyOf": [{"type": "string"}, {"type": "null"}],




"description": "End date of employment",










extractor =LlamaExtract(api_key="YOUR_API_KEY")




agent = extractor.create_agent(name="resume-parser",data_schema=schema)


```

