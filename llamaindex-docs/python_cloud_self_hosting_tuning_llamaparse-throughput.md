[Skip to content](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-throughput/#_top)
# LlamaParse Configuration - Throughput
##  Self-Hosting Documentation Access 
This section requires a password to access. Interested in self-hosting? [Contact sales](https://www.llamaindex.ai/contact) to learn more. 
Self-Hosting Documentation Access Granted  Logout 
# Concurrency and Max Pages Configuration
[Section titled “Concurrency and Max Pages Configuration”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-throughput/#concurrency-and-max-pages-configuration)
## Overview
[Section titled “Overview”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-throughput/#overview)
This document explains how concurrency settings affect the maximum number of pages that can be processed in LlamaParse, and how to configure these settings for different AI models.
## How It Works
[Section titled “How It Works”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-throughput/#how-it-works)
### Maximum Processable Pages Calculation
[Section titled “Maximum Processable Pages Calculation”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-throughput/#maximum-processable-pages-calculation)
The system determines the maximum number of pages that can be processed based on two factors:
  1. **Parse Mode Defaults** : Different parsing modes have different default limits
  2. **Model-Specific Concurrency** : Some models have higher API rate limits that allow processing more pages


The final `maxProcessablePages` is calculated as:
```


maxProcessablePages =max(defaultForParseMode, modelConcurrency *12)


```

The multiplier of **12** represents an estimate of pages that can be processed per concurrent request during the job time window.
### Default Max Pages by Parse Mode
[Section titled “Default Max Pages by Parse Mode”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-throughput/#default-max-pages-by-parse-mode)
Parse Mode | Default Max Pages | Description  
---|---|---  
`PARSE_PAGE_WITHOUT_LLM` | 10,000 | Fast mode without LLM processing  
`PARSE_PAGE_WITH_AGENT` | 700 | Agent-based page parsing  
`PARSE_DOCUMENT_WITH_AGENT` | 700 | Agent-based document parsing  
`PARSE_PAGE_WITH_LVM` | 700 | Large Vision Model parsing  
`PARSE_DOCUMENT_WITH_LLM` | 700 | LLM-based document parsing / continuous mode  
`PARSE_PAGE_WITH_LLM` | 5,000 | LLm per page parsing  
### Model Concurrency Override
[Section titled “Model Concurrency Override”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-throughput/#model-concurrency-override)
If a model has a defined concurrency value that would allow more pages than the default, the limit is automatically increased. The max page is the `concurrency * 12`
**Example:**
  * Parse mode: `PARSE_PAGE_WITH_AGENT` (default: 700 pages)
  * Model: `gemini-2.5-flash` (concurrency: 250)
  * Calculated max: `250 * 12 = 3,000 pages`
  * **Final limit: 3,000 pages** (higher value wins)


## How to Edit Concurrency Settings
[Section titled “How to Edit Concurrency Settings”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-throughput/#how-to-edit-concurrency-settings)
### Option 1: Per model configuration (Recommended for Production)
[Section titled “Option 1: Per model configuration (Recommended for Production)”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-throughput/#option-1-per-model-configuration-recommended-for-production)
For self-hosted deployments using Helm, you can configure model-specific concurrency through the `values.yaml` file. This is the **recommended approach** for production deployments as it doesn’t require code changes.
#### Configure Model Concurrency in Helm
[Section titled “Configure Model Concurrency in Helm”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-throughput/#configure-model-concurrency-in-helm)
Edit your Helm values file (or override values):
```


config:




parse:




concurrency:




# Google Gemini Models




gemini25Flash: 250# Gemini 2.5 Flash




gemini25Pro: 100# Gemini 2.5 Pro




gemini20Flash: 250# Gemini 2.0 Flash




gemini20FlashLite: 250# Gemini 2.0 Flash Lite




gemini15Flash: ""# Leave empty to use hardcoded defaults




gemini15Pro: ""





# OpenAI Models




openaiGpt4oMini: 250# GPT-4o Mini




openaiGpt4o: ""# GPT-4o




openaiGpt41: ""# GPT-4.1




openaiGpt41Mini: 250# GPT-4.1 Mini




openaiGpt41Nano: 250# GPT-4.1 Nano




openaiGpt5: ""# GPT-5




openaiGpt5Mini: ""# GPT-5 Mini




openaiGpt5Nano: ""# GPT-5 Nano




openaiWhisper1: ""# Whisper-1





# Anthropic Claude Models




anthropicSonnet37: ""# Claude Sonnet 3.7




anthropicSonnet35: ""# Claude Sonnet 3.5




anthropicSonnet40: ""# Claude Sonnet 4.0




anthropicSonnet45: ""# Claude Sonnet 4.5




anthropicHaiku35: ""# Claude Haiku 3.5




anthropicHaiku45: ""# Claude Haiku 4.5


```

**Important Notes:**
  * When set, these values override **all region and host** concurrency settings for that model
  * Leave values empty (`""`) to use the hardcoded defaults from the code
  * These settings apply to both `llamaParse` and `temporalParse.llamaParse` sections
  * Values are passed as environment variables: `GEMINI_2_5_FLASH_CONCURRENCY`, `OPENAI_GPT_4O_MINI_CONCURRENCY`, etc.


#### Deploy the Updated Configuration
[Section titled “Deploy the Updated Configuration”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-throughput/#deploy-the-updated-configuration)
Terminal window```

# Update your Helm deployment



helmupgradellamacloud./charts/llamacloud\




--namespacellamacloud\




--valuesyour-custom-values.yaml


```

### Option 2 updated per parsing mode default concurrency
[Section titled “Option 2 updated per parsing mode default concurrency”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-throughput/#option-2-updated-per-parsing-mode-default-concurrency)
In addition to model-specific concurrency, LlamaParse has several other concurrency settings that control different aspects of processing. **All of these can now be configured via Helm** in addition to environment variables.
#### Parse Mode Concurrency Settings
[Section titled “Parse Mode Concurrency Settings”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-throughput/#parse-mode-concurrency-settings)
These control the overall concurrency for different parsing modes:
Variable | Default | Description | Helm Path  
---|---|---|---  
`ACCURATE_MODE_LLM_CONCURRENCY` | 250 | Concurrency for accurate mode LLM processing (parse_page_with_llm) | `llamaParse.config.accurateModeLLMConcurrency`  
`MULTIMODAL_MODEL_CONCURRENCY` | 50 | Concurrency for multimodal models (parse_page_with_lvm) | `llamaParse.config.multimodalModelConcurrency`  
`PREMIUM_MODE_MODEL_CONCURRENCY` | 25 | Concurrency for premium mode processing (parse_page_with_agent) | `llamaParse.config.premiumModeModelConcurrency`  
**Example Helm Configuration:**
```


config:




parse:




# Parse mode concurrency settings




accurateModeLLMConcurrency: 300# Increase from default 250




multimodalModelConcurrency: 75# Increase from default 50




premiumModeModelConcurrency: 40# Increase from default 25


```

### Calculate the Impact
[Section titled “Calculate the Impact”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-throughput/#calculate-the-impact)
When setting a concurrency value, consider:
  1. **API Rate Limits** : Check the provider’s documented TPM (Tokens Per Minute) and RPM (Requests Per Minute)
  2. **Target Max Pages** : Divide your desired max pages by 12 
     * Example: Want 6,000 max pages? Set concurrency to 500 (6000 ÷ 12)
  3. **Conservative Settings** : Set concurrency below the theoretical limit to avoid rate limiting


## Best Practices
[Section titled “Best Practices”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-throughput/#best-practices)
### 1. Start Conservative
[Section titled “1. Start Conservative”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-throughput/#1-start-conservative)
Begin with lower concurrency values and gradually increase based on monitoring:
  * Monitor API rate limit errors
  * Track job success rates
  * Observe processing times


### 2. Match Provider Limits
[Section titled “2. Match Provider Limits”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-throughput/#2-match-provider-limits)
Align concurrency with the provider’s documented limits:
  * **RPM (Requests Per Minute)** : Concurrency should not exceed RPM
  * **TPM (Tokens Per Minute)** : Consider average tokens per request
  * **Rate Limit Headroom** : Leave 10-20% headroom for bursts


### 3. Test Thoroughly
[Section titled “3. Test Thoroughly”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-throughput/#3-test-thoroughly)
After changing concurrency:
  1. Test with various document sizes
  2. Monitor for rate limit errors in logs
  3. Verify job completion rates
  4. Check processing times


### 4. Region-Aware Settings
[Section titled “4. Region-Aware Settings”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-throughput/#4-region-aware-settings)
Different regions may have different API quotas:
  * EU regions often have stricter limits
  * Custom API keys may have different quotas
  * BYOC deployments can have higher limits


### Processing Pipeline Concurrency
[Section titled “Processing Pipeline Concurrency”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-throughput/#processing-pipeline-concurrency)
These control specific processing stages:
Variable | Default | Description | Helm Path  
---|---|---|---  
`OCR_CONCURRENCY` | 8 | OCR processing concurrency | `llamaParse.config.ocrConcurrency`  
`LAYOUT_EXTRACTION_CONCURRENCY` | 10 | Layout detection concurrency | `llamaParse.config.layoutExtractionConcurrency`  
`LAYOUT_EXTRACTION_V2_CONCURRENCY` | 10 | Layout detection v2 concurrency | `llamaParse.config.layoutExtractionV2Concurrency`  
`LAYOUT_MODE_BLOCK_PARSE_CONCURRENCY` | 5 | Block parsing in layout mode | `llamaParse.config.layoutModeBlockParseConcurrency`  
`LAYOUT_MODE_PAGE_CONCURRENCY` | 15 | Page-level layout processing | `llamaParse.config.layoutModePageConcurrency`  
`LAYOUT_MODE_READING_ORDER_DETECTION_CONCURRENCY` | 1 | Reading order detection | `llamaParse.config.layoutModeReadingOrderDetectionConcurrency`  
**Example Helm Configuration:**
```


config:




parse:




# Pipeline concurrency settings




ocrConcurrency: 12# Increase from default 8




layoutExtractionConcurrency: 15# Increase from default 10




layoutModePageConcurrency: 20# Increase from default 15




layoutModeReadingOrderDetectionConcurrency: 2# Increase from default 1


```

### Queue Concurrency
[Section titled “Queue Concurrency”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-throughput/#queue-concurrency)
Variable | Default | Description | Helm Path  
---|---|---|---  
`PDF_JOB_QUEUE_CONCURRENCY` | 1 | Number of jobs processed simultaneously | `llamaParse.config.maxQueueConcurrency`  
**Example Helm Configuration:**
```


config:




parse:




maxQueueConcurrency: 3# Process 3 jobs at once


```

### How These Interact
[Section titled “How These Interact”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-throughput/#how-these-interact)
The different concurrency settings work together:
  1. **Queue Concurrency** (`maxQueueConcurrency`): Controls how many jobs run in parallel
  2. **Mode Concurrency** (e.g., `ACCURATE_MODE_LLM_CONCURRENCY`): Controls how many operations within a job
  3. **Model Concurrency** (per model): Controls API calls for specific models
  4. **Pipeline Concurrency** (OCR, layout, etc.): Controls specific processing stages


**Example Scaling Strategy:**
```

# High-throughput configuration



config:




parse:




# Queue concurrency - how many jobs to process simultaneously




maxQueueConcurrency: 5




concurrency:




# Parse mode concurrency - operations within each job




accurateModeLLMConcurrency: 300




multimodalModelConcurrency: 75




premiumModeModelConcurrency: 40





# Pipeline concurrency - specific processing stages




ocrConcurrency: 12




layoutExtractionConcurrency: 15




layoutModePageConcurrency: 20





# Model-specific concurrency - API call limits per model




gemini25Flash: 300# High API concurrency for Gemini




openaiGpt4oMini: 250# High API concurrency for OpenAI




anthropicSonnet45: 150# Moderate concurrency for Anthropic


```

This configuration would:
  * Process **5 jobs** at the same time (queue concurrency)
  * Each job can make up to **300 concurrent calls** to Gemini 2.5 Flash (model concurrency)
  * Allow processing larger documents: **300 * 12 = 3,600 pages max** per job
  * Increase throughput for accurate mode operations (300 concurrent LLM calls)
  * Improve OCR and layout processing speeds


**Important:** Higher concurrency requires more system resources (CPU, memory, network). Monitor your deployment and adjust accordingly.
## Best Practices
[Section titled “Best Practices”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-throughput/#best-practices-1)
### 1. Start Conservative
[Section titled “1. Start Conservative”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-throughput/#1-start-conservative-1)
Begin with lower concurrency values and gradually increase based on monitoring:
  * Monitor API rate limit errors
  * Track job success rates
  * Observe processing times


### 2. Match Provider Limits
[Section titled “2. Match Provider Limits”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-throughput/#2-match-provider-limits-1)
Align concurrency with the provider’s documented limits:
  * **RPM (Requests Per Minute)** : Concurrency should not exceed RPM
  * **TPM (Tokens Per Minute)** : Consider average tokens per request
  * **Rate Limit Headroom** : Leave 10-20% headroom for bursts


### 3. Test Thoroughly
[Section titled “3. Test Thoroughly”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-throughput/#3-test-thoroughly-1)
After changing concurrency:
  1. Test with various document sizes
  2. Monitor for rate limit errors in logs
  3. Verify job completion rates
  4. Check processing times


### 4. Region-Aware Settings
[Section titled “4. Region-Aware Settings”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-throughput/#4-region-aware-settings-1)
Different regions may have different API quotas:
  * EU regions often have stricter limits
  * Custom API keys may have different quotas
  * BYOC deployments can have higher limits


## Troubleshooting
[Section titled “Troubleshooting”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-throughput/#troubleshooting)
### Job Fails with “DOCUMENT_TOO_LARGE” Error
[Section titled “Job Fails with “DOCUMENT_TOO_LARGE” Error”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-throughput/#job-fails-with-document_too_large-error)
**Symptoms:**
```

Error: Job would parse X pages, max pages allowed for parse mode Y is Z

```

**Solutions:**
  1. **Increase model concurrency via Helm (Recommended):**
```


config:




parse:




concurrency:




gemini25Flash: 400# Increase from default


```

  2. **Increase queue concurrency to process more jobs:**
```


config:




parse:




maxQueueConcurrency: 5# Process 5 jobs simultaneously


```

  3. Consider using a model with higher default concurrency
  4. Split the document into smaller batches


### Rate Limit Errors
[Section titled “Rate Limit Errors”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-throughput/#rate-limit-errors)
**Symptoms:**
  * API errors mentioning rate limits
  * Intermittent job failures
  * “429 Too Many Requests” errors


**Solutions:**
  1. **Reduce model concurrency via Helm:**
```


config:




parse:




concurrency:




openaiGpt4oMini: 150# Reduce from 250


```

  2. **Reduce queue concurrency:**
```


config:




parse:




maxQueueConcurrency: 1# Process one job at a time


```

  3. Contact provider to increase API quotas
  4. Consider using multiple API keys with load balancing


### Lower Than Expected Max Pages
[Section titled “Lower Than Expected Max Pages”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-throughput/#lower-than-expected-max-pages)
**Check:**
  1. Is model concurrency configured in your Helm values?
Terminal window```

# Check current ConfigMap values



kubectlgetconfigmapllamacloud-llamaparse-config-nllamacloud-oyaml|grepCONCURRENCY


```

  2. Is the concurrency value being applied?
Terminal window```

# Check environment variables in the pod



kubectlexec-itdeployment/llamacloud-llamaparse-nllamacloud--env|grepCONCURRENCY


```

  3. Verify the calculation: `concurrency * 12` should be greater than the parse mode default


### Configuration Not Taking Effect
[Section titled “Configuration Not Taking Effect”](https://developers.llamaindex.ai/python/cloud/self_hosting/tuning/llamaparse-throughput/#configuration-not-taking-effect)
**Helm values not applying:**
  1. Verify your values are in the correct section:
```


config:




parse:




concurrency:




gemini25Flash: 300


```

  2. Redeploy with explicit values file:
Terminal window```


helmupgradellamacloudllamacloud\




--valuesyour-values.yaml\




--debug


```

  3. Check the generated ConfigMap:
Terminal window```


kubectlgetconfigmapllamacloud-parse-oyaml


```



For questions or issues, please contact the LlamaParse development team.
