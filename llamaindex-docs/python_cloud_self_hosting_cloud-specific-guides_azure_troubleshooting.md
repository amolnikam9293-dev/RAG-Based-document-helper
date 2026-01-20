[Skip to content](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/troubleshooting/#_top)
# Troubleshooting Guide
##  Self-Hosting Documentation Access 
This section requires a password to access. Interested in self-hosting? [Contact sales](https://www.llamaindex.ai/contact) to learn more. 
Self-Hosting Documentation Access Granted  Logout 
This guide helps you diagnose and resolve common issues when deploying LlamaCloud on Azure. Use this after completing the [Azure Setup Guide](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/setup) if you encounter problems.
## General Debugging Commands
[Section titled “General Debugging Commands”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/troubleshooting/#general-debugging-commands)
### Pod Status and Logs
[Section titled “Pod Status and Logs”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/troubleshooting/#pod-status-and-logs)
Terminal window```

# Check all pod status



kubectlgetpods-nllamacloud-owide




# Describe problematic pods



kubectldescribepod<pod-name>-nllamacloud




# Check logs for specific services



kubectl-nllamacloudlogsdeployment/llamacloud-telemetry




kubectl-nllamacloudlogsdeployment/llamacloud-parse




kubectl-nllamacloudlogsdeployment/llamacloud-web




kubectl-nllamacloudlogsdeployment/llamacloud-worker




kubectl-nllamacloudlogsdeployment/llamacloud-ocr




kubectl-nllamacloudlogsdeployment/llamacloud-s3proxy


```

### Service and Secret Status
[Section titled “Service and Secret Status”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/troubleshooting/#service-and-secret-status)
Terminal window```

# Check services



kubectlgetsvc-nllamacloud




# Verify secrets exist



kubectlgetsecrets-nllamacloud




# Check configmaps



kubectlgetconfigmaps-nllamacloud


```

## Database Connection Issues
[Section titled “Database Connection Issues”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/troubleshooting/#database-connection-issues)
### PostgreSQL Connection Problems
[Section titled “PostgreSQL Connection Problems”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/troubleshooting/#postgresql-connection-problems)
**Symptoms:**
  * Backend pods failing to start
  * Database connection errors in logs
  * “connection refused” or “timeout” errors


**Solutions:**
  1. **Verify database connection:**
Terminal window```

# Test connection from AKS



kubectlrun-it--rmdebug--image=postgres:15--restart=Never--psql"postgresql://username:password@server.postgres.database.azure.com:5432/llamacloud"


```

  2. **Check secret values:**
Terminal window```


kubectlgetsecretpostgresql-secret-oyaml



# Verify DATABASE_HOST, DATABASE_USER, etc. are correct

```

  3. **Common fixes:**
     * Add AKS subnet to PostgreSQL firewall rules
     * Verify SSL is enabled (required by Azure Database for PostgreSQL)
     * Check database name exists
     * Verify user permissions


### Redis Connection Issues
[Section titled “Redis Connection Issues”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/troubleshooting/#redis-connection-issues)
**Symptoms:**
  * “Redis connection failed” in backend logs
  * Authentication errors
  * SSL/TLS errors


**Solutions:**
  1. **Test Redis connectivity:**
Terminal window```


kubectlrun-it--rmredis-test--image=redis:7--restart=Never--redis-cli-hyour-redis.redis.cache.windows.net-p6380--tls-ayour-access-keyping


```

  2. **Check SSL configuration:**
     * Azure Redis requires SSL on port 6380
     * Verify `REDIS_SCHEME: "rediss"` in secret
     * Ensure `REDIS_PORT: "6380"` for SSL
  3. **Verify access key:**
     * Copy primary access key exactly from Azure Portal
     * No extra spaces or characters


## Service Bus Connection Issues
[Section titled “Service Bus Connection Issues”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/troubleshooting/#service-bus-connection-issues)
**Symptoms:**
  * Jobs worker fails to start
  * “Service Bus connection failed” errors
  * Queue creation errors


**Solutions:**
  1. **Verify connection string format:**
```

Endpoint=sb://namespace.servicebus.windows.net/;SharedAccessKeyName=policy;SharedAccessKey=key

```

  2. **Check permissions:**
     * Shared access policy must have **Manage** , **Send** , and **Listen** rights
     * Standard tier or higher required (Basic not supported)
  3. **Test connectivity:**
Terminal window```

# From Azure Portal, test connection using Service Bus Explorer

```



## Cosmos DB (MongoDB) Issues
[Section titled “Cosmos DB (MongoDB) Issues”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/troubleshooting/#cosmos-db-mongodb-issues)
**Symptoms:**
  * MongoDB connection errors
  * “SSL/TLS handshake failed”
  * “API type not supported”


**Solutions:**
  1. **Verify MongoDB API:**
     * Must use MongoDB API, not SQL API
     * Check API type in Cosmos DB Overview
  2. **Check connection string:**
```

mongodb://account:key@account.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@account@

```

  3. **SSL requirements:**
     * SSL is required for Cosmos DB
     * Connection string includes `ssl=true`


## Storage Issues
[Section titled “Storage Issues”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/troubleshooting/#storage-issues)
### Blob Storage / S3Proxy Problems
[Section titled “Blob Storage / S3Proxy Problems”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/troubleshooting/#blob-storage--s3proxy-problems)
**Symptoms:**
  * File upload failures
  * S3Proxy pod crashlooping
  * “Access denied” errors


**Solutions:**
  1. **Check s3proxy logs:**
Terminal window```


kubectllogsdeployment/llamacloud-s3proxy-nllamacloud


```

  2. **Verify container names:**
     * All required containers must exist
     * Names are case-sensitive
     * Check containers in Azure Portal
  3. **Required containers:**
```

llama-platform-parsed-documents


llama-platform-etl


llama-platform-external-components


llama-platform-file-parsing


llama-platform-raw-files


llama-cloud-parse-output


llama-platform-file-screenshots


llama-platform-extract-output

```

  4. **Check s3proxy configuration:**
     * Review [s3proxy configuration docs](https://github.com/gaul/s3proxy)


## Azure OpenAI Issues
[Section titled “Azure OpenAI Issues”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/troubleshooting/#azure-openai-issues)
### Model Deployment Problems
[Section titled “Model Deployment Problems”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/troubleshooting/#model-deployment-problems)
**Symptoms:**
  * “Model not found” errors
  * “Deployment not found” errors
  * API version errors


**Solutions:**
  1. **Check job service logs:**
Terminal window```


kubectllogsdeployment/llamacloud-worker-nllamacloud


```

We run LLM integration validators on pod startup. You can find useful error logs for LLM integrations.
  2. **Verify deployment names:**
     * Use deployment name, not model name
     * Check in Azure Portal → Model deployments
  3. **Check quotas:**
     * Ensure sufficient TPM quota allocated
     * Verify deployment is not paused
  4. **API version:**
     * Use supported version: `2024-12-01-preview`
     * Check Azure OpenAI documentation for latest
  5. **Test direct access:**
Terminal window```


curl-H"api-key: YOUR_KEY"\




"https://YOUR_RESOURCE.openai.azure.com/openai/deployments/YOUR_DEPLOYMENT/completions?api-version=2024-12-01-preview"


```



## Authentication Issues
[Section titled “Authentication Issues”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/troubleshooting/#authentication-issues)
### Microsoft Entra ID OIDC Problems
[Section titled “Microsoft Entra ID OIDC Problems”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/troubleshooting/#microsoft-entra-id-oidc-problems)
**Symptoms:**
  * Authentication redirects fail
  * “Invalid client” errors
  * OIDC discovery errors


**Solutions:**
  1. **Verify app registration:**
     * Check client ID is correct
     * Verify redirect URIs are configured
     * Ensure client secret is valid (not expired)
  2. **Check discovery URL:**
```

https://login.microsoftonline.com/{tenant-id}/v2.0/.well-known/openid-configuration

```

  3. **Test OIDC endpoint:**
Terminal window```


curlhttps://login.microsoftonline.com/{tenant-id}/v2.0/.well-known/openid-configuration


```



## Pod-Specific Issues
[Section titled “Pod-Specific Issues”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/troubleshooting/#pod-specific-issues)
### Backend Pod Issues
[Section titled “Backend Pod Issues”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/troubleshooting/#backend-pod-issues)
**Common problems:**
  * Environment variable errors
  * Secret mounting failures
  * Database migration failures


**Debug steps:**
Terminal window```


kubectllogsdeployment/llamacloud--tail=100-nllamacloud




kubectldescribedeploymentllamacloud-nllamacloud




kubectlgetevents--sort-by='.lastTimestamp'-nllamacloud


```

### Frontend Pod Issues
[Section titled “Frontend Pod Issues”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/troubleshooting/#frontend-pod-issues)
**Common problems:**
  * Build failures
  * Configuration errors
  * Ingress connectivity


**Debug steps:**
Terminal window```


kubectl-nllamacloudlogsdeployment/llamacloud-web--tail=100




kubectl-nllamacloudport-forwardsvc/llamacloud-web3000:80


```

### Jobs Worker Issues
[Section titled “Jobs Worker Issues”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/troubleshooting/#jobs-worker-issues)
**Common problems:**
  * Queue connectivity
  * Job processing failures
  * Memory/CPU limits


**Debug steps:**
Terminal window```


kubectl-nllamacloudlogsdeployment/llamacloud-worker--tail=100




kubectl-nllamacloudtoppod-lapp=llamacloud-worker


```

## Network and Security Issues
[Section titled “Network and Security Issues”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/troubleshooting/#network-and-security-issues)
### AKS Networking Problems
[Section titled “AKS Networking Problems”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/troubleshooting/#aks-networking-problems)
**Symptoms:**
  * Pods cannot reach Azure services
  * DNS resolution failures
  * Intermittent connectivity


**Solutions:**
  1. **Check network security groups:**
     * Verify outbound rules allow Azure service connections
     * Check subnet NSG rules
  2. **Verify DNS:**
Terminal window```


kubectlrun-it--rmnslookup--image=busybox--restart=Never--nslookupyour-postgres.postgres.database.azure.com


```

  3. **Test private endpoints:**
     * If using private endpoints, verify routing
     * Check private DNS zones


### Ingress Issues
[Section titled “Ingress Issues”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/troubleshooting/#ingress-issues)
**Symptoms:**
  * Cannot access LlamaCloud UI externally
  * SSL certificate errors
  * Load balancer failures


**Solutions:**
  1. **Check ingress controller:**
Terminal window```


kubectlgetingress




kubectllogs-ningress-nginxdeployment/nginx-ingress-controller


```

  2. **Verify DNS configuration:**
     * Domain points to load balancer IP
     * SSL certificates are valid
  3. **Test load balancer:**
Terminal window```


kubectlgetsvc-ningress-nginx


```



## Performance Issues
[Section titled “Performance Issues”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/troubleshooting/#performance-issues)
### Slow Performance
[Section titled “Slow Performance”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/troubleshooting/#slow-performance)
**Common causes:**
  * Insufficient resources
  * Database performance issues
  * Network latency


**Solutions:**
  1. **Check resource usage:**
Terminal window```


kubectltoppods




kubectltopnodes


```

  2. **Scale resources:**
Terminal window```


kubectlscaledeploymentllamacloud--replicas=3-nllamacloud


```

  3. **Optimize Azure services:**
     * Increase PostgreSQL compute tier
     * Use Premium Redis tier
     * Enable auto-scaling for Cosmos DB


### Memory/CPU Issues
[Section titled “Memory/CPU Issues”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/troubleshooting/#memorycpu-issues)
**Symptoms:**
  * Pod restarts
  * OOMKilled events
  * High CPU usage


**Solutions:**
  1. **Check resource limits:**
Terminal window```


kubectldescribepod<pod-name>-nllamacloud


```

  2. **Increase limits in values.yaml:**
```


backend:




resources:




limits:




memory: 4Gi




cpu: 2


```



## Error Code Reference
[Section titled “Error Code Reference”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/troubleshooting/#error-code-reference)
### Common HTTP Errors
[Section titled “Common HTTP Errors”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/troubleshooting/#common-http-errors)
  * **500 Internal Server Error** : Check backend logs, database connectivity
  * **502 Bad Gateway** : Check if backend pods are running
  * **503 Service Unavailable** : Check service health, scaling issues
  * **401 Unauthorized** : OIDC configuration issues
  * **403 Forbidden** : Azure service permission issues


### Common Database Errors
[Section titled “Common Database Errors”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/troubleshooting/#common-database-errors)
  * **Connection refused** : Firewall or network issues
  * **Authentication failed** : Wrong credentials
  * **SSL required** : Missing SSL configuration
  * **Database does not exist** : Database name mismatch


## Getting Help
[Section titled “Getting Help”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/troubleshooting/#getting-help)
### Collect Diagnostic Information
[Section titled “Collect Diagnostic Information”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/troubleshooting/#collect-diagnostic-information)
Before contacting support, gather:
Terminal window```

# Basic cluster info



kubectl-nllamacloudgetpods-owide




kubectl-nllamacloudgetsvc




kubectl-nllamacloudgetsecrets




kubectl-nllamacloudgetconfigmaps




# Logs from all services



kubectl-nllamacloudlogsdeployment/llamacloudllamacloud.log




kubectl-nllamacloudlogsdeployment/llamacloud-layoutllamacloud-layout.log




kubectl-nllamacloudlogsdeployment/llamacloud-ocrllamacloud-ocr.log




kubectl-nllamacloudlogsdeployment/llamacloud-operatorllamacloud-operator.log




kubectl-nllamacloudlogsdeployment/llamacloud-parsellamacloud-parse.log




kubectl-nllamacloudlogsdeployment/llamacloud-telemetryllamacloud-telemetry.log




kubectl-nllamacloudlogsdeployment/llamacloud-webllamacloud-web.log




kubectl-nllamacloudlogsdeployment/llamacloud-workerllamacloud-worker.log




kubectl-nllamacloudlogsdeployment/llamacloud-s3proxyllamacloud-s3proxy.log




# Cluster events



kubectlgetevents--sort-by='.lastTimestamp'-nllamacloud




# Resource usage



kubectltoppods




kubectltopnodes


```

### Contact Support
[Section titled “Contact Support”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/troubleshooting/#contact-support)
  * **LlamaCloud Support** : support@llamaindex.ai
  * **Include** : Deployment configuration, error logs, Azure resource details
  * **Avoid** : Sharing secrets, credentials, or sensitive data


