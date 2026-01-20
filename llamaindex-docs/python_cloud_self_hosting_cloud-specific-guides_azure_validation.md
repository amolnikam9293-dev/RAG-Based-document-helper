[Skip to content](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/validation/#_top)
# Validation Guide
##  Self-Hosting Documentation Access 
This section requires a password to access. Interested in self-hosting? [Contact sales](https://www.llamaindex.ai/contact) to learn more. 
Self-Hosting Documentation Access Granted  Logout 
This guide helps you verify that your LlamaCloud deployment on Azure is working correctly. Follow these steps after completing the [Azure Setup Guide](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/setup/).
## Step 1: Verify Pod Status
[Section titled “Step 1: Verify Pod Status”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/validation/#step-1-verify-pod-status)
Check that all LlamaCloud pods are running correctly:
Terminal window```

# Check all pods are running



kubectlgetpods-nllamacloud




# Expected output should show all pods as Running:



llamacloud-64f468d5cf-sqjq61/1Running




llamacloud-layout-6d97b84c58-rld8x1/1Running




llamacloud-ocr-5cc459bdd-99xgt1/1Running




llamacloud-operator-5d4c58b854-dwnjk1/1Running




llamacloud-parse-7ffbc786b5-r98w21/1Running




llamacloud-telemetry-5fc9ff8c67-fv8xj1/1Running




llamacloud-web-b88d95588-rprhc1/1Running




llamacloud-worker-58b95ccc6f-vqmgx1/1Running




llamacloud-s3proxy-xxx1/1Running


```

If any pods are not in `Running` state, check the logs:
Terminal window```


kubectllogsdeployment/llamacloud-telemetry-nllamacloud


```

## Step 2: Access UI and Test Authentication
[Section titled “Step 2: Access UI and Test Authentication”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/validation/#step-2-access-ui-and-test-authentication)
### Access the LlamaCloud UI
[Section titled “Access the LlamaCloud UI”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/validation/#access-the-llamacloud-ui)
**Port Forward (for testing)**
Terminal window```


kubectl-nllamacloudport-forwardsvc/llamacloud-web3000:80


```

Open `http://localhost:3000` in your browser.
**Production Access (if ingress configured)** If you have an ingress controller set up, access your configured domain.
### Test Authentication
[Section titled “Test Authentication”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/validation/#test-authentication)
  1. **Navigate to LlamaCloud UI**
  2. **Click Sign In** - should redirect to Microsoft Entra ID
  3. **Complete OIDC flow** - authenticate with your Microsoft Entra ID credentials
  4. **Verify successful login** - should return to LlamaCloud dashboard


## Step 3: Access Admin UI
[Section titled “Step 3: Access Admin UI”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/validation/#step-3-access-admin-ui)
After successful authentication, verify admin functionality:
  1. **Navigate to Admin Settings** - Look for the admin/settings section in the UI
  2. **Check License Status** - Verify your LlamaCloud license shows as “Active”
  3. **Review LLM Availability** - Expand the LLM section to see provider and model status
  4. **Check File Storage** - Expand to verify all required buckets show as “Available”
  5. **Review Feature Availability** - Check that Parse, Extract, and Chat features work with your models


The admin UI displays three main expandable sections:
### License Status
[Section titled “License Status”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/validation/#license-status)
  * **License validity** and expiration date
  * **Version information** of your deployment
  * **Renewal reminders** if license is expiring


### LLM Availability
[Section titled “LLM Availability”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/validation/#llm-availability)
  * **Provider status** (OpenAI, Anthropic, etc.)
  * **Model validation** with ✅ for working models, ❌ for failed models
  * **Error messages** for any model connectivity issues


### File Storage Availability
[Section titled “File Storage Availability”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/validation/#file-storage-availability)
  * **Available buckets** - Should show all 8 required containers: 
    * `llama-platform-parsed-documents`
    * `llama-platform-etl`
    * `llama-platform-external-components`
    * `llama-platform-file-parsing`
    * `llama-platform-raw-files`
    * `llama-cloud-parse-output`
    * `llama-platform-file-screenshots`
    * `llama-platform-extract-output`
  * **Unavailable buckets** - Should be empty if properly configured


### Feature Availability
[Section titled “Feature Availability”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/validation/#feature-availability)
  * **Parse Features** - Shows preset modes (Fast, Balanced, Premium) and advanced parsing modes
  * **Extract Features** - Shows schema generation and extraction mode availability
  * **Chat Playground** - Shows available models for chat functionality


## Step 4: Test Basic Product Functionality
[Section titled “Step 4: Test Basic Product Functionality”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/validation/#step-4-test-basic-product-functionality)
### Test Document Parsing
[Section titled “Test Document Parsing”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/validation/#test-document-parsing)
  1. **Navigate to the Parse product** in the LlamaCloud UI
  2. **Keep the default setting** (Cost-effective mode)
  3. **Upload a test PDF** document
  4. **Verify the parsing job completes successfully**


## Validation Checklist
[Section titled “Validation Checklist”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/validation/#validation-checklist)
Use this checklist to ensure your deployment is fully validated:
  * All pods are in `Running` state
  * Frontend is accessible via browser
  * Microsoft Entra ID authentication works
  * Admin UI license status shows as “Active”
  * LLM models show ✅ status in admin UI
  * All 8 required storage buckets show as “Available”
  * Feature availability shows required capabilities working
  * Can navigate to Parse product
  * Can upload PDF documents
  * Document parsing job completes successfully


## Next Steps
[Section titled “Next Steps”](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/validation/#next-steps)
If you encounter any issues during validation, see the [Troubleshooting Guide](https://developers.llamaindex.ai/python/cloud/self_hosting/cloud-specific-guides/azure/troubleshooting/) for solutions to common problems.
Once validation is complete, your Azure LlamaCloud deployment is ready for use!
