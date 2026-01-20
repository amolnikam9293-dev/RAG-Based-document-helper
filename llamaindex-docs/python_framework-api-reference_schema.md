# Index
Base schema for data structures.
##  BaseComponent [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.BaseComponent "Permanent link")
Bases: `BaseModel`
Base component object to capture class names.
Source code in `llama_index/core/schema.py`
```
 80
 81
 82
 83
 84
 85
 86
 87
 88
 89
 90
 91
 92
 93
 94
 95
 96
 97
 98
 99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
```
| ```
class BaseComponent(BaseModel):
"""Base component object to capture class names."""

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        json_schema = handler(core_schema)
        json_schema = handler.resolve_ref_schema(json_schema)

        # inject class name to help with serde
        if "properties" in json_schema:
            json_schema["properties"]["class_name"] = {
                "title": "Class Name",
                "type": "string",
                "default": cls.class_name(),
            }
        return json_schema

    @classmethod
    def class_name(cls) -> str:
"""
        Get the class name, used as a unique ID in serialization.

        This provides a key that makes serialization robust against actual class
        name changes.
        """
        return "base_component"

    def json(self, **kwargs: Any) -> str:
        return self.to_json(**kwargs)

    @model_serializer(mode="wrap")
    def custom_model_dump(
        self, handler: SerializerFunctionWrapHandler, info: SerializationInfo
    ) -> Dict[str, Any]:
        data = handler(self)
        data["class_name"] = self.class_name()
        return data

    def dict(self, **kwargs: Any) -> Dict[str, Any]:
        return self.model_dump(**kwargs)

    def __getstate__(self) -> Dict[str, Any]:
        state = super().__getstate__()

        # remove attributes that are not pickleable -- kind of dangerous
        keys_to_remove = []
        for key, val in state["__dict__"].items():
            try:
                pickle.dumps(val)
            except Exception:
                keys_to_remove.append(key)

        for key in keys_to_remove:
            logging.warning(f"Removing unpickleable attribute {key}")
            del state["__dict__"][key]

        # remove private attributes if they aren't pickleable -- kind of dangerous
        keys_to_remove = []
        private_attrs = state.get("__pydantic_private__", None)
        if private_attrs:
            for key, val in state["__pydantic_private__"].items():
                try:
                    pickle.dumps(val)
                except Exception:
                    keys_to_remove.append(key)

            for key in keys_to_remove:
                logging.warning(f"Removing unpickleable private attribute {key}")
                del state["__pydantic_private__"][key]

        return state

    def __setstate__(self, state: Dict[str, Any]) -> None:
        # Use the __dict__ and __init__ method to set state
        # so that all variables initialize
        try:
            self.__init__(**state["__dict__"])  # type: ignore
        except Exception:
            # Fall back to the default __setstate__ method
            # This may not work if the class had unpickleable attributes
            super().__setstate__(state)

    def to_dict(self, **kwargs: Any) -> Dict[str, Any]:
        data = self.dict(**kwargs)
        data["class_name"] = self.class_name()
        return data

    def to_json(self, **kwargs: Any) -> str:
        data = self.to_dict(**kwargs)
        return json.dumps(data)

    # TODO: return type here not supported by current mypy version
    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs: Any) -> Self:  # type: ignore
        # In SimpleKVStore we rely on shallow coping. Hence, the data will be modified in the store directly.
        # And it is the same when the user is passing a dictionary to create a component. We can't modify the passed down dictionary.
        data = dict(data)
        if isinstance(kwargs, dict):
            data.update(kwargs)
        data.pop("class_name", None)
        return cls(**data)

    @classmethod
    def from_json(cls, data_str: str, **kwargs: Any) -> Self:  # type: ignore
        data = json.loads(data_str)
        return cls.from_dict(data, **kwargs)

```
  
---|---  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.BaseComponent.class_name "Permanent link")
```
class_name() -> 

```

Get the class name, used as a unique ID in serialization.
This provides a key that makes serialization robust against actual class name changes.
Source code in `llama_index/core/schema.py`
```
 99
100
101
102
103
104
105
106
107
```
| ```
@classmethod
def class_name(cls) -> str:
"""
    Get the class name, used as a unique ID in serialization.

    This provides a key that makes serialization robust against actual class
    name changes.
    """
    return "base_component"

```
  
---|---  
##  TransformComponent [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.TransformComponent "Permanent link")
Bases: , `DispatcherSpanMixin`
Base class for transform components.
Source code in `llama_index/core/schema.py`
```
190
191
192
193
194
195
196
197
198
199
200
201
202
203
```
| ```
class TransformComponent(BaseComponent, DispatcherSpanMixin):
"""Base class for transform components."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @abstractmethod
    def __call__(self, nodes: Sequence[BaseNode], **kwargs: Any) -> Sequence[BaseNode]:
"""Transform nodes."""

    async def acall(
        self, nodes: Sequence[BaseNode], **kwargs: Any
    ) -> Sequence[BaseNode]:
"""Async transform nodes."""
        return self.__call__(nodes, **kwargs)

```
  
---|---  
###  acall `async` [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.TransformComponent.acall "Permanent link")
```
acall(nodes: Sequence[], **kwargs: ) -> Sequence[]

```

Async transform nodes.
Source code in `llama_index/core/schema.py`
```
199
200
201
202
203
```
| ```
async def acall(
    self, nodes: Sequence[BaseNode], **kwargs: Any
) -> Sequence[BaseNode]:
"""Async transform nodes."""
    return self.__call__(nodes, **kwargs)

```
  
---|---  
##  NodeRelationship [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.NodeRelationship "Permanent link")
Bases: `str`, `Enum`
Node relationships used in `BaseNode` class.
Attributes:
Name | Type | Description  
---|---|---  
`SOURCE` |  The node is the source document.  
`PREVIOUS` |  The node is the previous node in the document.  
The node is the next node in the document.  
`PARENT` |  The node is the parent node in the document.  
`CHILD` |  The node is a child node in the document.  
Source code in `llama_index/core/schema.py`
```
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
```
| ```
class NodeRelationship(str, Enum):
"""
    Node relationships used in `BaseNode` class.

    Attributes:
        SOURCE: The node is the source document.
        PREVIOUS: The node is the previous node in the document.
        NEXT: The node is the next node in the document.
        PARENT: The node is the parent node in the document.
        CHILD: The node is a child node in the document.

    """

    SOURCE = auto()
    PREVIOUS = auto()
    NEXT = auto()
    PARENT = auto()
    CHILD = auto()

```
  
---|---  
##  RelatedNodeInfo [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.RelatedNodeInfo "Permanent link")
Bases: 
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`node_id` |  _required_  
`node_type` |  `Annotated[ObjectType, PlainSerializer] | str | None` |  `None`  
`hash` |  `str | None` |  `None`  
Source code in `llama_index/core/schema.py`
```
248
249
250
251
252
253
254
255
256
```
| ```
class RelatedNodeInfo(BaseComponent):
    node_id: str
    node_type: Annotated[ObjectType, EnumNameSerializer] | str | None = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    hash: Optional[str] = None

    @classmethod
    def class_name(cls) -> str:
        return "RelatedNodeInfo"

```
  
