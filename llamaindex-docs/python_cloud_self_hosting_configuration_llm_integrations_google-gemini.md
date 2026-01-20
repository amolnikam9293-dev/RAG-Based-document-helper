[Skip to content](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/google-gemini/#_top)
# Google Gemini API Setup
##  Self-Hosting Documentation Access 
This section requires a password to access. Interested in self-hosting? [Contact sales](https://www.llamaindex.ai/contact) to learn more. 
Self-Hosting Documentation Access Granted  Logout 
LlamaCloud supports Google Gemini API for direct access to Google’s AI models with simple API key authentication. This provides a straightforward alternative to Google Vertex AI when you don’t need enterprise Google Cloud Platform features.
## Prerequisites
[Section titled “Prerequisites”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/google-gemini/#prerequisites)
  * A valid Google account
  * Google Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
  * Access and quota for supported models: 
    * Gemini 1.5 Pro
    * Gemini 1.5 Flash
    * Gemini 2.0 Flash


## Environment Variables
[Section titled “Environment Variables”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/google-gemini/#environment-variables)
The Google Gemini API integration uses a single environment variable:
  * `GOOGLE_GEMINI_API_KEY` - Your Google Gemini API key (required)


## Configuration
[Section titled “Configuration”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/google-gemini/#configuration)
Follow these steps to configure Google Gemini API integration:
### Step 1: Get Google Gemini API Key
[Section titled “Step 1: Get Google Gemini API Key”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/google-gemini/#step-1-get-google-gemini-api-key)
Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
### Step 2: Create Kubernetes Secret
[Section titled “Step 2: Create Kubernetes Secret”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/google-gemini/#step-2-create-kubernetes-secret)
Create a secret with your Google Gemini API key:
```


apiVersion: v1




kind: Secret




metadata:




name: gemini-credentials




type: Opaque




stringData:




GOOGLE_GEMINI_API_KEY: "your-api-key-here"


```

Apply the secret:
Terminal window```


kubectlapply-fgemini-secret.yaml


```

### Step 3: Configure Helm Values
[Section titled “Step 3: Configure Helm Values”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/google-gemini/#step-3-configure-helm-values)
Reference the secret in your Helm configuration:
```

# External Secret



config:




llms:




gemini:




secret: "gemini-credentials"




# or direct configuration



config:




llms:




gemini:




apiKey: "your-api-key-here"


```

## Verification
[Section titled “Verification”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/google-gemini/#verification)
After configuration, verify your Google Gemini integration:
  1. **Verify in Admin UI** : Check available Google models in LlamaCloud admin interface
  2. **Test functionality** : Upload a document to confirm Gemini models are working


## Troubleshooting
[Section titled “Troubleshooting”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/google-gemini/#troubleshooting)
### Common Issues
[Section titled “Common Issues”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/google-gemini/#common-issues)
#### API Key Invalid
[Section titled “API Key Invalid”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/google-gemini/#api-key-invalid)
```

Error: API key not valid

```

**Solution** :
  * Ensure your API key is correctly set and hasn’t expired
  * Verify the key is from Google AI Studio
  * Check that the API key has proper permissions


#### Quota Exceeded
[Section titled “Quota Exceeded”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/google-gemini/#quota-exceeded)
```

Error: Quota exceeded

```

**Solution** :
  * Check your Google AI Studio quotas and usage limits
  * Consider upgrading your plan or requesting quota increases
  * Monitor API usage to avoid rate limiting


#### Model Access Issues
[Section titled “Model Access Issues”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/google-gemini/#model-access-issues)
```

Error: Model not found or access denied

```

**Solution** :
  * Verify the model is available in your region
  * Check if you have access to the specific model
  * Ensure your API key has model access permissions


### Debug Steps
[Section titled “Debug Steps”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/google-gemini/#debug-steps)
  1. **Test Gemini API directly** :
Terminal window```


curl-H"Content-Type: application/json"\




-H"x-goog-api-key: YOUR_API_KEY"\




-d'{"contents":[{"parts":[{"text":"Hello"}]}]}'\




"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"


```

  2. **Verify secret mounting** :
Terminal window```


kubectlgetsecretgemini-credentials-oyaml




kubectldescribepod<pod-name>|grep-A20Environment


```

  3. **Check network connectivity** : Ensure your cluster can reach `generativelanguage.googleapis.com`


