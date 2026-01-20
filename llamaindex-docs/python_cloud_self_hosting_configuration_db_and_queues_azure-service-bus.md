[Skip to content](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/db_and_queues/azure-service-bus/#_top)
# Azure Service Bus as Job Queue
##  Self-Hosting Documentation Access 
This section requires a password to access. Interested in self-hosting? [Contact sales](https://www.llamaindex.ai/contact) to learn more. 
Self-Hosting Documentation Access Granted  Logout 
LlamaCloud’s job queue is AMQP-compatible. You can use Azure Service Bus instead of a self-managed RabbitMQ by supplying a Service Bus connection string in your Helm values.
## Prerequisites
[Section titled “Prerequisites”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/db_and_queues/azure-service-bus/#prerequisites)
  * An Azure Service Bus namespace.
  * Namespace tier: Standard or higher (Basic is not supported).
  * A connection string with Manage, Send, and Listen permissions. 
    * Manage is needed so LlamaCloud can validate and, if necessary, create the queues on startup.
    * How to find it: <https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-dotnet-get-started-with-queues?tabs=connection-string>


## Configure via values.yaml (Recommended)
[Section titled “Configure via values.yaml (Recommended)”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/db_and_queues/azure-service-bus/#configure-via-valuesyaml-recommended)
Update your `values.yaml` as follows:
```


rabbitmq:




connectionString: "Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=<queue-name>"


```

## Configure via Kubernetes Secret (Optional)
[Section titled “Configure via Kubernetes Secret (Optional)”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/db_and_queues/azure-service-bus/#configure-via-kubernetes-secret-optional)
For production, you may prefer a secret instead of inlining credentials.
LlamaCloud reads the Azure Service Bus connection string from the `JOB_QUEUE_CONNECTION_STRING` environment variable. When supplying a Kubernetes Secret via `rabbitmq.secret`, ensure the secret contains a key named `JOB_QUEUE_CONNECTION_STRING` whose value is the full Service Bus connection string.
  1. Create a secret with the connection string:


Terminal window```


kubectlcreatesecretgenericmy-queue-secret\




--from-literal=JOB_QUEUE_CONNECTION_STRING='Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=<queue-name>'


```

  1. Reference the secret in `values.yaml`:


```


rabbitmq:




secret: my-queue-secret


```

## Verify
[Section titled “Verify”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/db_and_queues/azure-service-bus/#verify)
  * Upgrade your release and ensure pods start successfully.
  * Services will log successful connections to the job queue; check `llamacloud-worker` and `llamacloud-parse` pods for confirmation.