---|---  
##  BaseNode [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.BaseNode "Permanent link")
Bases: 
Base node Object.
Generic abstract interface for retrievable nodes
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`id_` |  Unique ID of the node. |  `'f64e9cec-5009-4429-bf4d-fa73983e3f01'`  
`embedding` |  `List[float] | None` |  Embedding of the node. |  `None`  
`excluded_embed_metadata_keys` |  `List[str]` |  Metadata keys that are excluded from text for the embed model. |  `<dynamic>`  
`excluded_llm_metadata_keys` |  `List[str]` |  Metadata keys that are excluded from text for the LLM. |  `<dynamic>`  
`metadata_template` |  Template for how metadata is formatted, with {key} and {value} placeholders. |  `'{key}: {value}'`  
`metadata_separator` |  Separator between metadata fields when converting to string. |  `'\n'`  
Source code in `llama_index/core/schema.py`
```
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419
420
421
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
440
441
442
443
444
445
446
447
448
449
450
451
452
453
454
455
456
457
458
459
460
461
462
463
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
481
```
| ```
class BaseNode(BaseComponent):
"""
    Base node Object.

    Generic abstract interface for retrievable nodes

    """

    # hash is computed on local field, during the validation process
    model_config = ConfigDict(populate_by_name=True, validate_assignment=True)

    id_: str = Field(
        default_factory=lambda: str(uuid.uuid4()), description="Unique ID of the node."
    )
    embedding: Optional[List[float]] = Field(
        default=None, description="Embedding of the node."
    )

""""
    metadata fields
    - injected as part of the text shown to LLMs as context
    - injected as part of the text for generating embeddings
    - used by vector DBs for metadata filtering

    """
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="A flat dictionary of metadata fields",
        alias="extra_info",
    )
    excluded_embed_metadata_keys: List[str] = Field(
        default_factory=list,
        description="Metadata keys that are excluded from text for the embed model.",
    )
    excluded_llm_metadata_keys: List[str] = Field(
        default_factory=list,
        description="Metadata keys that are excluded from text for the LLM.",
    )
    relationships: Dict[
        Annotated[NodeRelationship, EnumNameSerializer],
        RelatedNodeType,
    ] = Field(
        default_factory=dict,
        description="A mapping of relationships to other node information.",
    )
    metadata_template: str = Field(
        default=DEFAULT_METADATA_TMPL,
        description=(
            "Template for how metadata is formatted, with {key} and "
            "{value} placeholders."
        ),
    )
    metadata_separator: str = Field(
        default="\n",
        description="Separator between metadata fields when converting to string.",
        alias="metadata_seperator",
    )

    @classmethod
    @abstractmethod
    def get_type(cls) -> str:
"""Get Object type."""

    @abstractmethod
    def get_content(self, metadata_mode: MetadataMode = MetadataMode.ALL) -> str:
"""Get object content."""

    def get_metadata_str(self, mode: MetadataMode = MetadataMode.ALL) -> str:
"""Metadata info string."""
        if mode == MetadataMode.NONE:
            return ""

        usable_metadata_keys = set(self.metadata.keys())
        if mode == MetadataMode.LLM:
            for key in self.excluded_llm_metadata_keys:
                if key in usable_metadata_keys:
                    usable_metadata_keys.remove(key)
        elif mode == MetadataMode.EMBED:
            for key in self.excluded_embed_metadata_keys:
                if key in usable_metadata_keys:
                    usable_metadata_keys.remove(key)

        return self.metadata_separator.join(
            [
                self.metadata_template.format(key=key, value=str(value))
                for key, value in self.metadata.items()
                if key in usable_metadata_keys
            ]
        )

    @abstractmethod
    def set_content(self, value: Any) -> None:
"""Set the content of the node."""

    @property
    @abstractmethod
    def hash(self) -> str:
"""Get hash of node."""

    @property
    def node_id(self) -> str:
        return self.id_

    @node_id.setter
    def node_id(self, value: str) -> None:
        self.id_ = value

    @property
    def source_node(self) -> Optional[RelatedNodeInfo]:
"""
        Source object node.

        Extracted from the relationships field.

        """
        if NodeRelationship.SOURCE not in self.relationships:
            return None

        relation = self.relationships[NodeRelationship.SOURCE]
        if isinstance(relation, list):
            raise ValueError("Source object must be a single RelatedNodeInfo object")
        return relation

    @property
    def prev_node(self) -> Optional[RelatedNodeInfo]:
"""Prev node."""
        if NodeRelationship.PREVIOUS not in self.relationships:
            return None

        relation = self.relationships[NodeRelationship.PREVIOUS]
        if not isinstance(relation, RelatedNodeInfo):
            raise ValueError("Previous object must be a single RelatedNodeInfo object")
        return relation

    @property
    def next_node(self) -> Optional[RelatedNodeInfo]:
"""Next node."""
        if NodeRelationship.NEXT not in self.relationships:
            return None

        relation = self.relationships[NodeRelationship.NEXT]
        if not isinstance(relation, RelatedNodeInfo):
            raise ValueError("Next object must be a single RelatedNodeInfo object")
        return relation

    @property
    def parent_node(self) -> Optional[RelatedNodeInfo]:
"""Parent node."""
        if NodeRelationship.PARENT not in self.relationships:
            return None

        relation = self.relationships[NodeRelationship.PARENT]
        if not isinstance(relation, RelatedNodeInfo):
            raise ValueError("Parent object must be a single RelatedNodeInfo object")
        return relation

    @property
    def child_nodes(self) -> Optional[List[RelatedNodeInfo]]:
"""Child nodes."""
        if NodeRelationship.CHILD not in self.relationships:
            return None

        relation = self.relationships[NodeRelationship.CHILD]
        if not isinstance(relation, list):
            raise ValueError("Child objects must be a list of RelatedNodeInfo objects.")
        return relation

    @property
    def ref_doc_id(self) -> Optional[str]:  # pragma: no cover
"""Deprecated: Get ref doc id."""
        source_node = self.source_node
        if source_node is None:
            return None
        return source_node.node_id

    @property
    @deprecated(
        version="0.12.2",
        reason="'extra_info' is deprecated, use 'metadata' instead.",
    )
    def extra_info(self) -> dict[str, Any]:  # pragma: no coverde
        return self.metadata

    @extra_info.setter
    @deprecated(
        version="0.12.2",
        reason="'extra_info' is deprecated, use 'metadata' instead.",
    )
    def extra_info(self, extra_info: dict[str, Any]) -> None:  # pragma: no coverde
        self.metadata = extra_info

    def __str__(self) -> str:
        source_text_truncated = truncate_text(
            self.get_content().strip(), TRUNCATE_LENGTH
        )
        source_text_wrapped = textwrap.fill(
            f"Text: {source_text_truncated}\n", width=WRAP_WIDTH
        )
        return f"Node ID: {self.node_id}\n{source_text_wrapped}"

    def get_embedding(self) -> List[float]:
"""
        Get embedding.

        Errors if embedding is None.

        """
        if self.embedding is None:
            raise ValueError("embedding not set.")
        return self.embedding

    def as_related_node_info(self) -> RelatedNodeInfo:
"""Get node as RelatedNodeInfo."""
        return RelatedNodeInfo(
            node_id=self.node_id,
            node_type=self.get_type(),
            metadata=self.metadata,
            hash=self.hash,
        )

```
  
---|---  
###  embedding `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.BaseNode.embedding "Permanent link")
```
embedding: Optional[[float]] = (default=None, description='Embedding of the node.')

```

" metadata fields - injected as part of the text shown to LLMs as context - injected as part of the text for generating embeddings - used by vector DBs for metadata filtering
###  hash `abstractmethod` `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.BaseNode.hash "Permanent link")
```
hash: 

```

Get hash of node.
###  source_node `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.BaseNode.source_node "Permanent link")
```
source_node: Optional[]

```

Source object node.
Extracted from the relationships field.
###  prev_node `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.BaseNode.prev_node "Permanent link")
```
prev_node: Optional[]

```

Prev node.
###  next_node `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.BaseNode.next_node "Permanent link")
```
next_node: Optional[]

```

Next node.
###  parent_node `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.BaseNode.parent_node "Permanent link")
```
parent_node: Optional[]

```

Parent node.
###  child_nodes `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.BaseNode.child_nodes "Permanent link")
```
child_nodes: Optional[[]]

```

Child nodes.
###  ref_doc_id `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.BaseNode.ref_doc_id "Permanent link")
```
ref_doc_id: Optional[]

```

Deprecated: Get ref doc id.
###  get_type `abstractmethod` `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.BaseNode.get_type "Permanent link")
```
get_type() -> 

```

Get Object type.
Source code in `llama_index/core/schema.py`
```
321
322
323
324
```
| ```
@classmethod
@abstractmethod
def get_type(cls) -> str:
"""Get Object type."""

```
  
---|---  
###  get_content `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.BaseNode.get_content "Permanent link")
```
get_content(metadata_mode: MetadataMode = ) -> 

```

Get object content.
Source code in `llama_index/core/schema.py`
```
326
327
328
```
| ```
@abstractmethod
def get_content(self, metadata_mode: MetadataMode = MetadataMode.ALL) -> str:
"""Get object content."""

```
  
---|---  
###  get_metadata_str [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.BaseNode.get_metadata_str "Permanent link")
```
get_metadata_str(mode: MetadataMode = ) -> 

```

Metadata info string.
Source code in `llama_index/core/schema.py`
```
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
```
| ```
def get_metadata_str(self, mode: MetadataMode = MetadataMode.ALL) -> str:
"""Metadata info string."""
    if mode == MetadataMode.NONE:
        return ""

    usable_metadata_keys = set(self.metadata.keys())
    if mode == MetadataMode.LLM:
        for key in self.excluded_llm_metadata_keys:
            if key in usable_metadata_keys:
                usable_metadata_keys.remove(key)
    elif mode == MetadataMode.EMBED:
        for key in self.excluded_embed_metadata_keys:
            if key in usable_metadata_keys:
                usable_metadata_keys.remove(key)

    return self.metadata_separator.join(
        [
            self.metadata_template.format(key=key, value=str(value))
            for key, value in self.metadata.items()
            if key in usable_metadata_keys
        ]
    )

```
  
---|---  
###  set_content `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.BaseNode.set_content "Permanent link")
```
set_content(value: ) -> None

```

Set the content of the node.
Source code in `llama_index/core/schema.py`
```
353
354
355
```
| ```
@abstractmethod
def set_content(self, value: Any) -> None:
"""Set the content of the node."""

```
  
---|---  
###  get_embedding [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.BaseNode.get_embedding "Permanent link")
```
get_embedding() -> [float]

```

Get embedding.
Errors if embedding is None.
Source code in `llama_index/core/schema.py`
```
463
464
465
466
467
468
469
470
471
472
```
| ```
def get_embedding(self) -> List[float]:
"""
    Get embedding.

    Errors if embedding is None.

    """
    if self.embedding is None:
        raise ValueError("embedding not set.")
    return self.embedding

```
  
---|---  
###  as_related_node_info [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.BaseNode.as_related_node_info "Permanent link")
```
as_related_node_info() -> 

```

