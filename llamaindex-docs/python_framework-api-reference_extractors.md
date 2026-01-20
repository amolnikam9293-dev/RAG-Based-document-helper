# Index
Node parser interface.
##  BaseExtractor [#](https://developers.llamaindex.ai/python/framework-api-reference/extractors/#llama_index.core.extractors.interface.BaseExtractor "Permanent link")
Bases: 
Metadata extractor.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`is_text_node_only` |  `bool` |  `True`  
`show_progress` |  `bool` |  Whether to show progress. |  `True`  
`metadata_mode` |  `MetadataMode` |  Metadata mode to use when reading nodes. |  `<MetadataMode.ALL: 'all'>`  
`node_text_template` |  Template to represent how node text is mixed with metadata text. |  `'[Excerpt from document]\n{metadata_str}\nExcerpt:\n-----\n{content}\n-----\n'`  
`disable_template_rewrite` |  `bool` |  Disable the node template rewrite. |  `False`  
`in_place` |  `bool` |  Whether to process nodes in place. |  `True`  
`num_workers` |  Number of workers to use for concurrent async processing.  
Source code in `llama_index/core/extractors/interface.py`
```
 22
 23
 24
 25
 26
 27
 28
 29
 30
 31
 32
 33
 34
 35
 36
 37
 38
 39
 40
 41
 42
 43
 44
 45
 46
 47
 48
 49
 50
 51
 52
 53
 54
 55
 56
 57
 58
 59
 60
 61
 62
 63
 64
 65
 66
 67
 68
 69
 70
 71
 72
 73
 74
 75
 76
 77
 78
 79
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
```
| ```
class BaseExtractor(TransformComponent):
"""Metadata extractor."""

    is_text_node_only: bool = True

    show_progress: bool = Field(default=True, description="Whether to show progress.")

    metadata_mode: MetadataMode = Field(
        default=MetadataMode.ALL, description="Metadata mode to use when reading nodes."
    )

    node_text_template: str = Field(
        default=DEFAULT_NODE_TEXT_TEMPLATE,
        description="Template to represent how node text is mixed with metadata text.",
    )
    disable_template_rewrite: bool = Field(
        default=False, description="Disable the node template rewrite."
    )

    in_place: bool = Field(
        default=True, description="Whether to process nodes in place."
    )

    num_workers: int = Field(
        default=4,
        description="Number of workers to use for concurrent async processing.",
    )

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs: Any) -> Self:  # type: ignore
        if isinstance(kwargs, dict):
            data.update(kwargs)

        data.pop("class_name", None)

        llm_predictor = data.get("llm_predictor")
        if llm_predictor:
            from llama_index.core.llm_predictor.loading import load_predictor

            llm_predictor = load_predictor(llm_predictor)
            data["llm_predictor"] = llm_predictor

        llm = data.get("llm")
        if llm:
            from llama_index.core.llms.loading import load_llm

            llm = load_llm(llm)
            data["llm"] = llm

        return cls(**data)

    @classmethod
    def class_name(cls) -> str:
"""Get class name."""
        return "MetadataExtractor"

    @abstractmethod
    async def aextract(self, nodes: Sequence[BaseNode]) -> List[Dict]:
"""
        Extracts metadata for a sequence of nodes, returning a list of
        metadata dictionaries corresponding to each node.

        Args:
            nodes (Sequence[Document]): nodes to extract metadata from

        """

    def extract(self, nodes: Sequence[BaseNode]) -> List[Dict]:
"""
        Extracts metadata for a sequence of nodes, returning a list of
        metadata dictionaries corresponding to each node.

        Args:
            nodes (Sequence[Document]): nodes to extract metadata from

        """
        return asyncio_run(self.aextract(nodes))

    async def aprocess_nodes(
        self,
        nodes: Sequence[BaseNode],
        excluded_embed_metadata_keys: Optional[List[str]] = None,
        excluded_llm_metadata_keys: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> List[BaseNode]:
"""
        Post process nodes parsed from documents.

        Allows extractors to be chained.

        Args:
            nodes (List[BaseNode]): nodes to post-process
            excluded_embed_metadata_keys (Optional[List[str]]):
                keys to exclude from embed metadata
            excluded_llm_metadata_keys (Optional[List[str]]):
                keys to exclude from llm metadata

        """
        if self.in_place:
            new_nodes = nodes
        else:
            new_nodes = [deepcopy(node) for node in nodes]

        cur_metadata_list = await self.aextract(new_nodes)
        for idx, node in enumerate(new_nodes):
            node.metadata.update(cur_metadata_list[idx])

        for idx, node in enumerate(new_nodes):
            if excluded_embed_metadata_keys is not None:
                node.excluded_embed_metadata_keys.extend(excluded_embed_metadata_keys)
            if excluded_llm_metadata_keys is not None:
                node.excluded_llm_metadata_keys.extend(excluded_llm_metadata_keys)
            if not self.disable_template_rewrite:
                if isinstance(node, TextNode):
                    cast(TextNode, node).text_template = self.node_text_template

        return new_nodes  # type: ignore

    def process_nodes(
        self,
        nodes: Sequence[BaseNode],
        excluded_embed_metadata_keys: Optional[List[str]] = None,
        excluded_llm_metadata_keys: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> List[BaseNode]:
        return asyncio_run(
            self.aprocess_nodes(
                nodes,
                excluded_embed_metadata_keys=excluded_embed_metadata_keys,
                excluded_llm_metadata_keys=excluded_llm_metadata_keys,
                **kwargs,
            )
        )

    def __call__(self, nodes: Sequence[BaseNode], **kwargs: Any) -> List[BaseNode]:
"""
        Post process nodes parsed from documents.

        Allows extractors to be chained.

        Args:
            nodes (List[BaseNode]): nodes to post-process

        """
        return self.process_nodes(nodes, **kwargs)

    async def acall(self, nodes: Sequence[BaseNode], **kwargs: Any) -> List[BaseNode]:
"""
        Post process nodes parsed from documents.

        Allows extractors to be chained.

        Args:
            nodes (List[BaseNode]): nodes to post-process

        """
        return await self.aprocess_nodes(nodes, **kwargs)

```
  
