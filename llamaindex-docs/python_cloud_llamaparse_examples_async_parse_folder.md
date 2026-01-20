[Skip to content](https://developers.llamaindex.ai/python/cloud/llamaparse/examples/async_parse_folder/#_top)
# Parse All PDFs in a Folder with LlamaParse
This example demonstrates how to process multiple PDFs from a folder using LlamaParse with controlled concurrency using asyncio and semaphores. You can follow along with this tutorial alongside an example script that handles async parsing, given a directory name in our `llama_cloud_services` repository: [batch_parse_folder.py](https://github.com/run-llama/llama_cloud_services/blob/main/examples/parse/batch_parse_folder.py)
## Setup
[Section titled “Setup”](https://developers.llamaindex.ai/python/cloud/llamaparse/examples/async_parse_folder/#setup)
### Environment Variables
[Section titled “Environment Variables”](https://developers.llamaindex.ai/python/cloud/llamaparse/examples/async_parse_folder/#environment-variables)
Set your `LLAMA_CLOUD_API_KEY` environment variable:
Terminal window```


exportLLAMA_CLOUD_API_KEY='llx-...'


```

Or create a `.env` file:
Terminal window```


LLAMA_CLOUD_API_KEY=llx-...


```

### Install Dependencies
[Section titled “Install Dependencies”](https://developers.llamaindex.ai/python/cloud/llamaparse/examples/async_parse_folder/#install-dependencies)
Terminal window```


pipinstallllama-cloud-servicespython-dotenvrequests


```

## Quick Start
[Section titled “Quick Start”](https://developers.llamaindex.ai/python/cloud/llamaparse/examples/async_parse_folder/#quick-start)
### Download Example PDFs
[Section titled “Download Example PDFs”](https://developers.llamaindex.ai/python/cloud/llamaparse/examples/async_parse_folder/#download-example-pdfs)
Download sample PDFs to test with:
```


import os




import requests




from pathlib import Path




# Create sample_files directory



sample_dir =Path("sample_files")




sample_dir.mkdir(exist_ok=True)




# Sample documents to download



sample_docs = {




"attention.pdf": "https://arxiv.org/pdf/1706.03762.pdf",




"bert.pdf": "https://arxiv.org/pdf/1810.04805.pdf",





# Download sample documents with error handling



for filename, url in sample_docs.items():




filepath = sample_dir / filename




ifnot filepath.exists():




print(f"📥 Downloading {filename}...")




try:




response = requests.get(url,timeout=30)




response.raise_for_status()





# Basic content validation




if response.headers.get('content-type','').startswith('application/pdf'):




withopen(filepath,"wb") as f:




f.write(response.content)




print(f"   ✅ Downloaded {filename}")




else:




print(f"   ⚠️ Warning: {filename} may not be a valid PDF")




except requests.RequestException as e:




print(f"   ❌ Failed to download {filename}: {e}")




else:




print(f"📁 {filename} already exists")





print("\n✅ Sample files ready!")


```

## Use Asyncio and Semaphore with LlamaParse
[Section titled “Use Asyncio and Semaphore with LlamaParse”](https://developers.llamaindex.ai/python/cloud/llamaparse/examples/async_parse_folder/#use-asyncio-and-semaphore-with-llamaparse)
We can use asyncio to batch parse multiple files in a folder. Below is a complete example script that parses all PDF files in a directory with controlled concurrency:
```


import asyncio





from llama_cloud_services import LlamaParse





pdf_files =list(input_dir.glob("*.pdf"))




# Initialize parser



parser =LlamaParse(




api_key=api_key,




num_workers=1,# We control concurrency with semaphore




show_progress=False,# We'll show our own progress





# Create semaphore to limit concurrent requests



semaphore = asyncio.Semaphore(max_concurrent)




# A helper function to parse a single file with semaphore



asyncdefparse_single_file(




parser,




file_path,




semaphore,





asyncwith semaphore:




try:




print(f"Starting parse: {file_path.name}")





result =await parser.aparse(str(file_path))





print(f"✓ Completed: {file_path.name} ((result.pages)} pages)")





return {




"file": file_path.name,




"status": "success",




"result": result,




"pages": len(result.pages) if result.pages else0,





exceptExceptionas e:




print(f"✗ Error parsing {file_path.name}: (e)}")




return {




"file": file_path.name,




"status": "error",




"error": str(e),





# Create tasks for all files



tasks =[




parse_single_file(parser, pdf_file, semaphore)




for pdf_file in pdf_files






results =await asyncio.gather(*tasks)


```

Alternatively, you can use the `batch_parse_folder.py` script we’ve provided, which you can use with the `sample_files` directory you created before:
Terminal window```


pythonbatch_parse_folder.py--input-dir./sample_files--max-concurrent5


```

**Parameters:**
  * `--input-dir`: Directory containing PDF files to parse
  * `--max-concurrent`: Controls the maximum number of concurrent parse operations. Adjust based on: 
    * Your API rate limits (typically 5-10 for most accounts)
    * Available network bandwidth
    * Server capacity
    * File sizes (larger files may require lower concurrency to avoid memory issues)


## Example Output
[Section titled “Example Output”](https://developers.llamaindex.ai/python/cloud/llamaparse/examples/async_parse_folder/#example-output)
```

Found 2 PDF files to parse


Processing 2 files with max 5 concurrent operations...


Starting parse: attention.pdf


Starting parse: bert.pdf


Started parsing the file under job_id 1a7b8f3b-9119-4e38-954d-b67b8e96b3d6


Started parsing the file under job_id 28123aeb-dd3e-4398-b754-0cb101a3b78b


✓ Completed: attention.pdf (15 pages)


✓ Completed: bert.pdf (16 pages)


PARSE SUMMARY



Total files: 2


Successful: 2


Failed: 0


Total time: 10.00 seconds


Average time per file: 5.00 seconds

```

## How It Works
[Section titled “How It Works”](https://developers.llamaindex.ai/python/cloud/llamaparse/examples/async_parse_folder/#how-it-works)
  1. **Semaphore-based Concurrency** : Uses `asyncio.Semaphore` to limit concurrent requests, preventing API rate limit errors and managing resource usage.
  2. **Async Processing** : Each file is parsed asynchronously using `parser.aparse()`, allowing multiple files to be processed concurrently up to the semaphore limit.
  3. **Result Aggregation** : All results are collected and summarized at the end, providing a complete overview of the parsing operation.


