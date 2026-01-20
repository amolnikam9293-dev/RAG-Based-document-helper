[Skip to content](https://developers.llamaindex.ai/python/cloud/llamasheets/examples/llama_index/#_top)
# Using LlamaSheets with Custom Agents and Workflows
You can integrate LlamaSheets with any agent framework. Here, we go through an end-to-end example using agents from the LlamaIndex framework.
You can read more about LlamaIndex Agents [in the documentation.](https://developers.llamaindex.ai/python/framework/understanding/agent/)
The full code for this tutorial is available in the [examples folder for LlamaSheets](https://github.com/run-llama/llama_cloud_services/tree/main/examples/sheets/llama-index-agent/llama_index_example.py).
## Setup Guide
[Section titled “Setup Guide”](https://developers.llamaindex.ai/python/cloud/llamasheets/examples/llama_index/#setup-guide)
Follow these steps to set up your project for working with LlamaSheets and Claude.
### Step 1: Create Your Project Directory
[Section titled “Step 1: Create Your Project Directory”](https://developers.llamaindex.ai/python/cloud/llamasheets/examples/llama_index/#step-1-create-your-project-directory)
Terminal window```


mkdircoding-agent-analysis




cdcoding-agent-analysis




# Create directories



mkdirdata# For extracted parquet files




mkdirscripts# For analysis scripts




mkdirreports# For output reports


```

### Step 2: Install Dependencies
[Section titled “Step 2: Install Dependencies”](https://developers.llamaindex.ai/python/cloud/llamasheets/examples/llama_index/#step-2-install-dependencies)
Create a `requirements.txt`:
```

llama-cloud-services>=0.6.81  # LlamaSheets SDK


pandas>=2.0.0


pyarrow>=12.0.0


openpyxl>=3.0.0       # For Excel file support


matplotlib>=3.7.0     # For visualizations (optional)

```

Install dependencies:
Terminal window```


python-mvenvvenv




sourcevenv/bin/activate# On Windows: venv\Scripts\activate




pipinstall-rrequirements.txt


```

### Step 3: Set Up Environment Variables
[Section titled “Step 3: Set Up Environment Variables”](https://developers.llamaindex.ai/python/cloud/llamasheets/examples/llama_index/#step-3-set-up-environment-variables)
Create a `.env` file:
Terminal window```


LLAMA_CLOUD_API_KEY=your_api_key_here




OPENAI_API_KEY=your_api_key_here


```

### Step 4: Create an Extraction Helper Script
[Section titled “Step 4: Create an Extraction Helper Script”](https://developers.llamaindex.ai/python/cloud/llamasheets/examples/llama_index/#step-4-create-an-extraction-helper-script)
To help run extraction repeatedly on multiple files, the script below will help us automate larger tasks.
Create `scripts/extract.py`:
```


"""Helper script to extract spreadsheets using LlamaSheets."""





import asyncio




import json




import os




import dotenv




from pathlib import Path





from llama_cloud_services.beta.sheets import LlamaSheets




from llama_cloud_services.beta.sheets.types import (




SpreadsheetParsingConfig,




SpreadsheetResultType,






dotenv.load_dotenv()






asyncdefextract_spreadsheet(




file_path: str, output_dir: str="data", generate_metadata: bool=True




) -> dict:




"""Extract a spreadsheet using LlamaSheets."""





client =LlamaSheets(




base_url="https://api.cloud.llamaindex.ai",




api_key=os.getenv("LLAMA_CLOUD_API_KEY"),






print(f"Extracting {file_path}...")





# Extract regions




config =SpreadsheetParsingConfig(




sheet_names=None,# Extract all sheets




generate_additional_metadata=generate_metadata,






job_result =await client.aextract_regions(file_path,config=config)





print(f"Extracted (job_result.regions)} region(s)")





# Create output directory




output_path =Path(output_dir)




output_path.mkdir(parents=True,exist_ok=True)





# Get base name for files




base_name =Path(file_path).stem





# Save job metadata




job_metadata_path = output_path /f"{base_name}_job_metadata.json"




withopen(job_metadata_path,"w") as f:




json.dump(job_result.model_dump(mode="json"), f,indent=2)




print(f"Saved job metadata to {job_metadata_path}")





# Download each region




for idx, region inenumerate(job_result.regions,1):




sheet_name = region.sheet_name.replace("","_")





# Download region data




region_bytes =await client.adownload_region_result(




job_id=job_result.id,




region_id=region.region_id,




result_type=region.region_type,






region_path = output_path /f"{base_name}_region_{idx}_{sheet_name}.parquet"




withopen(region_path,"wb") as f:




f.write(region_bytes)




print(f"  Table {idx}: {region_path}")





# Download metadata




metadata_bytes =await client.adownload_region_result(




job_id=job_result.id,




region_id=region.region_id,




result_type=SpreadsheetResultType.CELL_METADATA,






metadata_path = output_path /f"{base_name}_metadata_{idx}_{sheet_name}.parquet"




withopen(metadata_path,"wb") as f:




f.write(metadata_bytes)




print(f"  Metadata {idx}: {metadata_path}")





print(f"\nAll files saved to {output_path}/")





return job_result.model_dump(mode="json")






if __name__ =="__main__":




import sys





iflen(sys.argv) 2:




print("Usage: python scripts/extract.py <spreadsheet_file>")




sys.exit(1)





file_path = sys.argv[1]





ifnotPath(file_path).exists():




print(f"❌ File not found: {file_path}")




sys.exit(1)





result = asyncio.run(extract_spreadsheet(file_path))




print(f"\n✅ Extraction complete! Job ID: {result['id']}")


```

### Step 5: Generate Sample Data (Optional)
[Section titled “Step 5: Generate Sample Data (Optional)”](https://developers.llamaindex.ai/python/cloud/llamasheets/examples/llama_index/#step-5-generate-sample-data-optional)
To follow along with the workflows below, you can generate sample spreadsheets using the provided generator script.
Download and save as `generate_sample_data.py`:
Terminal window```

# Get the script from GitHub examples or create it from the documentation



curl-ogenerate_sample_data.pyhttps://raw.githubusercontent.com/run-llama/llama-cloud-services/main/examples/sheets/coding-agent-analysis/generate_sample_data.py


```

Or copy the full script here (click to expand)
```

"""


Generate sample spreadsheets for LlamaSheets + Claude workflows.



This script creates example Excel files that demonstrate different use cases:


1. Simple data table (for Workflow 1)


2. Regional sales data (for Workflow 2)


3. Complex budget with formatting (for Workflow 3)


4. Weekly sales report (for Workflow 4)



Usage:



python generate_sample_data.py



"""




import random




from datetime import datetime, timedelta




from pathlib import Path





import pandas as pd




from openpyxl import Workbook




from openpyxl.styles import Font, PatternFill, Alignment, Border, Side






defgenerate_workflow_1_data(output_dir: Path):




"""Generate simple financial report for Workflow 1."""




print("📊 Generating Workflow 1: financial_report_q1.xlsx")





# Create sample quarterly data




months =["January", "February", "March"]




categories =["Revenue", "Cost of Goods Sold", "Operating Expenses", "Net Income"]





data =[]




for category in categories:




row = {"Category": category}




for month in months:




if category =="Revenue":




value = random.randint(80000,120000)




elif category =="Cost of Goods Sold":




value = random.randint(30000,50000)




elif category =="Operating Expenses":




value = random.randint(20000,35000)




else# Net Income




value = row.get("January",0) + row.get("February",0) + row.get("March",0)




value = random.randint(15000,40000)




row[month] = value




data.append(row)





df = pd.DataFrame(data)





# Write to Excel




output_file = output_dir /"financial_report_q1.xlsx"




with pd.ExcelWriter(output_file,engine="openpyxl") as writer:




df.to_excel(writer,sheet_name="Q1 Summary",index=False)





# Format it nicely




worksheet = writer.sheets["Q1 Summary"]




for cell in worksheet[1]:  # Header row




cell.font =Font(bold=True)




cell.fill =PatternFill(start_color="4F81BD",end_color="4F81BD",fill_type="solid")




cell.font =Font(color="FFFFFF",bold=True)





print(f"  ✅ Created {output_file}")






defgenerate_workflow_2_data(output_dir: Path):




"""Generate regional sales data for Workflow 2."""




print("\n📊 Generating Workflow 2: Regional sales data")





regions =["northeast", "southeast", "west"]




products =["Widget A", "Widget B", "Widget C", "Gadget X", "Gadget Y"]





for region in regions:




data =[]




start_date =datetime(2024,1,1)





# Generate 90 days of sales data




for day inrange(90):




date = start_date +timedelta(days=day)




# Random number of sales per day (3-8)




forinrange(random.randint(3,8)):




product = random.choice(products)




units_sold = random.randint(1,20)




price_per_unit = random.randint(50,200)




revenue = units_sold * price_per_unit





data.append({




"Date": date.strftime("%Y-%m-%d"),




"Product": product,




"Units_Sold": units_sold,




"Revenue": revenue






df = pd.DataFrame(data)





# Write to Excel




output_file = output_dir /f"sales_{region}.xlsx"




df.to_excel(output_file,sheet_name="Sales",index=False)




print(f"  ✅ Created {output_file} ((df)} rows)")






defgenerate_workflow_3_data(output_dir: Path):




"""Generate complex budget spreadsheet with formatting for Workflow 3."""




print("\n📊 Generating Workflow 3: company_budget_2024.xlsx")





wb =Workbook()




ws = wb.active




ws.title ="Budget"





# Define departments with colors




departments = {




"Engineering": "C6E0B4",




"Marketing": "FFD966",




"Sales": "F4B084",




"Operations": "B4C7E7"






# Define categories




categories = {




"Personnel": ["Salaries", "Benefits", "Training"],




"Infrastructure": ["Office Rent", "Equipment", "Software Licenses"],




"Operations": ["Travel", "Supplies", "Miscellaneous"]






# Styles




header_font =Font(bold=True,size=12)




category_font =Font(bold=True,size=11)




dept_fonts = {dept: Font(size=10) for dept in departments}





row =1





# Title




ws.merge_cells(f"A{row}:E{row}")




ws[f"A{row}"] ="2024 Annual Budget"




ws[f"A{row}"].font =Font(bold=True,size=14)




ws[f"A{row}"].alignment =Alignment(horizontal="center")




row +=2





# Headers




ws[f"A{row}"] ="Category"




ws[f"B{row}"] ="Item"




for i, dept inenumerate(departments.keys()):




ws.cell(row,3+ i, dept)




ws.cell(row,3+ i).font = header_font





for cell in ws[row]:




cell.font = header_font




row +=1





# Data




for category, items in categories.items():




# Category header (bold)




ws[f"A{row}"] = category




ws[f"A{row}"].font = category_font




row +=1





# Items with department budgets




for item in items:




ws[f"A{row}"] =""




ws[f"B{row}"] = item





# Add budget amounts for each department (with color)




for i, (dept, color) inenumerate(departments.items()):




amount = random.randint(5000,50000)




cell = ws.cell(row,3+ i, amount)




cell.fill =PatternFill(start_color=color,end_color=color,fill_type="solid")




cell.number_format ="$#,##0"





row +=1





row +=1# Blank row between categories





# Adjust column widths




ws.column_dimensions["A"].width =20




ws.column_dimensions["B"].width =25




forinrange(len(departments)):




ws.column_dimensions[chr(67+ i)].width =15# C, D, E, F





output_file = output_dir /"company_budget_2024.xlsx"




wb.save(output_file)




print(f"  ✅ Created {output_file}")




print(f"     • Bold categories, colored departments, merged title cell")






defgenerate_workflow_4_data(output_dir: Path):




"""Generate weekly sales report for Workflow 4."""




print("\n📊 Generating Workflow 4: sales_weekly.xlsx")





products =[




"Product A", "Product B", "Product C", "Product D", "Product E",




"Product F", "Product G", "Product H"






# Generate one week of data




data =[]




start_date =datetime(2024,11,4# Monday





for day inrange(7):




date = start_date +timedelta(days=day)




# Each product has 3-10 transactions per day




for product in products:




forinrange(random.randint(3,10)):




units = random.randint(1,15)




price = random.randint(20,150)




revenue = units * price





data.append({




"Date": date.strftime("%Y-%m-%d"),




"Product": product,




"Units": units,




"Revenue": revenue






df = pd.DataFrame(data)





# Write to Excel with some formatting




output_file = output_dir /"sales_weekly.xlsx"




with pd.ExcelWriter(output_file,engine="openpyxl") as writer:




df.to_excel(writer,sheet_name="Weekly Sales",index=False)





# Format header




worksheet = writer.sheets["Weekly Sales"]




for cell in worksheet[1]:




cell.font =Font(bold=True)





print(f"  ✅ Created {output_file} ((df)} rows)")






defmain():




"""Generate all sample data files."""




print("="*60)




print("Generating Sample Data for LlamaSheets + Coding Agent Workflows")




print("="*60)





# Create output directory




output_dir =Path("input_data")




output_dir.mkdir(exist_ok=True)





# Generate data for each workflow




generate_workflow_1_data(output_dir)




generate_workflow_2_data(output_dir)




generate_workflow_3_data(output_dir)




generate_workflow_4_data(output_dir)





print("\n"+"="*60)




print("✅ All sample data generated!")




print("="*60)




print(f"\nFiles created in {output_dir.absolute()}:")




print("\nWorkflow 1 (Understanding a New Spreadsheet):")




print("  • financial_report_q1.xlsx")




print("\nWorkflow 2 (Generating Analysis Scripts):")




print("  • sales_northeast.xlsx")




print("  • sales_southeast.xlsx")




print("  • sales_west.xlsx")




print("\nWorkflow 3 (Using Cell Metadata):")




print("  • company_budget_2024.xlsx")




print("\nWorkflow 4 (Complete Automation):")




print("  • sales_weekly.xlsx")




print("\nYou can now use these files with the workflows in the documentation!")






if __name__ =="__main__":




main()


```

Generate all sample files:
Terminal window```


pythongenerate_sample_data.py


```

This creates in `input_data/`:
  * `financial_report_q1.xlsx` - Simple financial data (Workflow 1)
  * `sales_northeast.xlsx`, `sales_southeast.xlsx`, `sales_west.xlsx` - Regional sales (Workflow 2)
  * `company_budget_2024.xlsx` - Budget with formatting (Workflow 3)
  * `sales_weekly.xlsx` - Weekly report data (Workflow 4)


### Step 6: Extract Your First Spreadsheet
[Section titled “Step 6: Extract Your First Spreadsheet”](https://developers.llamaindex.ai/python/cloud/llamasheets/examples/llama_index/#step-6-extract-your-first-spreadsheet)
Terminal window```

# Extract sample data or your own spreadsheet



pythonscripts/extract.pyinput_data/financial_report_q1.xlsx



# Or use your own:


# python scripts/extract.py your_spreadsheet.xlsx

```

This will create files in `data/`:
  * `financial_report_q1_region_1_Q1_Summary.parquet`
  * `financial_report_q1_metadata_1_Q1_Summary.parquet`
  * `financial_report_q1_job_metadata.json`


## Creating your Agent
[Section titled “Creating your Agent”](https://developers.llamaindex.ai/python/cloud/llamasheets/examples/llama_index/#creating-your-agent)
Now that we can extract regions and tables from spreadsheets, we can create an agent to automate tasks over that data.
The most straightforward way to do this is creating an agent that consists of two main parts:
  1. A prompt that includes the data it has access to, and details about the format of that data
  2. A tool that allows for code execution against that data


**Note:** Code execution should always be sandboxed into production applications.
Using LlamaIndex, creating this type of agent is fairly straightforward.
### Creating a Contextual System Prompt
[Section titled “Creating a Contextual System Prompt”](https://developers.llamaindex.ai/python/cloud/llamasheets/examples/llama_index/#creating-a-contextual-system-prompt)
In order to give the Agent enough information to act, we can build a prompt that includes the data it has access to.
Given a directory of extracted data, we can parse out the information into a system prompt.
A helper function to generate context:
```


import json




from pathlib import Path




# Helper function for initial agent context



deflist_extracted_data(data_dir: str="data") -> str:





List all regions and metadata files extracted by LlamaSheets.





This helps discover what data is available to work with.





Args:




data_dir: Directory containing extracted parquet files (default: "data")





Returns:




JSON string with information about available files





data_path =Path(data_dir)





ifnot data_path.exists():




return json.dumps({"error": f"Data directory '{data_dir}' not found"})





# Find all parquet and metadata files




region_files =list(data_path.glob("*_region_*.parquet"))




job_metadata_files =list(data_path.glob("*_job_metadata.json"))





regions =[]




for region_file in region_files:




# Quick peek at dimensions




df = pd.read_parquet(region_file)





# Find corresponding metadata file




base_name = region_file.stem.replace("_region_","_metadata_")




metadata_path = region_file.parent /f"{base_name}.parquet"





regions.append(





"region_file"(region_file),




"metadata_file"(metadata_path)if metadata_path.exists()elseNone,




"shape": {"rows"(df), "columns"(df.columns)},




"columns": list(df.columns),







result = {




"data_directory": str(data_path.absolute()),




"num_regions": len(regions),




"regions": regions,




"job_metadata_files": [str(f) forin job_metadata_files],






return json.dumps(result,indent=2)





# Generate a system prompt



available_regions =list_extracted_data()





system_prompt =f"""You are an AI assistant that helps analyze spreadsheet data extracted by LlamaSheets.




LlamaSheets extracts messy spreadsheets into clean parquet files with two types of outputs:


1. Region files (*_region_*.parquet) - The actual data with columns and rows


2. Metadata files (*_metadata_*.parquet) - Rich cell-level metadata including:



- Formatting: font_bold, font_italic, font_size, background_color_rgb




- Position: row_number, column_number, coordinate




- Type detection: data_type, is_date_like, is_percentage, is_currency




- Layout: is_in_first_row, is_merged_cell, horizontal_alignment




You have access to tools that allow you to execute Python pandas code against these files.


Use these tools to load the parquet files, analyze the data, and return results.



Key tips:


- Bold cells in metadata often indicate headers


- Background colors often indicate groupings or departments


- Load both region and metadata files for complete analysis


- Write clear pandas code - you have full pandas functionality available


- Store results in variables for reuse across multiple code executions



Existing Processed Regions:



{available_regions}



"""

```

### Giving the Agent Tools
[Section titled “Giving the Agent Tools”](https://developers.llamaindex.ai/python/cloud/llamasheets/examples/llama_index/#giving-the-agent-tools)
To be the most useful, we can give our agent a tool to execute code.
In LlamaIndex, tools are just python functions.
Here’s the python function that we will give our agent:
```


import io




import json




import sys




from typing import Any, Dict, Optional





import pandas as pd




# Global context for loaded dataframes



_code_context: Dict[str, Any] = {}






defexecute_code(code: str) -> str:





Execute Python pandas code against LlamaSheets extracted data.





This tool allows flexible data analysis by executing arbitrary pandas code.




You can load parquet files, manipulate dataframes, and return results.





The code executes in a context where:




- pandas is available as 'pd'




- json is available for formatting output





Args:




code: Python code to execute. Any print() statements or stdout/stderr




will be captured and returned. Optionally set a 'result' variable




for structured output.





Returns:




String containing:




- Any stdout/stderr output from the code execution




- The 'result' variable if it was set (formatted appropriately)




- Error message if execution failed





Example usage:




code = '''




# Load and inspect data




df = pd.read_parquet("data/sales_region_1.parquet")




print(f"Loaded {len(df)} rows")





result = {




"shape": df.shape,




"columns": list(df.columns),




"sample": df.head(3).to_dict(orient="records")







global _code_context





# Capture stdout and stderr




stdout_capture = io.StringIO()




stderr_capture = io.StringIO()




old_stdout = sys.stdout




old_stderr = sys.stderr





try:




# Redirect stdout/stderr




sys.stdout = stdout_capture




sys.stderr = stderr_capture





# Create execution context with pandas, json, and previously loaded dfs




exec_context = {




"pd": pd,




"json": json,




"Path": Path,




**_code_context,  # Include previously loaded dataframes






# Execute the code




exec(code, exec_context)





# Update global context with any new variables (excluding built-ins and modules)




for key, value in exec_context.items():




ifnot key.startswith("_") and key notin["pd", "json", "Path"]:




_code_context[key] = value





# Restore stdout/stderr




sys.stdout = old_stdout




sys.stderr = old_stderr





# Collect output




stdout_output = stdout_capture.getvalue()




stderr_output = stderr_capture.getvalue()





output_parts =[]





# Add stdout if any




if stdout_output:




output_parts.append(f"<stdout>{stdout_output}</stdout>")





# Add stderr if any




if stderr_output:




output_parts.append(f"<stderr>{stderr_output}</stderr>")





# Try to get a result (if code set a 'result' variable)




if"result"in exec_context:




result = exec_context["result"]




result_str =None





ifisinstance(result, pd.DataFrame):




# Convert DataFrame to readable format




result_str = result.to_string()




elifisinstance(result, (dict, list)):




result_str = json.dumps(result,indent=2,default=str)




else:




result_str =str(result)





if result_str:




output_parts.append(f"<result_var>{result_str}</result_var>")





# Return combined output or success message




if output_parts:




return"\n\n".join(output_parts)




else:




return"Code executed successfully (no output or result)"





exceptExceptionas e:




# Restore stdout/stderr in case of error




sys.stdout = old_stdout




sys.stderr = old_stderr





# Get any partial output




stdout_output = stdout_capture.getvalue()




stderr_output = stderr_capture.getvalue()





error_parts =[]




if stdout_output:




error_parts.append(f"=== STDOUT (before error) ===\n{stdout_output}")




if stderr_output:




error_parts.append(f"=== STDERR (before error) ===\n{stderr_output}")





error_parts.append(f"=== ERROR ===\n(e)}")




error_parts.append(f"\n=== CODE ===\n{code}")





return"\n\n".join(error_parts)


```

### Build the Final Agent
[Section titled “Build the Final Agent”](https://developers.llamaindex.ai/python/cloud/llamasheets/examples/llama_index/#build-the-final-agent)
Using our system prompt and tool function, we can finally assemble the final agent.
Here’s the code to build the agent in LlamaIndex
```


from llama_index.core.agent import FunctionAgent




from llama_index.llms.openai import OpenAI




# Setup the LLM to use



llm =OpenAI(model="gpt-4.1",api_key=api_key)




# Create tools - just one simple code execution tool for now



tools =[execute_code]




# Configure agent



agent =FunctionAgent(tools=tools,llm=llm,system_prompt=system_prompt)


```

## Running the Agent
[Section titled “Running the Agent”](https://developers.llamaindex.ai/python/cloud/llamasheets/examples/llama_index/#running-the-agent)
With our agent assembled, we can run queries against it.
When using LlamaIndex, agents stream events. The code below intercepts these events to print more detailed context about what the agent is doing.
You can read more about LlamaIndex Agents [in the documentation.](https://developers.llamaindex.ai/python/framework/understanding/agent/)
```


import io




import json




import sys




from pathlib import Path




from typing import Any, Dict, Optional





import dotenv




import pandas as pd




from llama_index.core.agent import FunctionAgent, ToolCall, ToolCallResult, AgentStream




from llama_index.llms.openai import OpenAI




from workflows import Context





dotenv.load_dotenv()




...




asyncdefmain():




"""Example of using the LlamaSheets agent."""





# Create the agent




agent =create_llamasheets_agent()




ctx =Context(agent)





# Example queries the agent can handle:




queries =[




# Discovery




"What spreadsheet data is available?",




# Simple analysis




"Load the sales data and show me the first few rows with column info",




# Using metadata




"Find all bold cells in the metadata - these are likely headers",






# Example: Run a query




for query in queries:




print(f"\n=== Query: {query} ===")




handler = agent.run(query,ctx=ctx)




asyncfor ev in handler.stream_events():




ifisinstance(ev, ToolCall):




tool_kwargs_str = (




str(ev.tool_kwargs)[:500]+" ..."




iflen(str(ev.tool_kwargs)) 500




elsestr(ev.tool_kwargs)





print(f"\n[Tool Call] {ev.tool_name} with args:\n{tool_kwargs_str}\n\n")




elifisinstance(ev, ToolCallResult):




result_str = (




str(ev.tool_output)[:500]+" ..."




iflen(str(ev.tool_output)) 500




elsestr(ev.tool_output)





print(f"\n[Tool Result] {ev.tool_name}:\n{result_str}\n\n")




elifisinstance(ev, AgentStream):




print(ev.delta,end="",flush=True)





_ =await handler




print("=== End Query ===\n")






if __name__ =="__main__":




import asyncio





asyncio.run(main())


```

You can read the full code in the [examples folder for LlamaSheets](https://github.com/run-llama/llama_cloud_services/tree/main/sheets/llama-index-agent/llama_index_example.py).
