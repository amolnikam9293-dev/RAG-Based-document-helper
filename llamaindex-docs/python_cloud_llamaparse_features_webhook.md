[Skip to content](https://developers.llamaindex.ai/python/cloud/llamaparse/features/webhook/#_top)
# Webhook
At the end of a LlamaParse job, you can chose to receive the result directly on one of your endpoint. You simply have to precise the URL of the webhook endpoint where the data should be sent.
The `webhook_url` parameter should be a valid URL that your application or service is set up to handle incoming data from.
There’s a few restriction on the webhook URL:
  * The protocol must be HTTPS.
  * The host must be a domain name rather than an IP address.
  * The URL must be less than 200 characters.


Data will be sent as a POST request with a JSON body and with the following format:
```



"txt": "raw text",




"md": "markdown text",




"json": [





"page": 1,




"text": "page 1 raw text",




"md": "page 1 markdown text",




"images": [





"name": "img_p0_1.png",




"height": 100,




"width": 100,




"x": 0,




"y": 0








"images": [




"img_p0_1.png"




```

## How to use
[Section titled “How to use”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/webhook/#how-to-use)
To use the Webhooks, set `webhook_url` to your URL (`https://example.com/webhook`).


```


parser =LlamaParse(




webhook_url="https://example.com/webhook"



```

Terminal window```


curl-X'POST'\




'https://api.cloud.llamaindex.ai/api/v1/parsing/upload'\




-H'accept: application/json'\




-H'Content-Type: multipart/form-data'\




-H"Authorization: Bearer $LLAMA_CLOUD_API_KEY"\




--form'webhook_url="https://example.com/webhook"'\




-F'file=@/path/to/your/file.pdf;type=application/pdf'


```

