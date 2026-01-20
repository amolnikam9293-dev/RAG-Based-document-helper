[Skip to content](https://developers.llamaindex.ai/python/cloud/llamaparse/features/structured_output/#_top)
# Structured Output (Beta)
Structured Output is deprecated on the llamaParse API, use the LlamaExtract API instead.
## About Structured Output
[Section titled “About Structured Output”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/structured_output/#about-structured-output)
Structured output allows you to extract structured data (such as JSON) from a document directly at the parsing stage, reducing cost and time needed.
Structured output is currently only compatible with our default parsing mode and can be activated by setting `structured_output=True` in the API.


```


parser =LlamaParse(




structured_output=True



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'structured_output="true"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

You then need to provide either:
  * a JSON schema in the `structured_output_json_schema` API variable, which will be used to extract data in the desired format
  * or the name of one of our pre-defined schemas in the variable `structured_output_json_schema_name`


  * [ Python (Schema) ](https://developers.llamaindex.ai/python/cloud/llamaparse/features/structured_output/#tab-panel-212)
  * [ Python (Preset) ](https://developers.llamaindex.ai/python/cloud/llamaparse/features/structured_output/#tab-panel-214)


```


parser =LlamaParse(




structured_output_json_schema='A JSON SCHEMA'



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'structured_output_json_schema="A JSON SCHEMA"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

```


parser =LlamaParse(




structured_output_json_schema_name="invoice"



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'structured_output_json_schema_name="invoice"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## Supported Pre-defined Schemas
[Section titled “Supported Pre-defined Schemas”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/structured_output/#supported-pre-defined-schemas)
## imFeelingLucky
[Section titled “imFeelingLucky”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/structured_output/#imfeelinglucky)
Wildcard schema that lets LlamaParse infer output format
Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'structured_output_json_schema_name="imFeelingLucky"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

## Invoice
[Section titled “Invoice”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/structured_output/#invoice)
Standard invoice schema for line items, tax, and totals
  * [ Invoice Schema ](https://developers.llamaindex.ai/python/cloud/llamaparse/features/structured_output/#tab-panel-217)


Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'structured_output_json_schema_name="invoice"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

#### Structured Output: Invoice Schema
[Section titled “Structured Output: Invoice Schema”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/structured_output/#structured-output-invoice-schema)
Type: `object`
**_Properties_**
  * **invoiceNumber** `required`
    * _Unique identifier for the invoice_
    * Type: `string`
  * **invoiceDate** `required`
    * _Date the invoice was issued (ISO format)_
    * Type: `string`
    * String format must be a “date”
  * **dueDate**
    * _Payment due date (ISO format)_
    * Type: `string`
    * String format must be a “date”
  * **billingAddress** `required`
    * _Billing address details_
    * Type: `object`
    * **_Properties_**
      * **name** `required`
        * Type: `string`
      * **street** `required`
        * Type: `string`
      * **city** `required`
        * Type: `string`
      * **state**
        * Type: `string`
      * **postalCode** `required`
        * Type: `string`
      * **country** `required`
        * Type: `string`
  * **shippingAddress**
    * _Shipping address details_
    * Type: `object`
    * **_Properties_**
      * **name** `required`
        * Type: `string`
      * **street** `required`
        * Type: `string`
      * **city** `required`
        * Type: `string`
      * **state**
        * Type: `string`
      * **postalCode** `required`
        * Type: `string`
      * **country** `required`
        * Type: `string`
  * **items** `required`
    * _List of items included in the invoice_
    * Type: `array`
      * **_Items_**
      * Type: `object`
      * **_Properties_**
        * **description** `required`
          * _Description of the item_
          * Type: `string`
        * **quantity** `required`
          * _Quantity of the item_
          * Type: `number`
          * Range: ≥ 1
        * **unitPrice** `required`
          * _Price per unit of the item_
          * Type: `number`
          * Range: ≥ 0
        * **totalPrice** `required`
          * _Total price for this item_
          * Type: `number`
          * Range: ≥ 0
  * **subTotal** `required`
    * _Subtotal for all items_
    * Type: `number`
    * Range: ≥ 0
  * **tax** `required`
    * _Tax details_
    * Type: `object`
    * **_Properties_**
      * **rate** `required`
        * _Tax rate as a percentage_
        * Type: `number`
        * Range: ≥ 0
      * **amount** `required`
        * _Total tax amount_
        * Type: `number`
        * Range: ≥ 0
  * **total** `required`
    * _Total amount due (subtotal + tax)_
    * Type: `number`
    * Range: ≥ 0
  * **notes**
    * _Additional notes or instructions for the invoice_
    * Type: `string`
  * **status** `required`
    * _Current payment status of the invoice_
    * Type: `string`
    * The value is restricted to the following: 
      1. _“Paid”_
      2. _“Unpaid”_
      3. _“Overdue”_


## Resume
[Section titled “Resume”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/structured_output/#resume)
Follows the JSON Resume standard


Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'structured_output_json_schema_name="resume"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

#### Structured Output: Resume Schema
[Section titled “Structured Output: Resume Schema”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/structured_output/#structured-output-resume-schema)
Based on <https://github.com/jsonresume/resume-schema>
Type: `object`
**_Properties_**
  * **basics**
    * Type: `object`
    * **_Properties_**
      * **name**
        * Type: `string`
      * **label**
        * _e.g. Web Developer_
        * Type: `string`
      * **image**
        * _URL (as per RFC 3986) to a image in JPEG or PNG format_
        * Type: `string`
      * **email**
        * _e.g.thomas@gmail.com_
        * Type: `string`
        * String format must be a “email”
      * **phone**
        * _Phone numbers are stored as strings so use any format you like, e.g. 712-117-2923_
        * Type: `string`
      * **url**
        * _URL (as per RFC 3986) to your website, e.g. personal homepage_
        * Type: `string`
        * String format must be a “uri”
      * **summary**
        * _Write a short 2-3 sentence biography about yourself_
        * Type: `string`
      * **location**
        * Type: `object`
        * **_Properties_**
          * **address**
            * Type: `string`
          * **postalCode**
            * Type: `string`
          * **city**
            * Type: `string`
          * **countryCode**
            * _code as per ISO-3166-1 ALPHA-2, e.g. US, AU, IN_
            * Type: `string`
          * **region**
            * _The general region where you live. Can be a US state, or a province, for instance._
            * Type: `string`
      * **profiles**
        * _Specify any number of social networks that you participate in_
        * Type: `array`
          * **_Items_**
          * Type: `object`
          * This schema accepts additional properties.
          * **_Properties_**
            * **network**
              * _e.g. Facebook or Twitter_
              * Type: `string`
            * **username**
              * _e.g. neutralthoughts_
              * Type: `string`
            * **url**
              * _e.g.<http://twitter.example.com/neutralthoughts>_
              * Type: `string`
              * String format must be a “uri”
  * **work**
    * Type: `array`
      * **_Items_**
      * Type: `object`
      * **_Properties_**
        * **name**
          * _e.g. Facebook_
          * Type: `string`
        * **location**
          * _e.g. Menlo Park, CA_
          * Type: `string`
        * **description**
          * _e.g. Social Media Company_
          * Type: `string`
        * **position**
          * _e.g. Software Engineer_
          * Type: `string`
        * **url**
          * _e.g.<http://facebook.example.com>_
          * Type: `string`
          * String format must be a “uri”
        * **startDate**
          * $ref: [#/definitions/iso8601](https://developers.llamaindex.ai/python/cloud/llamaparse/features/structured_output/#/definitions/iso8601)
        * **endDate**
          * $ref: [#/definitions/iso8601](https://developers.llamaindex.ai/python/cloud/llamaparse/features/structured_output/#/definitions/iso8601)
        * **summary**
          * _Give an overview of your responsibilities at the company_
          * Type: `string`
        * **highlights**
          * _Specify multiple accomplishments_
          * Type: `array`
            * **_Items_**
            * _e.g. Increased profits by 20% from 2011-2012 through viral advertising_
            * Type: `string`
  * **volunteer**
    * Type: `array`
      * **_Items_**
      * Type: `object`
      * **_Properties_**
        * **organization**
          * _e.g. Facebook_
          * Type: `string`
        * **position**
          * _e.g. Software Engineer_
          * Type: `string`
        * **url**
          * _e.g.<http://facebook.example.com>_
          * Type: `string`
          * String format must be a “uri”
        * **startDate**
          * $ref: [#/definitions/iso8601](https://developers.llamaindex.ai/python/cloud/llamaparse/features/structured_output/#/definitions/iso8601)
        * **endDate**
          * $ref: [#/definitions/iso8601](https://developers.llamaindex.ai/python/cloud/llamaparse/features/structured_output/#/definitions/iso8601)
        * **summary**
          * _Give an overview of your responsibilities at the company_
          * Type: `string`
        * **highlights**
          * _Specify accomplishments and achievements_
          * Type: `array`
            * **_Items_**
            * _e.g. Increased profits by 20% from 2011-2012 through viral advertising_
            * Type: `string`
  * **education**
    * Type: `array`
      * **_Items_**
      * Type: `object`
      * **_Properties_**
        * **institution**
          * _e.g. Massachusetts Institute of Technology_
          * Type: `string`
        * **url**
          * _e.g.<http://facebook.example.com>_
          * Type: `string`
          * String format must be a “uri”
        * **area**
          * _e.g. Arts_
          * Type: `string`
        * **studyType**
          * _e.g. Bachelor_
          * Type: `string`
        * **startDate**
          * $ref: [#/definitions/iso8601](https://developers.llamaindex.ai/python/cloud/llamaparse/features/structured_output/#/definitions/iso8601)
        * **endDate**
          * $ref: [#/definitions/iso8601](https://developers.llamaindex.ai/python/cloud/llamaparse/features/structured_output/#/definitions/iso8601)
        * **score**
          * _grade point average, e.g. 3.67/4.0_
          * Type: `string`
        * **courses**
          * _List notable courses/subjects_
          * Type: `array`
            * **_Items_**
            * _e.g. H1302 - Introduction to American history_
            * Type: `string`
  * **awards**
    * _Specify any awards you have received throughout your professional career_
    * Type: `array`
      * **_Items_**
      * Type: `object`
      * **_Properties_**
        * **title**
          * _e.g. One of the 100 greatest minds of the century_
          * Type: `string`
        * **date**
          * $ref: [#/definitions/iso8601](https://developers.llamaindex.ai/python/cloud/llamaparse/features/structured_output/#/definitions/iso8601)
        * **awarder**
          * _e.g. Time Magazine_
          * Type: `string`
        * **summary**
          * _e.g. Received for my work with Quantum Physics_
          * Type: `string`
  * **certificates**
    * _Specify any certificates you have received throughout your professional career_
    * Type: `array`
      * **_Items_**
      * Type: `object`
      * This schema accepts additional properties.
      * **_Properties_**
        * **name**
          * _e.g. Certified Kubernetes Administrator_
          * Type: `string`
        * **date**
          * $ref: [#/definitions/iso8601](https://developers.llamaindex.ai/python/cloud/llamaparse/features/structured_output/#/definitions/iso8601)
        * **url**
          * _e.g.<http://example.com>_
          * Type: `string`
          * String format must be a “uri”
        * **issuer**
          * _e.g. CNCF_
          * Type: `string`
  * **publications**
    * _Specify your publications through your career_
    * Type: `array`
      * **_Items_**
      * Type: `object`
      * **_Properties_**
        * **name**
          * _e.g. The World Wide Web_
          * Type: `string`
        * **publisher**
          * _e.g. IEEE, Computer Magazine_
          * Type: `string`
        * **releaseDate**
          * $ref: [#/definitions/iso8601](https://developers.llamaindex.ai/python/cloud/llamaparse/features/structured_output/#/definitions/iso8601)
        * **url**
          * _e.g.<http://www.computer.org.example.com/csdl/mags/co/1996/10/rx069-abs.html>_
          * Type: `string`
          * String format must be a “uri”
        * **summary**
          * _Short summary of publication. e.g. Discussion of the World Wide Web, HTTP, HTML._
          * Type: `string`
  * **skills**
    * _List out your professional skill-set_
    * Type: `array`
      * **_Items_**
      * Type: `object`
      * This schema accepts additional properties.
      * **_Properties_**
        * **name**
          * _e.g. Web Development_
          * Type: `string`
        * **level**
          * _e.g. Master_
          * Type: `string`
        * **keywords**
          * _List some keywords pertaining to this skill_
          * Type: `array`
            * **_Items_**
            * _e.g. HTML_
            * Type: `string`
  * **languages**
    * _List any other languages you speak_
    * Type: `array`
      * **_Items_**
      * Type: `object`
      * **_Properties_**
        * **language**
          * _e.g. English, Spanish_
          * Type: `string`
        * **fluency**
          * _e.g. Fluent, Beginner_
          * Type: `string`
  * **interests**
    * Type: `array`
      * **_Items_**
      * Type: `object`
      * **_Properties_**
        * **name**
          * _e.g. Philosophy_
          * Type: `string`
        * **keywords**
          * Type: `array`
            * **_Items_**
            * _e.g. Friedrich Nietzsche_
            * Type: `string`
  * **references**
    * _List references you have received_
    * Type: `array`
      * **_Items_**
      * Type: `object`
      * **_Properties_**
        * **name**
          * _e.g. Timothy Cook_
          * Type: `string`
        * **reference**
          * _e.g. Joe blogs was a great employee, who turned up to work at least once a week. He exceeded my expectations when it came to doing nothing._
          * Type: `string`
  * **projects**
    * _Specify career projects_
    * Type: `array`
      * **_Items_**
      * Type: `object`
      * **_Properties_**
        * **name**
          * _e.g. The World Wide Web_
          * Type: `string`
        * **description**
          * _Short summary of project. e.g. Collated works of 2017._
          * Type: `string`
        * **highlights**
          * _Specify multiple features_
          * Type: `array`
            * **_Items_**
            * _e.g. Directs you close but not quite there_
            * Type: `string`
        * **keywords**
          * _Specify special elements involved_
          * Type: `array`
            * **_Items_**
            * _e.g. AngularJS_
            * Type: `string`
        * **startDate**
          * $ref: [#/definitions/iso8601](https://developers.llamaindex.ai/python/cloud/llamaparse/features/structured_output/#/definitions/iso8601)
        * **endDate**
          * $ref: [#/definitions/iso8601](https://developers.llamaindex.ai/python/cloud/llamaparse/features/structured_output/#/definitions/iso8601)
        * **url**
          * _e.g.<http://www.computer.org/csdl/mags/co/1996/10/rx069-abs.html>_
          * Type: `string`
          * String format must be a “uri”
        * **roles**
          * _Specify your role on this project or in company_
          * Type: `array`
            * **_Items_**
            * _e.g. Team Lead, Speaker, Writer_
            * Type: `string`
        * **entity**
          * _Specify the relevant company/entity affiliations e.g. ‘greenpeace’, ‘corporationXYZ’_
          * Type: `string`
        * **type**
          * _ e.g. ‘volunteering’, ‘presentation’, ‘talk’, ‘application’, ‘conference’_
          * Type: `string`


