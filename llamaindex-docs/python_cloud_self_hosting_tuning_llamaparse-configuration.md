[Skip to content](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-configuration/#_top)
# LlamaParse Configuration
##  Self-Hosting Documentation Access 
This section requires a password to access. Interested in self-hosting? [Contact sales](https://www.llamaindex.ai/contact) to learn more. 
Self-Hosting Documentation Access Granted  Logout 
Configuration and scaling recommendations for LlamaParse OCR services and workers.
## Overview
[Section titled “Overview”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-configuration/#overview)
LlamaParse components:
  * **OCR Service** : Text extraction from document images
  * **LlamaParse Workers** : Document processing (fast, balanced, agentic modes)


## OCR Service Configuration
[Section titled “OCR Service Configuration”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-configuration/#ocr-service-configuration)
OCR service runs on GPU or CPU infrastructure.
### Hardware Recommendations
[Section titled “Hardware Recommendations”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-configuration/#hardware-recommendations)
**CPU deployments** : Use x86 architecture (50% better throughput than ARM).
#### Resource Requirements
[Section titled “Resource Requirements”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-configuration/#resource-requirements)
Configuration | GPU | CPU  
---|---|---  
**Minimum instances** | 2 | 12  
**Pages per minute per pod** | 100 | ~2 per worker  
**Recommended workers per pod** | 4 | Core count ÷ 2  
#### Scaling Ratios
[Section titled “Scaling Ratios”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-configuration/#scaling-ratios)
**CPU** : 2 CPU OCR workers (2 cores each) per LlamaParse worker **GPU** : 1 GPU OCR worker per 8 LlamaParse workers
## LlamaParse Worker Configuration
[Section titled “LlamaParse Worker Configuration”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-configuration/#llamaparse-worker-configuration)
Workers process documents in three modes:
### Performance by Mode
[Section titled “Performance by Mode”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-configuration/#performance-by-mode)
Mode | Pages per Minute | Use Case  
---|---|---  
**Fast** | ~10,000 | High-volume, basic text extraction  
**Balanced** | ~250 | Standard parsing with good accuracy  
**Agentic** | ~100 | Complex documents requiring AI analysis  
### Resource Requirements
[Section titled “Resource Requirements”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-configuration/#resource-requirements-1)
**Compute:**
  * **CPU** : 2 vCPUs per worker
  * **Memory** : 2-16 GB RAM per worker


**Deployment:**
  * Multiple workers per Kubernetes node
  * ~6 workers per node (production)


### Scaling Examples
[Section titled “Scaling Examples”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-configuration/#scaling-examples)
Target Throughput | LlamaParse Workers | CPU OCR Pods | GPU OCR Pods  
---|---|---|---  
1,000 pages/min | 8 | 16 | 2  
10,000 pages/min | 64 | 128 | 12  
## GenAI Providers
[Section titled “GenAI Providers”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-configuration/#genai-providers)
LlamaParse uses GenAI providers for parsing:
  * `parse_page_with_llm`: LLM parsing (supports `gpt-4o-mini`, `haiku-3.5`)
  * `parse_page_with_lvm`: Vision model parsing (supports `gemini`, `openai`, `claude sonnet`)
  * `parse_page_with_agent`: Agentic parsing (supports `claude`, `gemini`, `openai`)


**Provider fallback** : Multiple providers configured → automatic fallback on unavailability.
**Supported providers:**
  * **Claude/Haiku** : Anthropic (US), AWS Bedrock, Google VertexAI
  * **OpenAI** : OpenAI (US), OpenAI EU (`parse_page_with_llm` only), AzureAI
  * **Gemini** : Google Vertex AI, Google GenAI


## Advanced Configuration
[Section titled “Advanced Configuration”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-configuration/#advanced-configuration)
### OCR Worker Tuning
[Section titled “OCR Worker Tuning”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-configuration/#ocr-worker-tuning)
Terminal window```


OCR_WORKER=<value># Recommended: pod_core_count ÷ 2


```

### OCR Concurrency Control
[Section titled “OCR Concurrency Control”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-configuration/#ocr-concurrency-control)
Terminal window```


OCR_CONCURRENCY=8# Default


```

  * **Lower** : Fewer OCR pods, slower processing
  * **Higher** : More OCR pods, faster processing


### Image Processing Limits
[Section titled “Image Processing Limits”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-configuration/#image-processing-limits)
Terminal window```


MAX_EXTRACTED_IMAGES_PER_PAGES=30# Default


```

### Job Queue Concurrency
[Section titled “Job Queue Concurrency”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-configuration/#job-queue-concurrency)
Terminal window```


PDF_JOB_QUEUE_CONCURRENCY=1# Default (recommended)


```

Do not change `PDF_JOB_QUEUE_CONCURRENCY` without understanding performance implications.
### GenAI Throughput Tuning
[Section titled “GenAI Throughput Tuning”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-configuration/#genai-throughput-tuning)
Limit throughput per mode to match TPM/RPM quotas:
Terminal window```


ACCURATE_MODE_LLM_CONCURRENCY=250# parse_page_with_llm (default)




MULTIMODAL_MODEL_CONCURRENCY=50# parse_page_with_lvm (default)




PREMIUM_MODE_MODEL_CONCURRENCY=25# parse_page_with_agent (default)


```

**Token usage per 1k pages:**
Mode | Requests | Input Tokens | Output Tokens  
---|---|---|---  
`parse_page_with_llm` | 1,010 | 1.2M | 1.5M  
`parse_page_with_agent` | 2,000 | 4M | 2M  
`parse_page_with_lvm` | 1,200 | 3M | 1.5M  
Providers like AWS Bedrock have low default quotas. Verify quotas accommodate desired parsing volume.
## Autoscaling
[Section titled “Autoscaling”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-configuration/#autoscaling)
LlamaParse supports KEDA-based autoscaling to automatically adjust worker pods based on queue depth. This ensures optimal resource utilization during varying workloads.
### Queue-Based Scaling
[Section titled “Queue-Based Scaling”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-configuration/#queue-based-scaling)
Autoscaling uses the LlamaCloud queue status API to monitor parse job queues:
  * **Queue monitoring** : `/api/queue-statusz?queue_prefix=parse_raw_file_job`
  * **Scaling metric** : Total messages across healthy queues
  * **Target queue depth** : Total messages in queue KEDA tries to maintain (typically 20-100)


### Scaling Recommendations
[Section titled “Scaling Recommendations”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-configuration/#scaling-recommendations)
Environment | Min Pods | Max Pods | Target Queue Depth | Characteristics  
---|---|---|---|---  
**Development** | 3 | 12 | 20 | Fast scaling, testing  
**Staging** | 12 | 120 | 20 | Moderate scaling, validation  
**Production** | 96 | 600 | 100 | Conservative, high availability  
### Integration with OCR Services
[Section titled “Integration with OCR Services”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-configuration/#integration-with-ocr-services)
When scaling LlamaParse workers, consider OCR service capacity:
  * **CPU OCR** : Scale 2 OCR workers per LlamaParse worker
  * **GPU OCR** : Scale 1 OCR worker per 8 LlamaParse workers


For detailed autoscaling configuration, see the [Autoscaling Configuration](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/autoscaling-configuration) guide.
## Monitoring and Optimization
[Section titled “Monitoring and Optimization”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-configuration/#monitoring-and-optimization)
### Key Metrics
[Section titled “Key Metrics”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-configuration/#key-metrics)
  * **OCR throughput** : Pages/minute
  * **Worker utilization** : CPU/memory usage
  * **Queue depth** : Pending jobs
  * **Error rates** : Failed operations
  * **Scaling events** : Autoscaling frequency and effectiveness


### Optimization
[Section titled “Optimization”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-configuration/#optimization)
  1. **Node placement** : Collocate complementary resource usage patterns
  2. **Horizontal scaling** : Add workers before increasing per-worker resources
  3. **OCR scaling** : Scale OCR services independently
  4. **Memory management** : Use restart policies for long-running deployments
  5. **Autoscaling tuning** : Monitor queue depth and adjust scaling parameters


