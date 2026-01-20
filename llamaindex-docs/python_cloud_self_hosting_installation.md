[Skip to content](https://developers.llamaindex.ai/python/cloud/self_hosting/installation/#_top)
# Quick Start
##  Self-Hosting Documentation Access 
This section requires a password to access. Interested in self-hosting? [Contact sales](https://www.llamaindex.ai/contact) to learn more. 
Self-Hosting Documentation Access Granted  Logout 
## Before You Get Started
[Section titled “Before You Get Started”](https://developers.llamaindex.ai/python/cloud/self_hosting/installation/#before-you-get-started)
Welcome to LlamaCloud! Before you get started, please make sure you have the following prerequisites:
  * **LlamaCloud License Key**. To obtain a LlamaCloud License Key, please contact us at support@llamaindex.ai.
  * **Kubernetes cluster`>=1.28.0`** and a working installation of `kubectl`. 
    * We are largely aligned with the versions supported in [EKS](https://endoflife.date/amazon-eks), [AKS](https://learn.microsoft.com/en-us/azure/aks/supported-kubernetes-versions?tabs=azure-cli), and [GKE](https://cloud.google.com/kubernetes-engine/versioning).
  * **Helm`v3.7.0+`**
    * To install Helm, please refer to the [official Helm Documentation](https://helm.sh/docs/intro/install/).
  * **OpenAI API Key** or **Azure OpenAI Credentials**. Configuring OpenAI credentials is the easiest way to get started with your deployment. 
    * LlamaCloud tries to meet you at your organization’s needs and supports configuring more than OpenAI LLMs in including Anthropic, Bedrock, Vertex AI, and more.
    * Please refer to the docs in the **Configuration** section of the sidebar to learn more about configuring other LLMs.
  * **File Storage** : LlamaCloud must leverage your cloud provider’s object storage to store files. 
    * Please follow the [File Storage](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/file-storage) documentation to configure your deployment.
  * **Authentication Settings** : 
    * **OIDC**. OIDC is our recommended authentication mode for production deployments.
    * **Basic Auth** (email/password): As of July 24th, 2025 (`v0.5.0`), we support both `oidc` and `basic` authentication methods. This is a simpler authentication mode more suitable for staging deployments.
    * For more information, please refer to the [Authentication Modes](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/auth-modes) documentation.
  * **Credentials to External Services (See below)**.


## External Services
[Section titled “External Services”](https://developers.llamaindex.ai/python/cloud/self_hosting/installation/#external-services)
**LLamaCloud** requires the following external services to be available: **Postgres** , **MongoDB** , **RabbitMQ** and **Redis**.
Please follow the [Database and Queues](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/db_and_queues/overview) documentation to configure these services for your deployment.
## Hardware Requirements
[Section titled “Hardware Requirements”](https://developers.llamaindex.ai/python/cloud/self_hosting/installation/#hardware-requirements)
  * **Linux Instances running x86 CPUs**
    * We currently only linux/amd64 images. arm64 is not supported at this moment.
  * **Ubuntu >=22.04**
  * **> =12 vCPUs**
  * **> =80Gbi Memory**


**Warning #1** : LlamaParse, LlamaIndex’s proprietary document parser, can be a very resource-intensive deployment to run, especially if you want to maximize performance.
**Warning #2** : The base CPU/memory requirements may increase if you are running containerized deployments of LlamaCloud dependencies. (More information in the following section)
## Configure and Install Your Deployment
[Section titled “Configure and Install Your Deployment”](https://developers.llamaindex.ai/python/cloud/self_hosting/installation/#configure-and-install-your-deployment)
This section will walk you through the steps to configure a minimal LlamaCloud deployment.
### Minimal `values.yaml` configuration
[Section titled “Minimal values.yaml configuration”](https://developers.llamaindex.ai/python/cloud/self_hosting/installation/#minimal-valuesyaml-configuration)
To get a minimal LlamaCloud deployment up and running, you can create a `values.yaml` file with the following content:
  * [ OpenAI w/ OIDC Auth ](https://developers.llamaindex.ai/python/cloud/self_hosting/installation/#tab-panel-4)
  * [ Azure OpenAI w/ OIDC Auth ](https://developers.llamaindex.ai/python/cloud/self_hosting/installation/#tab-panel-5)
  * [ OpenAI w/ Basic Auth ](https://developers.llamaindex.ai/python/cloud/self_hosting/installation/#tab-panel-6)
  * [ Azure OpenAI w/ Basic Auth ](https://developers.llamaindex.ai/python/cloud/self_hosting/installation/#tab-panel-7)


```


license:




key: <LLAMACLOUD-LICENSE-KEY>





postgresql:




host: "postgresql"




port: "5432"




database: "llamacloud"




username: <POSTGRES-USERNAME>




password: <POSTGRES-PASSWORD>





mongodb:




host: "mongodb"




port: "27017"




username: <MONGODB-USERNAME>




password: <MONGODB-PASSWORD>





rabbitmq:




scheme: "amqp"




host: "rabbitmq"




port: "5672"




username: <RABBITMQ-USERNAME>




password: <RABBITMQ-PASSWORD>





redis:




scheme: "redis"




host: "redis-master"




port: "6379"




db: 0





config:




llms:




openAi:




apiKey: <OPENAI-APIKEY>





frontend:




enabled: true




parseOcr:




gpu: true





authentication:




oidc:




enabled: true




discoveryUrl: "https://login.microsoftonline.com/<TENANT-ID>/v2.0/.well-known/openid-configuration"




clientId: <CLIENT-ID>




clientSecret: <CLIENT-SECRET>


```

```


license:




key: <LLAMACLOUD-LICENSE-KEY>





postgresql:




host: "postgresql"




port: "5432"




database: "llamacloud"




username: <POSTGRES-USERNAME>




password: <POSTGRES-PASSWORD>





mongodb:




host: "mongodb"




port: "27017"




username: <MONGODB-USERNAME>




password: <MONGODB-PASSWORD>





rabbitmq:




scheme: "amqp"




host: "rabbitmq"




port: "5672"




username: <RABBITMQ-USERNAME>




password: <RABBITMQ-PASSWORD>





redis:




scheme: "redis"




host: "redis-master"




port: "6379"




db: 0





config:




llms:




azureOpenAi:




secret: ""




deployments: []





frontend:




enabled: true




parseOcr:




gpu: true





authentication:




oidc:




enabled: true




discoveryUrl: "https://login.microsoftonline.com/<TENANT-ID>/v2.0/.well-known/openid-configuration"




clientId: <CLIENT-ID>




clientSecret: <CLIENT-SECRET>


```

```


license:




key: <LLAMACLOUD-LICENSE-KEY>





postgresql:




host: "postgresql"




port: "5432"




database: "llamacloud"




username: <POSTGRES-USERNAME>




password: <POSTGRES-PASSWORD>





mongodb:




host: "mongodb"




port: "27017"




username: <MONGODB-USERNAME>




password: <MONGODB-PASSWORD>





rabbitmq:




scheme: "amqp"




host: "rabbitmq"




port: "5672"




username: <RABBITMQ-USERNAME>




password: <RABBITMQ-PASSWORD>





redis:




scheme: "redis"




host: "redis-master"




port: "6379"




db: 0





config:




llms:




openAi:




apiKey: <OPENAI-APIKEY>





frontend:




enabled: true




parseOcr:




gpu: true





authentication:




basicAuth:




enabled: true




validEmailDomain: "llamaindex.ai"# this is optional, but recommended for production deployments




jwtSecret: <YOUR-JWT-SECRET>


```

```


license:




key: <LLAMACLOUD-LICENSE-KEY>





postgresql:




host: "postgresql"




port: "5432"




database: "llamacloud"




username: <POSTGRES-USERNAME>




password: <POSTGRES-PASSWORD>





mongodb:




host: "mongodb"




port: "27017"




username: <MONGODB-USERNAME>




password: <MONGODB-PASSWORD>





rabbitmq:




scheme: "amqp"




host: "rabbitmq"




port: "5672"




username: <RABBITMQ-USERNAME>




password: <RABBITMQ-PASSWORD>





redis:




scheme: "redis"




host: "redis-master"




port: "6379"




db: 0





config:




llms:




azureOpenAi:




secret: ""




deployments: []





frontend:




enabled: true




parseOcr:




gpu: true





authentication:




basicAuth:




enabled: true




validEmailDomain: "llamaindex.ai"# this is optional, but recommended for production deployments




jwtSecret: <YOUR-JWT-SECRET>


```

## Install the Helm chart
[Section titled “Install the Helm chart”](https://developers.llamaindex.ai/python/cloud/self_hosting/installation/#install-the-helm-chart)
Terminal window```

# Add the Helm repository



helmrepoaddllamaindexhttps://run-llama.github.io/helm-charts




# Update your local Helm chart cache



helmrepoupdate




# Create the llamacloud namespace



kubectlcreatensllamacloud




# Install the Helm chart



helminstallllamacloudllamaindex/llamacloud-fvalues.yaml--namespacellamacloud


```

If you want to install a specific version of the Helm chart, you can specify the version:
Terminal window```


helminstallllamacloudllamaindex/llamacloud--versionx.y.z-fvalues.yaml--namespacellamacloud


```

## Validate the installation
[Section titled “Validate the installation”](https://developers.llamaindex.ai/python/cloud/self_hosting/installation/#validate-the-installation)
After installation, you will see the following output:
```

NNAME: llamacloud


LAST DEPLOYED: Tue Nov 18 10:12:03 2025


NAMESPACE: llamacloud


STATUS: deployed


REVISION: 1


TEST SUITE: None


NOTES:


Welcome to LlamaCloud!



View your deployment with the following:




kubectl --namespace default get pods -n llamacloud




To view LlamaCloud UI in your browser:



Run the following command:





kubectl --namespace llamacloud port-forward svc/llamacloud-web 3000:80


```

If you list the pods with `kubectl get pods -n llamacloud`, you should see the following pods:
```

NAME                                        READY   STATUS      RESTARTS     AGE


llamacloud-64f468d5cf-sqjq6                 1/1     Running     0            2m56s


llamacloud-layout-6d97b84c58-rld8x          1/1     Running     0            2m56s


llamacloud-ocr-5cc459bdd-99xgt              1/1     Running     0            2m56s


llamacloud-operator-5d4c58b854-dwnjk        1/1     Running     0            2m56s


llamacloud-parse-7ffbc786b5-r98w2           1/1     Running     0            2m56s


llamacloud-telemetry-5fc9ff8c67-fv8xj       1/1     Running     0            2m56s


llamacloud-web-b88d95588-rprhc              1/1     Running     0            2m56s


llamacloud-worker-58b95ccc6f-vqmgx          1/1     Running     0            2m56s

```

Port forward the frontend service to access the LlamaCloud UI:
Terminal window```


kubectl--namespacellamacloudport-forwardsvc/llamacloud-web3000:80


```

Open your web browser and navigate to `http://localhost:3000`. You should see the LlamaCloud UI.
## Next Steps
[Section titled “Next Steps”](https://developers.llamaindex.ai/python/cloud/self_hosting/installation/#next-steps)
Choose your deployment approach based on your needs:
### 🌩️ Cloud-Specific Deployment Guides
[Section titled “🌩️ Cloud-Specific Deployment Guides”](https://developers.llamaindex.ai/python/cloud/self_hosting/installation/#%EF%B8%8F-cloud-specific-deployment-guides)
**Recommended for most users** - Complete, opinionated guides for major cloud providers:
**[📋 Choose Your Cloud Provider →](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/overview)**
  * **Azure** : AKS + Azure-native services with Microsoft Entra ID
  * **AWS** : EKS + AWS-native services (coming soon)
  * **GCP** : GKE + GCP-native services (coming soon)


_These guides provide end-to-end instructions using cloud-native services and enterprise authentication._
### ⚙️ Custom Configuration Guides
[Section titled “⚙️ Custom Configuration Guides”](https://developers.llamaindex.ai/python/cloud/self_hosting/installation/#%EF%B8%8F-custom-configuration-guides)
**For advanced users** with specific requirements or non-standard setups:
  * [Authentication Modes](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/auth-modes) - Configure OIDC, basic auth, or custom authentication
  * [File Storage](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/file-storage) - Set up S3, Azure Blob, GCS, or other storage
  * [Database and Queues](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/db_and_queues/overview) - Configure external databases and message queues
  * [LLM Integrations](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/llm_integrations/overview) - Set up OpenAI, Azure OpenAI, Bedrock, or other LLMs
  * [Ingress Configuration](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/ingress) - Load balancers, SSL, and networking
  * [Autoscaling Configuration](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/autoscaling-configuration) - HPA and KEDA-based scaling for services
  * [Service Tuning](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/service-configurations) - Performance and scaling configurations


_Use these guides if you need custom integrations, have specific compliance requirements, or want to mix and match different services._
### 🚰 Data Sink Configuration
[Section titled “🚰 Data Sink Configuration”](https://developers.llamaindex.ai/python/cloud/self_hosting/installation/#-data-sink-configuration)
Configure at least one [Data Sink](https://developers.llamaindex.ai/python/cloud/llamacloud/integrations/data_sinks) to store the **vector embeddings** of your documents.
## More Examples and Guides
[Section titled “More Examples and Guides”](https://developers.llamaindex.ai/python/cloud/self_hosting/installation/#more-examples-and-guides)
  * there are many more configuration options available for each component. to see the full values.yaml specification, please refer to the [values.yaml](https://github.com/run-llama/helm-charts/blob/main/charts/llamacloud/values.yaml) file in the helm chart repository.
  * To see how common scenarios are configured, please refer to the `values.yaml` [examples](https://github.com/run-llama/helm-charts/tree/main/charts/llamacloud/examples) directory in the Helm chart repository.
  * Similarly, we have other configuration [docs](https://github.com/run-llama/helm-charts/tree/main/charts/llamacloud/docs) available there too for more advanced configurations.


