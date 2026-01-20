[Skip to content](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/overview/#_top)
# Overview
##  Self-Hosting Documentation Access 
This section requires a password to access. Interested in self-hosting? [Contact sales](https://www.llamaindex.ai/contact) to learn more. 
Self-Hosting Documentation Access Granted  Logout 
LlamaCloud supports multiple LLM models through different provider access methods to power its document parsing, extraction, and AI capabilities. This section provides guidance on configuring and choosing between different model providers for your self-hosted deployment.
## Supported Models and Providers
[Section titled “Supported Models and Providers”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/overview/#supported-models-and-providers)
Model Family | Developer Direct _(Simple Setup)_ | Enterprise Cloud _(Advanced Features)_  
---|---|---  
**OpenAI GPT** GPT-4o, GPT-4.1, GPT-5, GPT-5  
**Anthropic Claude** Claude 4.0 Sonnet, Claude 3.5 Haiku, Claude 3 Opus  
**Google Gemini** Gemini 2.5 Pro, Gemini 2.5 Flash, Gemini 2.0 Flash  
## Configuration Methods
[Section titled “Configuration Methods”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/overview/#configuration-methods)
### External Secrets (Recommended)
[Section titled “External Secrets (Recommended)”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/overview/#external-secrets-recommended)
Configure LLM credentials using Kubernetes secrets and reference them in your Helm values:
```


config:




llms:




openai:




secret: <your-openai-secret>




anthropic:




secret: <your-anthropic-secret>




gemini:




secret: <your-gemini-secret>




azureOpenAi:




secret: <your-azureOpenAi-secret>




awsBedrock:




secret: <your-bedrock-secret>




googleVertexAi:




secret: <your-vertex-secret>


```

Helm Values Configuration (Legacy)
Some providers support direct configuration in Helm values (being deprecated):
```


backend:




config:




openAiApiKey: "your-api-key"


```

## Next Steps
[Section titled “Next Steps”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/overview/#next-steps)
Choose your LLM provider and follow the detailed setup instructions:
  * [Google Gemini API Setup](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/google-gemini)
  * [Google Vertex AI Setup](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/google-vertex-ai)


## Troubleshooting
[Section titled “Troubleshooting”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/overview/#troubleshooting)
### Verification Steps
[Section titled “Verification Steps”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/overview/#verification-steps)
After configuration, verify your setup by:
  1. Using the LlamaCloud admin UI to confirm available models
  2. Testing with a simple parsing or extraction task


### Common Issues
[Section titled “Common Issues”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/overview/#common-issues)
  1. **Model not available** : Check provider documentation for model availability in your region
  2. **Authentication failures** : Verify API keys and permissions
  3. **Rate limiting** : Monitor usage and implement appropriate quotas


