[Skip to content](https://developers.llamaindex.ai/python/cloud/llamaparse/getting_started/#_top)
# Getting Started
Quickly start parsing documents with LlamaParse—whether you prefer Python, TypeScript, or using the web UI. This guide walks you through creating an API key and running your first job.
## Get your API Key
[Section titled “Get your API Key”](https://developers.llamaindex.ai/python/cloud/llamaparse/getting_started/#get-your-api-key)
🔑 **Before you begin** : You’ll need an API key to access LlamaParse services.
[**Get your API key →**](https://developers.llamaindex.ai/python/cloud/general/api_key)
## Choose Your Setup
[Section titled “Choose Your Setup”](https://developers.llamaindex.ai/python/cloud/llamaparse/getting_started/#choose-your-setup)


#### Using LlamaParse in the Web UI
[Section titled “Using LlamaParse in the Web UI”](https://developers.llamaindex.ai/python/cloud/llamaparse/getting_started/#using-llamaparse-in-the-web-ui)
If you’re non-technical or just want to quickly sandbox LlamaParse, the web interface is the easiest way to get started.
#### Step-by-Step Workflow
[Section titled “Step-by-Step Workflow”](https://developers.llamaindex.ai/python/cloud/llamaparse/getting_started/#step-by-step-workflow)
  1. Go to [LlamaCloud](https://cloud.llamaindex.ai/parse)
  2. Choose a parsing **Tier** from **Recommended Settings** or switch to **Advanced settings** for a custom configuration
  3. Upload your document
  4. Click **Parse** and view your parsed results right in the browser


#### Choosing a Tier
[Section titled “Choosing a Tier”](https://developers.llamaindex.ai/python/cloud/llamaparse/getting_started/#choosing-a-tier)
LlamaParse offers four main tiers:
  * [**Cost Effective**](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/presets#cost-effective) – Optimized for speed and cost. Best for text-heavy documents with minimal structure.
  * [**Agentic**](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/presets#agentic) – Works well with documents that have images and diagrams, but may struggle with complex layouts.
  * [**Agentic Plus**](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/presets#agentic-plus) – Maximum fidelity. Best for complex layouts, tables, and visual structure.
  * [**Fast**] – A special mode that only outputs the spatial text of your documents, but not the markdown.


[Learn more about parsing presets](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/presets)
#### Advanced Settings for Custom Modes
[Section titled “Advanced Settings for Custom Modes”](https://developers.llamaindex.ai/python/cloud/llamaparse/getting_started/#advanced-settings-for-custom-modes)
The **Advanced Settings** option gives you full control over how your documents are parsed. You can select from a wide range of modes including multimodal and model-specific options.
This is best suited for advanced use cases. [Learn more about parsing modes](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/advance_parsing_modes)
#### Install the package
[Section titled “Install the package”](https://developers.llamaindex.ai/python/cloud/llamaparse/getting_started/#install-the-package)
Terminal window```


pipinstallllama-cloud-services


```

#### Parse from CLI
[Section titled “Parse from CLI”](https://developers.llamaindex.ai/python/cloud/llamaparse/getting_started/#parse-from-cli)
You can parse your first PDF file using the command line interface. Use the command `llama-parse [file_paths]`. See the help text with `llama-parse --help`.
Terminal window```


exportLLAMA_CLOUD_API_KEY='llx-...'




# output as text



llama-parsemy_file.pdf--result-typetext--output-fileoutput.txt




# output as markdown



llama-parsemy_file.pdf--result-typemarkdown--output-fileoutput.md




# output as raw json



llama-parsemy_file.pdf--output-raw-json--output-fileoutput.json


```

#### Parse in Python
[Section titled “Parse in Python”](https://developers.llamaindex.ai/python/cloud/llamaparse/getting_started/#parse-in-python)
You can also create simple scripts:
```


from llama_cloud_services import LlamaParse





parser =LlamaParse(




api_key="llx-...",# can also be set in your env as LLAMA_CLOUD_API_KEY




num_workers=4,# if multiple files passed, split in `num_workers` API calls




verbose=True,




language="en",# optionally define a language, default=en





# sync



result = parser.parse("./my_file.pdf")




# sync batch



results = parser.parse(["./my_file1.pdf", "./my_file2.pdf"])




# async



result =await parser.aparse("./my_file.pdf")




# async batch



results =await parser.aparse(["./my_file1.pdf", "./my_file2.pdf"])


```

The result object is a fully typed `JobResult` object. You can interact with it to parse and transform various parts of the result:
```

# get the llama-index markdown documents



markdown_documents = result.get_markdown_documents(split_by_page=True)




# get the llama-index text documents



text_documents = result.get_text_documents(split_by_page=False)




# get the image documents



image_documents = result.get_image_documents(




include_screenshot_images=True,




include_object_images=False,




# Optional: download the images to a directory




# (default is to return the image bytes in ImageDocument objects)




image_download_dir="./images",





# access the raw job result


# Items will vary based on the parser configuration



for page in result.pages:




print(page.text)




print(page.md)




print(page.images)




print(page.layout)




print(page.structuredData)


```

That’s it! Take a look at the examples below or head to the [Python client docs ](https://github.com/run-llama/llama_cloud_services/blob/main/parse.md#llamaparse).
#### Examples
[Section titled “Examples”](https://developers.llamaindex.ai/python/cloud/llamaparse/getting_started/#examples)
Several end-to-end indexing examples can be found in the Client’s examples folder:


#### Install the package
[Section titled “Install the package”](https://developers.llamaindex.ai/python/cloud/llamaparse/getting_started/#install-the-package-1)
Terminal window```


npminit




npminstall-Dtypescript@types/node


```

LlamaParse support is built-in to LlamaIndex for TypeScript, so you’ll need to install LlamaIndex.TS:
Terminal window```


npminstallllama-cloud-servicesdotenv


```

Let’s create a `parse.ts` file and put our dependencies in it:
```


import {




LlamaParseReader,




// we'll add more here later




} from"llama-cloud-services";




import'dotenv/config'


```

Now let’s create our main function, which will load in [fun facts about Canada](https://media.canada.travel/sites/default/files/2018-06/MediaCentre-FunFacts_EN_1.pdf) and parse them:
```


asyncfunctionmain() {




// save the file linked above as sf_budget.pdf, or change this to match




const path"./canada.pdf";





// set up the llamaparse reader




const readernewLlamaParseReader({ resultType: "markdown" });





// parse the document




const documents = await reader.loadData(path);





// print the parsed document




console.log(documents)






main().catch(console.error);


```

Now run the file:
Terminal window```


npxtsxparse.ts


```

Congratulations! You’ve parsed the file, and should see output that looks like this:
```



Document {




id_: '02f5e252-9dca-47fa-80b2-abdd902b911a',




embedding: undefined,




metadata: { file_path: './canada.pdf' },




excludedEmbedMetadataKeys: [],




excludedLlmMetadataKeys: [],




relationships: {},




text: '# Fun Facts About Canada\n' +




'\n' +




'We may be known as the Great White North, but




...etc...


```

You can now use this in your own TypeScript projects. Head over to the [TypeScript docs](https://ts.llamaindex.ai/) to learn more about LlamaIndex in TypeScript.
#### Using the REST API
[Section titled “Using the REST API”](https://developers.llamaindex.ai/python/cloud/llamaparse/getting_started/#using-the-rest-api)
If you would prefer to use a raw API, the REST API lets you integrate parsing into any environment—no client required. Below are sample endpoints to help you get started.
#### 1. Upload a file and start parsing
[Section titled “1. Upload a file and start parsing”](https://developers.llamaindex.ai/python/cloud/llamaparse/getting_started/#1-upload-a-file-and-start-parsing)
Send a document to the API to begin the parsing job:
Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

#### 2. Check the status of a parsing job
[Section titled “2. Check the status of a parsing job”](https://developers.llamaindex.ai/python/cloud/llamaparse/getting_started/#2-check-the-status-of-a-parsing-job)
Use the `job_id` returned from the upload step to monitor parsing progress:
Terminal window```


curl-X'GET'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/job/<job_id>'\




-H'accept: application/json'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"


```

#### 3. Retrieve results in Markdown
[Section titled “3. Retrieve results in Markdown”](https://developers.llamaindex.ai/python/cloud/llamaparse/getting_started/#3-retrieve-results-in-markdown)
Once the job is complete, you can fetch the structured result:
Terminal window```


curl-X'GET'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/job/<job_id>/result/markdown'\




-H'accept: application/json'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"


```

See more details in our [API Reference](https://developers.llamaindex.ai/cloud-api-reference/category/parsing)
#### Example
[Section titled “Example”](https://developers.llamaindex.ai/python/cloud/llamaparse/getting_started/#example)
Here is an example notebook for [Raw API Usage](https://github.com/run-llama/llama_cloud_services/blob/main/examples/parse/demo_api.ipynb)
## Resources
[Section titled “Resources”](https://developers.llamaindex.ai/python/cloud/llamaparse/getting_started/#resources)
  * See [Credit Pricing & Usage](https://developers.llamaindex.ai/python/cloud/general/pricing)
  * Next steps? Check out [LlamaExtract](https://developers.llamaindex.ai/python/cloud/llamaextract/getting_started) to extract structured data from unstructured documents!


