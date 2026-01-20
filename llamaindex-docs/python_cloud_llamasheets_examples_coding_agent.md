[Skip to content](https://developers.llamaindex.ai/python/cloud/llamasheets/examples/coding_agent/#_top)
# Using LlamaSheets with Coding Agents
LlamaSheets extracts messy spreadsheets into clean, structured parquet files with rich metadata.
This guide shows you how to set up a project to work with this data using a coding agent (Claude-Code in this case), and then walks through common workflows.
This guide is completely applicable to any other coding agent (Codex, Gemini CLI, Cursor, etc.), since all these agents support an AGENTS.md file and have file-system access.
You can find the complete setup for this tutorial in the [llama-cloud-services github examples](https://github.com/run-llama/llama_cloud_services/tree/main/examples/sheets/coding-agent-analysis).
## Setup Guide
[Section titled “Setup Guide”](https://developers.llamaindex.ai/python/cloud/llamasheets/examples/coding_agent/#setup-guide)
Follow these steps to set up your project for working with LlamaSheets and Claude.
### Step 1: Create Your Project Directory
[Section titled “Step 1: Create Your Project Directory”](https://developers.llamaindex.ai/python/cloud/llamasheets/examples/coding_agent/#step-1-create-your-project-directory)
Terminal window```


mkdircoding-agent-analysis




cdcoding-agent-analysis




# Create directories



mkdirdata# For extracted parquet files




mkdirscripts# For analysis scripts




mkdirreports# For output reports


```

### Step 2: Install Dependencies
[Section titled “Step 2: Install Dependencies”](https://developers.llamaindex.ai/python/cloud/llamasheets/examples/coding_agent/#step-2-install-dependencies)
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
[Section titled “Step 3: Set Up Environment Variables”](https://developers.llamaindex.ai/python/cloud/llamasheets/examples/coding_agent/#step-3-set-up-environment-variables)
Create a `.env` file:
Terminal window```


LLAMA_CLOUD_API_KEY=your_api_key_here


```

### Step 4: Create a CLAUDE.md File
[Section titled “Step 4: Create a CLAUDE.md File”](https://developers.llamaindex.ai/python/cloud/llamasheets/examples/coding_agent/#step-4-create-a-claudemd-file)
Create a `CLAUDE.md` (or `AGENTS.md` if not using Claude) file in your project root to guide the agent’s interactions:
Expand to see the full `.md` text
```

This project uses LlamaSheets to extract data from spreadsheets for analysis.



## Current Project Structure



- `data/` - Contains extracted parquet files from LlamaSheets



- `{name}_region_{N}.parquet` - Table data files




- `{name}_metadata_{N}.parquet` - Cell metadata files




- `{name}_job_metadata.json` - Extraction job information



- `scripts/` - Analysis and helper scripts


- `reports/` - Your generated reports and outputs



## Working with LlamaSheets Data



### Understanding the Files



When a spreadsheet is extracted, you'll find:



1. **Table parquet files** (`region_*.parquet`): The actual region data



- Columns correspond to spreadsheet columns




- Data types are preserved (dates, numbers, strings, booleans)




2. **Metadata parquet files** (`metadata_*.parquet`): Rich cell-level metadata



- Formatting: `font_bold`, `font_italic`, `font_size`, `background_color_rgb`




- Position: `row_number`, `column_number`, `coordinate` (e.g., "A1")




- Type detection: `data_type`, `is_date_like`, `is_percentage`, `is_currency`




- Layout: `is_in_first_row`, `is_merged_cell`, `horizontal_alignment`




- Content: `cell_value`, `raw_cell_value`




3. **Job metadata JSON** (`job_metadata.json`): Overall extraction results



- `regions[]`: List of extracted regions with IDs, locations, and titles/descriptions




- `worksheet_metadata[]`: Generated titles and descriptions




- `status`: Success/failure status




### Key Principles



1. **Use metadata to understand structure**: Bold cells often indicate headers, colors indicate groupings


2. **Validate before analysis**: Check data types, look for missing values


3. **Preserve formatting context**: The metadata tells you what the spreadsheet author emphasized


4. **Save intermediate results**: Store cleaned data as new parquet files



### Common Patterns



**Loading data:**


```python


import pandas as pd



df = pd.read_parquet("data/region_1_Sheet1.parquet")


meta_df = pd.read_parquet("data/metadata_1_Sheet1.parquet")


```



**Finding headers:**


```python


headers = meta_df[meta_df["font_bold"] == True]["cell_value"].tolist()


```



**Finding date columns:**


```python


date_cols = meta_df[meta_df["is_date_like"] == True]["column_number"].unique()


```



## Tools Available



- **Python 3.11+**: For data analysis


- **pandas**: DataFrame manipulation


- **pyarrow**: Parquet file reading


- **matplotlib**: Visualization (optional)



## Guidelines



- Always read the job_metadata.json first to understand what was extracted


- Check both region data and metadata before making assumptions


- Write reusable functions for common operations


- Document any data quality issues discovered

```

### Step 5: Create an Extraction Helper Script
[Section titled “Step 5: Create an Extraction Helper Script”](https://developers.llamaindex.ai/python/cloud/llamasheets/examples/coding_agent/#step-5-create-an-extraction-helper-script)
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

### Step 6: Generate Sample Data (Optional)
[Section titled “Step 6: Generate Sample Data (Optional)”](https://developers.llamaindex.ai/python/cloud/llamasheets/examples/coding_agent/#step-6-generate-sample-data-optional)
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


### Step 7: Extract Your First Spreadsheet
[Section titled “Step 7: Extract Your First Spreadsheet”](https://developers.llamaindex.ai/python/cloud/llamasheets/examples/coding_agent/#step-7-extract-your-first-spreadsheet)
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


### Step 8: Open Your Project with your Agent
[Section titled “Step 8: Open Your Project with your Agent”](https://developers.llamaindex.ai/python/cloud/llamasheets/examples/coding_agent/#step-8-open-your-project-with-your-agent)
Now you’re ready to work with your Agent! Open Claude Code (or similar) and point it to your project directory. The agent will be able to:
  * Read your CLAUDE.md/AGENTS.md to understand the project structure
  * Access the extracted parquet files in `data/`
  * Write analysis scripts to `scripts/`
  * Generate reports to `reports/`


## Common Workflows
[Section titled “Common Workflows”](https://developers.llamaindex.ai/python/cloud/llamasheets/examples/coding_agent/#common-workflows)
Now that your project is set up, here are specific workflows you can follow with your agent.
### Workflow 1: Understanding a New Spreadsheet
[Section titled “Workflow 1: Understanding a New Spreadsheet”](https://developers.llamaindex.ai/python/cloud/llamasheets/examples/coding_agent/#workflow-1-understanding-a-new-spreadsheet)
**Goal:** Figure out what data you have and how it’s structured.
**Steps:**
  1. Extract your spreadsheet:


Terminal window```


pythonscripts/extract.pyinput_data/financial_report_q1.xlsx


```

  1. Ask the Agent:


```

I just extracted financial_report_q1.xlsx. Can you help me understand what's in this data? Please:


1. Read the job metadata to see what regions were extracted


2. Look at the region data to understand the columns and data types


3. Check the cell metadata to identify any formatting patterns (bold headers, colored cells, etc.)


4. Summarize what you find

```

**What the Agent will do:**
The Agent will read the files, execute some python commands, and output it’s findings. You might see something like this:
```

Summary of financial_report_q1.xlsx Analysis



1. Extraction Results (from job_metadata.json:30-38)



Extracted Regions:


- 1 table region extracted successfully


- Sheet name: "Q1 Summary"


- Location: A1:D5


- Title: "Q1 Financial Summary"


- Description: A financial summary tracking key metrics for Q1 (January-March)



2. Region Data Structure



Columns:


- Category (text): Financial line items


- January (int64): Q1 month 1 values


- February (int64): Q1 month 2 values


- March (int64): Q1 month 3 values



Data:


4 rows × 4 columns containing:


- Revenue: $104,818 (Jan), $84,197 (Feb), $111,619 (Mar)


- Cost of Goods Sold: $43,106, $46,318, $44,907


- Operating Expenses: $26,630, $20,736, $26,611


- Net Income: $15,251, $34,701, $39,718



All numeric values are properly typed as int64.



3. Cell Metadata Formatting Patterns



Formatting Summary:


- 16 total cells (4 rows × 4 columns)


- No bold formatting detected


- No colored cells (all background_color_rgb = 0.0)


- No merged cells


- No special formatting (dates, percentages, currency markers)


- Uniform font size: 11pt throughout


- Standard alignment: All cells use default alignment (0.0)



Data Types:


- 12 Number cells (all financial values)


- 4 Text cells (category labels)



Key Observations



The spreadsheet has a clean, minimal structure with no visual formatting applied. The header row (A1:D1 with


"Category", "January", "February", "March") was used to create the DataFrame column names but isn't included in


the metadata export since only rows 2-5 (the data rows) are captured. The data is well-structured as a simple


financial table ready for analysis without requiring cleanup.

```

**When to use this:** Any time you receive a new spreadsheet and need to understand its structure before analysis.
### Workflow 2: Generating Analysis Scripts
[Section titled “Workflow 2: Generating Analysis Scripts”](https://developers.llamaindex.ai/python/cloud/llamasheets/examples/coding_agent/#workflow-2-generating-analysis-scripts)
**Goal:** Create a reusable Python script for recurring analysis tasks.
**Steps:**
  1. Extract your spreadsheets (can be multiple):


Terminal window```


pythonscripts/extract.pyinput_data/sales_northeast.xlsx




pythonscripts/extract.pyinput_data/sales_southeast.xlsx




pythonscripts/extract.pyinput_data/sales_west.xlsx


```

  1. Ask the Agent:


```

I've extracted sales data from 3 regional spreadsheets. Can you create a script in scripts/analyze_sales.py that:


1. Loads all the regional data


2. Combines them and calculates total revenue by product and region


3. Finds the top 5 products overall


4. Saves a summary report to reports/sales_summary.csv

```

**What the Agent will do:**
The coding Agent will likely create a script like `scripts/analyze_sales.py`:
```

"""


Sales Data Analysis Script



This script analyzes sales data from 3 regional spreadsheets extracted by LlamaSheets.


It loads all regional data, combines them, calculates total revenue by product and region,


finds the top 5 products overall, and saves a summary report.


"""




import pandas as pd




from pathlib import Path




import sys






defload_regional_data(data_dir: Path) -> pd.DataFrame:





Load all regional sales data and combine them.





Args:




data_dir: Path to the data directory containing parquet files





Returns:




Combined DataFrame with all regional sales data





regions =['northeast', 'southeast', 'west']




dataframes =[]





for region in regions:




file_pattern =f"sales_{region}_region_1_Sales.parquet"




file_path = data_dir / file_pattern





ifnot file_path.exists():




print(f"Warning: {file_path} not found, skipping...",file=sys.stderr)




continue





df = pd.read_parquet(file_path)




df['Region'] = region.capitalize()




dataframes.append(df)




print(f"Loaded (df)} rows from {region}")





ifnot dataframes:




raiseValueError("No regional data files found!")





combined_df = pd.concat(dataframes,ignore_index=True)




print(f"\nTotal rows loaded: (combined_df)}")





return combined_df






defcalculate_revenue_by_product_and_region(df: pd.DataFrame) -> pd.DataFrame:





Calculate total revenue by product and region.





Args:




df: Combined sales DataFrame





Returns:




DataFrame with revenue aggregated by product and region





revenue_summary = df.groupby(['Product', 'Region']).agg({




'Revenue': 'sum',




'Units_Sold': 'sum'




}).reset_index()





revenue_summary = revenue_summary.sort_values(




['Product', 'Revenue'],




ascending=[True, False]






return revenue_summary






deffind_top_products(df: pd.DataFrame, n: int=5) -> pd.DataFrame:





Find the top N products by total revenue across all regions.





Args:




df: Combined sales DataFrame




n: Number of top products to return





Returns:




DataFrame with top N products and their total revenue





top_products = df.groupby('Product').agg({




'Revenue': 'sum',




'Units_Sold': 'sum'




}).reset_index()





top_products = top_products.sort_values('Revenue',ascending=False).head(n)




top_products['Rank'] =range(1,(top_products)+1)





return top_products[['Rank', 'Product', 'Revenue', 'Units_Sold']]






defcreate_summary_report(df: pd.DataFrame, output_path: Path) -> None:





Create and save a comprehensive summary report.





Args:




df: Combined sales DataFrame




output_path: Path to save the CSV report





# Calculate revenue by product and region




revenue_by_product_region =calculate_revenue_by_product_and_region(df)





# Find top 5 products




top_5_products =find_top_products(df,n=5)





# Create pivot table for easier reading




pivot_table = revenue_by_product_region.pivot(




index='Product',




columns='Region',




values='Revenue'




).fillna(0)





# Add total column




pivot_table['Total'] = pivot_table.sum(axis=1)




pivot_table = pivot_table.sort_values('Total',ascending=False)





# Save the summary report




output_path.parent.mkdir(parents=True,exist_ok=True)




pivot_table.to_csv(output_path)





print(f"\nSummary Report saved to: {output_path}")




print("\n"+"="*60)




print("SALES SUMMARY REPORT")




print("="*60)




print("\nRevenue by Product and Region:")




print(pivot_table.to_string())





print("\n"+"="*60)




print("TOP 5 PRODUCTS (by Total Revenue):")




print("="*60)




print(top_5_products.to_string(index=False))





# Additional statistics




print("\n"+"="*60)




print("OVERALL STATISTICS:")




print("="*60)




print(f"Total Revenue: ${df['Revenue'].sum():,}")




print(f"Total Units Sold: {df['Units_Sold'].sum():,}")




print(f"Number of Products: {df['Product'].nunique()}")




print(f"Number of Transactions: (df):,}")




print(f"Average Revenue per Transaction: ${df['Revenue'].mean():.2f}")





# Regional breakdown




print("\n"+"="*60)




print("REVENUE BY REGION:")




print("="*60)




regional_revenue = df.groupby('Region')['Revenue'].sum().sort_values(ascending=False)




for region, revenue in regional_revenue.items():




percentage = (revenue / df['Revenue'].sum()) *100




print(f"{region:12}: ${revenue:>12,} ({percentage:>5.1f}%)")






defmain():




"""Main execution function."""




# Set up paths




project_root =Path(__file__).parent.parent




data_dir = project_root /"data"




output_path = project_root /"reports"/"sales_summary.csv"





print("Starting Sales Data Analysis...")




print(f"Data directory: {data_dir}")




print(f"Output path: {output_path}")




print()





# Load data




print("Loading regional sales data...")




sales_df =load_regional_data(data_dir)





# Create and save summary report




print("\nGenerating summary report...")




create_summary_report(sales_df, output_path)





print("\nAnalysis complete!")






if __name__ =="__main__":




main()


```

And if you run the script:
```

Starting Sales Data Analysis...


Data directory: /Users/loganmarkewich/llama_parse/examples/sheets/coding-agent-analysis/data


Output path: /Users/loganmarkewich/llama_parse/examples/sheets/coding-agent-analysis/reports/sales_summary.csv



Loading regional sales data...


Loaded 476 rows from northeast


Loaded 472 rows from southeast


Loaded 507 rows from west



Total rows loaded: 1455



Generating summary report...



Summary Report saved to: /Users/loganmarkewich/llama_parse/examples/sheets/coding-agent-analysis/reports/sales_summary.csv



============================================================


SALES SUMMARY REPORT


============================================================



Revenue by Product and Region:


Region    Northeast  Southeast    West   Total


Product


Gadget X     149293     131784  136002  417079


Widget A     131675     116294  123649  371618


Widget C     116575     109187  141610  367372


Gadget Y     131642     101125  125050  357817


Widget B     117451     122948  113463  353862



============================================================


TOP 5 PRODUCTS (by Total Revenue):


============================================================



Rank  Product  Revenue  Units_Sold




1 Gadget X   417079        3301




2 Widget A   371618        3004




3 Widget C   367372        3005




4 Gadget Y   357817        2935




5 Widget B   353862        2961




============================================================


OVERALL STATISTICS:


============================================================


Total Revenue: $1,867,748


Total Units Sold: 15,206


Number of Products: 5


Number of Transactions: 1,455


Average Revenue per Transaction: $1283.68



============================================================


REVENUE BY REGION:


============================================================


Northeast   : $     646,636 ( 34.6%)


West        : $     639,774 ( 34.3%)


Southeast   : $     581,338 ( 31.1%)



Analysis complete!

```

  1. Run the script:


Terminal window```


pythonscripts/analyze_sales.py


```

**When to use this:** When you need reusable analysis that runs regularly (weekly reports, monthly summaries, etc.)
### Workflow 3: Using Cell Metadata to Understand Structure
[Section titled “Workflow 3: Using Cell Metadata to Understand Structure”](https://developers.llamaindex.ai/python/cloud/llamasheets/examples/coding_agent/#workflow-3-using-cell-metadata-to-understand-structure)
**Goal:** Extract structured data from a messy spreadsheet by using formatting cues.
**Steps:**
  1. Extract your complex spreadsheet:


Terminal window```


pythonscripts/extract.pyinput_data/company_budget_2024.xlsx


```

  1. Ask the Agent:


```

I have a budget spreadsheet where:


- Bold cells in the first column are category headers


- Different background colors represent different departments


- Some cells are merged for section groupings



Can you create a script that uses the cell metadata to parse this into a clean, structured dataset with proper category and department labels?

```

**What the Agent will do:**
The Agent will likely create a script like `scripts/parse_budget_with_metadata.py` and likely run the script for you:
```

"""


Parse budget spreadsheet using LlamaSheets metadata.



This script uses cell metadata (bold formatting, background colors, merged cells)


to parse a budget spreadsheet into a clean, structured dataset with proper


category and department labels.


"""




import pandas as pd




import json




from pathlib import Path




from typing import Dict, List, Tuple






defload_budget_data(data_dir: str="data", prefix: str="company_budget_2024") -> Tuple[pd.DataFrame, pd.DataFrame, dict]:




"""Load table data, metadata, and job metadata."""




data_path =Path(data_dir)





# Load job metadata to understand structure




withopen(data_path /f"{prefix}_job_metadata.json") as f:




job_meta = json.load(f)





# Load first table (main budget data)




table_df = pd.read_parquet(data_path /f"{prefix}_region_1_Budget.parquet")




metadata_df = pd.read_parquet(data_path /f"{prefix}_metadata_1_Budget.parquet")





# Flatten multi-level column names if present




ifisinstance(table_df.columns, pd.MultiIndex):




table_df.columns =[col[0] if col[1] ==''elsef"{col[0]}_{col[1]}"for col in table_df.columns]





return table_df, metadata_df, job_meta






defidentify_categories(metadata_df: pd.DataFrame) -> Dict[int, str]:





Identify category headers using bold formatting in the first column.





Returns:




Dict mapping row numbers to category names





# Find bold cells in the first column (column_number == 1)




bold_first_col = metadata_df[




(metadata_df['font_bold'] ==True) 




(metadata_df['column_number'] ==1)






categories = {}




for _, row in bold_first_col.iterrows():




row_num = row['row_number']




category_name = row['cell_value']




categories[row_num] = category_name





print(f"Found (categories)} categories:")




for row_num, cat insorted(categories.items()):




print(f"  Row {row_num}: {cat}")





return categories






defmap_colors_to_departments(metadata_df: pd.DataFrame, table_df: pd.DataFrame) -> Dict[float, str]:





Map background colors to department names using the column headers.





Returns:




Dict mapping background color values to department names





# Get unique background colors (excluding 0.0 which is no color)




colors =sorted([c forin metadata_df['background_color_rgb'].unique()if0])





# Get department names from table columns (skip first two columns: Category and Item)




dept_columns =[col for col in table_df.columns if col notin['Category', 'Item']]





# Map colors to departments




# Assumption: colors are used in the same order as departments appear in columns




color_map = {}




for i, color inenumerate(colors):




iflen(dept_columns):




color_map[color] = dept_columns[i]





print(f"\nColor to Department mapping:")




for color, dept in color_map.items():




print(f"  Color {color:.4f}: {dept}")





return color_map






defassign_category_to_rows(table_df: pd.DataFrame, categories: Dict[int, str]) -> List[str]:





Assign category labels to each row based on bold headers.




Rows belong to the most recent category header above them.





category_labels =[]




current_category =None




category_values =set(categories.values())





# Categories dict uses absolute row numbers from metadata




# Need to map to table dataframe row indices




for idx inrange(len(table_df)):




# Check if this row is a category header




row_value = table_df.iloc[idx]['Category_l_0']




if pd.notna(row_value) and row_value in category_values:




current_category = row_value




category_labels.append(current_category)




else:




category_labels.append(current_category)





return category_labels






defparse_budget_to_structured_data(table_df: pd.DataFrame, metadata_df: pd.DataFrame) -> pd.DataFrame:





Parse the budget spreadsheet into a clean, structured dataset.





Returns:




DataFrame with columns: Category, Item, Department, Amount





# Step 1: Identify categories from bold cells




categories =identify_categories(metadata_df)





# Step 2: Map colors to departments




color_map =map_colors_to_departments(metadata_df, table_df)





# Step 3: Build mapping of (row, col) to department based on background color




cell_to_dept = {}




for idx, row in metadata_df.iterrows():




row_num = row['row_number']




col_num = row['column_number']




bg_color = row['background_color_rgb']




if bg_color in color_map:




cell_to_dept[(row_num, col_num)] = color_map[bg_color]





# Step 4: Create structured dataset




records =[]





# Assign categories to rows




category_labels =assign_category_to_rows(table_df, categories)





# Get department columns (skip Category and Item)




dept_columns =[col for col in table_df.columns ifnot col.startswith('Category') andnot col.startswith('Item')]





for idx, row in table_df.iterrows():




category = category_labels[idx]




item = row['Item_l_1']





# Skip rows that are category headers or have no item




if pd.isna(item) or item =='None':




continue





# Extract values for each department




for dept in dept_columns:




amount = row[dept]




if pd.notna(amount):




records.append({




'Category': category,




'Item': item,




'Department': dept,




'Amount': amount






structured_df = pd.DataFrame(records)





print(f"\nStructured dataset created:")




print(f"  Total records: (structured_df)}")




print(f"  Categories: {structured_df['Category'].nunique()}")




print(f"  Items: {structured_df['Item'].nunique()}")




print(f"  Departments: {structured_df['Department'].nunique()}")





return structured_df






defmain():




"""Main execution function."""




print("="*60)




print("Budget Spreadsheet Parser - Using LlamaSheets Metadata")




print("="*60)




print()





# Load data




print("Loading data...")




table_df, metadata_df, job_meta =load_budget_data()




print(f"Loaded table with shape: {table_df.shape}")




print(f"Loaded metadata with shape: {metadata_df.shape}")




print()





# Parse into structured format




print("Parsing budget data...")




print("-"*60)




structured_df =parse_budget_to_structured_data(table_df, metadata_df)





# Save results




output_path =Path("data/budget_structured.parquet")




structured_df.to_parquet(output_path,index=False)




print()




print(f"Saved structured data to: {output_path}")





# Display sample results




print()




print("="*60)




print("Sample Results:")




print("="*60)




print(structured_df.head(15).to_string(index=False))





# Summary statistics




print()




print("="*60)




print("Summary by Category:")




print("="*60)




summary = structured_df.groupby('Category')['Amount'].agg(['count', 'sum', 'mean'])




print(summary)





print()




print("="*60)




print("Summary by Department:")




print("="*60)




dept_summary = structured_df.groupby('Department')['Amount'].agg(['count', 'sum', 'mean'])




print(dept_summary)





return structured_df






if __name__ =="__main__":




structured_df =main()


```

And if the agent runs the script for you, it might say:
```

Summary



I've created two comprehensive scripts that parse your budget spreadsheet using LlamaSheets cell metadata:



Created Files



1. scripts/parse_budget_with_metadata.py - Basic parser demonstrating core concepts


- Uses bold formatting to identify category headers (Personnel, Infrastructure, Operations)


- Maps background colors to departments


- Creates clean structured output


2. scripts/parse_budget_advanced.py - Enhanced parser with full analysis


- Detailed metadata inspection (bold cells, colors, merged cells, data types)


- Data validation (verifies totals match: $986,239)


- Multiple output formats (structured + pivot view)


- Comprehensive summary statistics


3. scripts/README.md - Complete documentation with examples and patterns



Output Files



- data/budget_structured.parquet - 36 records in clean format (Category, Item, Department, Amount)


- data/budget_structured_advanced.parquet - Same data with enhanced validation


- data/budget_pivot_view.parquet - Pivot table matching original layout



Key Features



The scripts demonstrate how to:


- Identify structure from formatting: Bold cells in column 1 = category headers


- Use background colors: 4 different colors mapped to 4 departments (Engineering, Marketing, Sales, Operations)


- Handle complex layouts: Navigate rows with different meanings (headers vs data)


- Validate results: Ensure parsed data totals match original ($986,239 ✓)



Usage



# Run basic parser


python3 scripts/parse_budget_with_metadata.py



# Run advanced parser with full analysis


python3 scripts/parse_budget_advanced.py



The scripts are fully reusable - just update the prefix parameter in load_budget_data() to parse other budget files with


similar formatting patterns!

```

  1. Run the script:


Terminal window```


pythonscripts/parse_budget_with_metadata.py


```

**When to use this:** When you have complex spreadsheets with visual formatting that conveys structure (headers, groupings, categories).
### Workflow 4: Building Complete Automation
[Section titled “Workflow 4: Building Complete Automation”](https://developers.llamaindex.ai/python/cloud/llamasheets/examples/coding_agent/#workflow-4-building-complete-automation)
**Goal:** Create an end-to-end pipeline that runs regularly without manual intervention.
**Steps:**
  1. Ask the Agent:


```

I receive a weekly sales report as input_data/sales_weekly.xlsx. I need a complete automation that:


1. Extracts the data using LlamaSheets


2. Validates that all expected columns are present (Date, Product, Units, Revenue)


3. Calculates KPIs: total revenue, top 5 products, daily average


4. Generates a text report and saves the data as CSV


5. Can be run with a single command



Can you create this as scripts/weekly_report.py?

```

**What the Agent will do:**
The Agent will likely create a script like `scripts/weekly_report.py`:
```

"""


Weekly Sales Report Automation



This script automates the weekly sales report generation:


1. Extracts data from input_data/sales_weekly.xlsx using LlamaSheets


2. Validates required columns (Date, Product, Units, Revenue)


3. Calculates KPIs (total revenue, top 5 products, daily average)


4. Generates a text report and saves data as CSV



Usage:



python scripts/weekly_report.py



"""




import asyncio




import json




import os




import sys




from datetime import datetime




from pathlib import Path





import dotenv




import pandas as pd





from llama_cloud_services.beta.sheets import LlamaSheets




from llama_cloud_services.beta.sheets.types import (




SpreadsheetParsingConfig,




SpreadsheetResultType,






dotenv.load_dotenv()






classWeeklyReportGenerator:




"""Handles weekly sales report generation."""





def__init__(




self,




input_file: str="input_data/sales_weekly.xlsx",




data_dir: str="data",




reports_dir: str="reports",





self.input_file =Path(input_file)




self.data_dir =Path(data_dir)




self.reports_dir =Path(reports_dir)




self.required_columns =["Date", "Product", "Units", "Revenue"]





# Create directories if they don't exist




self.data_dir.mkdir(parents=True,exist_ok=True)




self.reports_dir.mkdir(parents=True,exist_ok=True)





asyncdefextract_spreadsheet(self) -> dict:




"""Extract the spreadsheet using LlamaSheets."""




print("="*60)




print("STEP 1: EXTRACTING DATA WITH LLAMASHEETS")




print("="*60)





ifnotself.input_file.exists():




raiseFileNotFoundError(f"Input file not found: {self.input_file}")





client =LlamaSheets(




base_url="https://api.staging.llamaindex.ai",




api_key=os.getenv("LLAMA_CLOUD_API_KEY"),






print(f"Extracting {self.input_file}...")





# Extract regions




config =SpreadsheetParsingConfig(




sheet_names=None,# Extract all sheets




generate_additional_metadata=True,






job_result =await client.aextract_regions(str(self.input_file),config=config)





print(f"✓ Extracted (job_result.regions)} region(s)")





# Get base name for files




base_name =self.input_file.stem





# Save job metadata




job_metadata_path =self.data_dir /f"{base_name}_job_metadata.json"




withopen(job_metadata_path,"w") as f:




json.dump(job_result.model_dump(mode="json"), f,indent=2)




print(f"✓ Saved job metadata to {job_metadata_path}")





# Download each region




region_files =[]




for idx, region inenumerate(job_result.regions,1):




sheet_name = region.sheet_name.replace("","_")





# Download region data




region_bytes =await client.adownload_region_result(




job_id=job_result.id,




region_id=region.region_id,




result_type=region.region_type,






region_path =self.data_dir /f"{base_name}_region_{idx}_{sheet_name}.parquet"




withopen(region_path,"wb") as f:




f.write(region_bytes)




region_files.append(region_path)




print(f"✓ Table {idx}: {region_path}")





# Download metadata




metadata_bytes =await client.adownload_region_result(




job_id=job_result.id,




region_id=region.region_id,




result_type=SpreadsheetResultType.CELL_METADATA,






metadata_path =self.data_dir /f"{base_name}_metadata_{idx}_{sheet_name}.parquet"




withopen(metadata_path,"wb") as f:




f.write(metadata_bytes)




print(f"✓ Metadata {idx}: {metadata_path}")





print(f"\n✓ All files saved to {self.data_dir}/\n")





return {




"job_result": job_result.model_dump(mode="json"),




"region_files": region_files,






defvalidate_columns(self, df: pd.DataFrame) -> tuple[bool, list[str]]:




"""Validate that all required columns are present."""




print("="*60)




print("STEP 2: VALIDATING DATA")




print("="*60)





missing_columns =[]




for col inself.required_columns:




if col notin df.columns:




missing_columns.append(col)





if missing_columns:




print(f"✗ Missing required columns: {missing_columns}")




print(f"  Available columns: {list(df.columns)}")




returnFalse, missing_columns




else:




print(f"✓ All required columns present: {self.required_columns}")




print(f"  Total rows: (df)}")




print(f"  Date range: {df['Date'].min()} to {df['Date'].max()}")




print(f"  Unique products: {df['Product'].nunique()}")




print()




returnTrue, []





defcalculate_kpis(self, df: pd.DataFrame) -> dict:




"""Calculate KPIs: total revenue, top 5 products, daily average."""




print("="*60)




print("STEP 3: CALCULATING KPIs")




print("="*60)





# Ensure Date column is datetime




ifnot pd.api.types.is_datetime64_any_dtype(df["Date"]):




df["Date"] = pd.to_datetime(df["Date"])





# Calculate total revenue




total_revenue = df["Revenue"].sum()




print(f"✓ Total Revenue: ${total_revenue:,.2f}")





# Calculate top 5 products by revenue




top_products = (




df.groupby("Product")["Revenue"]




.sum()




.sort_values(ascending=False)




.head(5)





print(f"\n✓ Top 5 Products by Revenue:")




for rank, (product, revenue) inenumerate(top_products.items(),1):




print(f{rank}. {product}: ${revenue:,.2f}")





# Calculate daily average revenue




daily_revenue = df.groupby("Date")["Revenue"].sum()




daily_average = daily_revenue.mean()




print(f"\n✓ Daily Average Revenue: ${daily_average:,.2f}")





# Additional stats




total_units = df["Units"].sum()




num_days = df["Date"].nunique()





print(f"\n✓ Additional Stats:")




print(f"  Total Units Sold: {total_units:,}")




print(f"  Number of Days: {num_days}")




print(f"  Average Units per Day: {total_units / num_days:.1f}")




print()





return {




"total_revenue": total_revenue,




"top_products": top_products.to_dict(),




"daily_average": daily_average,




"total_units": total_units,




"num_days": num_days,




"daily_revenue": daily_revenue.to_dict(),






defgenerate_report(self, df: pd.DataFrame, kpis: dict) -> str:




"""Generate a text report."""




print("="*60)




print("STEP 4: GENERATING REPORT")




print("="*60)





# Get date range




date_min = df["Date"].min()




date_max = df["Date"].max()





# Build report




report_lines =[




"="*60,




"WEEKLY SALES REPORT",




"="*60,




f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",




f"Period: {date_min.strftime('%Y-%m-%d')} to {date_max.strftime('%Y-%m-%d')}",





"KEY PERFORMANCE INDICATORS",




"-"*60,




f"Total Revenue:        ${kpis['total_revenue']:,.2f}",




f"Total Units Sold:     {kpis['total_units']:,}",




f"Number of Days:       {kpis['num_days']}",




f"Daily Average Revenue: ${kpis['daily_average']:,.2f}",




f"Daily Average Units:   {kpis['total_units'] / kpis['num_days']:.1f}",





"TOP 5 PRODUCTS BY REVENUE",




"-"*60,






for rank, (product, revenue) inenumerate(kpis["top_products"].items(),1):




report_lines.append(f"{rank}. {product:<30} ${revenue:>12,.2f}")





report_lines.extend([





"DAILY REVENUE BREAKDOWN",




"-"*60,






for date_str, revenue insorted(kpis["daily_revenue"].items()):




date_obj = pd.to_datetime(date_str)




report_lines.append(




f"{date_obj.strftime('%Y-%m-%d')} ({date_obj.strftime('%A'):<9}): ${revenue:>12,.2f}"






report_lines.extend([





"="*60,




"END OF REPORT",




"="*60,






report ="\n".join(report_lines)





# Save report




report_path =self.reports_dir /f"weekly_sales_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"




withopen(report_path,"w") as f:




f.write(report)





print(f"✓ Report saved to: {report_path}")





return report





defsave_csv(self, df: pd.DataFrame) -> Path:




"""Save the data as CSV."""




print("="*60)




print("STEP 5: SAVING DATA AS CSV")




print("="*60)





csv_path =self.reports_dir /f"sales_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"




df.to_csv(csv_path,index=False)





print(f"✓ CSV saved to: {csv_path}")




print(f"  Rows: (df)}")




print(f"  Columns: (df.columns)}")




print()





return csv_path





asyncdefrun(self) -> dict:




"""Run the complete weekly report automation."""




try:




# Step 1: Extract data




extraction_result =awaitself.extract_spreadsheet()





# Load the first region (assuming weekly sales is in the first region)




region_file = extraction_result["region_files"][0]




df = pd.read_parquet(region_file)





# Step 2: Validate columns




is_valid, missing =self.validate_columns(df)




ifnot is_valid:




raiseValueError(f"Validation failed: missing columns {missing}")





# Step 3: Calculate KPIs




kpis =self.calculate_kpis(df)





# Step 4: Generate report




report =self.generate_report(df, kpis)





# Step 5: Save CSV




csv_path =self.save_csv(df)





# Print summary




print("="*60)




print("SUCCESS! REPORT GENERATION COMPLETE")




print("="*60)




print(f"✓ Data extracted from: {self.input_file}")




print(f"✓ Report generated: (report.splitlines())} lines")




print(f"✓ CSV exported: {csv_path}")




print()





# Print the report to console




print(report)





return {




"success": True,




"csv_path": str(csv_path),




"kpis": kpis,






exceptExceptionas e:




print(f"\n✗ ERROR: (e)}",file=sys.stderr)




return {




"success": False,




"error": str(e),







asyncdefmain():




"""Main entry point."""




generator =WeeklyReportGenerator()




result =await generator.run()





ifnot result["success"]:




sys.exit(1)






if __name__ =="__main__":




asyncio.run(main())


```

And if you run the script:
```

============================================================


STEP 1: EXTRACTING DATA WITH LLAMASHEETS


============================================================


Extracting input_data/sales_weekly.xlsx...


✓ Extracted 1 region(s)


✓ Saved job metadata to data/sales_weekly_job_metadata.json


✓ Table 1: data/sales_weekly_region_1_Weekly_Sales.parquet


✓ Metadata 1: data/sales_weekly_metadata_1_Weekly_Sales.parquet



✓ All files saved to data/



============================================================


STEP 2: VALIDATING DATA


============================================================


✓ All required columns present: ['Date', 'Product', 'Units', 'Revenue']



Total rows: 380




Date range: 2024-11-04 to 2024-11-10




Unique products: 8




============================================================


STEP 3: CALCULATING KPIs


============================================================


✓ Total Revenue: $266,287.00



✓ Top 5 Products by Revenue:



1. Product B: $37,219.00




2. Product C: $36,490.00




3. Product H: $34,898.00




4. Product E: $34,024.00




5. Product F: $31,847.00




✓ Daily Average Revenue: $38,041.00



✓ Additional Stats:



Total Units Sold: 3,041




Number of Days: 7




Average Units per Day: 434.4




============================================================


STEP 4: GENERATING REPORT


============================================================


✓ Report saved to: reports/weekly_sales_report_20251117_102847.txt


============================================================


STEP 5: SAVING DATA AS CSV


============================================================


✓ CSV saved to: reports/sales_data_20251117_102847.csv



Rows: 380




Columns: 4




============================================================


SUCCESS! REPORT GENERATION COMPLETE


============================================================


✓ Data extracted from: input_data/sales_weekly.xlsx


✓ Report generated: 35 lines


✓ CSV exported: reports/sales_data_20251117_102847.csv



============================================================


WEEKLY SALES REPORT


============================================================


Generated: 2025-11-17 10:28:47


Period: 2024-11-04 to 2024-11-10



KEY PERFORMANCE INDICATORS


------------------------------------------------------------


Total Revenue:        $266,287.00


Total Units Sold:     3,041


Number of Days:       7


Daily Average Revenue: $38,041.00


Daily Average Units:   434.4



TOP 5 PRODUCTS BY REVENUE


------------------------------------------------------------


1. Product B                      $   37,219.00


2. Product C                      $   36,490.00


3. Product H                      $   34,898.00


4. Product E                      $   34,024.00


5. Product F                      $   31,847.00



DAILY REVENUE BREAKDOWN


------------------------------------------------------------


2024-11-04 (Monday   ): $   34,801.00


2024-11-05 (Tuesday  ): $   50,355.00


2024-11-06 (Wednesday): $   32,130.00


2024-11-07 (Thursday ): $   34,948.00


2024-11-08 (Friday   ): $   41,255.00


2024-11-09 (Saturday ): $   34,228.00


2024-11-10 (Sunday   ): $   38,570.00



============================================================


END OF REPORT


============================================================

```

  1. Run it weekly:


Terminal window```


pythonscripts/weekly_report.py


```

  1. (Optional) Automate with cron:


Terminal window```

# Add to crontab to run every Monday at 9 AM



09**1cd/path/to/project/path/to/venv/bin/pythonscripts/weekly_report.py


```

**When to use this:** When you need a complete end-to-end pipeline that runs regularly without manual intervention.
