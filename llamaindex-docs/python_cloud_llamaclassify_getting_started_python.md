[Skip to content](https://developers.llamaindex.ai/python/cloud/llamaclassify/getting_started/python/#_top)
# Classify Python SDK
This guide shows how to classify documents using the Python SDK. You will:
  * Create classification rules
  * Upload files
  * Submit a classify job
  * Read predictions (type, confidence, reasoning)


The SDK is available in [llama-cloud-services](https://github.com/run-llama/llama_cloud_services).
## Setup
[Section titled “Setup”](https://developers.llamaindex.ai/python/cloud/llamaclassify/getting_started/python/#setup)
First, get an API key: [Get an API key](https://developers.llamaindex.ai/python/cloud/general/api_key)
Put it in a `.env` file:
Terminal window```


LLAMA_CLOUD_API_KEY=llx-xxxxxx


```

Install dependencies:
Terminal window```


pipinstallllama-cloud-servicespython-dotenv


```

or with `uv`:
Terminal window```


uvaddllama-cloud-servicespython-dotenv


```

## Quick start
[Section titled “Quick start”](https://developers.llamaindex.ai/python/cloud/llamaclassify/getting_started/python/#quick-start)
The snippet below uses a convenience `LlamaClassify` wrapper from `llama-cloud-services` that uploads files, creates a classify job, polls for completion and returns results.
```


import os




from dotenv import load_dotenv




from llama_cloud.client import AsyncLlamaCloud




from llama_cloud.types import ClassifierRule, ClassifyMode, ClassifyParsingConfiguration




from llama_cloud_services.beta.classifier.client import LlamaClassify  # helper wrapper





load_dotenv()





client =AsyncLlamaCloud(token=os.environ["LLAMA_CLOUD_API_KEY"])




project_id ="your-project-id"




classifier =LlamaClassify(client,project_id=project_id)





rules =[




ClassifierRule(




type="invoice",




description="Documents that contain an invoice number, invoice date, bill-to section, and line items with totals."





ClassifierRule(




type="receipt",




description="Short purchase receipts, typically from POS systems, with merchant, items and total, often a single page."







parsing =ClassifyParsingConfiguration(




lang=ParserLanguages.EN,




max_pages=5,# optional, parse at most 5 pages




# target_pages=[1]        # optional, parse only specific pages (1-indexed), can't be used with max_pages





# for async usage, use `await classifier.aclassify(...)`



results = classifier.classify(




rules=rules,




files=[




"/path/to/doc1.pdf",




"/path/to/doc2.pdf",





parsing_configuration=parsing,




mode=ClassifyMode.FAST,# optional, "FAST" (default) or "MULTIMODAL"






for item in results.items:




# in cases of partial success, some of the items may not have a result




if item.result isNone:




print(f"Classification job {item.classify_job_id} error-ed on file {item.file_id}")




continue




print(item.file_id, item.result.type, item.result.confidence)




print(item.result.reasoning)


```

Notes:
  * `ClassifierRule` requires a `type` and a descriptive `description` that the model can follow.
  * `ClassifyParsingConfiguration` is optional; set `lang`, `max_pages`, or `target_pages` to control parsing.
  * In cases of partial failure, some of the items may not have a result (i.e. `results.items[*].result` could be `None`).


## Classification modes
[Section titled “Classification modes”](https://developers.llamaindex.ai/python/cloud/llamaclassify/getting_started/python/#classification-modes)
LlamaClassify supports two modes:
Mode | Credits per Page | Description  
---|---|---  
`FAST` | 1 | Text-based classification (default)  
`MULTIMODAL` | 2 | Vision-based classification for visual documents  
Use **Multimodal mode** when your documents contain images, charts, or complex layouts that are important for classification:
```


results = classifier.classify(




rules=rules,




files=["/path/to/visual-doc.pdf"],




mode=ClassifyMode.MULTIMODAL,# use vision model for classification



```

## Tips for writing good rules
[Section titled “Tips for writing good rules”](https://developers.llamaindex.ai/python/cloud/llamaclassify/getting_started/python/#tips-for-writing-good-rules)
  * Be specific about content features that distinguish the type.
  * Include key fields the document usually contains (e.g., invoice number, total amount).
  * Add multiple rules when needed to cover distinct patterns.
  * Start simple, test on a small set, then refine.