Get node as RelatedNodeInfo.
Source code in `llama_index/core/schema.py`
```
474
475
476
477
478
479
480
481
```
| ```
def as_related_node_info(self) -> RelatedNodeInfo:
"""Get node as RelatedNodeInfo."""
    return RelatedNodeInfo(
        node_id=self.node_id,
        node_type=self.get_type(),
        metadata=self.metadata,
        hash=self.hash,
    )

```
  
---|---  
##  MediaResource [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.MediaResource "Permanent link")
Bases: `BaseModel`
A container class for media content.
This class represents a generic media resource that can be stored and accessed in multiple ways - as raw bytes, on the filesystem, or via URL. It also supports storing vector embeddings for the media content.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`embeddings` |  `dict[Literal['sparse', 'dense'], list[float]] | None` |  Vector representation of this resource. |  `None`  
`data` |  `bytes | None` |  base64 binary representation of this resource. |  `None`  
`text` |  `str | None` |  Text representation of this resource. |  `None`  
`path` |  `Path | None` |  Filesystem path of this resource. |  `None`  
`url` |  `AnyUrl | None` |  URL to reach this resource. |  `None`  
`mimetype` |  `str | None` |  MIME type of this resource. |  `None`  
Attributes:
Name | Type | Description  
---|---|---  
`embeddings` |  Multi-vector dict representation of this resource for embedding-based search/retrieval  
`text` |  Plain text representation of this resource  
`data` |  Raw binary data of the media content  
`mimetype` |  The MIME type indicating the format/type of the media content  
`path` |  Local filesystem path where the media content can be accessed  
URL where the media content can be accessed remotely  
Source code in `llama_index/core/schema.py`
```
487
488
489
490
491
492
493
494
495
496
497
498
499
500
501
502
503
504
505
506
507
508
509
510
511
512
513
514
515
516
517
518
519
520
521
522
523
524
525
526
527
528
529
530
531
532
533
534
535
536
537
538
539
540
541
542
543
544
545
546
547
548
549
550
551
552
553
554
555
556
557
558
559
560
561
562
563
564
565
566
567
568
569
570
571
572
573
574
575
576
577
578
579
580
581
582
583
584
585
586
587
588
589
590
591
592
593
594
595
596
597
598
599
600
601
602
603
604
605
606
607
608
609
```
| ```
class MediaResource(BaseModel):
"""
    A container class for media content.

    This class represents a generic media resource that can be stored and accessed
    in multiple ways - as raw bytes, on the filesystem, or via URL. It also supports
    storing vector embeddings for the media content.

    Attributes:
        embeddings: Multi-vector dict representation of this resource for embedding-based search/retrieval
        text: Plain text representation of this resource
        data: Raw binary data of the media content
        mimetype: The MIME type indicating the format/type of the media content
        path: Local filesystem path where the media content can be accessed
        url: URL where the media content can be accessed remotely

    """

    embeddings: dict[EmbeddingKind, list[float]] | None = Field(
        default=None, description="Vector representation of this resource."
    )
    data: bytes | None = Field(
        default=None,
        exclude=True,
        description="base64 binary representation of this resource.",
    )
    text: str | None = Field(
        default=None, description="Text representation of this resource."
    )
    path: Path | None = Field(
        default=None, description="Filesystem path of this resource."
    )
    url: AnyUrl | None = Field(default=None, description="URL to reach this resource.")
    mimetype: str | None = Field(
        default=None, description="MIME type of this resource."
    )

    model_config = {
        # This ensures validation runs even for None values
        "validate_default": True
    }

    @field_validator("data", mode="after")
    @classmethod
    def validate_data(cls, v: bytes | None, info: ValidationInfo) -> bytes | None:
"""
        If binary data was passed, store the resource as base64 and guess the mimetype when possible.

        In case the model was built passing binary data but without a mimetype,
        we try to guess it using the filetype library. To avoid resource-intense
        operations, we won't load the path or the URL to guess the mimetype.
        """
        if v is None:
            return v

        try:
            # Check if data is already base64 encoded.
            # b64decode() can succeed on random binary data, so we
            # pass verify=True to make sure it's not a false positive
            decoded = base64.b64decode(v, validate=True)
        except BinasciiError:
            # b64decode failed, return encoded
            return base64.b64encode(v)

        # Good as is, return unchanged
        return v

    @field_validator("mimetype", mode="after")
    @classmethod
    def validate_mimetype(cls, v: str | None, info: ValidationInfo) -> str | None:
        if v is not None:
            return v

        # Since this field validator runs after the one for `data`
        # then the contents of `data` should be encoded already
        b64_data = info.data.get("data")
        if b64_data:  # encoded bytes
            decoded_data = base64.b64decode(b64_data)
            if guess := filetype.guess(decoded_data):
                return guess.mime

        # guess from path
        rpath: str | None = info.data["path"]
        if rpath:
            extension = Path(rpath).suffix.replace(".", "")
            if ftype := filetype.get_type(ext=extension):
                return ftype.mime

        return v

    @field_serializer("path")  # type: ignore
    def serialize_path(
        self, path: Optional[Path], _info: ValidationInfo
    ) -> Optional[str]:
        if path is None:
            return path
        return str(path)

    @property
    def hash(self) -> str:
"""
        Generate a hash to uniquely identify the media resource.

        The hash is generated based on the available content (data, path, text or url).
        Returns an empty string if no content is available.
        """
        bits: list[str] = []
        if self.text is not None:
            bits.append(self.text)
        if self.data is not None:
            # Hash the binary data if available
            bits.append(str(sha256(self.data).hexdigest()))
        if self.path is not None:
            # Hash the file path if provided
            bits.append(str(sha256(str(self.path).encode("utf-8")).hexdigest()))
        if self.url is not None:
            # Use the URL string as basis for hash
            bits.append(str(sha256(str(self.url).encode("utf-8")).hexdigest()))

        doc_identity = "".join(bits)
        if not doc_identity:
            return ""
        return str(sha256(doc_identity.encode("utf-8", "surrogatepass")).hexdigest())

```
  
---|---  
###  hash `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.MediaResource.hash "Permanent link")
```
hash: 

```

Generate a hash to uniquely identify the media resource.
The hash is generated based on the available content (data, path, text or url). Returns an empty string if no content is available.
###  validate_data `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.MediaResource.validate_data "Permanent link")
```
validate_data(v: bytes | None, info: ValidationInfo) -> bytes | None

```

If binary data was passed, store the resource as base64 and guess the mimetype when possible.
In case the model was built passing binary data but without a mimetype, we try to guess it using the filetype library. To avoid resource-intense operations, we won't load the path or the URL to guess the mimetype.
Source code in `llama_index/core/schema.py`
```
529
530
531
532
533
534
535
536
537
538
539
540
541
542
543
544
545
546
547
548
549
550
551
552
```
| ```
@field_validator("data", mode="after")
@classmethod
def validate_data(cls, v: bytes | None, info: ValidationInfo) -> bytes | None:
"""
    If binary data was passed, store the resource as base64 and guess the mimetype when possible.

    In case the model was built passing binary data but without a mimetype,
    we try to guess it using the filetype library. To avoid resource-intense
    operations, we won't load the path or the URL to guess the mimetype.
    """
    if v is None:
        return v

    try:
        # Check if data is already base64 encoded.
        # b64decode() can succeed on random binary data, so we
        # pass verify=True to make sure it's not a false positive
        decoded = base64.b64decode(v, validate=True)
    except BinasciiError:
        # b64decode failed, return encoded
        return base64.b64encode(v)

    # Good as is, return unchanged
    return v

```
  
---|---  
##  Node [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Node "Permanent link")
Bases: 
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`text_resource` |  `MediaResource[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.MediaResource "llama_index.core.schema.MediaResource") | None` |  Text content of the node. |  `None`  
`image_resource` |  `MediaResource[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.MediaResource "llama_index.core.schema.MediaResource") | None` |  Image content of the node. |  `None`  
`audio_resource` |  `MediaResource[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.MediaResource "llama_index.core.schema.MediaResource") | None` |  Audio content of the node. |  `None`  
`video_resource` |  `MediaResource[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.MediaResource "llama_index.core.schema.MediaResource") | None` |  Video content of the node. |  `None`  
`text_template` |  Template for how text_resource is formatted, with {content} and {metadata_str} placeholders. |  `'{metadata_str}\n\n{content}'`  
Source code in `llama_index/core/schema.py`
```
612
613
614
615
616
617
618
619
620
621
622
623
624
625
626
627
628
629
630
631
632
633
634
635
636
637
638
639
640
641
642
643
644
645
646
647
648
649
650
651
652
653
654
655
656
657
658
659
660
661
662
663
664
665
666
667
668
669
670
671
672
673
674
675
676
677
678
679
680
681
682
683
684
685
686
687
688
```
| ```
class Node(BaseNode):
    text_resource: MediaResource | None = Field(
        default=None, description="Text content of the node."
    )
    image_resource: MediaResource | None = Field(
        default=None, description="Image content of the node."
    )
    audio_resource: MediaResource | None = Field(
        default=None, description="Audio content of the node."
    )
    video_resource: MediaResource | None = Field(
        default=None, description="Video content of the node."
    )
    text_template: str = Field(
        default=DEFAULT_TEXT_NODE_TMPL,
        description=(
            "Template for how text_resource is formatted, with {content} and "
            "{metadata_str} placeholders."
        ),
    )

    @classmethod
    def class_name(cls) -> str:
        return "Node"

    @classmethod
    def get_type(cls) -> str:
"""Get Object type."""
        return ObjectType.MULTIMODAL

    def get_content(self, metadata_mode: MetadataMode = MetadataMode.NONE) -> str:
"""
        Get the text content for the node if available.

        Provided for backward compatibility, use self.text_resource directly instead.
        """
        if self.text_resource:
            metadata_str = self.get_metadata_str(metadata_mode)
            if metadata_mode == MetadataMode.NONE or not metadata_str:
                return self.text_resource.text or ""

            return self.text_template.format(
                content=self.text_resource.text or "",
                metadata_str=metadata_str,
            ).strip()
        return ""

    def set_content(self, value: str) -> None:
"""
        Set the text content of the node.

        Provided for backward compatibility, set self.text_resource instead.
        """
        self.text_resource = MediaResource(text=value)

    @property
    def hash(self) -> str:
"""
        Generate a hash representing the state of the node.

        The hash is generated based on the available resources (audio, image, text or video) and its metadata.
        """
        doc_identities = []
        metadata_str = self.get_metadata_str(mode=MetadataMode.ALL)
        if metadata_str:
            doc_identities.append(metadata_str)
        if self.audio_resource is not None:
            doc_identities.append(self.audio_resource.hash)
        if self.image_resource is not None:
            doc_identities.append(self.image_resource.hash)
        if self.text_resource is not None:
            doc_identities.append(self.text_resource.hash)
        if self.video_resource is not None:
            doc_identities.append(self.video_resource.hash)

        doc_identity = "-".join(doc_identities)
        return str(sha256(doc_identity.encode("utf-8", "surrogatepass")).hexdigest())

```
  
