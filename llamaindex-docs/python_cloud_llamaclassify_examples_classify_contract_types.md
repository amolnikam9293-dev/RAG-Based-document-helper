[Skip to content](https://developers.llamaindex.ai/python/cloud/llamaclassify/examples/classify_contract_types/#_top)
# Classify Contract Types
In this example, we’ll be classifying various contracts by type, using LlamaClassify, and the `llama-cloud-services` Python SDK. When provided with a file, we’ll classify it either as a `co_branding` contract or an `affiliate_agreement`.
As an example, we’ll be making use of the [CUAD](https://zenodo.org/records/4595826) dataset, which includes various contracts such as: Affiliate Agreements, Co-Branding contracts, Franchise contracts and more.
The example we go through below is also replicable within the LlamaCloud as well, where you will also be able to create classification rules via the UI, instead of defining them in code:
```


!pip install llama-cloud-services


```

## Download Contracts
[Section titled “Download Contracts”](https://developers.llamaindex.ai/python/cloud/llamaclassify/examples/classify_contract_types/#download-contracts)
To start off, we recommend downloading a few contracts from the ‘Affiliate Agreements’ and ‘Co-Branding’ sections.
## Connect to Llama Cloud
[Section titled “Connect to Llama Cloud”](https://developers.llamaindex.ai/python/cloud/llamaclassify/examples/classify_contract_types/#connect-to-llama-cloud)
To get started, make sure you provide your [Llama Cloud](https://cloud.llamaindex.ai?utm_campaign=extract&utm_medium=recipe) API key.
```


import os




from getpass import getpass





if"LLAMA_CLOUD_API_KEY"notin os.environ:




os.environ["LLAMA_CLOUD_API_KEY"] =getpass("Enter your Llama Cloud API Key: ")


```

## Initialize a LlamaClassify Client
[Section titled “Initialize a LlamaClassify Client”](https://developers.llamaindex.ai/python/cloud/llamaclassify/examples/classify_contract_types/#initialize-a-llamaclassify-client)
```


from llama_cloud_services.beta.classifier.client import ClassifyClient




from llama_cloud.client import AsyncLlamaCloud





client =AsyncLlamaCloud(token=os.environ["LLAMA_CLOUD_API_KEY"])




project_id ="your-project-id"




organization_id ="your-organization-id"




classifier =ClassifyClient(client,project_id=project_id,organization_id=organization_id)


```

## Define Classification Rules
[Section titled “Define Classification Rules”](https://developers.llamaindex.ai/python/cloud/llamaclassify/examples/classify_contract_types/#define-classification-rules)
For this example, we’ll narrow down the scope to classifying between `co_branding` and `affiliate_agreements` types:
```


from llama_cloud.types import ClassifierRule





rules =[




ClassifierRule(




type="affiliate_agreements",




description="This is a contract that outlines an affiliate agreement",





ClassifierRule(




type="co_branding",




description="This is a contract that outlines a co-branding deal/agreement",




```

## Classify Files
[Section titled “Classify Files”](https://developers.llamaindex.ai/python/cloud/llamaclassify/examples/classify_contract_types/#classify-files)
Finally, we can classify a file (or files):
```


result =await classifier.aclassify_file_path(




rules=rules,




file_input_path="CybergyHoldingsInc_Affliate Agreement.pdf",



```

Once classification is complete, the results will include not only the contract type the file was classified as, but also the reasoning for this classification by LlamaClassify. For example, in this case this is the result we got:
```


classification = result.items[0].result




print("Classification Result: "+ classification.type)




print("Classification Reason: "+ classification.reasoning)


```

```

Classification Result: affiliate_agreements


Classification Reason: The document is titled 'MARKETING AFFILIATE AGREEMENT' and repeatedly refers to one party as the 'Marketing Affiliate.' The agreement outlines the rights and obligations of the 'Marketing Affiliate' (MA) to market, sell, and support certain technology products, and details the relationship between the company and the affiliate. There is no mention of joint branding, shared trademarks, or collaborative marketing under both parties' brands, which would be indicative of a co-branding agreement. The content is entirely consistent with an affiliate agreement, where one party (the affiliate) is authorized to market and sell the products of another company, rather than a co-branding arrangement. Therefore, the best match is 'affiliate_agreements' with very high confidence.

```

