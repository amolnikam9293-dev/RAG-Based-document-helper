[Skip to content](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/db_and_queues/overview/#_top)
# Overview
##  Self-Hosting Documentation Access 
This section requires a password to access. Interested in self-hosting? [Contact sales](https://www.llamaindex.ai/contact) to learn more. 
Self-Hosting Documentation Access Granted  Logout 
LlamaCloud requires a few external dependencies — Postgres, MongoDB, Redis, and RabbitMQ.
## Requirements
[Section titled “Requirements”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/db_and_queues/overview/#requirements)
We officially support the following versions of the dependencies:
  * **Postgres**
    * Minimum Version `>=15.x`
    * Admin Access to the database. LlamaCloud will read/write and apply migrations.
    * We recommend `1 - 2 vCPUs` and `1 - 2 GBi RAM` as a starting point for the database. As your usage grows, you can scale the database accordingly.
    * Recommended Managed Services: 
      * [Azure Database for PostgreSQL](https://learn.microsoft.com/en-us/azure/postgresql/single-server/quickstart-create-server-database-portal)
  * **MongoDB**
    * Minimum Version `>=7.x`
    * We recommend `1 - 2 vCPUs` and `1 - 2 GBi RAM` as a starting point for the database. As your usage grows, you can scale the database accordingly.
    * Recommended Managed Services: 
      * [Amazon DocumentDB](https://aws.amazon.com/documentdb/)
  * **RabbitMQ**
    * Minimum Version `>=3.11.x`
    * We recommend `200 - 500m vCPUs` and `500Mi - 2GBi RAM` as a starting point for the database. As your usage grows, you can scale the database accordingly.
    * Recommended Managed Services: 
      * [Azure Service Bus](https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-messaging-overview) — see setup: [Azure Service Bus as Job Queue](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/db_and_queues/azure-service-bus)
      * [Google Cloud Marketplace](https://console.cloud.google.com/marketplace/product/google/rabbitmq)
  * **Redis**
    * Minimum Version `>=7.x`
    * We recommend `200 - 500m vCPUs` and `500Mi - 2GBi RAM` as a starting point for the database. As your usage grows, you can scale the database accordingly.
    * Recommended Managed Services: 
      * [Amazon ElastiCache](https://aws.amazon.com/elasticache/)
      * [Azure Cache for Redis](https://learn.microsoft.com/en-us/azure/azure-cache-for-redis/cache-overview)
      * [Google Cloud Memorystore](https://cloud.google.com/memorystore/docs/redis)


## External Dependency Configuration
[Section titled “External Dependency Configuration”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/db_and_queues/overview/#external-dependency-configuration)
To connect your LlamaCloud deployment to an external dependency, configure the necessary sections in your `values.yaml` file.


```


postgresql:




host: "postgresql"




port: "5432"




database: "llamacloud"




username: "llamacloud"




password: "llamacloud"





mongodb:




host: "mongodb"




port: "27017"




username: "root"




password: "password"





rabbitmq:




scheme: "amqp"




host: "rabbitmq"




port: "5672"




username: "guest"




password: "guest"





redis:




scheme: "redis"




host: "redis-master"




port: "6379"




db: 0


```

## Example Postgresql Configuration
[Section titled “Example Postgresql Configuration”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/db_and_queues/overview/#example-postgresql-configuration)
Example Postgresql installation:
```

helm upgrade --install postgresql \



oci://registry-1.docker.io/bitnamicharts/postgresql \




-f postgresql.yaml --wait --timeout 10m


```

postgresql.yaml```


image:




registry: docker.io




repository: bitnamilegacy/postgresql





auth:




enabled: true




database: llamacloud




username: llamacloud




password: llamacloud




## Ref: https://github.com/bitnami/charts/blob/main/bitnami/postgresql/values.yaml#L481



primary:




resources:




requests:




cpu: 250m




memory: 128Mi




limits:




cpu: 250m




memory: 256Mi





global:




security:




allowInsecureImages: true





resourcesPreset: micro


```

## Example MongoDB Configuration
[Section titled “Example MongoDB Configuration”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/db_and_queues/overview/#example-mongodb-configuration)
Example MongoDB installation:
```

helm upgrade --install \



mongodb oci://registry-1.docker.io/bitnamicharts/mongodb \




-f mongodb.yaml --wait --timeout 10m


```

mongodb.yaml```


image:




registry: ghcr.io




repository: xavidop/mongodb




tag: '7.0'





auth:




enabled: true




rootUser: root




rootPassword: password





global:




security:




allowInsecureImages: true





resourcesPreset: micro


```

## Example Redis Configuration
[Section titled “Example Redis Configuration”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/db_and_queues/overview/#example-redis-configuration)
Example Redis installation:
```

helm upgrade --install redis \



oci://registry-1.docker.io/bitnamicharts/redis \




-f redis.yaml --wait --timeout 10m


```

redis.yaml```


image:




registry: docker.io




repository: bitnamilegacy/redis





auth:




enabled: false




#password: "password"





tls:




enabled: false





architecture: standalone





global:




security:




allowInsecureImages: true





resourcesPreset: micro


```

## Example RabbitMQ Configuration
[Section titled “Example RabbitMQ Configuration”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/db_and_queues/overview/#example-rabbitmq-configuration)
Example RabbitMQ installation:
```

helm upgrade --install rabbitmq \



oci://registry-1.docker.io/bitnamicharts/rabbitmq \




-f rabbitmq.yaml --wait --timeout 10m


```

rabbimq.yaml```


image:




registry: docker.io




repository: bitnamilegacy/rabbitmq




digest: sha256:8a36cf44a55be2ae25cafa0376b89041412c50bbcab9fa0109713d60b2ec06fb





global:




security:




allowInsecureImages: true





auth:




username: guest




password: guest




erlangCookie: secretcookie





resourcesPreset: micro


```

## Complete Configuration Reference
[Section titled “Complete Configuration Reference”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/db_and_queues/overview/#complete-configuration-reference)
For the most up-to-date and comprehensive configuration options, refer directly to our Helm repository:
  * **[Complete values.yaml reference](https://github.com/run-llama/helm-charts/blob/main/charts/llamacloud/values.yaml)** - Full configuration options with detailed comments
  * **[External dependencies example](https://github.com/run-llama/helm-charts/blob/main/charts/llamacloud/examples/external-deps-config.yaml)** - Complete working example for external dependencies
  * **[Helm chart documentation](https://github.com/run-llama/helm-charts/blob/main/charts/llamacloud/README.md)** - Generated documentation with all configuration parameters