---|---  
###  hash `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Node.hash "Permanent link")
```
hash: 

```

Generate a hash representing the state of the node.
The hash is generated based on the available resources (audio, image, text or video) and its metadata.
###  get_type `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Node.get_type "Permanent link")
```
get_type() -> 

```

Get Object type.
Source code in `llama_index/core/schema.py`
```
637
638
639
640
```
| ```
@classmethod
def get_type(cls) -> str:
"""Get Object type."""
    return ObjectType.MULTIMODAL

```
  
---|---  
###  get_content [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Node.get_content "Permanent link")
```
get_content(metadata_mode: MetadataMode = ) -> 

```

Get the text content for the node if available.
Provided for backward compatibility, use self.text_resource directly instead.
Source code in `llama_index/core/schema.py`
```
642
643
644
645
646
647
648
649
650
651
652
653
654
655
656
657
```
| ```
def get_content(self, metadata_mode: MetadataMode = MetadataMode.NONE) -> str:
"""
    Get the text content for the node if available.

    Provided for backward compatibility, use self.text_resource directly instead.
    """
    if self.text_resource:
        metadata_str = self.get_metadata_str(metadata_mode)
        if metadata_mode == MetadataMode.NONE or not metadata_str:
            return self.text_resource.text or ""

        return self.text_template.format(
            content=self.text_resource.text or "",
            metadata_str=metadata_str,
        ).strip()
    return ""

```
  
---|---  
###  set_content [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Node.set_content "Permanent link")
```
set_content(value: ) -> None

```

Set the text content of the node.
Provided for backward compatibility, set self.text_resource instead.
Source code in `llama_index/core/schema.py`
```
659
660
661
662
663
664
665
```
| ```
def set_content(self, value: str) -> None:
"""
    Set the text content of the node.

    Provided for backward compatibility, set self.text_resource instead.
    """
    self.text_resource = MediaResource(text=value)

```
  
---|---  
##  TextNode [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.TextNode "Permanent link")
Bases: 
Provided for backward compatibility.
Note: we keep the field with the typo "seperator" to maintain backward compatibility for serialized objects.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`text` |  Text content of the node.  
`mimetype` |  MIME type of the node content. |  `'text/plain'`  
`start_char_idx` |  `int | None` |  Start char index of the node. |  `None`  
`end_char_idx` |  `int | None` |  End char index of the node. |  `None`  
`metadata_seperator` |  Separator between metadata fields when converting to string. |  `'\n'`  
`text_template` |  Template for how text is formatted, with {content} and {metadata_str} placeholders. |  `'{metadata_str}\n\n{content}'`  
Source code in `llama_index/core/schema.py`
```
691
692
693
694
695
696
697
698
699
700
701
702
703
704
705
706
707
708
709
710
711
712
713
714
715
716
717
718
719
720
721
722
723
724
725
726
727
728
729
730
731
732
733
734
735
736
737
738
739
740
741
742
743
744
745
746
747
748
749
750
751
752
753
754
755
756
757
758
759
760
761
762
763
764
765
766
767
768
769
770
771
772
773
774
775
776
777
778
779
780
781
782
783
784
785
786
787
788
789
790
791
792
793
794
795
796
```
| ```
class TextNode(BaseNode):
"""
    Provided for backward compatibility.

    Note: we keep the field with the typo "seperator" to maintain backward compatibility for
    serialized objects.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
"""Make TextNode forward-compatible with Node by supporting 'text_resource' in the constructor."""
        if "text_resource" in kwargs:
            tr = kwargs.pop("text_resource")
            if isinstance(tr, MediaResource):
                kwargs["text"] = tr.text
            else:
                kwargs["text"] = tr["text"]
        super().__init__(*args, **kwargs)

    text: str = Field(default="", description="Text content of the node.")
    mimetype: str = Field(
        default="text/plain", description="MIME type of the node content."
    )
    start_char_idx: Optional[int] = Field(
        default=None, description="Start char index of the node."
    )
    end_char_idx: Optional[int] = Field(
        default=None, description="End char index of the node."
    )
    metadata_seperator: str = Field(
        default="\n",
        description="Separator between metadata fields when converting to string.",
    )
    text_template: str = Field(
        default=DEFAULT_TEXT_NODE_TMPL,
        description=(
            "Template for how text is formatted, with {content} and "
            "{metadata_str} placeholders."
        ),
    )

    @classmethod
    def class_name(cls) -> str:
        return "TextNode"

    @property
    def hash(self) -> str:
        doc_identity = str(self.text) + str(self.metadata)
        return str(sha256(doc_identity.encode("utf-8", "surrogatepass")).hexdigest())

    @classmethod
    def get_type(cls) -> str:
"""Get Object type."""
        return ObjectType.TEXT

    def get_content(self, metadata_mode: MetadataMode = MetadataMode.NONE) -> str:
"""Get object content."""
        metadata_str = self.get_metadata_str(mode=metadata_mode).strip()
        if metadata_mode == MetadataMode.NONE or not metadata_str:
            return self.text

        return self.text_template.format(
            content=self.text, metadata_str=metadata_str
        ).strip()

    def get_metadata_str(self, mode: MetadataMode = MetadataMode.ALL) -> str:
"""Metadata info string."""
        if mode == MetadataMode.NONE:
            return ""

        usable_metadata_keys = set(self.metadata.keys())
        if mode == MetadataMode.LLM:
            for key in self.excluded_llm_metadata_keys:
                if key in usable_metadata_keys:
                    usable_metadata_keys.remove(key)
        elif mode == MetadataMode.EMBED:
            for key in self.excluded_embed_metadata_keys:
                if key in usable_metadata_keys:
                    usable_metadata_keys.remove(key)

        return self.metadata_seperator.join(
            [
                self.metadata_template.format(key=key, value=str(value))
                for key, value in self.metadata.items()
                if key in usable_metadata_keys
            ]
        )

    def set_content(self, value: str) -> None:
"""Set the content of the node."""
        self.text = value

    def get_node_info(self) -> Dict[str, Any]:
"""Get node info."""
        return {"start": self.start_char_idx, "end": self.end_char_idx}

    def get_text(self) -> str:
        return self.get_content(metadata_mode=MetadataMode.NONE)

    @property
    @deprecated(
        version="0.12.2",
        reason="'node_info' is deprecated, use 'get_node_info' instead.",
    )
    def node_info(self) -> Dict[str, Any]:
"""Deprecated: Get node info."""
        return self.get_node_info()

```
  
---|---  
###  node_info `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.TextNode.node_info "Permanent link")
```
node_info: [, ]

```

Deprecated: Get node info.
###  get_type `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.TextNode.get_type "Permanent link")
```
get_type() -> 

```

Get Object type.
Source code in `llama_index/core/schema.py`
```
740
741
742
743
```
| ```
@classmethod
def get_type(cls) -> str:
"""Get Object type."""
    return ObjectType.TEXT

```
  
---|---  
###  get_content [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.TextNode.get_content "Permanent link")
```
get_content(metadata_mode: MetadataMode = ) -> 

```

Get object content.
Source code in `llama_index/core/schema.py`
```
745
746
747
748
749
750
751
752
753
```
| ```
def get_content(self, metadata_mode: MetadataMode = MetadataMode.NONE) -> str:
"""Get object content."""
    metadata_str = self.get_metadata_str(mode=metadata_mode).strip()
    if metadata_mode == MetadataMode.NONE or not metadata_str:
        return self.text

    return self.text_template.format(
        content=self.text, metadata_str=metadata_str
    ).strip()

```
  
