# Otel
##  LlamaIndexOpenTelemetry [#](https://developers.llamaindex.ai/python/framework-api-reference/observability/otel/#llama_index.observability.otel.LlamaIndexOpenTelemetry "Permanent link")
Bases: `BaseModel`
LlamaIndexOpenTelemetry is a configuration and integration class for OpenTelemetry tracing within LlamaIndex. This class manages the setup and registration of OpenTelemetry span and event handlers, configures the tracer provider, and exports trace data using the specified span exporter and processor. It supports both simple and batch span processors, and allows customization of the service name or resource, as well as the dispatcher name.
Attributes:
Name | Type | Description  
---|---|---  
`span_exporter` |  `Optional[SpanExporter]` |  The OpenTelemetry span exporter. Defaults to ConsoleSpanExporter.  
`span_processor` |  `Literal['simple', 'batch']` |  The span processor type, either 'simple' or 'batch'. Defaults to 'batch'.  
`service_name_or_resource` |  `Union[str, Resource]` |  The service name or OpenTelemetry Resource. Defaults to a Resource with service name 'llamaindex.opentelemetry'.  
Source code in `llama_index/observability/otel/base.py`
```
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
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
```
| ```
class LlamaIndexOpenTelemetry(BaseModel):
"""
    LlamaIndexOpenTelemetry is a configuration and integration class for OpenTelemetry tracing within LlamaIndex.
    This class manages the setup and registration of OpenTelemetry span and event handlers, configures the tracer provider,
    and exports trace data using the specified span exporter and processor. It supports both simple and batch span processors,
    and allows customization of the service name or resource, as well as the dispatcher name.

    Attributes:
        span_exporter (Optional[SpanExporter]): The OpenTelemetry span exporter. Defaults to ConsoleSpanExporter.
        span_processor (Literal["simple", "batch"]): The span processor type, either 'simple' or 'batch'. Defaults to 'batch'.
        service_name_or_resource (Union[str, Resource]): The service name or OpenTelemetry Resource. Defaults to a Resource with service name 'llamaindex.opentelemetry'.

    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    span_exporter: Optional[SpanExporter] = Field(
        default=ConsoleSpanExporter(),
        description="OpenTelemetry span exporter. Supports all SpanExporter-compatible interfaces, defaults to ConsoleSpanExporter.",
    )
    span_processor: Literal["simple", "batch"] = Field(
        default="batch",
        description="OpenTelemetry span processor. Can be either 'batch' (-> BatchSpanProcessor) or 'simple' (-> SimpleSpanProcessor). Defaults to 'batch'",
    )
    service_name_or_resource: Union[str, Resource] = Field(
        default=Resource(attributes={SERVICE_NAME: "llamaindex.opentelemetry"}),
        description="Service name or resource for OpenTelemetry. Defaults to a Resource with 'llamaindex.opentelemetry' as service name.",
    )
    debug: bool = Field(
        default=False,
        description="Debug the start and end of span and the recording of events",
    )
    _tracer: Optional[trace.Tracer] = PrivateAttr(default=None)

    def _start_otel(
        self,
    ) -> None:
        if isinstance(self.service_name_or_resource, str):
            self.service_name_or_resource = Resource(
                attributes={SERVICE_NAME: self.service_name_or_resource}
            )
        tracer_provider = TracerProvider(resource=self.service_name_or_resource)
        if self.span_processor == "simple":
            span_processor = SimpleSpanProcessor(self.span_exporter)
        else:
            span_processor = BatchSpanProcessor(self.span_exporter)
        tracer_provider.add_span_processor(span_processor=span_processor)
        trace.set_tracer_provider(tracer_provider)
        self._tracer = trace.get_tracer("llamaindex.opentelemetry.tracer")

    def start_registering(
        self,
    ) -> None:
"""Starts LlamaIndex instrumentation."""
        self._start_otel()
        dispatcher = instrument.get_dispatcher()
        span_handler = OTelCompatibleSpanHandler(tracer=self._tracer, debug=self.debug)
        dispatcher.add_span_handler(span_handler)
        dispatcher.add_event_handler(
            OTelCompatibleEventHandler(span_handler=span_handler, debug=self.debug)
        )

```
  
---|---  
###  start_registering [#](https://developers.llamaindex.ai/python/framework-api-reference/observability/otel/#llama_index.observability.otel.LlamaIndexOpenTelemetry.start_registering "Permanent link")
```
start_registering() -> None

```

Starts LlamaIndex instrumentation.
Source code in `llama_index/observability/otel/base.py`
```
258
259
260
261
262
263
264
265
266
267
268
```
| ```
def start_registering(
    self,
) -> None:
"""Starts LlamaIndex instrumentation."""
    self._start_otel()
    dispatcher = instrument.get_dispatcher()
    span_handler = OTelCompatibleSpanHandler(tracer=self._tracer, debug=self.debug)
    dispatcher.add_span_handler(span_handler)
    dispatcher.add_event_handler(
        OTelCompatibleEventHandler(span_handler=span_handler, debug=self.debug)
    )

```
  
---|---  
options: members: - LlamaIndexOpenTelemetry
