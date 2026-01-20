[Skip to content](https://developers.llamaindex.ai/python/cloud/llamaextract/getting_started/python/#_top)
# Python SDK
For a more programmatic approach, the Python SDK is the recommended way to experiment with different schemas and run extractions at scale. The Github repo for the Python SDK is [here](https://github.com/run-llama/llama_cloud_services/).
First, [get an api key](https://developers.llamaindex.ai/python/cloud/general/api_key). We recommend putting your key in a file called `.env` that looks like this:
Terminal window```


LLAMA_CLOUD_API_KEY=llx-xxxxxx


```

Set up a new python environment using the tool of your choice, we used `poetry init`. Then install the deps you’ll need:
Terminal window```


pipinstallllama-cloud-servicespython-dotenv


```

Now we have our libraries and our API key available, let’s create a `extract.py` file and extract data from files. In this case, we’re using some sample [resumes](https://github.com/run-llama/llama_cloud_services/tree/main/examples/extract/data) from our example:
## Quick Start
[Section titled “Quick Start”](https://developers.llamaindex.ai/python/cloud/llamaextract/getting_started/python/#quick-start)
```


from llama_cloud_services import LlamaExtract




from pydantic import BaseModel, Field




# bring in our LLAMA_CLOUD_API_KEY



from dotenv import load_dotenv




load_dotenv()




# Initialize client



extractor =LlamaExtract()




# Define schema using Pydantic



classResume(BaseModel):




name: str=Field(description="Full name of candidate")




email: str=Field(description="Email address")




skills: list[str] =Field(description="Technical skills and technologies")




# Create extraction agent



agent = extractor.create_agent(name="resume-parser",data_schema=Resume)




# Extract data from document



result = agent.extract("resume.pdf")




print(result.data)


```

Now run it like any python file. This will print the results of the extraction.
Terminal window```


pythonextract.py


```

## Defining Schemas
[Section titled “Defining Schemas”](https://developers.llamaindex.ai/python/cloud/llamaextract/getting_started/python/#defining-schemas)
Schemas can be defined using either Pydantic models or JSON Schema. Refer to the [Schemas](https://developers.llamaindex.ai/python/cloud/llamaextract/features/schema_design) page for more details.
## Other Extraction APIs
[Section titled “Other Extraction APIs”](https://developers.llamaindex.ai/python/cloud/llamaextract/getting_started/python/#other-extraction-apis)
### Extraction over bytes or text
[Section titled “Extraction over bytes or text”](https://developers.llamaindex.ai/python/cloud/llamaextract/getting_started/python/#extraction-over-bytes-or-text)
You can use the `SourceText` class to extract from bytes or text directly without using a file. If passing the file bytes, you will need to pass the filename to the `SourceText` class.
```


withopen("resume.pdf","rb") as f:




file_bytes = f.read()




result = test_agent.extract(SourceText(file=file_bytes,filename="resume.pdf"))


```

```


result = test_agent.extract(SourceText(text_content="Candidate Name: Jane Doe"))


```

### Batch Processing
[Section titled “Batch Processing”](https://developers.llamaindex.ai/python/cloud/llamaextract/getting_started/python/#batch-processing)
Process multiple files asynchronously:
```

# Queue multiple files for extraction



jobs =await agent.queue_extraction(["resume1.pdf", "resume2.pdf"])




# Check job status



for job in jobs:




status = agent.get_extraction_job(job.id).status




print(f"Job {job.id}: {status}")




# Get results when complete



results =[agent.get_extraction_run_for_job(job.id) for job in jobs]


```

### Updating Schemas
[Section titled “Updating Schemas”](https://developers.llamaindex.ai/python/cloud/llamaextract/getting_started/python/#updating-schemas)
Schemas can be modified and updated after creation:
```

# Update schema



agent.data_schema = new_schema




# Save changes



agent.save()


```

### Managing Agents
[Section titled “Managing Agents”](https://developers.llamaindex.ai/python/cloud/llamaextract/getting_started/python/#managing-agents)
```

# List all agents



agents = extractor.list_agents()




# Get specific agent



agent = extractor.get_agent(name="resume-parser")




# Delete agent



extractor.delete_agent(agent.id)


```