---|---  
###  get_metadata_str [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.TextNode.get_metadata_str "Permanent link")
```
get_metadata_str(mode: MetadataMode = ) -> 

```

Metadata info string.
Source code in `llama_index/core/schema.py`
```
755
756
757
758
759
760
761
762
763
764
765
766
767
768
769
770
771
772
773
774
775
776
```
| ```
def get_metadata_str(self, mode: MetadataMode = MetadataMode.ALL) -> str:
"""Metadata info string."""
    if mode == MetadataMode.NONE:
        return ""

    usable_metadata_keys = set(self.metadata.keys())
    if mode == MetadataMode.LLM:
        for key in self.excluded_llm_metadata_keys:
            if key in usable_metadata_keys:
                usable_metadata_keys.remove(key)
    elif mode == MetadataMode.EMBED:
        for key in self.excluded_embed_metadata_keys:
            if key in usable_metadata_keys:
                usable_metadata_keys.remove(key)

    return self.metadata_seperator.join(
        [
            self.metadata_template.format(key=key, value=str(value))
            for key, value in self.metadata.items()
            if key in usable_metadata_keys
        ]
    )

```
  
---|---  
###  set_content [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.TextNode.set_content "Permanent link")
```
set_content(value: ) -> None

```

Set the content of the node.
Source code in `llama_index/core/schema.py`
```
778
779
780
```
| ```
def set_content(self, value: str) -> None:
"""Set the content of the node."""
    self.text = value

```
  
---|---  
###  get_node_info [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.TextNode.get_node_info "Permanent link")
```
get_node_info() -> [, ]

```

Get node info.
Source code in `llama_index/core/schema.py`
```
782
783
784
```
| ```
def get_node_info(self) -> Dict[str, Any]:
"""Get node info."""
    return {"start": self.start_char_idx, "end": self.end_char_idx}

```
  
---|---  
##  ImageNode [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.ImageNode "Permanent link")
Bases: 
Node with image.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`image` |  `str | None` |  `None`  
`image_path` |  `str | None` |  `None`  
`image_url` |  `str | None` |  `None`  
`image_mimetype` |  `str | None` |  `None`  
`text_embedding` |  `List[float] | None` |  Text embedding of image node, if text field is filled out |  `None`  
Source code in `llama_index/core/schema.py`
```
799
800
801
802
803
804
805
806
807
808
809
810
811
812
813
814
815
816
817
818
819
820
821
822
823
824
825
826
827
828
829
830
831
832
833
834
835
836
837
838
839
840
841
842
843
844
845
846
847
848
849
850
851
852
853
854
855
856
857
858
859
860
861
862
863
864
865
866
867
868
869
```
| ```
class ImageNode(TextNode):
"""Node with image."""

    # TODO: store reference instead of actual image
    # base64 encoded image str
    image: Optional[str] = None
    image_path: Optional[str] = None
    image_url: Optional[str] = None
    image_mimetype: Optional[str] = None
    text_embedding: Optional[List[float]] = Field(
        default=None,
        description="Text embedding of image node, if text field is filled out",
    )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
"""Make ImageNode forward-compatible with Node by supporting 'image_resource' in the constructor."""
        if "image_resource" in kwargs:
            ir = kwargs.pop("image_resource")
            if isinstance(ir, MediaResource):
                kwargs["image_path"] = ir.path.as_posix() if ir.path else None
                kwargs["image_url"] = ir.url
                kwargs["image_mimetype"] = ir.mimetype
            else:
                kwargs["image_path"] = ir.get("path", None)
                kwargs["image_url"] = ir.get("url", None)
                kwargs["image_mimetype"] = ir.get("mimetype", None)

        mimetype = kwargs.get("image_mimetype")
        if not mimetype and kwargs.get("image_path") is not None:
            # guess mimetype from image_path
            extension = Path(kwargs["image_path"]).suffix.replace(".", "")
            if ftype := filetype.get_type(ext=extension):
                kwargs["image_mimetype"] = ftype.mime

        super().__init__(*args, **kwargs)

    @classmethod
    def get_type(cls) -> str:
        return ObjectType.IMAGE

    @classmethod
    def class_name(cls) -> str:
        return "ImageNode"

    def resolve_image(self) -> ImageType:
"""Resolve an image such that PIL can read it."""
        if self.image is not None:
            import base64

            return BytesIO(base64.b64decode(self.image))
        elif self.image_path is not None:
            return self.image_path
        elif self.image_url is not None:
            # load image from URL
            import requests

            response = requests.get(self.image_url, timeout=(60, 60))
            return BytesIO(response.content)
        else:
            raise ValueError("No image found in node.")

    @property
    def hash(self) -> str:
"""Get hash of node."""
        # doc identity depends on if image, image_path, or image_url is set
        image_str = self.image or "None"
        image_path_str = self.image_path or "None"
        image_url_str = self.image_url or "None"
        image_text = self.text or "None"
        doc_identity = f"{image_str}-{image_path_str}-{image_url_str}-{image_text}"
        return str(sha256(doc_identity.encode("utf-8", "surrogatepass")).hexdigest())

```
  
---|---  
###  hash `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.ImageNode.hash "Permanent link")
```
hash: 

```

Get hash of node.
###  resolve_image [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.ImageNode.resolve_image "Permanent link")
```
resolve_image() -> ImageType

```

Resolve an image such that PIL can read it.
Source code in `llama_index/core/schema.py`
```
843
844
845
846
847
848
849
850
851
852
853
854
855
856
857
858
```
| ```
def resolve_image(self) -> ImageType:
"""Resolve an image such that PIL can read it."""
    if self.image is not None:
        import base64

        return BytesIO(base64.b64decode(self.image))
    elif self.image_path is not None:
        return self.image_path
    elif self.image_url is not None:
        # load image from URL
        import requests

        response = requests.get(self.image_url, timeout=(60, 60))
        return BytesIO(response.content)
    else:
        raise ValueError("No image found in node.")

```
  
---|---  
##  IndexNode [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.IndexNode "Permanent link")
Bases: 
Node with reference to any object.
This can include other indices, query engines, retrievers.
This can also include other nodes (though this is overlapping with `relationships` on the Node class).
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`index_id` |  _required_  
`obj` |  `None`  
Source code in `llama_index/core/schema.py`
```
872
873
874
875
876
877
878
879
880
881
882
883
884
885
886
887
888
889
890
891
892
893
894
895
896
897
898
899
900
901
902
903
904
905
906
907
908
909
910
911
912
913
914
915
916
917
918
919
920
921
922
923
924
925
926
927
928
929
930
931
932
933
934
935
936
937
938
939
940
941
942
943
944
945
946
947
```
| ```
class IndexNode(TextNode):
"""
    Node with reference to any object.

    This can include other indices, query engines, retrievers.

    This can also include other nodes (though this is overlapping with `relationships`
    on the Node class).

    """

    index_id: str
    obj: Any = None

    def dict(self, **kwargs: Any) -> Dict[str, Any]:
        from llama_index.core.storage.docstore.utils import doc_to_json

        data = super().dict(**kwargs)

        try:
            if self.obj is None:
                data["obj"] = None
            elif isinstance(self.obj, BaseNode):
                data["obj"] = doc_to_json(self.obj)
            elif isinstance(self.obj, BaseModel):
                data["obj"] = self.obj.model_dump()
            else:
                data["obj"] = json.dumps(self.obj)
        except Exception:
            raise ValueError("IndexNode obj is not serializable: " + str(self.obj))

        return data

    @classmethod
    def from_text_node(
        cls,
        node: TextNode,
        index_id: str,
    ) -> IndexNode:
"""Create index node from text node."""
        # copy all attributes from text node, add index id
        return cls(
            **node.dict(),
            index_id=index_id,
        )

    # TODO: return type here not supported by current mypy version
    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs: Any) -> Self:  # type: ignore
        output = super().from_dict(data, **kwargs)

        obj = data.get("obj")
        parsed_obj = None

        if isinstance(obj, str):
            parsed_obj = TextNode(text=obj)
        elif isinstance(obj, dict):
            from llama_index.core.storage.docstore.utils import json_to_doc

            # check if its a node, else assume stringable
            try:
                parsed_obj = json_to_doc(obj)  # type: ignore[assignment]
            except Exception:
                parsed_obj = TextNode(text=str(obj))

        output.obj = parsed_obj

        return output

    @classmethod
    def get_type(cls) -> str:
        return ObjectType.INDEX

    @classmethod
    def class_name(cls) -> str:
        return "IndexNode"

```
  
---|---  
###  from_text_node `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.IndexNode.from_text_node "Permanent link")
```
from_text_node(node: , index_id: ) -> 

```

Create index node from text node.
Source code in `llama_index/core/schema.py`
```
905
906
907
908
909
910
911
912
913
914
915
916
```
| ```
@classmethod
def from_text_node(
    cls,
    node: TextNode,
    index_id: str,
) -> IndexNode:
"""Create index node from text node."""
    # copy all attributes from text node, add index id
    return cls(
        **node.dict(),
        index_id=index_id,
    )

```
  
