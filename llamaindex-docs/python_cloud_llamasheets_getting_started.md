[Skip to content](https://developers.llamaindex.ai/python/cloud/llamasheets/getting_started/#_top)
# Getting Started
LlamaSheets is a new beta API for extracting regions and tables out of messy spreadsheets. A critical step in document understanding is normalizing inputs. Using the LlamaSheets API, it will
  1. Intelligently identify regions per spreadsheet
  2. Isolate and extract each region in a spreadsheet
  3. Output them as [Parquet files](https://parquet.apache.org/docs/overview/), a portable format supported by many languages that retains type information. For example, you can load these directly as dataframes with Pandas in Python.
  4. Generates additional metadata about the regions (extracted location, title, description) and spreadsheets (title, description) to assist in downstream flows.


## Basic Usage
[Section titled “Basic Usage”](https://developers.llamaindex.ai/python/cloud/llamasheets/getting_started/#basic-usage)
The Python SDK provides an end-to-end method across multiple API calls to complete the extraction.
```


from llama_cloud_services.beta.sheets import LlamaSheets, SpreadsheetParsingConfig





client =LlamaSheets(api_key="...")





results =await client.aextract_regions(




"path_to_file.xlsx",# Supports paths, bytes, and streams




config=SpreadsheetParsingConfig(




sheet_names=None,# Parse all sheets




generate_additional_metadata=True,# Generate titles/descriptions per sheet






# Download parquet files



file_bytes =await client.adownload_region_result(




results.id,




results.regions[0].region_id,




result_type="table",# can be `table`, `extra`, or `cell_metadata`





# Download parquet files and convert to pandas dataframes



df =await client.adownload_region_as_dataframe(




results.id,




results.regions[0].region_id,




result_type="table",



```

### Lower-Level Usage
[Section titled “Lower-Level Usage”](https://developers.llamaindex.ai/python/cloud/llamasheets/getting_started/#lower-level-usage)
Using the LlamaSheets API for region and table extraction generally consists of 4 main steps.
Below, we detail each step using both the Python SDK and raw HTTP calls.
#### 1. Upload a File
[Section titled “1. Upload a File”](https://developers.llamaindex.ai/python/cloud/llamasheets/getting_started/#1-upload-a-file)
First, upload a file, and get a File ID:


```


from llama_cloud_services.beta.sheets import LlamaSheets




# Initialize the client



client =LlamaSheets(api_key="your_api_key")




# Upload a file



file_response =await client.aupload_file("path/to/your/spreadsheet.xlsx")




print(f"File ID: {file_response.id}")


```

Terminal window```


curl-XPOST"https://api.cloud.llamaindex.ai/api/v1/files"\




-H"Authorization: Bearer YOUR_API_KEY"\




-F"upload_file=@path/to/your/spreadsheet.xlsx"


```

Response:
```



"id": "file-id-here",




```

#### 2. Create a job
[Section titled “2. Create a job”](https://developers.llamaindex.ai/python/cloud/llamasheets/getting_started/#2-create-a-job)
Using the File ID, you can create a job for extraction to get a job ID:


```


from llama_cloud_services.beta.sheets.types import SpreadsheetParsingConfig




# Create a job with optional configuration



config =SpreadsheetParsingConfig(




sheet_names=None,# Parse all sheets (default)




generate_additional_metadata=True# Generate extra metadata






job =await client.acreate_job(file_id=file_response.id,config=config)




print(f"Job ID: {job.id}")




print(f"Status: {job.status}")


```

You can also pass the config as a dict:
```


job =await client.acreate_job(




file_id=file_response.id,




config={"generate_additional_metadata": True}



```

Terminal window```


curl-XPOST"https://api.cloud.llamaindex.ai/api/v1/beta/sheets/jobs"\




-H"Authorization: Bearer YOUR_API_KEY"\




-H"Content-Type: application/json"\





"file_id": "file-id-here",




"config": {




"sheet_names": null,




"generate_additional_metadata": true




```

Response:
```



"id": "job-id-here",




"file_id": "file-id-here",




"status": "PENDING",




"project_id": "project-id",




"created_at": "2024-01-01T00:00:00Z",




```

#### 3. Wait for completion
[Section titled “3. Wait for completion”](https://developers.llamaindex.ai/python/cloud/llamasheets/getting_started/#3-wait-for-completion)
Now that you have a job ID, you can wait for the job to finish:


```

# Wait for the job to complete (polls automatically)



job_result =await client.await_for_completion(job_id=job.id)




print(f"Job Status: {job_result.status}")




# Access extracted regions metadata



if job_result.regions:




print(f"Found (job_result.regions)} region(s)")




for region in job_result.regions:




print(f"  - Region ID: {region.region_id}")




print(f"    Sheet: {region.sheet_name}")




print(f"    Location: {region.location}")





for worksheet_metadata in job_result.worksheet_metadata:




print(f"Worksheet Title: {worksheet_metadata.title}")




print(f"Worksheet Description: {worksheet_metadata.description}")


```

Alternatively, you can manually poll:
```


whileTrue:




job_result =await client.aget_job(job_id=job.id,include_results_metadata=True)





if job_result.status in["SUCCESS", "PARTIAL_SUCCESS", "ERROR", "FAILURE"]:




break





print(f"Status: {job_result.status}")




await asyncio.sleep(5)


```

Terminal window```

# Poll for job status



curl-XGET"https://api.cloud.llamaindex.ai/api/v1/beta/sheets/jobs/job-id-here?include_results=true"\




-H"Authorization: Bearer YOUR_API_KEY"


```

Response when complete:
```



"id": "job-id-here",




"status": "SUCCESS",




"regions": [





"region_id": "region-id-1",




"sheet_name": "Sheet1",




"location": "A1:D10",




"title": "Sales Data",




"description": "Monthly sales figures"






```

Keep polling until `status` is one of: `SUCCESS`, `PARTIAL_SUCCESS`, `ERROR`, or `FAILURE`.
#### 4. Download the result
[Section titled “4. Download the result”](https://developers.llamaindex.ai/python/cloud/llamasheets/getting_started/#4-download-the-result)
With a completed job, you can download the generated Parquet file and read any additional metadata about the job result:


```


from llama_cloud_services.beta.sheets.types import SpreadsheetResultType




import pandas as pd




# Download a region directly as a pandas DataFrame



region_id = job_result.regions[0].region_id




result_type = job_result.regions[0].region_type




df =await client.adownload_region_as_dataframe(




job_id=job.id,




region_id=region_id,




result_type=result_type,# Use region_type from result or `cell_metadata`






print(f"Region shape: {df.shape}")




print(df.head())




# Optionally, download cell metadata



metadata_df =await client.adownload_region_as_dataframe(




job_id=job.id,




region_id=region_id,




result_type=SpreadsheetResultType.CELL_METADATA





print(f"Metadata shape: {metadata_df.shape}")


```

You can also download raw parquet bytes:
```

# Download as raw bytes



parquet_bytes =await client.adownload_region_result(




job_id=job.id,




region_id=region_id,




result_type=SpreadsheetResultType.TABLE





# Save to file



withopen("region.parquet","wb") as f:




f.write(parquet_bytes)


```

Terminal window```

# Step 1: Get presigned URL for the regino



curl-XGET"https://api.cloud.llamaindex.ai/api/v1/beta/sheets/jobs/job-id-here/regions/region-id-here/result/table"\




-H"Authorization: Bearer YOUR_API_KEY"


```

Response:
```



"url": "https://s3.amazonaws.com/...",




"expires_at": "2024-01-01T01:00:00Z"



```

Terminal window```

# Step 2: Download the parquet file using the presigned URL



curl-XGET"https://s3.amazonaws.com/..."-oregion.parquet




# Load with pandas



python-c"import pandas as pd; df = pd.read_parquet('region.parquet'); print(df.head())"


```

To download cell metadata, use `result/cell_metadata` instead of `result/table`:
Terminal window```


curl-XGET"https://api.cloud.llamaindex.ai/api/v1/beta/sheets/jobs/job-id-here/regions/region-id-here/result/cell_metadata"\




-H"Authorization: Bearer YOUR_API_KEY"


```

## Understanding the Output Format
[Section titled “Understanding the Output Format”](https://developers.llamaindex.ai/python/cloud/llamasheets/getting_started/#understanding-the-output-format)
When a LlamaSheets job completes successfully, you receive rich structured data about the extracted regions. This section explains the different components of the output.
### Job Result Structure
[Section titled “Job Result Structure”](https://developers.llamaindex.ai/python/cloud/llamasheets/getting_started/#job-result-structure)
The job result object contains:
```



"id": "job-id",




"status": "SUCCESS",




"file_id": "original-file-id",




"config": { /* your parsing config */ },




"created_at": "2024-01-01T00:00:00Z",




"updated_at": "2024-01-01T00:05:00Z",




"regions": [





"region_id": "uuid-here",




"sheet_name": "Sheet1",




"location": "A2:E11",




"title": "Some title",




"description": "Some description"






"worksheet_metadata": [





"sheet_name": "Sheet1",




"title": "Sales Data Q1 2024",




"description": "Quarterly sales figures with revenue, units sold, and regional breakdowns"






"errors": []



```

**Key fields:**
  * `regions`: Array of extracted regions and tables with their IDs and locations
  * `worksheet_metadata`: Generated titles and descriptions for each sheet (when `generate_additional_metadata: true`)
  * `status`: One of `SUCCESS`, `PARTIAL_SUCCESS`, `ERROR`, or `FAILURE`


### Region Table Data (Parquet Files)
[Section titled “Region Table Data (Parquet Files)”](https://developers.llamaindex.ai/python/cloud/llamasheets/getting_started/#region-table-data-parquet-files)
Each extracted region is saved as a [Parquet file](https://parquet.apache.org/docs/overview/) containing the normalized table data. Parquet is a columnar storage format that:
  * Preserves data types (dates, numbers, strings, booleans)
  * Is highly efficient and compressed
  * Can be read by pandas, polars, DuckDB, and many other tools


**Example region structure:**
```


import pandas as pd





df = pd.read_parquet("region.parquet")




print(df.head())




# Output:


#    col_0  col_1      col_2       col_3  col_4


# 0     44  -124.6  Value_0_2  2020-01-01  False


# 1    153   -34.4  Value_1_2  2020-01-02   True


# 2    184    34.4  Value_2_2  2020-01-03  False

```

### Cell Metadata (Parquet Files)
[Section titled “Cell Metadata (Parquet Files)”](https://developers.llamaindex.ai/python/cloud/llamasheets/getting_started/#cell-metadata-parquet-files)
In addition to the region data, you can download rich **cell-level metadata** that provides detailed information about each cell in the extracted region. This is particularly useful for:
  * Understanding cell formatting and styling
  * Analyzing table structure and layout
  * Detecting data types and patterns
  * Preserving formatting for downstream processing


The following types of fields are available:
**Position & Layout:**
  * `row_number`, `column_number`: Cell coordinates
  * `coordinate`: Excel-style cell reference (e.g., “A1”)
  * `relative_row_position`, `relative_column_position`: Normalized position (0.0 to 1.0)
  * `is_in_first_row`, `is_in_last_row`, `is_in_first_column`, `is_in_last_column`: Boolean flags
  * `distance_from_origin`, `distance_from_center`: Geometric distances


**Formatting:**
  * `font_bold`, `font_italic`: Font style flags
  * `font_size`: Font size in points
  * `font_color_rgb`, `background_color_rgb`: Color values
  * `has_border`, `border_style_score`: Border information
  * `horizontal_alignment`, `vertical_alignment`: Alignment values
  * `text_wrap`: Text wrapping setting


**Cell Properties:**
  * `is_merged_cell`: Whether the cell is part of a merged range
  * `horizontal_size`, `vertical_size`: Cell dimensions
  * `alignment_indent`: Indentation level


**Data Type Detection:**
  * `data_type`: Detected type (Number, Text, Date, etc.)
  * `is_date_like`: Boolean flag for date detection
  * `is_percentage`, `is_currency`: Boolean flags for special number formats
  * `number_format_category`: Excel number format category
  * `text_length`: Length of text content
  * `has_special_chars`: Whether text contains special characters


**Content:**
  * `cell_value`: Processed cell value
  * `raw_cell_value`: Original raw value


**Clustering & Grouping:**
  * `group`, `sub_group`: Cell grouping identifiers
  * `l0_category`, `f_group`: Hierarchical categorization


**Example metadata usage:**
```


import pandas as pd




# Load cell metadata



metadata_df = pd.read_parquet("metadata.parquet")




# Find all header cells (first row)



headers = metadata_df[metadata_df['is_in_first_row'] ==True]




# Find all bolded cells (likely headers or emphasis)



bold_cells = metadata_df[metadata_df['font_bold'] ==True]




# Find date columns



date_cells = metadata_df[metadata_df['is_date_like'] ==True]




date_columns = date_cells['column_number'].unique()




# Analyze formatting patterns



print(f"Font sizes used: {metadata_df['font_size'].unique()}")




print(f"Data types present: {metadata_df['data_type'].unique()}")


```

### Downloading Results
[Section titled “Downloading Results”](https://developers.llamaindex.ai/python/cloud/llamasheets/getting_started/#downloading-results)
You can download two types of parquet files for each extracted region:
  1. **Table data** (`result_type="table"`): The actual table content
  2. **Extra data** (`result_type="extra"`): Any region that is not strictly a table of data (notes, titles, etc.)
  3. **Cell metadata** (`result_type="cell_metadata"`): Rich formatting and position metadata


All are stored as parquet files and can be easily loaded into pandas DataFrames for analysis.
## Beta Limitations
[Section titled “Beta Limitations”](https://developers.llamaindex.ai/python/cloud/llamasheets/getting_started/#beta-limitations)
As part of the beta period, there are a few key limitations to note:
  1. Job creation is limited to 1 request per second
  2. Sheet size is limited to max 100 columns or 10,000 rows (whichever limit is reached first per-sheet)


## Learn More
[Section titled “Learn More”](https://developers.llamaindex.ai/python/cloud/llamasheets/getting_started/#learn-more)
Beyond just extracting the regions, there are many downstream use-cases that can wrap these outputs.
  * [Use LlamaSheets with a Coding Agent](https://developers.llamaindex.ai/python/cloud/llamasheets/examples/coding_agent/)
  * [Code your own agent around LlamaSheets](https://developers.llamaindex.ai/python/cloud/llamasheets/examples/llama_index/)


