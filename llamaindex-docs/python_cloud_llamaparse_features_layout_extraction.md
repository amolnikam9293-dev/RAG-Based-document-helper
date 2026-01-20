[Skip to content](https://developers.llamaindex.ai/python/cloud/llamaparse/features/layout_extraction/#_top)
# Layout Extraction
LlamaParse supports layout extraction. This can be useful if you want to be able to reconstitute the original look of the document by putting things back in their original places.
If you set `extract_layout=True` on the API and request [JSON output](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/output_modes/) it will include bounding boxes for the following types:
  * tables
  * figures
  * titles
  * text
  * lists


The layout data is returned in the JSON data, as a `layout` property attached to each page.
Each layout entry contains:
  * A `bbox` expressed as a fraction of page width and height (a number between 0 and 1)
  * An `image` name corresponding to an image of the element. This can be retrieved with the [image API](https://developers.llamaindex.ai/python/cloud/llamaparse/presets_and_modes/output_modes/#images) just like other images.
  * A `confidence` score (for 0 to 1, 1 mean good)
  * A `label` indicating the type of element
  * `isLikelyNoise`, set to `true` if our [NMS](https://builtin.com/machine-learning/non-maximum-suppression) detects that the element is likely to be noise.


## Ignore document elements for layout detection
[Section titled “Ignore document elements for layout detection”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/layout_extraction/#ignore-document-elements-for-layout-detection)
By default the layout extraction is aligned on the underlying bbox of element we extract form the document. If this is causing issue it is possible to deactivate this alignment by setting `ignore_document_elements_for_layout_detection=true`.
## Example
[Section titled “Example”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/layout_extraction/#example)
```



"bbox": {




"x": 0.176,




"y": 0.497,




"w": 0.651,




"h": 0.112





"image": "page_1_text_1.jpg",




"confidence": 0.996,




"label": "text",




"isLikelyNoise": false



```

## Cost
[Section titled “Cost”](https://developers.llamaindex.ai/python/cloud/llamaparse/features/layout_extraction/#cost)
Layout extraction costs 1 extra credit per page.