---|---  
##  NodeWithScore [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.NodeWithScore "Permanent link")
Bases: 
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`node` |  |  _required_  
`score` |  `float | None` |  `None`  
Source code in `llama_index/core/schema.py`
```
 950
 951
 952
 953
 954
 955
 956
 957
 958
 959
 960
 961
 962
 963
 964
 965
 966
 967
 968
 969
 970
 971
 972
 973
 974
 975
 976
 977
 978
 979
 980
 981
 982
 983
 984
 985
 986
 987
 988
 989
 990
 991
 992
 993
 994
 995
 996
 997
 998
 999
1000
1001
1002
1003
1004
1005
1006
```
| ```
class NodeWithScore(BaseComponent):
    node: SerializeAsAny[BaseNode]
    score: Optional[float] = None

    def __str__(self) -> str:
        score_str = "None" if self.score is None else f"{self.score: 0.3f}"
        return f"{self.node}\nScore: {score_str}\n"

    def get_score(self, raise_error: bool = False) -> float:
"""Get score."""
        if self.score is None:
            if raise_error:
                raise ValueError("Score not set.")
            else:
                return 0.0
        else:
            return self.score

    @classmethod
    def class_name(cls) -> str:
        return "NodeWithScore"

    ##### pass through methods to BaseNode #####
    @property
    def node_id(self) -> str:
        return self.node.node_id

    @property
    def id_(self) -> str:
        return self.node.id_

    @property
    def text(self) -> str:
        if isinstance(self.node, TextNode):
            return self.node.text
        else:
            raise ValueError("Node must be a TextNode to get text.")

    @property
    def metadata(self) -> Dict[str, Any]:
        return self.node.metadata

    @property
    def embedding(self) -> Optional[List[float]]:
        return self.node.embedding

    def get_text(self) -> str:
        if isinstance(self.node, TextNode):
            return self.node.get_text()
        else:
            raise ValueError("Node must be a TextNode to get text.")

    def get_content(self, metadata_mode: MetadataMode = MetadataMode.NONE) -> str:
        return self.node.get_content(metadata_mode=metadata_mode)

    def get_embedding(self) -> List[float]:
        return self.node.get_embedding()

```
  
---|---  
###  get_score [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.NodeWithScore.get_score "Permanent link")
```
get_score(raise_error:  = False) -> float

```

Get score.
Source code in `llama_index/core/schema.py`
```
958
959
960
961
962
963
964
965
966
```
| ```
def get_score(self, raise_error: bool = False) -> float:
"""Get score."""
    if self.score is None:
        if raise_error:
            raise ValueError("Score not set.")
        else:
            return 0.0
    else:
        return self.score

```
  
---|---  
##  Document [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Document "Permanent link")
Bases: 
Generic interface for a data document.
This document connects to data sources.
Source code in `llama_index/core/schema.py`
```
1012
1013
1014
1015
1016
1017
1018
1019
1020
1021
1022
1023
1024
1025
1026
1027
1028
1029
1030
1031
1032
1033
1034
1035
1036
1037
1038
1039
1040
1041
1042
1043
1044
1045
1046
1047
1048
1049
1050
1051
1052
1053
1054
1055
1056
1057
1058
1059
1060
1061
1062
1063
1064
1065
1066
1067
1068
1069
1070
1071
1072
1073
1074
1075
1076
1077
1078
1079
1080
1081
1082
1083
1084
1085
1086
1087
1088
1089
1090
1091
1092
1093
1094
1095
1096
1097
1098
1099
1100
1101
1102
1103
1104
1105
1106
1107
1108
1109
1110
1111
1112
1113
1114
1115
1116
1117
1118
1119
1120
1121
1122
1123
1124
1125
1126
1127
1128
1129
1130
1131
1132
1133
1134
1135
1136
1137
1138
1139
1140
1141
1142
1143
1144
1145
1146
1147
1148
1149
1150
1151
1152
1153
1154
1155
1156
1157
1158
1159
1160
1161
1162
1163
1164
1165
1166
1167
1168
1169
1170
1171
1172
1173
1174
1175
1176
1177
1178
1179
1180
1181
1182
1183
1184
1185
1186
1187
1188
1189
1190
1191
1192
1193
1194
1195
1196
1197
1198
1199
1200
1201
1202
1203
1204
1205
1206
1207
1208
1209
1210
1211
1212
1213
1214
1215
1216
1217
1218
1219
1220
1221
```
| ```
class Document(Node):
"""
    Generic interface for a data document.

    This document connects to data sources.
    """

    def __init__(self, **data: Any) -> None:
"""
        Keeps backward compatibility with old 'Document' versions.

        If 'text' was passed, store it in 'text_resource'.
        If 'doc_id' was passed, store it in 'id_'.
        If 'extra_info' was passed, store it in 'metadata'.
        """
        if "doc_id" in data:
            value = data.pop("doc_id")
            if "id_" in data:
                msg = "'doc_id' is deprecated and 'id_' will be used instead"
                logging.warning(msg)
            else:
                data["id_"] = value

        if "extra_info" in data:
            value = data.pop("extra_info")
            if "metadata" in data:
                msg = "'extra_info' is deprecated and 'metadata' will be used instead"
                logging.warning(msg)
            else:
                data["metadata"] = value

        if data.get("text"):
            text = data.pop("text")
            if "text_resource" in data:
                text_resource = (
                    data["text_resource"]
                    if isinstance(data["text_resource"], MediaResource)
                    else MediaResource.model_validate(data["text_resource"])
                )
                if (text_resource.text or "").strip() != text.strip():
                    msg = (
                        "'text' is deprecated and 'text_resource' will be used instead"
                    )
                    logging.warning(msg)
            else:
                data["text_resource"] = MediaResource(text=text)

        super().__init__(**data)

    @model_serializer(mode="wrap")
    def custom_model_dump(
        self, handler: SerializerFunctionWrapHandler, info: SerializationInfo
    ) -> Dict[str, Any]:
"""For full backward compatibility with the text field, we customize the model serializer."""
        data = super().custom_model_dump(handler, info)
        exclude_set = set(info.exclude or [])
        if "text" not in exclude_set:
            data["text"] = self.text
        return data

    @property
    def text(self) -> str:
"""Provided for backward compatibility, it returns the content of text_resource."""
        return self.get_content()

    @classmethod
    def get_type(cls) -> str:
"""Get Document type."""
        return ObjectType.DOCUMENT

    @property
    def doc_id(self) -> str:
"""Get document ID."""
        return self.id_

    @doc_id.setter
    def doc_id(self, id_: str) -> None:
        self.id_ = id_

    def __str__(self) -> str:
        source_text_truncated = truncate_text(
            self.get_content().strip(), TRUNCATE_LENGTH
        )
        source_text_wrapped = textwrap.fill(
            f"Text: {source_text_truncated}\n", width=WRAP_WIDTH
        )
        return f"Doc ID: {self.doc_id}\n{source_text_wrapped}"

    @deprecated(
        version="0.12.2",
        reason="'get_doc_id' is deprecated, access the 'id_' property instead.",
    )
    def get_doc_id(self) -> str:  # pragma: nocover
        return self.id_

    def to_langchain_format(self) -> LCDocument:
"""Convert struct to LangChain document format."""
        from llama_index.core.bridge.langchain import (
            Document as LCDocument,  # type: ignore
        )

        metadata = self.metadata or {}
        return LCDocument(page_content=self.text, metadata=metadata, id=self.id_)

    @classmethod
    def from_langchain_format(cls, doc: LCDocument) -> Document:
"""Convert struct from LangChain document format."""
        if doc.id:
            return cls(text=doc.page_content, metadata=doc.metadata, id_=doc.id)
        return cls(text=doc.page_content, metadata=doc.metadata)

    def to_haystack_format(self) -> HaystackDocument:
"""Convert struct to Haystack document format."""
        from haystack import Document as HaystackDocument  # type: ignore

        return HaystackDocument(
            content=self.text, meta=self.metadata, embedding=self.embedding, id=self.id_
        )

    @classmethod
    def from_haystack_format(cls, doc: HaystackDocument) -> Document:
"""Convert struct from Haystack document format."""
        return cls(
            text=doc.content, metadata=doc.meta, embedding=doc.embedding, id_=doc.id
        )

    def to_embedchain_format(self) -> Dict[str, Any]:
"""Convert struct to EmbedChain document format."""
        return {
            "doc_id": self.id_,
            "data": {"content": self.text, "meta_data": self.metadata},
        }

    @classmethod
    def from_embedchain_format(cls, doc: Dict[str, Any]) -> Document:
"""Convert struct from EmbedChain document format."""
        return cls(
            text=doc["data"]["content"],
            metadata=doc["data"]["meta_data"],
            id_=doc["doc_id"],
        )

    def to_semantic_kernel_format(self) -> MemoryRecord:
"""Convert struct to Semantic Kernel document format."""
        import numpy as np
        from semantic_kernel.memory.memory_record import MemoryRecord  # type: ignore

        return MemoryRecord(
            id=self.id_,
            text=self.text,
            additional_metadata=self.get_metadata_str(),
            embedding=np.array(self.embedding) if self.embedding else None,
        )

    @classmethod
    def from_semantic_kernel_format(cls, doc: MemoryRecord) -> Document:
"""Convert struct from Semantic Kernel document format."""
        return cls(
            text=doc._text,
            metadata={"additional_metadata": doc._additional_metadata},
            embedding=doc._embedding.tolist() if doc._embedding is not None else None,
            id_=doc._id,
        )

    def to_vectorflow(self, client: Any) -> None:
"""Send a document to vectorflow, since they don't have a document object."""
        # write document to temp file
        import tempfile

        with tempfile.NamedTemporaryFile() as f:
            f.write(self.text.encode("utf-8"))
            f.flush()
            client.embed(f.name)

    @classmethod
    def example(cls) -> Document:
        return Document(
            text=SAMPLE_TEXT,
            metadata={"filename": "README.md", "category": "codebase"},
        )

    @classmethod
    def class_name(cls) -> str:
        return "Document"

    def to_cloud_document(self) -> CloudDocument:
"""Convert to LlamaCloud document type."""
        from llama_cloud.types.cloud_document import CloudDocument  # type: ignore

        return CloudDocument(
            text=self.text,
            metadata=self.metadata,
            excluded_embed_metadata_keys=self.excluded_embed_metadata_keys,
            excluded_llm_metadata_keys=self.excluded_llm_metadata_keys,
            id=self.id_,
        )

    @classmethod
    def from_cloud_document(
        cls,
        doc: CloudDocument,
    ) -> Document:
"""Convert from LlamaCloud document type."""
        return Document(
            text=doc.text,
            metadata=doc.metadata,
            excluded_embed_metadata_keys=doc.excluded_embed_metadata_keys,
            excluded_llm_metadata_keys=doc.excluded_llm_metadata_keys,
            id_=doc.id,
        )

```
  
