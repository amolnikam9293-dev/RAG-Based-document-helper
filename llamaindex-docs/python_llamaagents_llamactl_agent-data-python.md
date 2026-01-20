[Skip to content](https://developers.llamaindex.ai/python/llamaagents/llamactl/agent-data-python/#_top)
# Agent Data (Python)
See the [Agent Data Overview](https://developers.llamaindex.ai/python/llamaagents/llamactl/agent-data-overview) for concepts, constraints, and environment details.
### Install
[Section titled “Install”](https://developers.llamaindex.ai/python/llamaagents/llamactl/agent-data-python/#install)
Terminal window```


uvaddllama-cloud-services


```

### Client overview
[Section titled “Client overview”](https://developers.llamaindex.ai/python/llamaagents/llamactl/agent-data-python/#client-overview)
The Python `llama-cloud-services` SDK provides `AsyncAgentDataClient` for working with the Agent Data API.
```


import httpx




import os




from pydantic import BaseModel




from llama_cloud_services.beta.agent_data import AsyncAgentDataClient




from llama_cloud.client import AsyncLlamaCloud





classExtractedPerson(BaseModel):




name: str




age: int




email: str





project_id = os.getenv("LLAMA_DEPLOY_PROJECT_ID")




# Base URL and API key (if running outside LlamaCloud)



base_url = os.getenv("LLAMA_CLOUD_BASE_URL")




api_key = os.getenv("LLAMA_CLOUD_API_KEY")




# Reusable async HTTP client with optional project scoping



http_client = httpx.AsyncClient(headers={"Project-Id": project_id} if project_id elseNone)




# Optional: base client for other SDK operations



base_client =AsyncLlamaCloud(




base_url=base_url,




token=api_key,




httpx_client=http_client,





# Only set when deployed in LlamaCloud (falls back inside the Agent Data client)



deployment_name = os.getenv("LLAMA_DEPLOY_DEPLOYMENT_NAME")





client =AsyncAgentDataClient(




type=ExtractedPerson,




collection="extracted_people",




# If omitted, uses LLAMA_DEPLOY_DEPLOYMENT_NAME or "_public"




deployment_name=deployment_name,




client=base_client,



```

### Create, Get, Update, Delete
[Section titled “Create, Get, Update, Delete”](https://developers.llamaindex.ai/python/llamaagents/llamactl/agent-data-python/#create-get-update-delete)
```


person =ExtractedPerson(name="John Doe",age=30,email="john@example.com")




created =await client.create_item(person)




fetched =await client.get_item(created.id)




updated =await client.update_item(created.id,ExtractedPerson(name="Jane",age=31,email="jane@example.com"))




await client.delete_item(updated.id)


```

Retry behavior: Network errors (timeouts, connection errors, retriable HTTP statuses) are retried up to 3 times with exponential backoff.
Notes:
  * Updates overwrite the entire `data` object.
  * `get_item` raises an `httpx.HTTPStatusError` with status code 404 if not found.


### Delete by query
[Section titled “Delete by query”](https://developers.llamaindex.ai/python/llamaagents/llamactl/agent-data-python/#delete-by-query)
Delete multiple items that match a filter. Returns the number of deleted items.
```


deleted_count =await client.delete(




filter={




"status": {"eq": "inactive"},




"age": {"gte": 65},






print(deleted_count)


```

### Search
[Section titled “Search”](https://developers.llamaindex.ai/python/llamaagents/llamactl/agent-data-python/#search)
You can filter by `data` fields and by `created_at`/`updated_at` (top-level fields). Sort using a comma-delimited list of fields; the `data.` prefix is required when sorting by data fields. The default page size is 50 (max 1000).
```


results =await client.search(




filter={




# Data fields




"age": {"gte": 21, "lt": 65},




"status": {"eq": "active"},




"tags": {"includes": ["python", "ml"]},




# Top-level timestamps (ISO strings accepted)




"created_at": {"gte": "2024-01-01T00:00:00Z"},





order_by="data.name desc, created_at",




page_size=50,




offset=0,




include_total=True,# request only on the first page if needed






for item in results.items:




print(item.data)





print(results.has_more, results.total)


```

Sorting:
  * Example: `"data.name desc, created_at"`.
  * If no sort is provided, results default to `created_at desc`.


Pagination:
  * Use `offset` and `page_size`. The server may return `has_more` and a `next_page_token` (SDK exposes `has_more`).


### Aggregate
[Section titled “Aggregate”](https://developers.llamaindex.ai/python/llamaagents/llamactl/agent-data-python/#aggregate)
Group data by one or more `data` fields, optionally count items per group, and/or fetch the first item per group.
```


agg =await client.aggregate(




filter={"status": {"eq": "active"}},




group_by=["department", "role"],




count=True,




first=True,# return the earliest item per group (by created_at)




order_by="data.department asc, data.role asc",




page_size=100,






for group in agg.items:  # items are groups




print(group.group_key# {"department": "Sales", "role": "AE"}




print(group.count# optional




print(group.first_item) # optional dict


```

Details:
  * `group_by`: dot-style data paths (e.g., `"department"`, `"contact.email"`).
  * `count`: adds a `count` per group.
  * `first`: returns the first `data` item per group (earliest `created_at`).
  * `order_by`: uses the same semantics as search (applies to group key expressions).
  * Pagination uses `offset` and `page_size` similarly to search.


### Untyped APIs
[Section titled “Untyped APIs”](https://developers.llamaindex.ai/python/llamaagents/llamactl/agent-data-python/#untyped-apis)
Use the untyped methods when you want to skip Pydantic validation of your model. These methods response objects where the `.data` payload is a plain `dict` rather than a Pydantic model.
```

# Get raw item (AgentData object; .data is a dict)



raw_item =await client.untyped_get_item(created.id)




print(raw_item.id, raw_item.deployment_name, raw_item.collection)




print(raw_item.data["name"])  # dict access




# Search (raw paginated response)



raw_page =await client.untyped_search(




filter={"status": {"eq": "active"}},




order_by="data.name desc, created_at",




page_size=50,





for item in raw_page.items:  # each item is an AgentData object




print(item.data# dict




# Pagination fields match the API



print(raw_page.next_page_token, raw_page.total_size)




# Aggregate (raw paginated response)



raw_groups =await client.untyped_aggregate(




filter={"status": {"eq": "active"}},




group_by=["department", "role"],




count=True,




first=True,





for grp in raw_groups.items:  # each item is an AggregateGroup object




print(grp.group_key, grp.count, grp.first_item# first_item is a dict




print(raw_groups.next_page_token, raw_groups.total_size)


```

### ExtractedData wrapper
[Section titled “ExtractedData wrapper”](https://developers.llamaindex.ai/python/llamaagents/llamactl/agent-data-python/#extracteddata-wrapper)
For extraction workflows, use `ExtractedData[T]` as the type parameter for your Agent Data client. This wrapper type is designed for workflows where data goes through review and approval stages.
```


from llama_cloud_services.beta.agent_data import AsyncAgentDataClient, ExtractedData





classInvoice(BaseModel):




vendor: str|None=None




total: float|None=None




date: str|None=None




# Client stores ExtractedData[Invoice] records



client =AsyncAgentDataClient(




type=ExtractedData[Invoice],




collection="invoices",




deployment_name=deployment_name,




client=base_client,



```

**Creating from LlamaExtract results:**
The `from_extraction_result` factory method creates an `ExtractedData` instance directly from a LlamaExtract result, automatically capturing field metadata (confidence scores, citations):
```


from llama_cloud_services import LlamaExtract




from llama_cloud_services.beta.agent_data import ExtractedData





extractor =LlamaExtract()




result =await extractor.aextract(data_schema=Invoice,files="invoice.pdf")




# Automatically extracts confidence scores and citations from the extraction result



extracted = ExtractedData.from_extraction_result(




result=result,




schema=Invoice,




status="pending_review",# optional, defaults to "pending_review"






await client.create_item(extracted)


```

**Creating manually:**
Use `ExtractedData.create` when you need to transform the data to a different schema or construct extracted data from other sources:
```


from llama_cloud_services.beta.agent_data import ExtractedData





invoice =Invoice(vendor="Acme Corp",total=1500.00,date="2024-01-15")





extracted = ExtractedData.create(




data=invoice,




status="pending_review",




file_id="file-abc123",# LlamaCloud file ID for linking




file_name="invoice.pdf",




file_hash="sha256:...",# optional content hash for deduplication




field_metadata={




"vendor": {"confidence": 0.95, "citation": [{"page": 1, "matching_text": "Acme Corp"}]},




"total": {"confidence": 0.92},




```

**ExtractedData fields:**
Field | Description  
---|---  
`original_data` | The data as originally extracted (preserved for change tracking)  
`data` | The current state of the data (updated by human review)  
`status` | Workflow status: `pending_review`, `accepted`, `rejected`, `error`, or custom string  
`overall_confidence` | Aggregated confidence score (auto-calculated from field_metadata)  
`field_metadata` | Dict mapping field paths to `ExtractedFieldMetadata` (confidence, citations)  
`file_id` | LlamaCloud file ID of the source document  
`file_name` | Name of the source file  
`file_hash` | Content hash for deduplication  
`metadata` | Additional application-specific metadata  
**Transforming schemas:**
When you need a different presentation schema than what was extracted:
```

# Extract with one schema



result =await extractor.aextract(data_schema=RawInvoice,files="invoice.pdf")




raw_invoice = RawInvoice.model_validate(result.data)




# Transform to presentation schema



presentation =PresentationInvoice(




vendor_name=raw_invoice.vendor,




amount=raw_invoice.total,




# ... additional transformations





# Preserve field metadata for citations/confidence if fields align



field_metadata = result.extraction_metadata.get("field_metadata", {})





extracted = ExtractedData.create(




data=presentation,




file_id=result.file.id,




file_name=result.file.name,




field_metadata=field_metadata,# retains citation/confidence for matching paths



```

