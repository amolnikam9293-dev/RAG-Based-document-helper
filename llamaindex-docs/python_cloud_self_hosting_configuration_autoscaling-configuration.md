[Skip to content](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/autoscaling-configuration/#_top)
# Autoscaling
##  Self-Hosting Documentation Access 
This section requires a password to access. Interested in self-hosting? [Contact sales](https://www.llamaindex.ai/contact) to learn more. 
Self-Hosting Documentation Access Granted  Logout 
Configure autoscaling for LlamaCloud services to automatically scale based on resource utilization or queue depth.
## Overview
[Section titled “Overview”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/autoscaling-configuration/#overview)
LlamaCloud supports two autoscaling approaches:
  1. **Standard HPA (Default)** - CPU/memory-based scaling using Kubernetes HPA
  2. **KEDA-based scaling (Recommended for Production)** - Queue-depth based scaling for better workload responsiveness


Both options are configured through Helm values and provide automatic scaling based on different metrics to ensure optimal resource utilization.
## Autoscaling Options
[Section titled “Autoscaling Options”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/autoscaling-configuration/#autoscaling-options)
### Standard HPA
[Section titled “Standard HPA”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/autoscaling-configuration/#standard-hpa)
  * **Metrics** : CPU and memory utilization
  * **Best for** : General workloads, development environments
  * **Setup** : Enabled by default, no additional components required


### KEDA-based Scaling
[Section titled “KEDA-based Scaling”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/autoscaling-configuration/#keda-based-scaling)
  * **Metrics** : Queue depth from LlamaCloud API
  * **Best for** : Production workloads with variable processing queues
  * **Setup** : Requires KEDA operator installation
  * **Advantage** : Scales based on actual work to be done, not just resource usage


## Prerequisites
[Section titled “Prerequisites”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/autoscaling-configuration/#prerequisites)
### For Standard HPA
[Section titled “For Standard HPA”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/autoscaling-configuration/#for-standard-hpa)
  * Kubernetes Metrics Server (usually pre-installed)


### For KEDA-based Scaling
[Section titled “For KEDA-based Scaling”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/autoscaling-configuration/#for-keda-based-scaling)
  * **KEDA Operator** installed in your Kubernetes cluster
  * LlamaCloud version 0.5.8+ (for queue status API)


## Helm Configuration
[Section titled “Helm Configuration”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/autoscaling-configuration/#helm-configuration)
### Option 1: Standard HPA (Default)
[Section titled “Option 1: Standard HPA (Default)”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/autoscaling-configuration/#option-1-standard-hpa-default)
By default, LlamaParse uses standard Kubernetes HPA based on CPU and memory metrics:
```

# Basic HPA configuration (enabled by default)



llamaParse:




horizontalPodAutoscalerSpec:




minReplicas: 2




maxReplicas: 8




metrics:




- resource:




name: cpu




target:




averageUtilization: 40




type: Utilization




type: Resource




- resource:




name: memory




target:




averageUtilization: 60




type: Utilization




type: Resource




scaleTargetRef:




apiVersion: apps/v1




kind: Deployment




name: llamacloud-parse


```

Other services can also be scaled in this way, e.g. `backend`.
### Option 2: KEDA Queue-Based Scaling (Recommended for Production)
[Section titled “Option 2: KEDA Queue-Based Scaling (Recommended for Production)”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/autoscaling-configuration/#option-2-keda-queue-based-scaling-recommended-for-production)
We recommend KEDA-based configuration for more robust queue-depth based scaling in production. **Note: You must disable HPA when using KEDA.**
```

# KEDA configuration for queue-based scaling



extraObjects:




- apiVersion: keda.sh/v1alpha1




kind: ScaledObject




metadata:




name: llamacloud-parse




namespace: <your-namespace>




spec:




cooldownPeriod: 120




initialCooldownPeriod: 0




maxReplicaCount: 10




minReplicaCount: 1




pollingInterval: 15




scaleTargetRef:




apiVersion: apps/v1




kind: Deployment




name: llamacloud-parse




triggers:




- metadata:




activationTargetQueueSize: "0"




endpoint: "http://llamacloud:80/api/queue-statusz?queue_prefix=parse_raw_file_job"




targetQueueSize: "20"




taskQueue: llamacloud-all




type: temporal


```

## OCR Pod Scaling Based on LlamaParse Worker Pods
[Section titled “OCR Pod Scaling Based on LlamaParse Worker Pods”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/autoscaling-configuration/#ocr-pod-scaling-based-on-llamaparse-worker-pods)
For workloads that use OCR services, you can configure KEDA to scale OCR pods based on the number of LlamaParse worker pods. This ensures OCR capacity matches parsing demand.
### KEDA Configuration for OCR Scaling
[Section titled “KEDA Configuration for OCR Scaling”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/autoscaling-configuration/#keda-configuration-for-ocr-scaling)
The OCR pod scaling uses KEDA’s ability to monitor the number of running LlamaParse Worker pods and applies the formula: `Min(3, llamaparse_pods / 3)` to determine the optimal number of OCR pods.
```

# OCR scaling configuration based on LlamaParse Worker pods



extraObjects:




- apiVersion: keda.sh/v1alpha1




kind: ScaledObject




metadata:




name: llamacloud-ocr




namespace: <your-namespace>




spec:




cooldownPeriod: 120




initialCooldownPeriod: 0




maxReplicaCount: 10




minReplicaCount: 1




pollingInterval: 15




scaleTargetRef:




apiVersion: apps/v1




kind: Deployment




name: llamacloud-ocr




triggers:




- metadata:




activationTargetQueueSize: "0"




endpoint: "http://llamacloud:80/api/queue-statusz?queue_prefix=parse_raw_file_job"




targetQueueSize: "20"




taskQueue: llamacloud-all




type: temporal


```

### Scaling Logic
[Section titled “Scaling Logic”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/autoscaling-configuration/#scaling-logic)
OCR pods scale based on parse job count using the formula `Min(3, estimated_parse_workers / 3)`. The target value of 60 assumes ~20 jobs per LlamaParse Worker pod, maintaining a 3:1 LlamaParse Worker to OCR pod ratio for optimal resource efficiency.
