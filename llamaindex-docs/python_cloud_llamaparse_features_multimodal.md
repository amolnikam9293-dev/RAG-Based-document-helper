[Skip to content](https://developers.llamaindex.ai/python/cloud/llamaparse/features/multimodal/#_top)
# Multimodal Parsing
You can use a Vendor multimodal model to handle document extraction. This is more expensive than regular parsing but can get better results for some documents.
Supported models are models are [here](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/advance_parsing_modes#under-the-hood-2).
When using this mode, LlamaParse’s regular parsing is bypassed and instead the following process is used:
  * A screenshot of every page of your document is taken
  * Each page screenshot is sent to the multimodal with instruction to extract as `markdown`
  * The resulting markdown of each page is consolidated into the final result.


## Using Multimodal mode
[Section titled “Using Multimodal mode”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/multimodal/#using-multimodal-mode)
To use the multimodal mode, set `use_vendor_multimodal_model` to `True`. You can then select which model to use ny setting `vendor_multimodal_model_name` to the model you want to target (eg: `anthropic-sonnet-3.5`).


```


parser =LlamaParse(




use_vendor_multimodal_model=True,




vendor_multimodal_model_name="anthropic-sonnet-3.5"



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'use_vendor_multimodal_model=True'\




--form'vendor_multimodal_model_name="anthropic-sonnet-3.5"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## Bring your own LLM key (Optional)
[Section titled “Bring your own LLM key (Optional)”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/multimodal/#bring-your-own-llm-key-optional)
When using To use the multimodal mode, you can supply your own vendor key to parse the document. If you choose to do so LlamaParse will only charge you 1 credit (0.3c) per page.
Using your own API key will incur some price from your model provider, and could led to fail page/document if you do not have high usage limits.
To use your own API key set the parameter `vendor_multimodal_api_key` to your own key value.


```


parser =LlamaParse(




parse_mode="parse_page_with_lvm",




model="openai-gpt4o",




vendor_multimodal_api_key="sk-proj-xxxxxx"



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'parse_mode="parse_page_with_lvm"'\




--form'model="openai-gpt4o"'\




--form'vendor_multimodal_api_key="sk-proj-xxxxxx"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

Note on Gemini model in EU SAAS: In our EU SAAS you need to provide a vertex AI certificate (as a string), for a valid project in europe-west1 google region.
## Custom Azure Model
[Section titled “Custom Azure Model”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/multimodal/#custom-azure-model)
You also have the possibility to use your own Azure Model Deployment using the following parameters:


```


parser =LlamaParse(




use_vendor_multimodal_model=True,




azure_openai_deployment_name="llamaparse-gpt-4o",




azure_openai_endpoint="https://<org>.openai.azure.com/openai/deployments/<dep>/chat/completions?api-version=<ver>",




azure_openai_api_version="2024-02-15-preview",




azure_openai_key="xxx"



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'use_vendor_multimodal_model="true"'\




--form'azure_openai_deployment_name="llamaparse-gpt-4o"'\




--form'azure_openai_endpoint="https://<org>.openai.azure.com/openai/deployments/<dep>/chat/completions?api-version=<ver>"'\




--form'azure_openai_api_version="2024-02-15-preview"'\




--form'azure_openai_key="xxx"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## GPt4-o mode (Deprecated)
[Section titled “GPt4-o mode (Deprecated)”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/multimodal/#gpt4-o-mode-deprecated)
By Setting `gpt4o_mode` to `True` LlamaParse will use openAI GPT4-o to do the document reconstruction. This is still working, but we recommend using `use_vendor_multimodal_model` to `True` and `vendor_multimodal_model_name` to `openai-gpt4o` instead.
The parameter `gpt4o_api_key` is still working but we recommend using the parameter `vendor_multimodal_api_key` instead.