---|---  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/extractors/#llama_index.core.extractors.interface.BaseExtractor.class_name "Permanent link")
```
class_name() -> 

```

Get class name.
Source code in `llama_index/core/extractors/interface.py`
```
73
74
75
76
```
| ```
@classmethod
def class_name(cls) -> str:
"""Get class name."""
    return "MetadataExtractor"

```
  
---|---  
###  aextract `abstractmethod` `async` [#](https://developers.llamaindex.ai/python/framework-api-reference/extractors/#llama_index.core.extractors.interface.BaseExtractor.aextract "Permanent link")
```
aextract(nodes: Sequence[]) -> []

```

Extracts metadata for a sequence of nodes, returning a list of metadata dictionaries corresponding to each node.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`nodes` |  `Sequence[Document[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Document "llama_index.core.schema.Document")]` |  nodes to extract metadata from |  _required_  
Source code in `llama_index/core/extractors/interface.py`
```
78
79
80
81
82
83
84
85
86
87
```
| ```
@abstractmethod
async def aextract(self, nodes: Sequence[BaseNode]) -> List[Dict]:
"""
    Extracts metadata for a sequence of nodes, returning a list of
    metadata dictionaries corresponding to each node.

    Args:
        nodes (Sequence[Document]): nodes to extract metadata from

    """

```
  
---|---  
###  extract [#](https://developers.llamaindex.ai/python/framework-api-reference/extractors/#llama_index.core.extractors.interface.BaseExtractor.extract "Permanent link")
```
extract(nodes: Sequence[]) -> []

```

