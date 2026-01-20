[Skip to content](https://developers.llamaindex.ai/python/cloud/llamaparse/faq/#_top)
# LlamaParse FAQ
## How do credits work?
[Section titled “How do credits work?”](https://developers.llamaindex.ai/python/cloud/llamaparse/faq/#how-do-credits-work)
All features are priced using credits, which are billed per page (or minute for audio). Credits vary by parsing mode, model, and whether files are cached. Check the [Credit Pricing & Usage](https://developers.llamaindex.ai/python/cloud/general/pricing) page
## How to see credit usage?
[Section titled “How to see credit usage?”](https://developers.llamaindex.ai/python/cloud/llamaparse/faq/#how-to-see-credit-usage)
You can see how many credits you’ve used and have left in the UI or usage metadata included in every API call. Check the [metadata docs](https://developers.llamaindex.ai/python/cloud/llamaparse/features/metadata#result-format) for instructions on how to get this data)
## Are the documents stored or cached anywhere, if so for how long?
[Section titled “Are the documents stored or cached anywhere, if so for how long?”](https://developers.llamaindex.ai/python/cloud/llamaparse/faq/#are-the-documents-stored-or-cached-anywhere-if-so-for-how-long)
Privacy is an important consideration when parsing sensitive documents. Your data is kept private to you only and is used only to return your results, never for model training. To avoid charging multiple times for parsing the same document, your files are cached for 48 hours and then permanently deleted from our servers.
## How to avoid caching sensitive documents?
[Section titled “How to avoid caching sensitive documents?”](https://developers.llamaindex.ai/python/cloud/llamaparse/faq/#how-to-avoid-caching-sensitive-documents)
If you wish to avoid caching sensitive documents, you may set do_not_cache=True.
## How long does parsing typically take?
[Section titled “How long does parsing typically take?”](https://developers.llamaindex.ai/python/cloud/llamaparse/faq/#how-long-does-parsing-typically-take)
It depends on the length and complexity of the document, in particular:
  * The number of pages
  * The number of images 
    * And whether text must be extracted from those images
  * The density of text on each page


On average, parsing a block of takes 45 seconds. However, this is a rough estimate and the actual time may vary. For example, a document with many images may take longer to parse than a text-only document with the same number of pages.
## What are some of the current limitations?
[Section titled “What are some of the current limitations?”](https://developers.llamaindex.ai/python/cloud/llamaparse/faq/#what-are-some-of-the-current-limitations)
  * Maximum run time for jobs : 30 minutes. If your job take more than 30 minutes to process, a TIMEOUT error will be raised.
  * Maximum size of files: 300Mb.
  * Maximum image extracted / OCR per page: 35 images. If more images are present in a page, only the 35 biggest one are extracted / OCR.
  * Maximum amount of text extracted per page: 64Kb. Content beyond the 64Kb mark is ignored.


