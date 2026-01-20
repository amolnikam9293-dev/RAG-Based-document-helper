[Skip to content](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/setup/#_top)
# Azure Setup Guide
##  Self-Hosting Documentation Access 
This section requires a password to access. Interested in self-hosting? [Contact sales](https://www.llamaindex.ai/contact) to learn more. 
Self-Hosting Documentation Access Granted  Logout 
This guide helps Azure shops connect LlamaCloud to existing Azure services. It assumes you already have Azure infrastructure provisioned (via Terraform, ARM templates, or other means) and focuses on gathering the right credentials and configuring LlamaCloud to connect to your Azure services.
## Overview
[Section titled “Overview”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/setup/#overview)
This guide covers connecting LlamaCloud to:
  * **Azure Kubernetes Service (AKS)** for container orchestration
  * **Azure Database for PostgreSQL** for primary data storage
  * **Azure Cache for Redis** for caching and sessions
  * **Azure Service Bus** for job queue management
  * **Azure Cosmos DB (MongoDB API)** for document storage
  * **Azure Blob Storage** for file storage
  * **Azure OpenAI** for LLM integration
  * **Microsoft Entra ID** for authentication (OIDC)


## Prerequisites
[Section titled “Prerequisites”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/setup/#prerequisites)
  * **Existing Azure infrastructure** with the required services provisioned
  * **AKS cluster** with kubectl access configured
  * **Helm v3.7.0+** installed
  * **LlamaCloud License Key** (contact support@llamaindex.ai)


## Step 1: Configure External Azure Services
[Section titled “Step 1: Configure External Azure Services”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/setup/#step-1-configure-external-azure-services)
LlamaCloud requires the following Azure services to be provisioned and configured. Click each section below to view requirements and credential gathering steps:
### Azure Database for PostgreSQL
[Section titled “Azure Database for PostgreSQL”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/setup/#azure-database-for-postgresql)
**Click to expand PostgreSQL configuration**
#### Requirements:
[Section titled “Requirements:”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/setup/#requirements)
  * **Version** : PostgreSQL 14 or higher
  * **Networking** : Accessible from your AKS cluster
  * **Performance** : General Purpose or Memory Optimized tier recommended


#### Gather Credentials:
[Section titled “Gather Credentials:”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/setup/#gather-credentials)
**From Azure Portal:**
  1. Navigate to your **Azure Database for PostgreSQL Flexible Server**
  2. Go to **Settings** → **Connection strings**
  3. Copy the **ADO.NET** connection string (it will look similar to below)


**Connection String Format:**
```

postgresql://username:password@servername.postgres.database.azure.com:5432/databasename

```

**Required Information:**
  * **Server FQDN** : `your-server.postgres.database.azure.com`
  * **Database Name** : Usually `llamacloud`
  * **Username** : Your admin username or dedicated LlamaCloud user
  * **Password** : The password for the user
  * **Port** : 5432 (default)


**Ensure pgvector Extension:** Connect to your database and enable the vector extension:
```


CREATE EXTENSION IFNOTEXISTSvector;


```

**Create PostgreSQL Secret:** Create `postgresql-secret.yaml`:
```


apiVersion: v1




kind: Secret




metadata:




name: postgresql-secret




namespace: default




type: Opaque




stringData:




DATABASE_HOST: "your-server.postgres.database.azure.com"




DATABASE_PORT: "5432"




DATABASE_NAME: "llamacloud"




DATABASE_USER: "your-username"




DATABASE_PASSWORD: "your-password"


```

Apply the secret:
Terminal window```


kubectlapply-fpostgresql-secret.yaml


```

### Azure Cache for Redis
[Section titled “Azure Cache for Redis”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/setup/#azure-cache-for-redis)
**Click to expand Redis configuration**
#### Requirements:
[Section titled “Requirements:”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/setup/#requirements-1)
  * **Tier** : Standard or Premium (Basic not supported for clustering)
  * **Configuration** : Default configuration works
  * **Networking** : Accessible from your AKS cluster


#### Gather Credentials:
[Section titled “Gather Credentials:”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/setup/#gather-credentials-1)
**From Azure Portal:**
  1. Navigate to your **Azure Cache for Redis** instance
  2. Go to **Settings** → **Access keys**
  3. Copy the **Primary connection string**


**Connection String Format:**
```

redis://your-redis-name.redis.cache.windows.net:6380

```

**For SSL Connection (Recommended):**
```

rediss://your-redis-name.redis.cache.windows.net:6380,password=your-primary-access-key,ssl=True

```

**Required Information:**
  * **Redis Host** : `your-redis-name.redis.cache.windows.net`
  * **Port** : 6380 (SSL) or 6379 (non-SSL)
  * **Access Key** : Primary or Secondary access key from the portal


**Create Redis Secret:** Create `redis-secret.yaml`:
```


apiVersion: v1




kind: Secret




metadata:




name: redis-secret




namespace: default




type: Opaque




stringData:




REDIS_SCHEME: "rediss"# Use "redis" for non-SSL




REDIS_HOST: "your-redis-name.redis.cache.windows.net"




REDIS_PORT: "6380"# Use "6379" for non-SSL




REDIS_PASSWORD: "your-primary-access-key"


```

Apply the secret:
Terminal window```


kubectlapply-fredis-secret.yaml


```

### Azure Service Bus
[Section titled “Azure Service Bus”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/setup/#azure-service-bus)
**Click to expand Service Bus configuration**
#### Requirements:
[Section titled “Requirements:”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/setup/#requirements-2)
  * **Tier** : Standard or higher (Basic tier lacks required features)
  * **Configuration** : Namespace with appropriate access policies
  * **Permissions** : Manage, Send, and Listen rights required


#### Gather Credentials:
[Section titled “Gather Credentials:”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/setup/#gather-credentials-2)
**From Azure Portal:**
  1. Navigate to your **Service Bus Namespace**
  2. Go to **Settings** → **Shared access policies**
  3. Select or create a policy with **Manage** , **Send** , and **Listen** permissions
  4. Copy the **Primary Connection String**


**Connection String Format:**
```

Endpoint=sb://your-namespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=your-key;EntityPath=your-queue

```

**Required Information:**
  * **Service Bus Namespace** : `your-namespace.servicebus.windows.net`
  * **Policy Name** : Name of your shared access policy
  * **Primary Key** : The access key for the policy
  * **Queue Names** : LlamaCloud will create queues automatically if the policy has Manage permissions


**Create Service Bus Secret:** Create `servicebus-secret.yaml`:
```


apiVersion: v1




kind: Secret




metadata:




name: servicebus-secret




namespace: default




type: Opaque




stringData:




JOB_QUEUE_CONNECTION_STRING: "Endpoint=sb://your-namespace.servicebus.windows.net/;SharedAccessKeyName=your-policy-name;SharedAccessKey=your-access-key"


```

Apply the secret:
Terminal window```


kubectlapply-fservicebus-secret.yaml


```

### Azure Cosmos DB (MongoDB API)
[Section titled “Azure Cosmos DB (MongoDB API)”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/setup/#azure-cosmos-db-mongodb-api)
**Click to expand Cosmos DB configuration**
#### Requirements:
[Section titled “Requirements:”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/setup/#requirements-3)
  * **API** : Must use MongoDB API (not SQL API)
  * **Configuration** : Default settings work for most deployments
  * **Networking** : Accessible from your AKS cluster
  * **Performance** : Provisioned throughput or serverless


#### Gather Credentials:
[Section titled “Gather Credentials:”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/setup/#gather-credentials-3)
**From Azure Portal:**
  1. Navigate to your **Azure Cosmos DB account**
  2. Verify it’s using the **MongoDB API** (check the API type in Overview)
  3. Go to **Settings** → **Keys**
  4. Copy the **Primary Connection String** or **Secondary Connection String**


**Connection String Format:**
```

mongodb://account-name:primary-key@account-name.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@account-name@

```

**Required Information:**
  * **Account Name** : Your Cosmos DB account name
  * **Primary Key** : The primary or secondary key from the portal
  * **Connection String** : Full MongoDB connection string (recommended)
  * **Database Name** : LlamaCloud will create `llamacloud` database automatically


**Important Notes:**
  * **Must use MongoDB API** : SQL API or other APIs won’t work
  * **SSL Required** : Azure Cosmos DB requires SSL connections
  * **Auto-scaling** : Consider enabling auto-scale for variable workloads


**Create Cosmos DB Secret:** Create `cosmosdb-secret.yaml`:
```


apiVersion: v1




kind: Secret




metadata:




name: cosmosdb-secret




namespace: default




type: Opaque




stringData:




MONGODB_URL: "mongodb://your-account:your-primary-key@your-account.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@your-account@"


```

Apply the secret:
Terminal window```


kubectlapply-fcosmosdb-secret.yaml


```

### Azure Blob Storage
[Section titled “Azure Blob Storage”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/setup/#azure-blob-storage)
**Click to expand Blob Storage configuration**
#### Requirements:
[Section titled “Requirements:”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/setup/#requirements-4)
  * **Performance** : Standard performance tier is sufficient
  * **Access** : Account key or managed identity access


#### Required Storage Containers:
[Section titled “Required Storage Containers:”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/setup/#required-storage-containers)
LlamaCloud requires these containers to exist in your storage account:
  * `llama-platform-parsed-documents`
  * `llama-platform-etl`
  * `llama-platform-external-components`
  * `llama-platform-file-parsing`
  * `llama-platform-raw-files`
  * `llama-cloud-parse-output`
  * `llama-platform-file-screenshots`
  * `llama-platform-extract-output`


#### Gather Credentials:
[Section titled “Gather Credentials:”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/setup/#gather-credentials-4)
**From Azure Portal:**
  1. Navigate to your **Storage Account**
  2. Go to **Security + networking** → **Access keys**
  3. Copy **Storage account name** and **Key** (key1 or key2)


**Required Information:**
  * **Storage Account Name** : The name of your storage account
  * **Storage Account Key** : Primary or secondary access key
  * **Storage Endpoint** : `https://yourstorageaccount.blob.core.windows.net`
  * **Azure Region** : The region where your storage account is located (e.g., `eastus`, `westus2`)


**Required Storage Containers:** LlamaCloud requires these containers to exist in your storage account:
  * `llama-platform-parsed-documents`
  * `llama-platform-etl`
  * `llama-platform-external-components`
  * `llama-platform-file-parsing`
  * `llama-platform-raw-files`
  * `llama-cloud-parse-output`
  * `llama-platform-file-screenshots`
  * `llama-platform-extract-output`


**Create Blob Storage Secret:** Create `blobstorage-secret.yaml`:
```


apiVersion: v1




kind: Secret




metadata:




name: blobstorage-secret




namespace: default




type: Opaque




stringData:




JCLOUDS_IDENTITY: "your-storage-account-name"




JCLOUDS_CREDENTIAL: "your-storage-account-key"




JCLOUDS_REGION: "eastus"# Change to your Azure region




JCLOUDS_ENDPOINT: "https://yourstorageaccount.blob.core.windows.net"


```

Apply the secret:
Terminal window```


kubectlapply-fblobstorage-secret.yaml


```

### Azure OpenAI
[Section titled “Azure OpenAI”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/setup/#azure-openai)
**Click to expand Azure OpenAI configuration**
#### Requirements:
[Section titled “Requirements:”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/setup/#requirements-5)
  * **Required Models** : gpt-4o, gpt-4o-mini, or other supported models
  * **Deployment** : Models must be deployed, not just available


#### Gather Credentials:
[Section titled “Gather Credentials:”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/setup/#gather-credentials-5)
If using Azure OpenAI instead of OpenAI API:
**From Azure Portal:**
  1. Navigate to your **Azure OpenAI** resource
  2. Go to **Resource Management** → **Keys and Endpoint**
  3. Copy **Endpoint** and **KEY 1** or **KEY 2**
  4. Go to **Model deployments** to get deployment names


**Required Information for Each Model:**
  * **Endpoint** : `https://your-resource.openai.azure.com`
  * **API Key** : One of the access keys
  * **Deployment Names** : The actual deployment names (may be model names by default, e.g. `gpt-4o-mini` or a custom name, e.g. `our-fast-gpt`)
  * **API Version** : Use `2024-12-01-preview` or latest


**Example Deployment Mapping:**
```

Model: gpt-4o → Deployment Name: my-gpt-4o-deployment


Model: gpt-4o-mini → Deployment Name: my-gpt-4o-mini-deployment

```

**Create Azure OpenAI Secret:** Create `azure-openai-secret.yaml`:
```


apiVersion: v1




kind: Secret




metadata:




name: azure-openai-secret




namespace: default




type: Opaque




stringData:




AZURE_OPENAI_GPT_4O_API_KEY: "your-api-key"




AZURE_OPENAI_GPT_4O_BASE_URL: "https://your-resource.openai.azure.com"




AZURE_OPENAI_GPT_4O_DEPLOYMENT_NAME: "your-gpt-4o-deployment-name"




AZURE_OPENAI_GPT_4O_API_VERSION: "2024-12-01-preview"




# Add additional models as needed:




# AZURE_OPENAI_GPT_4O_MINI_API_KEY: "your-api-key"




# AZURE_OPENAI_GPT_4O_MINI_BASE_URL: "https://your-resource.openai.azure.com"




# AZURE_OPENAI_GPT_4O_MINI_DEPLOYMENT_NAME: "your-gpt-4o-mini-deployment-name"




# AZURE_OPENAI_GPT_4O_MINI_API_VERSION: "2024-12-01-preview"


```

Apply the secret:
Terminal window```


kubectlapply-fazure-openai-secret.yaml


```

## Step 2: Configure Microsoft Entra ID (OIDC)
[Section titled “Step 2: Configure Microsoft Entra ID (OIDC)”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/setup/#step-2-configure-microsoft-entra-id-oidc)
**Click to expand Microsoft Entra ID OIDC configuration steps**
### For Microsoft Entra ID Authentication:
[Section titled “For Microsoft Entra ID Authentication:”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/setup/#for-microsoft-entra-id-authentication)
  1. Navigate to **Microsoft Entra ID** → **App registrations**
  2. Find or create your application registration
  3. Configure redirect URI:


  * under “Select a platform”, select **“Web”** (not SPA!)
  * if you are port-forwarding: `http://localhost:3000/api/v1/auth/callback`
  * if you have ingress configured: `https://<internal-domain-for-llamacloud>/api/v1/auth/callback`


  1. Go to **Overview** to get **Application (client) ID**
  2. Go to **Certificates & secrets** to get or create a **client secret**
  3. Note your **Tenant ID** from the Overview page


### Required Information:
[Section titled “Required Information:”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/setup/#required-information)
  * **Tenant ID** : Your Microsoft Entra ID tenant ID
  * **Client ID** : Application (client) ID
  * **Client Secret** : Secret value (not the secret ID)
  * **Discovery URL** : `https://login.microsoftonline.com/{tenant-id}/v2.0/.well-known/openid-configuration`


The OIDC configuration will be set directly in your Helm values file with the client secret included.
## Step 3: Create License Key Secret
[Section titled “Step 3: Create License Key Secret”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/setup/#step-3-create-license-key-secret)
Contact your LlamaIndex account manger (or enterprise-support@runllama.ai) to obtain your LlamaCloud license key.
Create your LlamaCloud license key secret:
Create `license-secret.yaml`:
```


apiVersion: v1




kind: Secret




metadata:




name: license-secret




namespace: default




type: Opaque




stringData:




license-key: <LLAMACLOUD-LICENSE-KEY>


```

Apply the secret:
Terminal window```


kubectlapply-flicense-secret.yaml


```

## Step 4: Configure Helm Values
[Section titled “Step 4: Configure Helm Values”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/setup/#step-4-configure-helm-values)
Create your `azure-values.yaml` file with the appropriate configuration:
### Complete Azure Configuration:
[Section titled “Complete Azure Configuration:”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/setup/#complete-azure-configuration)
```


license:




secret: "license-secret"




# External Azure services



postgresql:




secret: "postgresql-secret"




redis:




secret: "redis-secret"




rabbitmq:




secret: "servicebus-secret"




mongodb:




secret: "cosmosdb-secret"





config:




authentication:




# Microsoft Entra ID OIDC configuration




oidc:




enabled: true




discoveryUrl: "https://login.microsoftonline.com/<TENANT-ID>/v2.0/.well-known/openid-configuration"




clientId: <CLIENT-ID>




clientSecret: <CLIENT-SECRET>





llms:




# Azure OpenAI via secrets (or use OpenAI secret if preferred)




azureOpenAi:




secret: "azure-openai-credentials"





storageBuckets:




provider: "azure"




# S3Proxy for Azure Blob Storage




s3proxy:




config:




S3PROXY_ENDPOINT: "http://0.0.0.0:80"




S3PROXY_AUTHORIZATION: "none"




S3PROXY_IGNORE_UNKNOWN_HEADERS: "true"




S3PROXY_CORS_ALLOW_ORIGINS: "*"




JCLOUDS_PROVIDER: "azureblob"




JCLOUDS_AZUREBLOB_AUTH: "azureKey"




AZURE_STORAGE_ACCOUNT: <AZURE-STORAGE-ACCOUNT>




AZURE_STORAGE_KEY: <AZURE-STORAGE-KEY>


```

**Note LLM Provider Options:** While this guide uses Azure OpenAI, LlamaCloud supports many LLM providers including but not limited to:
  * **OpenAI** (GPT-4o, GPT-4.1, GPT-5, …)
  * **Anthropic** (Claude 4.0 Sonnet, Claude 3 Opus, …)
  * **Google** (Gemini 2.5 Pro, Gemini 2.0 Flash, …)


For complete setup instructions for other providers, see the [LLM Integrations Overview](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/overview).
## Step 5: Deploy LlamaCloud
[Section titled “Step 5: Deploy LlamaCloud”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/setup/#step-5-deploy-llamacloud)
Terminal window```

# Add Helm repository



helmrepoaddllamaindexhttps://run-llama.github.io/helm-charts




helmrepoupdate




# Install LlamaCloud



helminstallllamacloudllamaindex/llamacloud-fazure-values.yaml--namespacellamacloud




# Monitor deployment



kubectlgetpods--namespacellamacloud-w


```

## Next Steps
[Section titled “Next Steps”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/setup/#next-steps)
  * - Verify your deployment is working correctly
  * **[Troubleshooting Guide](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/troubleshooting/)** - Common issues and solutions


For additional configuration options and advanced setups, refer to the [detailed configuration guides](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/auth-modes/) in the main documentation.