Extracts metadata for a sequence of nodes, returning a list of metadata dictionaries corresponding to each node.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`nodes` |  `Sequence[Document[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Document "llama_index.core.schema.Document")]` |  nodes to extract metadata from |  _required_  
Source code in `llama_index/core/extractors/interface.py`
```
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
```
| ```
def extract(self, nodes: Sequence[BaseNode]) -> List[Dict]:
"""
    Extracts metadata for a sequence of nodes, returning a list of
    metadata dictionaries corresponding to each node.

    Args:
        nodes (Sequence[Document]): nodes to extract metadata from

    """
    return asyncio_run(self.aextract(nodes))

```
  
---|---  
###  aprocess_nodes `async` [#](https://developers.llamaindex.ai/python/framework-api-reference/extractors/#llama_index.core.extractors.interface.BaseExtractor.aprocess_nodes "Permanent link")
```
aprocess_nodes(nodes: Sequence[], excluded_embed_metadata_keys: Optional[[]] = None, excluded_llm_metadata_keys: Optional[[]] = None, **kwargs: ) -> []

```

Post process nodes parsed from documents.
Allows extractors to be chained.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`nodes` |  `List[BaseNode[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.BaseNode "llama_index.core.schema.BaseNode")]` |  nodes to post-process |  _required_  
`excluded_embed_metadata_keys` |  `Optional[List[str]]` |  keys to exclude from embed metadata |  `None`  
`excluded_llm_metadata_keys` |  `Optional[List[str]]` |  keys to exclude from llm metadata |  `None`  
Source code in `llama_index/core/extractors/interface.py`
```
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
```
| ```
async def aprocess_nodes(
    self,
    nodes: Sequence[BaseNode],
    excluded_embed_metadata_keys: Optional[List[str]] = None,
    excluded_llm_metadata_keys: Optional[List[str]] = None,
    **kwargs: Any,
) -> List[BaseNode]:
"""
    Post process nodes parsed from documents.

    Allows extractors to be chained.

    Args:
        nodes (List[BaseNode]): nodes to post-process
        excluded_embed_metadata_keys (Optional[List[str]]):
            keys to exclude from embed metadata
        excluded_llm_metadata_keys (Optional[List[str]]):
            keys to exclude from llm metadata

    """
    if self.in_place:
        new_nodes = nodes
    else:
        new_nodes = [deepcopy(node) for node in nodes]

    cur_metadata_list = await self.aextract(new_nodes)
    for idx, node in enumerate(new_nodes):
        node.metadata.update(cur_metadata_list[idx])

    for idx, node in enumerate(new_nodes):
        if excluded_embed_metadata_keys is not None:
            node.excluded_embed_metadata_keys.extend(excluded_embed_metadata_keys)
        if excluded_llm_metadata_keys is not None:
            node.excluded_llm_metadata_keys.extend(excluded_llm_metadata_keys)
        if not self.disable_template_rewrite:
            if isinstance(node, TextNode):
                cast(TextNode, node).text_template = self.node_text_template

    return new_nodes  # type: ignore

```
  
---|---  
###  acall `async` [#](https://developers.llamaindex.ai/python/framework-api-reference/extractors/#llama_index.core.extractors.interface.BaseExtractor.acall "Permanent link")
```
acall(nodes: Sequence[], **kwargs: ) -> []

```

Post process nodes parsed from documents.
Allows extractors to be chained.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`nodes` |  `List[BaseNode[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.BaseNode "llama_index.core.schema.BaseNode")]` |  nodes to post-process |  _required_  
Source code in `llama_index/core/extractors/interface.py`
```
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
```
| ```
async def acall(self, nodes: Sequence[BaseNode], **kwargs: Any) -> List[BaseNode]:
"""
    Post process nodes parsed from documents.

    Allows extractors to be chained.

    Args:
        nodes (List[BaseNode]): nodes to post-process

    """
    return await self.aprocess_nodes(nodes, **kwargs)

```
  
---|---  
options: members: - BaseExtractor
