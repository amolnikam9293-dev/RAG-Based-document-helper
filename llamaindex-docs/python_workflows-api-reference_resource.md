# Resource
Declare a resource to inject into step functions.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`factory` |  `Callable[..., T] | None` |  Function returning the resource instance. May be async. |  _required_  
`cache` |  `bool` |  If True, reuse the produced resource across steps. Defaults to True. |  `True`  
Returns:
Type | Description  
---|---  
`_Resource` |  _Resource[T]: A resource descriptor to be used in `typing.Annotated`.  
Examples:
```
fromtypingimport Annotated
fromworkflows.resourceimport Resource

defget_memory(**kwargs) -> Memory:
    return Memory.from_defaults("user123", token_limit=60000)

classMyWorkflow(Workflow):
    @step
    async deffirst(
        self,
        ev: StartEvent,
        memory: Annotated[Memory, Resource(get_memory)],
    ) -> StopEvent:
        await memory.aput(...)
        return StopEvent(result="ok")

```

Source code in `workflows/resource.py`
```
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
188
189
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
204
```
| ```
defResource(
    factory: Callable[..., T],
    cache: bool = True,
) -> _Resource:
"""Declare a resource to inject into step functions.

    Args:
        factory (Callable[..., T] | None): Function returning the resource instance. May be async.
        cache (bool): If True, reuse the produced resource across steps. Defaults to True.

    Returns:
        _Resource[T]: A resource descriptor to be used in `typing.Annotated`.

    Examples:
        ```python
        from typing import Annotated
        from workflows.resource import Resource

        def get_memory(**kwargs) -> Memory:
            return Memory.from_defaults("user123", token_limit=60000)

        class MyWorkflow(Workflow):
            @step
            async def first(
                self,
                ev: StartEvent,
                memory: Annotated[Memory, Resource(get_memory)],
            ) -> StopEvent:
                await memory.aput(...)
                return StopEvent(result="ok")
        ```
    """
    return _Resource(factory, cache)

```
  
---|---
