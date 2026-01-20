[Skip to content](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/azure-openai/#_top)
# Azure OpenAI Setup
##  Self-Hosting Documentation Access 
This section requires a password to access. Interested in self-hosting? [Contact sales](https://www.llamaindex.ai/contact) to learn more. 
Self-Hosting Documentation Access Granted  Logout 
LlamaCloud supports Azure OpenAI as an enterprise-grade alternative to OpenAI for organizations requiring enhanced compliance, security, and private deployments. This page guides you through configuring Azure OpenAI integration with your self-hosted LlamaCloud deployment.
## Prerequisites
[Section titled “Prerequisites”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/azure-openai/#prerequisites)
  * A valid Azure OpenAI account
  * Azure OpenAI resource deployed in Azure
  * Access and quota for the supported models: 
    * `gpt-4o`
    * `gpt-4o-mini`
    * `gpt-4.1`
    * `gpt-4.1-mini`
    * `gpt-4.1-nano`
    * `gpt-5`
    * `gpt-5-mini`
    * `gpt-5-nano`
    * `text-embedding-3-small`
    * `text-embedding-3-large`
    * `whisper-1`


## Environment Variables
[Section titled “Environment Variables”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/azure-openai/#environment-variables)
Azure OpenAI supports per-model configuration using environment variables. Each model uses its own set of credentials:
### Environment Variable Pattern
[Section titled “Environment Variable Pattern”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/azure-openai/#environment-variable-pattern)
  * `AZURE_OPENAI_<MODEL_NAME>_API_KEY` - Deployment API key
  * `AZURE_OPENAI_<MODEL_NAME>_BASE_URL` - Azure OpenAI endpoint
  * `AZURE_OPENAI_<MODEL_NAME>_DEPLOYMENT_NAME` - Deployment name (not model name)
  * `AZURE_OPENAI_<MODEL_NAME>_API_VERSION` - API version


### Supported Models
[Section titled “Supported Models”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/azure-openai/#supported-models)
  * **GPT-4o** : `AZURE_OPENAI_GPT_4O_*`
  * **GPT-4o Mini** : `AZURE_OPENAI_GPT_4O_MINI_*`
  * **GPT-4.1** : `AZURE_OPENAI_GPT_4_1_*`
  * **GPT-4.1 Mini** : `AZURE_OPENAI_GPT_4_1_MINI_*`
  * **GPT-4.1 Nano** : `AZURE_OPENAI_GPT_4_1_NANO_*`
  * **GPT-5** : `AZURE_OPENAI_GPT_5_*`
  * **GPT-5 Mini** : `AZURE_OPENAI_GPT_5_MINI_*`
  * **GPT-5 Nano** : `AZURE_OPENAI_GPT_5_NANO_*`
  * **Text Embedding 3 Small** : `AZURE_OPENAI_TEXT_EMBEDDING_3_SMALL_*`
  * **Text Embedding 3 Large** : `AZURE_OPENAI_TEXT_EMBEDDING_3_LARGE_*`
  * **Whisper 1** : `AZURE_OPENAI_WHISPER_1_*`


## Configuration
[Section titled “Configuration”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/azure-openai/#configuration)
Azure OpenAI uses per-model configuration with separate credentials for each model. Follow these steps:
### Step 1: Gather Azure OpenAI Information
[Section titled “Step 1: Gather Azure OpenAI Information”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/azure-openai/#step-1-gather-azure-openai-information)
For each model you want to use, collect:
  * **API Key** : From your Azure OpenAI resource’s “Keys and Endpoint” section
  * **Base URL** : Your Azure endpoint (e.g., `https://your-resource.openai.azure.com`)
  * **Deployment Name** : The name of your model deployment (not the model name)
  * **API Version** : Current version is `2024-12-01-preview`


### Step 2: Create Kubernetes Secret
[Section titled “Step 2: Create Kubernetes Secret”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/azure-openai/#step-2-create-kubernetes-secret)
Create a secret with your Azure OpenAI credentials for each model:
```


apiVersion: v1




kind: Secret




metadata:




name: azure-openai-credentials




type: Opaque




stringData:




# GPT-4o configuration




AZURE_OPENAI_GPT_4O_API_KEY: "your-gpt-4o-api-key"




AZURE_OPENAI_GPT_4O_BASE_URL: "https://your-resource.openai.azure.com"




AZURE_OPENAI_GPT_4O_DEPLOYMENT_NAME: "your-gpt-4o-deployment"




AZURE_OPENAI_GPT_4O_API_VERSION: "2024-12-01-preview"





# GPT-4o Mini configuration




AZURE_OPENAI_GPT_4O_MINI_API_KEY: "your-gpt-4o-mini-api-key"




AZURE_OPENAI_GPT_4O_MINI_BASE_URL: "https://your-resource.openai.azure.com"




AZURE_OPENAI_GPT_4O_MINI_DEPLOYMENT_NAME: "your-gpt-4o-mini-deployment"




AZURE_OPENAI_GPT_4O_MINI_API_VERSION: "2024-12-01-preview"





# Add other models as needed...


```

Apply the secret:
Terminal window```


kubectlapply-fazure-openai-secret.yaml


```

### Step 3: Configure Helm Values
[Section titled “Step 3: Configure Helm Values”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/azure-openai/#step-3-configure-helm-values)
Reference the secret in your Helm configuration:
```


config:




llms:




azureOpenAi:




secret: "azure-openai-credentials"


```

Direct Configuration
```


config:




llms:




azureOpenAi:




deployments: []




# - model: "gpt-4o-mini"




#   deploymentName: "gpt-4o-mini"




#   apiKey: ""




#   baseUrl: "https://api.openai.com/v1"




#   apiVersion: "2024-08-06"


```

## Finding Azure OpenAI Configuration Values
[Section titled “Finding Azure OpenAI Configuration Values”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/azure-openai/#finding-azure-openai-configuration-values)
### Base URL
[Section titled “Base URL”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/azure-openai/#base-url)
  1. Go to your Azure OpenAI resource in the Azure Portal
  2. Navigate to **Resource Management** → **Keys and Endpoint**
  3. Copy the **Endpoint** value (format: `https://your-resource.openai.azure.com`)


### API Key
[Section titled “API Key”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/azure-openai/#api-key)
  1. In the same **Keys and Endpoint** section
  2. Copy either **KEY 1** or **KEY 2**


### Deployment Name
[Section titled “Deployment Name”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/azure-openai/#deployment-name)
  1. Go to **Model deployments** in your Azure OpenAI resource
  2. Use the **Deployment name** (not the Model name)
  3. Example: If you have a deployment called “my-gpt-4o” using the “gpt-4o” model, use “my-gpt-4o”


### API Version
[Section titled “API Version”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/azure-openai/#api-version)
  * Use the latest stable version: `2024-12-01-preview`
  * Check [Azure OpenAI API reference](https://docs.microsoft.com/en-us/azure/cognitive-services/openai/reference) for current versions


## Verification
[Section titled “Verification”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/azure-openai/#verification)
After configuration, verify your Azure OpenAI integration:
  1. **Verify in Admin UI** : Check available models in the LlamaCloud admin interface
  2. **Test functionality** : Upload a document to confirm Azure OpenAI models are working


## Troubleshooting
[Section titled “Troubleshooting”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/azure-openai/#troubleshooting)
### Common Issues
[Section titled “Common Issues”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/azure-openai/#common-issues)
#### Authentication Errors
[Section titled “Authentication Errors”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/azure-openai/#authentication-errors)
```

Error: Access denied due to invalid subscription key

```

**Solution** :
  * Verify your API key is correct
  * Ensure the key hasn’t expired
  * Check that you’re using the right key for the deployment


#### Deployment Not Found
[Section titled “Deployment Not Found”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/azure-openai/#deployment-not-found)
```

Error: The API deployment for this resource does not exist

```

**Solution** :
  * Verify the deployment name exactly matches what’s in Azure
  * Check that the deployment is in the same region as your resource
  * Ensure the deployment is not paused or stopped


#### API Version Issues
[Section titled “API Version Issues”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/azure-openai/#api-version-issues)
```

Error: Invalid API version specified

```

**Solution** :
  * Use a supported API version (e.g., `2024-12-01-preview`)
  * Check Azure OpenAI documentation for current versions


#### Rate Limiting
[Section titled “Rate Limiting”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/azure-openai/#rate-limiting)
```

Error: Rate limit exceeded

```

**Solution** :
  * Check your Azure OpenAI quotas
  * Consider upgrading your deployment tier
  * Implement request throttling


### Debug Steps
[Section titled “Debug Steps”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/azure-openai/#debug-steps)
  1. **Test endpoint directly** :
Terminal window```


curl-H"api-key: YOUR_KEY"\




"https://YOUR_RESOURCE.openai.azure.com/openai/deployments/YOUR_DEPLOYMENT/completions?api-version=2024-12-01-preview"


```

  2. **Verify secret mounting** :
Terminal window```


kubectlgetsecretyour-azure-openai-secret-oyaml




kubectldescribepod<pod-name>|grep-A20Environment


```

  3. **Check network connectivity** : Ensure your cluster can reach your Azure OpenAI endpoint


