[Skip to content](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/openai/#_top)
# OpenAI Setup
##  Self-Hosting Documentation Access 
This section requires a password to access. Interested in self-hosting? [Contact sales](https://www.llamaindex.ai/contact) to learn more. 
Self-Hosting Documentation Access Granted  Logout 
LlamaCloud supports OpenAI as the primary LLM provider for document parsing, extraction, and AI capabilities. This page guides you through configuring OpenAI integration with your self-hosted LlamaCloud deployment.
## Prerequisites
[Section titled “Prerequisites”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/openai/#prerequisites)
  * A valid OpenAI account
  * OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)
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
[Section titled “Environment Variables”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/openai/#environment-variables)
The OpenAI integration uses these environment variables:
  * `OPENAI_API_KEY` - Your OpenAI API key for LlamaParse service (required)


Note: Both variables typically contain the same API key value but are used by different services within LlamaCloud.
## Configuration
[Section titled “Configuration”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/openai/#configuration)
Follow these steps to configure OpenAI integration:
### Step 1: Create Kubernetes Secret
[Section titled “Step 1: Create Kubernetes Secret”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/openai/#step-1-create-kubernetes-secret)
Create a secret with your OpenAI API key:
```


apiVersion: v1




kind: Secret




metadata:




name: openai-credentials




type: Opaque




stringData:




OPENAI_API_KEY: "sk-your-openai-api-key-here"


```

Apply the secret to your cluster:
Terminal window```


kubectlapply-fopenai-secret.yaml


```

### Step 2: Configure Helm Values
[Section titled “Step 2: Configure Helm Values”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/openai/#step-2-configure-helm-values)
Reference the secret in your Helm configuration:
```

# External Secret (recommended)



config:




llms:




openAi:




secret: "openai-credentials"




######################################################################



# or direct configuration (not recommended for production)



config:




llms:




openAi:




apiKey: sk-your-openai-api-key-here"# Sets OPENAI_API_KEY


```

## Verification
[Section titled “Verification”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/openai/#verification)
After configuration, verify your OpenAI integration:
  1. **Verify in Admin UI** : Check the LlamaCloud admin interface for available OpenAI models
  2. **Test parsing** : Upload a document to confirm OpenAI models are working


## Troubleshooting
[Section titled “Troubleshooting”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/openai/#troubleshooting)
### Common Issues
[Section titled “Common Issues”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/openai/#common-issues)
#### API Key Invalid
[Section titled “API Key Invalid”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/openai/#api-key-invalid)
```

Error: Incorrect API key provided

```

**Solution** : Verify your API key is correct and active in the OpenAI Platform
#### Rate Limiting
[Section titled “Rate Limiting”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/openai/#rate-limiting)
```

Error: Rate limit exceeded

```

**Solution** :
  * Check your OpenAI usage limits
  * Consider upgrading your OpenAI plan
  * Implement request throttling if needed


#### Quota Exceeded
[Section titled “Quota Exceeded”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/openai/#quota-exceeded)
```

Error: You exceeded your current quota

```

**Solution** :
  * Check your OpenAI billing and usage
  * Add credits to your OpenAI account
  * Set up billing alerts


#### Model Access Issues
[Section titled “Model Access Issues”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/openai/#model-access-issues)
```

Error: The model 'gpt-4o' does not exist or you do not have access to it

```

**Solution** :
  * Verify model availability in your region
  * Check if you have access to the specific model


### Debug Steps
[Section titled “Debug Steps”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/openai/#debug-steps)
  1. **Test API key directly** :
Terminal window```


curlhttps://api.openai.com/v1/models\




-H"Authorization: Bearer $OPENAI_API_KEY"


```

  2. **Check secret mounting** :
Terminal window```


kubectldescribepod<llamacloud-pod-name>|grep-A10"Environment"


```

  3. **Verify network connectivity** : Ensure your cluster can reach `api.openai.com`


