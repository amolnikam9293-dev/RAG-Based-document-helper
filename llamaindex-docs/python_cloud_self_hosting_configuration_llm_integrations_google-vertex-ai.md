[Skip to content](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/google-vertex-ai/#_top)
# Google Vertex AI Setup
##  Self-Hosting Documentation Access 
This section requires a password to access. Interested in self-hosting? [Contact sales](https://www.llamaindex.ai/contact) to learn more. 
Self-Hosting Documentation Access Granted  Logout 
LlamaCloud supports Google Vertex AI for enterprise-grade access to Google’s AI models through Google Cloud Platform. Vertex AI provides advanced features like private endpoints, enhanced security, and deep GCP integration compared to the direct Gemini API.
## Prerequisites
[Section titled “Prerequisites”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/google-vertex-ai/#prerequisites)
  * A valid Google Cloud Platform account
  * Google Cloud project with Vertex AI API enabled
  * Service account with appropriate IAM permissions
  * Access and quota for supported models: 
    * Gemini 1.5 Pro
    * Gemini 1.5 Flash
    * Gemini 2.0 Flash


## Environment Variables
[Section titled “Environment Variables”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/google-vertex-ai/#environment-variables)
The Google Vertex AI integration uses the following environment variables:
  * `GOOGLE_VERTEX_AI_ENABLED` - Set to “true” to enable Google Vertex AI (required)
  * `GOOGLE_VERTEX_AI_PROJECT_ID` - Google Cloud project ID (required)
  * `GOOGLE_VERTEX_AI_LOCATION` - Google Cloud location/region (optional, defaults to `us-central1`)
  * `GOOGLE_VERTEX_AI_CREDENTIALS_JSON` - Service account credentials JSON string (required)


## Configuration
[Section titled “Configuration”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/google-vertex-ai/#configuration)
Follow these steps to configure Google Vertex AI integration:
### Step 1: Setup Google Cloud Project
[Section titled “Step 1: Setup Google Cloud Project”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/google-vertex-ai/#step-1-setup-google-cloud-project)
  1. Create or use an existing Google Cloud project
  2. Enable the Vertex AI API: 
Terminal window```


gcloudservicesenableaiplatform.googleapis.com


```

  3. Ensure billing is enabled for the project


### Step 2: Create Service Account
[Section titled “Step 2: Create Service Account”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/google-vertex-ai/#step-2-create-service-account)
Create a service account with the required IAM permissions:
#### Required IAM Permissions
[Section titled “Required IAM Permissions”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/google-vertex-ai/#required-iam-permissions)
Your service account needs the following permissions:
  * `aiplatform.endpoints.predict`
  * `aiplatform.endpoints.explain`
  * `ml.models.predict` (for legacy model versions)


#### Option 1: Use Predefined Role
[Section titled “Option 1: Use Predefined Role”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/google-vertex-ai/#option-1-use-predefined-role)
Terminal window```


gcloudiamservice-accountscreatellamacloud-vertex\




--description="Service account for LlamaCloud Vertex AI"\




--display-name="LlamaCloud Vertex AI"





gcloudprojectsadd-iam-policy-bindingPROJECT_ID\




--member="serviceAccount:llamacloud-vertex@PROJECT_ID.iam.gserviceaccount.com"\




--role="roles/aiplatform.user"


```

#### Option 2: Custom Role
[Section titled “Option 2: Custom Role”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/google-vertex-ai/#option-2-custom-role)
Create a custom role with minimal permissions:
```



"title": "LlamaCloud Vertex AI User",




"description": "Custom role for LlamaCloud Vertex AI access",




"stage": "GA",




"includedPermissions": [




"aiplatform.endpoints.predict",




"aiplatform.endpoints.explain",




"ml.models.predict"




```

### Step 3: Generate Service Account Key
[Section titled “Step 3: Generate Service Account Key”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/google-vertex-ai/#step-3-generate-service-account-key)
Generate a JSON key for the service account:
Terminal window```


gcloudiamservice-accountskeyscreatellamacloud-vertex-key.json\




--iam-account=llamacloud-vertex@PROJECT_ID.iam.gserviceaccount.com


```

### Step 4: Create Kubernetes Secret
[Section titled “Step 4: Create Kubernetes Secret”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/google-vertex-ai/#step-4-create-kubernetes-secret)
Create a secret with your Vertex AI credentials:
```


apiVersion: v1




kind: Secret




metadata:




name: vertex-ai-credentials




type: Opaque




stringData:




GOOGLE_VERTEX_AI_ENABLED: "true"




GOOGLE_VERTEX_AI_PROJECT_ID: "your-project-id"




GOOGLE_VERTEX_AI_LOCATION: "us-central1"




GOOGLE_VERTEX_AI_CREDENTIALS_JSON: |





"type": "service_account",




"project_id": "your-project-id",




"private_key_id": "key-id",




"private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",




"client_email": "llamacloud-vertex@your-project-id.iam.gserviceaccount.com",




"client_id": "client-id",




"auth_uri": "https://accounts.google.com/o/oauth2/auth",




"token_uri": "https://oauth2.googleapis.com/token",




"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",




"client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/llamacloud-vertex%40your-project-id.iam.gserviceaccount.com"



```

Apply the secret:
Terminal window```


kubectlapply-fvertex-ai-secret.yaml


```

### Step 5: Configure Helm Values
[Section titled “Step 5: Configure Helm Values”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/google-vertex-ai/#step-5-configure-helm-values)
Reference the secret in your Helm configuration:
```

# External Secret (recommended)



config:




llms:




googleVertexAi:




secret: "vertex-ai-credentials"




# or direct configuration (not recommended for production)



config:




llms:




googleVertexAi:




projectId: "your-project-id"




location: "us-central1"




credentialsJson: |





"type": "service_account",




```

## Verification
[Section titled “Verification”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/google-vertex-ai/#verification)
After configuration, verify your Google Vertex AI integration:
  1. **Verify in Admin UI** : Check available Google models in LlamaCloud admin interface
  2. **Test functionality** : Upload a document to confirm Vertex AI models are working


## Troubleshooting
[Section titled “Troubleshooting”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/google-vertex-ai/#troubleshooting)
### Common Issues
[Section titled “Common Issues”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/google-vertex-ai/#common-issues)
#### Service Account Permissions
[Section titled “Service Account Permissions”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/google-vertex-ai/#service-account-permissions)
```

Error: Permission denied

```

**Solution** :
  * Verify your service account has the required IAM permissions
  * Ensure `aiplatform.endpoints.predict` permission is granted
  * Check that the service account is active and not disabled


#### Project Configuration
[Section titled “Project Configuration”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/google-vertex-ai/#project-configuration)
```

Error: Project not found or Vertex AI API not enabled

```

**Solution** :
  * Ensure Vertex AI API is enabled in your Google Cloud project
  * Verify the project ID is correct in your configuration
  * Check that billing is enabled for the project


#### Credentials Issues
[Section titled “Credentials Issues”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/google-vertex-ai/#credentials-issues)
```

Error: Could not load credentials

```

**Solution** :
  * Verify the service account JSON is properly formatted
  * Ensure all required fields are present in the credentials JSON
  * Check that the private key is properly escaped in the secret
  * Verify the service account key hasn’t been deleted or expired


#### Region Restrictions
[Section titled “Region Restrictions”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/google-vertex-ai/#region-restrictions)
```

Error: Model not available in region

```

**Solution** :
  * Check model availability in your specified region
  * Try a different region (e.g., `us-central1`, `us-east1`)
  * Some models may not be available in all regions


### Debug Steps
[Section titled “Debug Steps”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/google-vertex-ai/#debug-steps)
  1. **Test Vertex AI authentication** :
Terminal window```


gcloudauthactivate-service-account--key-file=vertex-key.json




gcloudaimodelslist--region=us-central1


```

  2. **Verify secret mounting** :
Terminal window```


kubectlgetsecretvertex-ai-credentials-oyaml




kubectldescribepod<pod-name>|grep-A20Environment


```

  3. **Check network connectivity** : Ensure your cluster can reach `aiplatform.googleapis.com`
  4. **Test API call** :
Terminal window```


curl-XPOST\




-H"Authorization: Bearer $(gcloudauthprint-access-token)"\




-H"Content-Type: application/json"\




"https://us-central1-aiplatform.googleapis.com/v1/projects/PROJECT_ID/locations/us-central1/publishers/google/models/gemini-pro:predict"\




-d'{"instances": [{"content": "Hello"}]}'


```



