[Skip to content](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/file-storage/#_top)
# File Storage
##  Self-Hosting Documentation Access 
This section requires a password to access. Interested in self-hosting? [Contact sales](https://www.llamaindex.ai/contact) to learn more. 
Self-Hosting Documentation Access Granted  Logout 
File storage is an integral part of LlamaCloud. Without it, many key features would not be possible. This page walks through how to configure file storage for your deployment — which buckets you need to create and for non-AWS deployments, how to configure the S3 Proxy to interact with them.
## Requirements
[Section titled “Requirements”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/file-storage/#requirements)
  * A valid blob storage service. We recommend the following: 
    * [Google Cloud Storage](https://cloud.google.com/storage)
  * Because LlamaCloud heavily relies on file storage, you will need to create the following buckets: 
    * `llama-platform-parsed-documents`
    * `llama-platform-etl`
    * `llama-platform-external-components`
    * `llama-platform-file-parsing`
    * `llama-platform-raw-files`
    * `llama-cloud-parse-output`
    * `llama-platform-file-screenshots`
    * `llama-platform-extract-output` (for `LlamaExtract`)


## Connecting to AWS S3
[Section titled “Connecting to AWS S3”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/file-storage/#connecting-to-aws-s3)
Below are two ways to configure a connection to AWS S3:
### (Recommended) IAM Role for Service Accounts
[Section titled “(Recommended) IAM Role for Service Accounts”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/file-storage/#recommended-iam-role-for-service-accounts)
We recommend that users create a new IAM Role and Policy for LlamaCloud. You can then attach the role ARN as a service account annotation.
```

// Example IAM Policy




"Version": "2012-10-17",




"Statement": [





"Effect": "Allow",




"Action": ["s3:*"], // this is not secure




"Resource": [




"arn:aws:s3:::llama-platform-parsed-documents",




"arn:aws:s3:::llama-platform-parsed-documents/*",







```

After creating something similar to the above policy, update the `backend`, `jobsService`, `jobsWorker`, and `llamaParse` service accounts with the EKS annotation.
```

# Example for the backend service account. Repeat for each of the services listed above.



backend:




serviceAccountAnnotations:




eks.amazonaws.com/role-arn: arn:aws:iam::<account-id>:role/<role-name>


```

For more information, feel free to refer to the [official AWS documentation](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html) about this topic.
### AWS Credentials
[Section titled “AWS Credentials”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/file-storage/#aws-credentials)
Create a user with a policy attached for the aforementioned s3 buckets. Afterwards, you can configure the platform to use the aws credentials of that user by setting the following values in your `values.yaml` file:
```


config:




storageBuckets:




provider: "aws"




s3proxy:




enabled: true




containerPort: 8080




config:




JCLOUDS_PROVIDER: "aws-s3"




JCLOUDS_IDENTITY: <AWS-ACCESS-KEY>




JCLOUDS_CREDENTIAL: <AWS-SECRET-KEY>




JCLOUDS_REGION: <AWS-REGION># e.g. "us-east-1"




JCLOUDS_ENDPOINT: "https://s3.<AWS-REGION>.amazonaws.com"


```

## Overriding Default Bucket Names
[Section titled “Overriding Default Bucket Names”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/file-storage/#overriding-default-bucket-names)
We allow users to override the default bucket names in the `values.yaml` file.
```


config:




storageBuckets:




parsedDocuments: "<your-bucket-name>"




parsedEtl: "<your-bucket-name>"




parsedExternalComponents: "<your-bucket-name>"




parsedFileParsing: "<your-bucket-name>"




parsedRawFile: "<your-bucket-name>"




parseOutput: "<your-bucket-name>"




parsedFileScreenshot: "<your-bucket-name>"




extractOutput: "<your-bucket-name>"




parseFileUpload: "<your-bucket-name>"




parseFileOutput: "<your-bucket-name>"


```

## Connecting to Azure Blob Storage or Other Providers with S3Proxy
[Section titled “Connecting to Azure Blob Storage or Other Providers with S3Proxy”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/file-storage/#connecting-to-azure-blob-storage-or-other-providers-with-s3proxy)
LlamaCloud was first developed on AWS, which means that we started by natively supporting S3. However, to make a self-hosted solution possible, we need a way for the platform to interact with other providers.
We leverage the open-source project [S3Proxy](https://github.com/gaul/s3proxy) to translate the S3 API requests into requests to other storage providers. A containerized deployment of S3Proxy is supported out of the box in our helm charts.
S3Proxy should always be set to `enabled: true`, even when deploying LlamaCloud on AWS. This causes S3Proxy to be deployed as a sidecar on several of the LlamaCloud pods.
The following is an example for how to connect your LlamaCloud deployment to Azure Blob Storage. For more examples of connecting to different providers, please refer to the project’s [Examples](https://github.com/gaul/s3proxy/wiki/Storage-backend-examples) page.
  * [ Azure Blob Storage with S3 Proxy ](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/file-storage/#tab-panel-56)


```


config:




storageBuckets:




provider: "azure"




s3proxy:




enabled: true




containerPort: 8080




config:




S3PROXY_ENDPOINT: "http://0.0.0.0:80"




S3PROXY_AUTHORIZATION: "none"




S3PROXY_IGNORE_UNKNOWN_HEADERS: "true"




S3PROXY_CORS_ALLOW_ORIGINS: "*"




JCLOUDS_PROVIDER: "azureblob"




JCLOUDS_REGION: "eastus"# Change to your region




JCLOUDS_AZUREBLOB_AUTH: "azureKey"




JCLOUDS_IDENTITY: "fill-out"# Change to your storage account name




JCLOUDS_CREDENTIAL: "fill-out"# Change to your storage account key




JCLOUDS_ENDPOINT: "fill-out"# Change to your storage account endpoint


```

