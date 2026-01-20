[Skip to content](https://developers.llamaindex.ai/python/cloud/split/examples/document_splitting/#_top)
# Splitting Concatenated Documents
This guide demonstrates how to use the Split API to automatically segment a concatenated PDF into logical document sections based on content categories.
## Use Case
[Section titled “Use Case”](https://developers.llamaindex.ai/python/cloud/split/examples/document_splitting/#use-case)
When dealing with large PDFs that contain multiple distinct documents or sections (e.g., a bundle of research papers, a collection of reports), you often need to split them into individual segments. The Split API uses AI to:
  1. Analyze each page’s content
  2. Classify pages into user-defined categories
  3. Group consecutive pages of the same category into segments


## Example Document
[Section titled “Example Document”](https://developers.llamaindex.ai/python/cloud/split/examples/document_splitting/#example-document)
We’ll use a PDF containing three concatenated documents:
  * **Alan Turing’s essay** “Intelligent Machinery, A Heretical Theory” (an essay)
  * **ImageNet paper** (a research paper)
  * **“Attention is All You Need”** paper (a research paper)


We’ll split this into segments categorized as either `essay` or `research_paper`.
📄 [Download the example PDF](https://github.com/run-llama/llama_cloud_services/blob/main/examples/split/document_splitting/data/turing%2Bimagenet%2Battention.pdf)
## Setup
[Section titled “Setup”](https://developers.llamaindex.ai/python/cloud/split/examples/document_splitting/#setup)
Install the required packages:
Terminal window```


pipinstallllama-cloudpython-dotenvrequests


```

Set up your environment:
```


import os




import time




import requests




from dotenv import load_dotenv





load_dotenv()





LLAMA_CLOUD_API_KEY= os.environ.get("LLAMA_CLOUD_API_KEY")




BASE_URL= os.environ.get("LLAMA_CLOUD_BASE_URL","https://api.cloud.llamaindex.ai")




PROJECT_ID= os.environ.get("LLAMA_CLOUD_PROJECT_ID",None)





headers = {




"Authorization": f"Bearer {LLAMA_CLOUD_API_KEY}",




"Content-Type": "application/json",



```

## Step 1: Upload the PDF
[Section titled “Step 1: Upload the PDF”](https://developers.llamaindex.ai/python/cloud/split/examples/document_splitting/#step-1-upload-the-pdf)
Upload the concatenated PDF to LlamaCloud using the `llama-cloud` SDK:
```


from llama_cloud.client import LlamaCloud





client =LlamaCloud(token=LLAMA_CLOUD_API_KEY,base_url=BASE_URL)





pdf_path ="./data/turing+imagenet+attention.pdf"





withopen(pdf_path,"rb") as f:




uploaded_file = client.files.upload_file(upload_file=f,project_id=PROJECT_ID)





file_id = uploaded_file.id




print(f"✅ File uploaded: {uploaded_file.name}")


```

## Step 2: Create a Split Job
[Section titled “Step 2: Create a Split Job”](https://developers.llamaindex.ai/python/cloud/split/examples/document_splitting/#step-2-create-a-split-job)
Create a split job with category definitions. Each category needs a `name` and a `description` that helps the AI understand what content belongs to that category:
```


split_request = {




"document_input": {




"type": "file_id",




"value": file_id,





"categories": [





"name": "essay",




"description": "A philosophical or reflective piece of writing that presents personal viewpoints, arguments, or thoughts on a topic without strict formal structure",






"name": "research_paper",




"description": "A formal academic document presenting original research, methodology, experiments, results, and conclusions with citations and references",








response = requests.post(




f"{BASE_URL}/api/v1/beta/split/jobs",




params={"project_id": PROJECT_ID},




headers=headers,




json=split_request,





response.raise_for_status()





split_job = response.json()




job_id = split_job["id"]





print(f"✅ Split job created: {job_id}")




print(f"   Status: {split_job['status']}")


```

## Step 3: Poll for Completion
[Section titled “Step 3: Poll for Completion”](https://developers.llamaindex.ai/python/cloud/split/examples/document_splitting/#step-3-poll-for-completion)
The split job runs asynchronously. Poll until it completes:
```


defpoll_split_job(job_id: str, max_wait_seconds: int=180, poll_interval: int=5):




start_time = time.time()





while (time.time() - start_time)  max_wait_seconds:




response = requests.get(




f"{BASE_URL}/api/v1/beta/split/jobs/{job_id}",




params={"project_id": PROJECT_ID},




headers=headers,





response.raise_for_status()




job = response.json()





status = job["status"]




elapsed =int(time.time()- start_time)




print(f"   Status: {status} (elapsed: {elapsed}s)")





if status in["completed", "failed"]:




return job





time.sleep(poll_interval)





raiseTimeoutError(f"Job did not complete within {max_wait_seconds} seconds")





completed_job =poll_split_job(job_id)


```

## Step 4: Analyze Results
[Section titled “Step 4: Analyze Results”](https://developers.llamaindex.ai/python/cloud/split/examples/document_splitting/#step-4-analyze-results)
Examine the split results:
```


segments = completed_job.get("result", {}).get("segments",[])





print(f"📊 Total segments found: (segments)}")





for i, segment inenumerate(segments,1):




category = segment["category"]




pages = segment["pages"]




confidence = segment["confidence_category"]





iflen(pages) ==1:




page_range =f"Page {pages[0]}"




else:




page_range =f"Pages (pages)}-(pages)}"





print(f"\nSegment {i}:")




print(f"   Category: {category}")




print(f{page_range} ((pages)} pages)")




print(f"   Confidence: {confidence}")


```

### Expected Output
[Section titled “Expected Output”](https://developers.llamaindex.ai/python/cloud/split/examples/document_splitting/#expected-output)
```

📊 Total segments found: 3



Segment 1:



Category: essay




Pages 1-4 (4 pages)




Confidence: high




Segment 2:



Category: research_paper




Pages 5-13 (9 pages)




Confidence: high




Segment 3:



Category: research_paper




Pages 14-24 (11 pages)




Confidence: high


```

The Split API correctly identified:
  * **1 essay segment** : Alan Turing’s “Intelligent Machinery, A Heretical Theory”
  * **2 research paper segments** : ImageNet paper and “Attention is All You Need”


## Using `allow_uncategorized`
[Section titled “Using allow_uncategorized”](https://developers.llamaindex.ai/python/cloud/split/examples/document_splitting/#using-allow_uncategorized)
You can use the `allow_uncategorized` strategy when you want to capture pages that don’t match any defined category:
```


split_request_uncategorized = {




"document_input": {"type": "file_id", "value": file_id},




"categories": [





"name": "essay",




"description": "A philosophical or reflective piece of writing that presents personal viewpoints",





# Only 'essay' defined - research papers will be 'uncategorized'





"splitting_strategy": {"allow_uncategorized": True},



```

With this configuration, pages that don’t match `essay` will be grouped as `uncategorized`.
## Next Steps
[Section titled “Next Steps”](https://developers.llamaindex.ai/python/cloud/split/examples/document_splitting/#next-steps)
  * Explore the [REST API reference](https://developers.llamaindex.ai/python/cloud/split/examples/getting_started/api) for all available options
  * Combine Split with [LlamaExtract](https://developers.llamaindex.ai/python/cloud/split/llamaextract/getting_started) to run targeted extraction on each segment
  * Use [LlamaParse](https://developers.llamaindex.ai/python/cloud/split/llamaparse/getting_started) to parse individual segments with optimized settings