---|---  
###  text `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Document.text "Permanent link")
```
text: 

```

Provided for backward compatibility, it returns the content of text_resource.
###  doc_id `property` `writable` [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Document.doc_id "Permanent link")
```
doc_id: 

```

Get document ID.
###  custom_model_dump [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Document.custom_model_dump "Permanent link")
```
custom_model_dump(handler: SerializerFunctionWrapHandler, info: SerializationInfo) -> [, ]

```

For full backward compatibility with the text field, we customize the model serializer.
Source code in `llama_index/core/schema.py`
```
1061
1062
1063
1064
1065
1066
1067
1068
1069
1070
```
| ```
@model_serializer(mode="wrap")
def custom_model_dump(
    self, handler: SerializerFunctionWrapHandler, info: SerializationInfo
) -> Dict[str, Any]:
"""For full backward compatibility with the text field, we customize the model serializer."""
    data = super().custom_model_dump(handler, info)
    exclude_set = set(info.exclude or [])
    if "text" not in exclude_set:
        data["text"] = self.text
    return data

```
  
---|---  
###  get_type `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Document.get_type "Permanent link")
```
get_type() -> 

```

Get Document type.
Source code in `llama_index/core/schema.py`
```
1077
1078
1079
1080
```
| ```
@classmethod
def get_type(cls) -> str:
"""Get Document type."""
    return ObjectType.DOCUMENT

```
  
---|---  
###  to_langchain_format [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Document.to_langchain_format "Permanent link")
```
to_langchain_format() -> Document

```

Convert struct to LangChain document format.
Source code in `llama_index/core/schema.py`
```
1107
1108
1109
1110
1111
1112
1113
1114
```
| ```
def to_langchain_format(self) -> LCDocument:
"""Convert struct to LangChain document format."""
    from llama_index.core.bridge.langchain import (
        Document as LCDocument,  # type: ignore
    )

    metadata = self.metadata or {}
    return LCDocument(page_content=self.text, metadata=metadata, id=self.id_)

```
  
---|---  
###  from_langchain_format `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Document.from_langchain_format "Permanent link")
```
from_langchain_format(doc: Document) -> 

```

Convert struct from LangChain document format.
Source code in `llama_index/core/schema.py`
```
1116
1117
1118
1119
1120
1121
```
| ```
@classmethod
def from_langchain_format(cls, doc: LCDocument) -> Document:
"""Convert struct from LangChain document format."""
    if doc.id:
        return cls(text=doc.page_content, metadata=doc.metadata, id_=doc.id)
    return cls(text=doc.page_content, metadata=doc.metadata)

```
  
---|---  
###  to_haystack_format [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Document.to_haystack_format "Permanent link")
```
to_haystack_format() -> Document

```

Convert struct to Haystack document format.
Source code in `llama_index/core/schema.py`
```
1123
1124
1125
1126
1127
1128
1129
```
| ```
def to_haystack_format(self) -> HaystackDocument:
"""Convert struct to Haystack document format."""
    from haystack import Document as HaystackDocument  # type: ignore

    return HaystackDocument(
        content=self.text, meta=self.metadata, embedding=self.embedding, id=self.id_
    )

```
  
---|---  
###  from_haystack_format `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Document.from_haystack_format "Permanent link")
```
from_haystack_format(doc: Document) -> 

```

Convert struct from Haystack document format.
Source code in `llama_index/core/schema.py`
```
1131
1132
1133
1134
1135
1136
```
| ```
@classmethod
def from_haystack_format(cls, doc: HaystackDocument) -> Document:
"""Convert struct from Haystack document format."""
    return cls(
        text=doc.content, metadata=doc.meta, embedding=doc.embedding, id_=doc.id
    )

```
  
---|---  
###  to_embedchain_format [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Document.to_embedchain_format "Permanent link")
```
to_embedchain_format() -> [, ]

```

Convert struct to EmbedChain document format.
Source code in `llama_index/core/schema.py`
```
1138
1139
1140
1141
1142
1143
```
| ```
def to_embedchain_format(self) -> Dict[str, Any]:
"""Convert struct to EmbedChain document format."""
    return {
        "doc_id": self.id_,
        "data": {"content": self.text, "meta_data": self.metadata},
    }

```
  
---|---  
###  from_embedchain_format `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Document.from_embedchain_format "Permanent link")
```
from_embedchain_format(doc: [, ]) -> 

```

Convert struct from EmbedChain document format.
Source code in `llama_index/core/schema.py`
```
1145
1146
1147
1148
1149
1150
1151
1152
```
| ```
@classmethod
def from_embedchain_format(cls, doc: Dict[str, Any]) -> Document:
"""Convert struct from EmbedChain document format."""
    return cls(
        text=doc["data"]["content"],
        metadata=doc["data"]["meta_data"],
        id_=doc["doc_id"],
    )

```
  
---|---  
###  to_semantic_kernel_format [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Document.to_semantic_kernel_format "Permanent link")
```
to_semantic_kernel_format() -> MemoryRecord

```

Convert struct to Semantic Kernel document format.
Source code in `llama_index/core/schema.py`
```
1154
1155
1156
1157
1158
1159
1160
1161
1162
1163
1164
```
| ```
def to_semantic_kernel_format(self) -> MemoryRecord:
"""Convert struct to Semantic Kernel document format."""
    import numpy as np
    from semantic_kernel.memory.memory_record import MemoryRecord  # type: ignore

    return MemoryRecord(
        id=self.id_,
        text=self.text,
        additional_metadata=self.get_metadata_str(),
        embedding=np.array(self.embedding) if self.embedding else None,
    )

```
  
---|---  
###  from_semantic_kernel_format `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Document.from_semantic_kernel_format "Permanent link")
```
from_semantic_kernel_format(doc: MemoryRecord) -> 

```

Convert struct from Semantic Kernel document format.
Source code in `llama_index/core/schema.py`
```
1166
1167
1168
1169
1170
1171
1172
1173
1174
```
| ```
@classmethod
def from_semantic_kernel_format(cls, doc: MemoryRecord) -> Document:
"""Convert struct from Semantic Kernel document format."""
    return cls(
        text=doc._text,
        metadata={"additional_metadata": doc._additional_metadata},
        embedding=doc._embedding.tolist() if doc._embedding is not None else None,
        id_=doc._id,
    )

```
  
---|---  
###  to_vectorflow [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Document.to_vectorflow "Permanent link")
```
to_vectorflow(client: ) -> None

```

Send a document to vectorflow, since they don't have a document object.
Source code in `llama_index/core/schema.py`
```
1176
1177
1178
1179
1180
1181
1182
1183
1184
```
| ```
def to_vectorflow(self, client: Any) -> None:
"""Send a document to vectorflow, since they don't have a document object."""
    # write document to temp file
    import tempfile

    with tempfile.NamedTemporaryFile() as f:
        f.write(self.text.encode("utf-8"))
        f.flush()
        client.embed(f.name)

```
  
---|---  
###  to_cloud_document [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Document.to_cloud_document "Permanent link")
```
to_cloud_document() -> CloudDocument

```

Convert to LlamaCloud document type.
Source code in `llama_index/core/schema.py`
```
1197
1198
1199
1200
1201
1202
1203
1204
1205
1206
1207
```
| ```
def to_cloud_document(self) -> CloudDocument:
"""Convert to LlamaCloud document type."""
    from llama_cloud.types.cloud_document import CloudDocument  # type: ignore

    return CloudDocument(
        text=self.text,
        metadata=self.metadata,
        excluded_embed_metadata_keys=self.excluded_embed_metadata_keys,
        excluded_llm_metadata_keys=self.excluded_llm_metadata_keys,
        id=self.id_,
    )

```
  
---|---  
###  from_cloud_document `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Document.from_cloud_document "Permanent link")
```
from_cloud_document(doc: CloudDocument) -> 

```

