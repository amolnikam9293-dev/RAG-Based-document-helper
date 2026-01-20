[Skip to content](https://developers.llamaindex.ai/python/cloud/llamaextract/getting_started/api/#_top)
# REST API
## Quickstart
[Section titled “Quickstart”](https://developers.llamaindex.ai/python/cloud/llamaextract/getting_started/api/#quickstart)
### Create a new agent
[Section titled “Create a new agent”](https://developers.llamaindex.ai/python/cloud/llamaextract/getting_started/api/#create-a-new-agent)
```

curl -X 'POST' \



'https://api.cloud.llamaindex.ai/api/v1/extraction/extraction-agents' \




-H 'accept: application/json' \




-H "Authorization: Bearer $LLAMA_CLOUD_API_KEY" \




-H 'Content-Type: application/json' \




-d '{




"name": "resume_parser",




"data_schema": {




"type": "object",




"properties": {




"name": {




"type": "string",




"description": "Candidate name"





"experience": {




"type": "array",




"description": "Work history",




"items": {




"type": "object",




"properties": {




"company": {




"type": "string",




"description": "Company name"





"title": {




"type": "string",




"description": "Job title"





"start_date": {




"anyOf": [





"type": "string"






"type": "null"






"description": "Start date of employment"





"end_date": {




"anyOf": [





"type": "string"






"type": "null"






"description": "End date of employment"










"config": {




"extraction_target": "PER_DOC",




"extraction_mode": "BALANCED",




```

You can list all your existing agents with the following command. The `project_id` can be obtained from the [web UI](https://developers.llamaindex.ai/python/cloud/llamaextract/getting_started/web_ui).
Also refer to the the [Projects API](https://developers.llamaindex.ai/cloud-api-reference/category/projects) for programmatically creating/editing projects.
```

curl -X 'GET' \



'https://api.cloud.llamaindex.ai/api/v1/extraction/extraction-agents?project_id={project_id}' \




-H 'accept: application/json' \




-H "Authorization: Bearer $LLAMA_CLOUD_API_KEY"


```

You can also fetch a specific `agent_id` by name:
```

curl -X 'GET' \



'https://api.cloud.llamaindex.ai/api/v1/extraction/extraction-agents/by-name/{agent_name}' \




-H 'accept: application/json' \




-H "Authorization: Bearer $LLAMA_CLOUD_API_KEY"


```

### Upload a document
[Section titled “Upload a document”](https://developers.llamaindex.ai/python/cloud/llamaextract/getting_started/api/#upload-a-document)
Upload a document using our [Upload API](https://developers.llamaindex.ai/cloud-api-reference/upload-file-api-v-1-files-post).
```

curl -X 'POST' \



'https://api.cloud.llamaindex.ai/api/v1/files' \




-H 'accept: application/json' \




-H 'Content-Type: multipart/form-data' \




-H "Authorization: Bearer $LLAMA_CLOUD_API_KEY" \




-F 'upload_file=@/path/to/your/file.pdf;type=application/pdf'


```

### Run an extraction job
[Section titled “Run an extraction job”](https://developers.llamaindex.ai/python/cloud/llamaextract/getting_started/api/#run-an-extraction-job)
Use the `extraction_agent_id` and `file_id` from the previous steps to run an extraction job.
```

curl -X 'POST' \



'https://api.cloud.llamaindex.ai/api/v1/extraction/jobs' \




-H 'accept: application/json' \




-H 'Content-Type: application/json' \




-H "Authorization: Bearer $LLAMA_CLOUD_API_KEY" \




-d '{




"extraction_agent_id": "{$AGENT_ID}",




"file_id": "{$FILE_ID}",



```

### Poll for extraction job status
[Section titled “Poll for extraction job status”](https://developers.llamaindex.ai/python/cloud/llamaextract/getting_started/api/#poll-for-extraction-job-status)
Jobs are processed asynchronously. You can poll for the status of a job using the following endpoint.
```

curl -X 'GET' \



'https://api.cloud.llamaindex.ai/api/v1/extraction/jobs/{$JOB_ID}' \




-H 'accept: application/json' \




-H "Authorization: Bearer $LLAMA_CLOUD_API_KEY"


```

### Get the results of an extraction job
[Section titled “Get the results of an extraction job”](https://developers.llamaindex.ai/python/cloud/llamaextract/getting_started/api/#get-the-results-of-an-extraction-job)
If the job is successfully completed, you will see the status as `SUCCESS`. You can then retrieve the results from the following endpoint.
```

curl -X 'GET' \



'https://api.cloud.llamaindex.ai/api/v1/extraction/jobs/{$JOB_ID}/result' \




-H 'accept: application/json' \




-H "Authorization: Bearer $LLAMA_CLOUD_API_KEY"


```

## Full API documentation
[Section titled “Full API documentation”](https://developers.llamaindex.ai/python/cloud/llamaextract/getting_started/api/#full-api-documentation)
This is just a subset of the available endpoints to help you get started.
You can see all the available endpoints in our [full API documentation](https://developers.llamaindex.ai/cloud-api-reference/category/llama-extract).
