[Skip to content](https://developers.llamaindex.ai/python/cloud/self_hosting/faq/#_top)
# Frequently Asked Questions
##  Self-Hosting Documentation Access 
This section requires a password to access. Interested in self-hosting? [Contact sales](https://www.llamaindex.ai/contact) to learn more. 
Self-Hosting Documentation Access Granted  Logout 
## Which LlamaCloud services communicate with which database/queue/filestore dependencies?
[Section titled “Which LlamaCloud services communicate with which database/queue/filestore dependencies?”](https://developers.llamaindex.ai/python/cloud/self_hosting/faq/#which-llamacloud-services-communicate-with-which-databasequeuefilestore-dependencies)
  * Backend: Postgres, MongoDB, Redis, Filestore
  * Jobs Service: Postgres, MongoDB, Filestore
  * Jobs Worker: RabbitMQ, Redis, MongoDB
  * Usage: MongoDB and Redis
  * LlamaParse: Consumes from RabbitMQ, Reads/Writes from Filestore
  * LlamaParse OCR: None


## Which Features Require an LLM and what model?
[Section titled “Which Features Require an LLM and what model?”](https://developers.llamaindex.ai/python/cloud/self_hosting/faq/#which-features-require-an-llm-and-what-model)
  * Chat UI: This feature requires the customer’s OpenAI Key to have access to either the Text-Only models and/or the Multi-Modal model (if multi-modal index)
    * These keys are set up via the Helm chart:
      * ```


config:




llms:




openAi:




apiKey: <OPENAI-APIKEY>




# Name of the existing secret to use for the OpenAI API key




# secret: ""





# If you are using Azure OpenAI, you can configure it like this:




# azureOpenAi:




#  secret: ""




#  deployments: []




#  # - model: "gpt-4o-mini"




#  #   deploymentName: "gpt-4o-mini"




#  #   apiKey: ""




#  #   baseUrl: "https://api.openai.com/v1"




#  #   apiVersion: "2024-08-06"


```

  * Embeddings: Credentials to connect to an embedding model provider are input within the application directly during the Index creation workflow.
  * LlamaParse Fast: Text extraction only. No LLM.
  * LlamaParse Accurate: This mode uses the `gpt-4o` under the hood.


## LLM API Rate Limits
[Section titled “LLM API Rate Limits”](https://developers.llamaindex.ai/python/cloud/self_hosting/faq/#llm-api-rate-limits)
There will be many instances where you may run into some kind of rate limit with an LLM provider. The easiest way to debug is to view the logs, and if you see a 429 error, increase your tokens per minute limit.
## How do I adjust log levels?
[Section titled “How do I adjust log levels?”](https://developers.llamaindex.ai/python/cloud/self_hosting/faq/#how-do-i-adjust-log-levels)
```


config:




## Log level for the application (DEBUG, INFO, WARNING, ERROR, CRITICAL)




logLevel: INFO


```

## What auth modes are supported at the moment?
[Section titled “What auth modes are supported at the moment?”](https://developers.llamaindex.ai/python/cloud/self_hosting/faq/#what-auth-modes-are-supported-at-the-moment)
We support both OIDC and Basic Auth for self-hosted deployments. For more information, please refer to the [Authentication Modes documentation](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/auth-modes).
## Known Issues
[Section titled “Known Issues”](https://developers.llamaindex.ai/python/cloud/self_hosting/faq/#known-issues)
### BYOC Port-Forwarding with Custom Helm Release Names
[Section titled “BYOC Port-Forwarding with Custom Helm Release Names”](https://developers.llamaindex.ai/python/cloud/self_hosting/faq/#byoc-port-forwarding-with-custom-helm-release-names)
**Issue** : When testing BYOC deployments without ingress setup (using port-forwarding), the backend service must be reachable at `http://llamacloud-backend:8000`.
**Affected Setup** :
  * BYOC deployments without ingress configuration
  * Using `kubectl port-forward` for testing


**Workarounds** (until permanent fix is available):
  1. **Manual Service Creation** : Create an additional backend service with the expected name.
  2. **Setup Ingress** : Configure proper ingress instead of relying on port-forwarding. See the [Ingress Configuration documentation](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/ingress) for details.


**Recommendation** : For production deployments, always use proper ingress configuration rather than port-forwarding.
**Manual Service Creation**
When you do not have ingress properly configured you can use these steps as a workaround.
Create a Kuberentes `Service` object:
llamacoud-backend-service.yaml```


apiVersion: v1




kind: Service




metadata:




name: llamacloud-backend




namespace: <your namespace>




spec:




ports:




- name: http




port: 8000




protocol: TCP




targetPort: http




selector:




app.kubernetes.io/instance: llamacloud




app.kubernetes.io/name: llamacloud




type: ClusterIP




status:




loadBalancer: {}


```

Apply the object: `kubectl apply -f llamacloud-backend-service.yaml -n <your namespace>`.
You should now be able to create accounts and log into the LlamaCloud UI. If you would also like to test document parsing, you must tell the browswer how to talk to the `llamacloud-backend` service. You can do this by adding this line to your `/etc/hosts` file on your local machine:
/etc/hosts```

127.0.0.1  llamacloud-backend

```

