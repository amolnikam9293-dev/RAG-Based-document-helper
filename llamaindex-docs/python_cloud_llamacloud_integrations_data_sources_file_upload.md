[Skip to content](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/file_upload/#_top)
# File Upload Data Source
Directly upload files
## Configure via UI
[Section titled “Configure via UI”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/file_upload/#configure-via-ui)
## Configure via API / Client
[Section titled “Configure via API / Client”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/file_upload/#configure-via-api--client)
```python with open('', 'rb') as f: file = client.files.upload_file(upload_file=f) ```  ```Typescript import fs from "fs" 
const filePath = “node_modules/llamaindex/examples/abramov.txt”;
file = await client.files.uploadFile(project.id, fs.createReadStream(filePath))
```


</TabItem>




<TabItem value="curl" label="curl" default>


```

# Step 1: Generate a presigned URL for file upload
[Section titled “Step 1: Generate a presigned URL for file upload”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/file_upload/#step-1-generate-a-presigned-url-for-file-upload)
curl -X POST “<https://api.cloud.llamaindex.ai/api/v1/files/presigned-url>” -H “Content-Type: application/json” -H “Authorization: Bearer $LLAMA_CLOUD_API_KEY” -d ’{ “name”: “example.txt” }‘
# Step 2: Use the presigned URL to upload the file to S3 within 30 seconds
[Section titled “Step 2: Use the presigned URL to upload the file to S3 within 30 seconds”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/file_upload/#step-2-use-the-presigned-url-to-upload-the-file-to-s3-within-30-seconds)
curl -X PUT “<https://your-presigned-url-from-step-1>” -H “Content-Type: text/plain” -F ‘file=@path/to/your/example.txt’
# Step 3: Confirm the file upload with LlamaCloud
[Section titled “Step 3: Confirm the file upload with LlamaCloud”](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sources/file_upload/#step-3-confirm-the-file-upload-with-llamacloud)
curl -X PUT “<https://api.cloud.llamaindex.ai/api/v1/files/sync>” -H “Content-Type: application/json” -H “Authorization: Bearer $LLAMA_CLOUD_API_KEY”
```


</TabItem>



</Tabs>

```