Convert from LlamaCloud document type.
Source code in `llama_index/core/schema.py`
```
1209
1210
1211
1212
1213
1214
1215
1216
1217
1218
1219
1220
1221
```
| ```
@classmethod
def from_cloud_document(
    cls,
    doc: CloudDocument,
) -> Document:
"""Convert from LlamaCloud document type."""
    return Document(
        text=doc.text,
        metadata=doc.metadata,
        excluded_embed_metadata_keys=doc.excluded_embed_metadata_keys,
        excluded_llm_metadata_keys=doc.excluded_llm_metadata_keys,
        id_=doc.id,
    )

```
  
---|---  
##  ImageDocument [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.ImageDocument "Permanent link")
Bases: 
Backward compatible wrapper around Document containing an image.
Source code in `llama_index/core/schema.py`
```
1245
1246
1247
1248
1249
1250
1251
1252
1253
1254
1255
1256
1257
1258
1259
1260
1261
1262
1263
1264
1265
1266
1267
1268
1269
1270
1271
1272
1273
1274
1275
1276
1277
1278
1279
1280
1281
1282
1283
1284
1285
1286
1287
1288
1289
1290
1291
1292
1293
1294
1295
1296
1297
1298
1299
1300
1301
1302
1303
1304
1305
1306
1307
1308
1309
1310
1311
1312
1313
1314
1315
1316
1317
1318
1319
1320
1321
1322
1323
1324
1325
1326
1327
1328
1329
1330
1331
1332
1333
1334
1335
1336
1337
1338
1339
1340
1341
1342
1343
1344
1345
1346
1347
1348
1349
1350
1351
1352
1353
1354
1355
1356
1357
1358
1359
1360
```
| ```
class ImageDocument(Document):
"""Backward compatible wrapper around Document containing an image."""

    def __init__(self, **kwargs: Any) -> None:
        image = kwargs.pop("image", None)
        image_path = kwargs.pop("image_path", None)
        image_url = kwargs.pop("image_url", None)
        image_mimetype = kwargs.pop("image_mimetype", None)
        text_embedding = kwargs.pop("text_embedding", None)

        if image:
            kwargs["image_resource"] = MediaResource(
                data=image, mimetype=image_mimetype
            )
        elif image_path:
            if not is_image_pil(image_path):
                raise ValueError("The specified file path is not an accessible image")
            kwargs["image_resource"] = MediaResource(
                path=image_path, mimetype=image_mimetype
            )
        elif image_url:
            if not is_image_url_pil(image_url):
                raise ValueError("The specified URL is not an accessible image")
            kwargs["image_resource"] = MediaResource(
                url=image_url, mimetype=image_mimetype
            )

        super().__init__(**kwargs)

    @property
    def image(self) -> str | None:
        if self.image_resource and self.image_resource.data:
            return self.image_resource.data.decode("utf-8")
        return None

    @image.setter
    def image(self, image: str) -> None:
        self.image_resource = MediaResource(data=image.encode("utf-8"))

    @property
    def image_path(self) -> str | None:
        if self.image_resource and self.image_resource.path:
            return str(self.image_resource.path)
        return None

    @image_path.setter
    def image_path(self, image_path: str) -> None:
        self.image_resource = MediaResource(path=Path(image_path))

    @property
    def image_url(self) -> str | None:
        if self.image_resource and self.image_resource.url:
            return str(self.image_resource.url)
        return None

    @image_url.setter
    def image_url(self, image_url: str) -> None:
        self.image_resource = MediaResource(url=AnyUrl(url=image_url))

    @property
    def image_mimetype(self) -> str | None:
        if self.image_resource:
            return self.image_resource.mimetype
        return None

    @image_mimetype.setter
    def image_mimetype(self, image_mimetype: str) -> None:
        if self.image_resource:
            self.image_resource.mimetype = image_mimetype

    @property
    def text_embedding(self) -> list[float] | None:
        if self.text_resource and self.text_resource.embeddings:
            return self.text_resource.embeddings.get("dense")
        return None

    @text_embedding.setter
    def text_embedding(self, embeddings: list[float]) -> None:
        if self.text_resource:
            if self.text_resource.embeddings is None:
                self.text_resource.embeddings = {}
            self.text_resource.embeddings["dense"] = embeddings

    @classmethod
    def class_name(cls) -> str:
        return "ImageDocument"

    def resolve_image(self, as_base64: bool = False) -> BytesIO:
"""
        Resolve an image such that PIL can read it.

        Args:
            as_base64 (bool): whether the resolved image should be returned as base64-encoded bytes

        """
        if self.image_resource is None:
            return BytesIO()

        if self.image_resource.data is not None:
            if as_base64:
                return BytesIO(self.image_resource.data)
            return BytesIO(base64.b64decode(self.image_resource.data))
        elif self.image_resource.path is not None:
            img_bytes = self.image_resource.path.read_bytes()
            if as_base64:
                return BytesIO(base64.b64encode(img_bytes))
            return BytesIO(img_bytes)
        elif self.image_resource.url is not None:
            # load image from URL
            response = requests.get(str(self.image_resource.url), timeout=(60, 60))
            img_bytes = response.content
            if as_base64:
                return BytesIO(base64.b64encode(img_bytes))
            return BytesIO(img_bytes)
        else:
            raise ValueError("No image found in the chat message!")

```
  
---|---  
###  resolve_image [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.ImageDocument.resolve_image "Permanent link")
```
resolve_image(as_base64:  = False) -> BytesIO

```

Resolve an image such that PIL can read it.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`as_base64` |  `bool` |  whether the resolved image should be returned as base64-encoded bytes |  `False`  
Source code in `llama_index/core/schema.py`
```
1332
1333
1334
1335
1336
1337
1338
1339
1340
1341
1342
1343
1344
1345
1346
1347
1348
1349
1350
1351
1352
1353
1354
1355
1356
1357
1358
1359
1360
```
| ```
def resolve_image(self, as_base64: bool = False) -> BytesIO:
"""
    Resolve an image such that PIL can read it.

    Args:
        as_base64 (bool): whether the resolved image should be returned as base64-encoded bytes

    """
    if self.image_resource is None:
        return BytesIO()

    if self.image_resource.data is not None:
        if as_base64:
            return BytesIO(self.image_resource.data)
        return BytesIO(base64.b64decode(self.image_resource.data))
    elif self.image_resource.path is not None:
        img_bytes = self.image_resource.path.read_bytes()
        if as_base64:
            return BytesIO(base64.b64encode(img_bytes))
        return BytesIO(img_bytes)
    elif self.image_resource.url is not None:
        # load image from URL
        response = requests.get(str(self.image_resource.url), timeout=(60, 60))
        img_bytes = response.content
        if as_base64:
            return BytesIO(base64.b64encode(img_bytes))
        return BytesIO(img_bytes)
    else:
        raise ValueError("No image found in the chat message!")

```
  
---|---  
##  QueryBundle `dataclass` [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.QueryBundle "Permanent link")
Bases: `DataClassJsonMixin`
Query bundle.
This dataclass contains the original query string and associated transformations.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`query_str` |  the original user-specified query string. This is currently used by all non embedding-based queries. |  _required_  
`custom_embedding_strs` |  `list[str]` |  list of strings used for embedding the query. This is currently used by all embedding-based queries. |  `None`  
`embedding` |  `list[float]` |  the stored embedding for the query. |  `None`  
`image_path` |  `None`  
Source code in `llama_index/core/schema.py`
```
1363
1364
1365
1366
1367
1368
1369
1370
1371
1372
1373
1374
1375
1376
1377
1378
1379
1380
1381
1382
1383
1384
1385
1386
1387
1388
1389
1390
1391
1392
1393
1394
1395
1396
1397
1398
1399
1400
1401
1402
1403
1404
```
| ```
@dataclass
class QueryBundle(DataClassJsonMixin):
"""
    Query bundle.

    This dataclass contains the original query string and associated transformations.

    Args:
        query_str (str): the original user-specified query string.
            This is currently used by all non embedding-based queries.
        custom_embedding_strs (list[str]): list of strings used for embedding the query.
            This is currently used by all embedding-based queries.
        embedding (list[float]): the stored embedding for the query.

    """

    query_str: str
    # using single image path as query input
    image_path: Optional[str] = None
    custom_embedding_strs: Optional[List[str]] = None
    embedding: Optional[List[float]] = None

    @property
    def embedding_strs(self) -> List[str]:
"""Use custom embedding strs if specified, otherwise use query str."""
        if self.custom_embedding_strs is None:
            if len(self.query_str) == 0:
                return []
            return [self.query_str]
        else:
            return self.custom_embedding_strs

    @property
    def embedding_image(self) -> List[ImageType]:
"""Use image path for image retrieval."""
        if self.image_path is None:
            return []
        return [self.image_path]

    def __str__(self) -> str:
"""Convert to string representation."""
        return self.query_str

```
  
---|---  
###  embedding_strs `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.QueryBundle.embedding_strs "Permanent link")
```
embedding_strs: []

```

Use custom embedding strs if specified, otherwise use query str.
###  embedding_image `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.QueryBundle.embedding_image "Permanent link")
```
embedding_image: [ImageType]

```

Use image path for image retrieval.
