[Skip to content](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/service-configurations/#_top)
# Service Configurations
##  Self-Hosting Documentation Access 
This section requires a password to access. Interested in self-hosting? [Contact sales](https://www.llamaindex.ai/contact) to learn more. 
Self-Hosting Documentation Access Granted  Logout 
Individual LlamaCloud services can be configured based on your specific needs. This page will cover the different configurations for each service.
## Global Configurations
[Section titled “Global Configurations”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/service-configurations/#global-configurations)
At the time of writing, the only global configurations are for external dependencies. For more information, please refer to the [Database and Queues](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/db_and_queues/overview) page.
## Backend Service
[Section titled “Backend Service”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/service-configurations/#backend-service)
### Qdrant
[Section titled “Qdrant”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/service-configurations/#qdrant)
[Qdrant](https://qdrant.tech/) is a popular vector database that is used to store and retrieve embeddings. Users can configure Qdrant as a Data Sink on a project by project basis, or if they prefer, they can configure it to be used as a Data Sink across all projects and organizations. For the latter, the following configurations can be set:
```

# basic example



qdrant:




enabled: true




url: "http://qdrant:6333"




apiKey: <QDRANT-API-KEY>




# or, if you prefer to use an existing secret



qdrant:




enabled: true




url: "http://qdrant:6333"




secret: "qdrant-secret"


```

## Jobs Worker Service
[Section titled “Jobs Worker Service”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/service-configurations/#jobs-worker-service)
There are several configs that can be set to modify how the Jobs Worker handled job executions.
### Concurrency Settings
[Section titled “Concurrency Settings”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/service-configurations/#concurrency-settings)
These settings modify how concurrent jobs get distributed across the job worker pods. These are mainly used to:
  1. Prevent a noisy neighbor problem whereby a single user can flood the job workers, thereby leading to starvation for other users
  2. Prevent external resources such as Mongo, Embeddings API, Vector DBs etc. from being overloaded with too many requests


  * **maxJobsInExecutionPerJobType** : This setting defines the maximum number of concurrent jobs a user can have running per job type. It is used by the job runner to help prevent any one user from overloading the system.
    * Set this to 0 to disable this concurrency check.
  * **maxIndexJobsInExecution** : This configuration specifies the maximum number of ingestion (indexing) jobs that a single pipeline is allowed to execute concurrently. It is applied to pipelines handling document ingestion and indexing operations to control resource usage.
    * Set this to 0 to disable this concurrency check.
  * **maxDocumentIngestionJobsInExecution** : This parameter limits the number of concurrent document ingestion jobs a user can have in execution. Document ingestion is typically resource intensive, so this should be kept relatively low to avoid overloading the system.
    * Set this to 0 to disable this concurrency check.


```

# example values.yaml for high throughput



config:




jobs:




maxJobsInExecutionPerJobType: 25




maxIndexJobsInExecution: 0




maxDocumentIngestionJobsInExecution: 10


```

### Timeout and Limit Settings
[Section titled “Timeout and Limit Settings”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/service-configurations/#timeout-and-limit-settings)
These settings control the execution timeout and data processing limits for jobs handled by the Jobs Worker service:
  * **defaultTransformDocumentTimeoutSeconds** : This setting defines the default timeout in seconds for document transformation jobs. Document transformation can be resource-intensive and may take significant time depending on document size and complexity.
    * Default value is `240` (4 minutes).
  * **transformEmbeddingCharLimit** : This configuration specifies the maximum number of characters that can be processed in a single transform embedding operation. This helps prevent memory issues and ensures consistent performance when processing large documents.
    * Default value is `11520000` (11.52 million characters).


```

# example values.yaml with custom timeout and limits



config:




jobs:




defaultTransformDocumentTimeoutSeconds: "7200"# 2 hours




transformEmbeddingCharLimit: "2000000"# 2 million characters


```

**Note** : These configuration values must be provided as quoted strings to prevent YAML parsing issues with large numbers.
## LlamaParse
[Section titled “LlamaParse”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/service-configurations/#llamaparse)
### Job Throughput Settings
[Section titled “Job Throughput Settings”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/service-configurations/#job-throughput-settings)
  * **maxQueueConcurrency** : This configuration sets the maximum number of jobs that can be processed concurrently by the LlamaParse service. It helps enable the service to process a high volume of jobs efficiently. The higher the number, the more resources will be used, so please be mindful of this. 
    * Default value is `3`.


```

# example values.yaml for high throughput



config:




parse:




maxQueueConcurrency: 10


```

