# Context
##  Context [#](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.Context "Permanent link")
Bases: `Generic[MODEL_T]`
Global, per-run context for a `Workflow`. Provides an interface into the underlying broker run, for both external (workflow run oberservers) and internal consumption by workflow steps.
The `Context` coordinates event delivery between steps, tracks in-flight work, exposes a global state store, and provides utilities for streaming and synchronization. It is created by a `Workflow` at run time and can be persisted and restored.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`workflow` |  |  The owning workflow instance. Used to infer step configuration and instrumentation. |  _required_  
`previous_context` |  `dict[str, Any] | None` |  A previous context snapshot to resume from. |  `None`  
`serializer` |  `BaseSerializer[](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.serializers.BaseSerializer "BaseSerializer \(workflows.context.serializers.BaseSerializer\)") | None` |  A serializer to use for serializing and deserializing the current and previous context snapshots. |  `None`  
Attributes:
Name | Type | Description  
---|---|---  
|  `bool` |  Whether the workflow is currently running.  
|  `InMemoryStateStore[](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.state_store.InMemoryStateStore "InMemoryStateStore \(workflows.context.state_store.InMemoryStateStore\)")[MODEL_T]` |  Type-safe, async state store shared across steps. See also [InMemoryStateStore](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.state_store.InMemoryStateStore "InMemoryStateStore").  
Examples:
Basic usage inside a step:
```
fromworkflowsimport step
fromworkflows.eventsimport StartEvent, StopEvent

@step
async defstart(self, ctx: Context, ev: StartEvent) -> StopEvent:
    await ctx.store.set("query", ev.topic)
    ctx.write_event_to_stream(ev)  # surface progress to UI
    return StopEvent(result="ok")

```

Persisting the state of a workflow across runs:
```
fromworkflowsimport Context

# Create a context and run the workflow with the same context
ctx = Context(my_workflow)
result_1 = await my_workflow.run(..., ctx=ctx)
result_2 = await my_workflow.run(..., ctx=ctx)

# Serialize the context and restore it
ctx_dict = ctx.to_dict()
restored_ctx = Context.from_dict(my_workflow, ctx_dict)
result_3 = await my_workflow.run(..., ctx=restored_ctx)

```

See Also

Source code in `workflows/context/context.py`
```
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
205
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
482
483
484
485
486
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
```
| ```
classContext(Generic[MODEL_T]):
"""
    Global, per-run context for a `Workflow`. Provides an interface into the
    underlying broker run, for both external (workflow run oberservers) and
    internal consumption by workflow steps.

    The `Context` coordinates event delivery between steps, tracks in-flight work,
    exposes a global state store, and provides utilities for streaming and
    synchronization. It is created by a `Workflow` at run time and can be
    persisted and restored.

    Args:
        workflow (Workflow): The owning workflow instance. Used to infer
            step configuration and instrumentation.
        previous_context: A previous context snapshot to resume from.
        serializer: A serializer to use for serializing and deserializing the current and previous context snapshots.

    Attributes:
        is_running (bool): Whether the workflow is currently running.
        store (InMemoryStateStore[MODEL_T]): Type-safe, async state store shared
            across steps. See also
            [InMemoryStateStore][workflows.context.state_store.InMemoryStateStore].

    Examples:
        Basic usage inside a step:

        ```python
        from workflows import step
        from workflows.events import StartEvent, StopEvent

        @step
        async def start(self, ctx: Context, ev: StartEvent) -> StopEvent:
            await ctx.store.set("query", ev.topic)
            ctx.write_event_to_stream(ev)  # surface progress to UI
            return StopEvent(result="ok")
        ```

        Persisting the state of a workflow across runs:

        ```python
        from workflows import Context

        # Create a context and run the workflow with the same context
        ctx = Context(my_workflow)
        result_1 = await my_workflow.run(..., ctx=ctx)
        result_2 = await my_workflow.run(..., ctx=ctx)

        # Serialize the context and restore it
        ctx_dict = ctx.to_dict()
        restored_ctx = Context.from_dict(my_workflow, ctx_dict)
        result_3 = await my_workflow.run(..., ctx=restored_ctx)
        ```


    See Also:
        - [Workflow][workflows.Workflow]
        - [Event][workflows.events.Event]
        - [InMemoryStateStore][workflows.context.state_store.InMemoryStateStore]
    """

    # These keys are set by pre-built workflows and
    # are known to be unserializable in some cases.
    known_unserializable_keys = ("memory",)

    # Backing state store; serialized as `state`
    _state_store: InMemoryStateStore[MODEL_T]
    _broker_run: WorkflowBroker[MODEL_T] | None
    _plugin: Plugin
    _workflow: Workflow

    def__init__(
        self,
        workflow: Workflow,
        previous_context: dict[str, Any] | None = None,
        serializer: BaseSerializer | None = None,
        plugin: Plugin = basic_runtime,
    ) -> None:
        self._serializer = serializer or JsonSerializer()
        self._broker_run = None
        self._plugin = plugin
        self._workflow = workflow

        # parse the serialized context
        serializer = serializer or JsonSerializer()
        if previous_context is not None:
            try:
                # Auto-detect and convert V0 to V1 if needed
                previous_context_parsed = SerializedContext.from_dict_auto(
                    previous_context
                )
                # validate it fully parses synchronously to avoid delayed validation errors
                BrokerState.from_serialized(
                    previous_context_parsed, workflow, serializer
                )
            except ValidationError as e:
                raise ContextSerdeError(
                    f"Context dict specified in an invalid format: {e}"
                ) frome
        else:
            previous_context_parsed = SerializedContext()

        self._init_snapshot = previous_context_parsed

        # initialization of the state store is a bit complex, due to inferring and validating its type from the
        # provided workflow context args

        state_types: set[Type[BaseModel]] = set()
        for _, step_func in workflow._get_steps().items():
            step_config: StepConfig = step_func._step_config
            if (
                step_config.context_state_type is not None
                and step_config.context_state_type != DictState
                and issubclass(step_config.context_state_type, BaseModel)
            ):
                state_type = step_config.context_state_type
                state_types.add(state_type)

        if len(state_types)  1:
            raise ValueError(
                "Multiple state types are not supported. Make sure that each Context[...] has the same generic state type. Found: "
                + ", ".join([state_type.__name__ for state_type in state_types])
            )
        state_type = state_types.pop() if state_types else DictState
        if previous_context_parsed.state:
            # perhaps offer a way to clear on invalid
            store_state = InMemoryStateStore.from_dict(
                previous_context_parsed.state, serializer
            )
            if store_state.state_type != state_type:
                raise ValueError(
                    f"State type mismatch. Workflow context expected {state_type.__name__}, got {store_state.state_type.__name__}"
                )
            self._state_store = cast(InMemoryStateStore[MODEL_T], store_state)
        else:
            try:
                state_instance = cast(MODEL_T, state_type())
                self._state_store = InMemoryStateStore(state_instance)
            except Exception as e:
                raise WorkflowRuntimeError(
                    f"Failed to initialize state of type {state_type}. Does your state define defaults for all fields? Original error:\n{e}"
                ) frome

    @property
    defis_running(self) -> bool:
"""Whether the workflow is currently running."""
        if self._broker_run is None:
            return self._init_snapshot.is_running
        else:
            return self._broker_run.is_running

    def_init_broker(
        self, workflow: Workflow, plugin: WorkflowRuntime | None = None
    ) -> WorkflowBroker[MODEL_T]:
        if self._broker_run is not None:
            raise WorkflowRuntimeError("Broker already initialized")
        # Initialize a runtime plugin (asyncio-based by default)
        runtime: WorkflowRuntime = plugin or self._plugin.new_runtime(str(uuid.uuid4()))
        # Initialize the new broker implementation (broker2)
        broker: WorkflowBroker[MODEL_T] = WorkflowBroker(
            workflow=workflow,
            context=cast("Context[MODEL_T]", self),
            runtime=runtime,
            plugin=self._plugin,
        )
        self._broker_run = broker
        return broker

    def_workflow_run(
        self,
        workflow: Workflow,
        start_event: StartEvent | None = None,
        semaphore: asyncio.Semaphore | None = None,
    ) -> WorkflowHandler:
"""
        called by package internally from the workflow to run it
        """
        prev_broker: WorkflowBroker[MODEL_T] | None = None
        if self._broker_run is not None:
            prev_broker = self._broker_run
            self._broker_run = None

        self._broker_run = self._init_broker(workflow)

        async defbefore_start() -> None:
            if prev_broker is not None:
                try:
                    await prev_broker.shutdown()
                except Exception:
                    pass
            if semaphore is not None:
                await semaphore.acquire()

        async defafter_complete() -> None:
            if semaphore is not None:
                semaphore.release()

        state = BrokerState.from_serialized(
            self._init_snapshot, workflow, self._serializer
        )
        return self._broker_run.start(
            workflow=workflow,
            previous=state,
            start_event=start_event,
            before_start=before_start,
            after_complete=after_complete,
        )

    def_workflow_cancel_run(self) -> None:
"""
        Called internally from the handler to cancel a context's run
        """
        self._running_broker.cancel_run()

    @property
    def_running_broker(self) -> WorkflowBroker[MODEL_T]:
        if self._broker_run is None:
            raise WorkflowRuntimeError(
                "Workflow run is not yet running. Make sure to only call this method after the context has been passed to a workflow.run call."
            )
        return self._broker_run

    @property
    defstore(self) -> InMemoryStateStore[MODEL_T]:
"""Typed, process-local state store shared across steps.

        If no state was initialized yet, a default
        [DictState][workflows.context.state_store.DictState] store is created.

        Returns:
            InMemoryStateStore[MODEL_T]: The state store instance.
        """
        return self._state_store

    defto_dict(self, serializer: BaseSerializer | None = None) -> dict[str, Any]:
"""Serialize the context to a JSON-serializable dict.

        Persists the global state store, event queues, buffers, accepted events,
        broker log, and running flag. This payload can be fed to
        [from_dict][workflows.context.context.Context.from_dict] to resume a run
        or carry state across runs.

        Args:
            serializer (BaseSerializer | None): Value serializer used for state
                and event payloads. Defaults to
                [JsonSerializer][workflows.context.serializers.JsonSerializer].

        Returns:
            dict[str, Any]: A dict suitable for JSON encoding and later
            restoration via `from_dict`.

        See Also:
            - [InMemoryStateStore.to_dict][workflows.context.state_store.InMemoryStateStore.to_dict]

        Examples:
            ```python
            ctx_dict = ctx.to_dict()
            my_db.set("key", json.dumps(ctx_dict))

            ctx_dict = my_db.get("key")
            restored_ctx = Context.from_dict(my_workflow, json.loads(ctx_dict))
            result = await my_workflow.run(..., ctx=restored_ctx)

        """
        serializer = serializer or self._serializer

        # Serialize state using the state manager's method
        state_data = {}
        if self._state_store is not None:
            state_data = self._state_store.to_dict(serializer)

        # Get the broker state - either from the running broker or from the init snapshot
        if self._broker_run is not None:
            broker_state = self._broker_run._state
        else:
            # Deserialize the init snapshot to get a BrokerState, then re-serialize it
            # This ensures we always output the current format
            broker_state = BrokerState.from_serialized(
                self._init_snapshot, self._workflow, serializer
            )

        context = broker_state.to_serialized(serializer)
        context.state = state_data
        # mode="python" to support pickling over json if one so chooses. This should perhaps be moved into the serializers
        return context.model_dump(mode="python")

    @classmethod
    deffrom_dict(
        cls,
        workflow: "Workflow",
        data: dict[str, Any],
        serializer: BaseSerializer | None = None,
    ) -> "Context[MODEL_T]":
"""Reconstruct a `Context` from a serialized payload.

        Args:
            workflow (Workflow): The workflow instance that will own this
                context.
            data (dict[str, Any]): Payload produced by
                [to_dict][workflows.context.context.Context.to_dict].
            serializer (BaseSerializer | None): Serializer used to decode state
                and events. Defaults to JSON.

        Returns:
            Context[MODEL_T]: A context instance initialized with the persisted
                state and queues.

        Raises:
            ContextSerdeError: If the payload is missing required fields or is
                in an incompatible format.

        Examples:
            ```python
            ctx_dict = ctx.to_dict()
            my_db.set("key", json.dumps(ctx_dict))

            ctx_dict = my_db.get("key")
            restored_ctx = Context.from_dict(my_workflow, json.loads(ctx_dict))
            result = await my_workflow.run(..., ctx=restored_ctx)

        """
        try:
            return cls(workflow, previous_context=data, serializer=serializer)
        except KeyError as e:
            msg = "Error creating a Context instance: the provided payload has a wrong or old format."
            raise ContextSerdeError(msg) frome

    async defrunning_steps(self) -> list[str]:
"""Return the list of currently running step names.

        Returns:
            list[str]: Names of steps that have at least one active worker.
        """
        return await self._running_broker.running_steps()

    defcollect_events(
        self, ev: Event, expected: list[Type[Event]], buffer_id: str | None = None
    ) -> list[Event] | None:
"""
        Buffer events until all expected types are available, then return them.

        This utility is helpful when a step can receive multiple event types
        and needs to proceed only when it has a full set. The returned list is
        ordered according to `expected`.

        Args:
            ev (Event): The incoming event to add to the buffer.
            expected (list[Type[Event]]): Event types to collect, in order.
            buffer_id (str | None): Optional stable key to isolate buffers across
                steps or workers. Defaults to an internal key derived from the
                task name or expected types.

        Returns:
            list[Event] | None: The events in the requested order when complete,
            otherwise `None`.

        Examples:
            ```python
            @step
            async def synthesize(
                self, ctx: Context, ev: QueryEvent | RetrieveEvent
            ) -> StopEvent | None:
                events = ctx.collect_events(ev, [QueryEvent, RetrieveEvent])
                if events is None:
                    return None
                query_ev, retrieve_ev = events
                # ... proceed with both inputs present ...


        See Also:
            - [Event][workflows.events.Event]
        """
        return self._running_broker.collect_events(ev, expected, buffer_id)

    defsend_event(self, message: Event, step: str | None = None) -> None:
"""Dispatch an event to one or all workflow steps.

        If `step` is omitted, the event is broadcast to all step queues and
        non-matching steps will ignore it. When `step` is provided, the target
        step must accept the event type or a
        [WorkflowRuntimeError][workflows.errors.WorkflowRuntimeError] is raised.

        Args:
            message (Event): The event to enqueue.
            step (str | None): Optional step name to target.

        Raises:
            WorkflowRuntimeError: If the target step does not exist or does not
                accept the event type.

        Examples:
            It's common to use this method to fan-out events:

            ```python
            @step
            async def my_step(self, ctx: Context, ev: StartEvent) -> WorkerEvent | GatherEvent:
                for i in range(10):
                    ctx.send_event(WorkerEvent(msg=i))
                return GatherEvent()


            You also see this method used from the caller side to send events into the workflow:

            ```python
            handler = my_workflow.run(...)
            async for ev in handler.stream_events():
                if isinstance(ev, SomeEvent):
                    handler.ctx.send_event(SomeOtherEvent(msg="Hello!"))

            result = await handler

        """
        return self._running_broker.send_event(message, step)

    async defwait_for_event(
        self,
        event_type: Type[T],
        waiter_event: Event | None = None,
        waiter_id: str | None = None,
        requirements: dict[str, Any] | None = None,
        timeout: float | None = 2000,
    ) -> T:
"""Wait for the next matching event of type `event_type`.

        The runtime pauses by throwing an internal control-flow exception and replays
        the entire step when the event arrives, so keep this call near the top of the
        step and make any preceding work safe to repeat.

        Optionally emits a `waiter_event` to the event stream once per `waiter_id` to
        inform callers that the workflow is waiting for external input.
        This helps to prevent duplicate waiter events from being sent to the event stream.

        Args:
            event_type (type[T]): Concrete event class to wait for.
            waiter_event (Event | None): Optional event to write to the stream
                once when the wait begins.
            waiter_id (str | None): Stable identifier to avoid emitting multiple
                waiter events for the same logical wait.
            requirements (dict[str, Any] | None): Key/value filters that must be
                satisfied by the event via `event.get(key) == value`.
            timeout (float | None): Max seconds to wait. `None` means no
                timeout. Defaults to 2000 seconds.

        Returns:
            T: The received event instance of the requested type.

        Raises:
            asyncio.TimeoutError: If the timeout elapses.

        Examples:
            ```python
            @step
            async def my_step(self, ctx: Context, ev: StartEvent) -> StopEvent:
                response = await ctx.wait_for_event(
                    HumanResponseEvent,
                    waiter_event=InputRequiredEvent(msg="What's your name?"),
                    waiter_id="user_name",
                    timeout=60,

                return StopEvent(result=response.response)

        """
        return await self._running_broker.wait_for_event(
            event_type, waiter_event, waiter_id, requirements, timeout
        )

    defwrite_event_to_stream(self, ev: Event | None) -> None:
"""Enqueue an event for streaming to [WorkflowHandler]](workflows.handler.WorkflowHandler).

        Args:
            ev (Event | None): The event to stream. `None` can be used as a
                sentinel in some streaming modes.

        Examples:
            ```python
            @step
            async def my_step(self, ctx: Context, ev: StartEvent) -> StopEvent:
                ctx.write_event_to_stream(ev)
                return StopEvent(result="ok")

        """
        self._running_broker.write_event_to_stream(ev)

    defget_result(self) -> RunResultT:
"""Return the final result of the workflow run.

        Deprecated:
            This method is deprecated and will be removed in a future release.
            Prefer awaiting the handler returned by `Workflow.run`, e.g.:
            `result = await workflow.run(..., ctx=ctx)`.

        Examples:
            ```python
            # Preferred
            result = await my_workflow.run(..., ctx=ctx)

            # Deprecated
            result_agent = ctx.get_result()


        Returns:
            RunResultT: The value provided via a `StopEvent`.
        """
        _warn_get_result()
        if self._running_broker._handler is None:
            raise WorkflowRuntimeError("Workflow handler is not set")
        return self._running_broker._handler.result()

    defstream_events(self) -> AsyncGenerator[Event, None]:
"""The internal queue used for streaming events to callers."""
        return self._running_broker.stream_published_events()

    @property
    defstreaming_queue(self) -> asyncio.Queue:
"""Deprecated queue-based event stream.

        Returns an asyncio.Queue that is populated by iterating this context's
        stream_events(). A deprecation warning is emitted once per process.
        """
        _warn_streaming_queue()
        q: asyncio.Queue[Event] = asyncio.Queue()

        async def_pump() -> None:
            async for ev in self.stream_events():
                await q.put(ev)
                if isinstance(ev, StopEvent):
                    break

        try:
            asyncio.create_task(_pump())
        except RuntimeError:
            loop = asyncio.get_event_loop()
            loop.create_task(_pump())
        return q

```
  
---|---  
###  is_running `property` [#](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.Context.is_running "Permanent link")
```
is_running: 

```

Whether the workflow is currently running.
###  store `property` [#](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.Context.store "Permanent link")
```
store: [MODEL_T]

```

Typed, process-local state store shared across steps.
If no state was initialized yet, a default [DictState](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.state_store.DictState "DictState") store is created.
Returns:
Type | Description  
---|---  
`InMemoryStateStore[](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.state_store.InMemoryStateStore "InMemoryStateStore \(workflows.context.state_store.InMemoryStateStore\)")[MODEL_T]` |  InMemoryStateStore[MODEL_T]: The state store instance.  
###  collect_events [#](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.Context.collect_events "Permanent link")
```
collect_events(ev: , expected: [[]], buffer_id:  | None = None) -> [] | None

```

Buffer events until all expected types are available, then return them.
This utility is helpful when a step can receive multiple event types and needs to proceed only when it has a full set. The returned list is ordered according to `expected`.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
|  The incoming event to add to the buffer. |  _required_  
`expected` |  `list[Type[Event[](https://developers.llamaindex.ai/python/workflows-api-reference/events/#workflows.events.Event "Event \(workflows.events.Event\)")]]` |  Event types to collect, in order. |  _required_  
`buffer_id` |  `str | None` |  Optional stable key to isolate buffers across steps or workers. Defaults to an internal key derived from the task name or expected types. |  `None`  
Returns:
Type | Description  
---|---  
`list[Event[](https://developers.llamaindex.ai/python/workflows-api-reference/events/#workflows.events.Event "Event \(workflows.events.Event\)")] | None` |  list[Event] | None: The events in the requested order when complete,  
`list[Event[](https://developers.llamaindex.ai/python/workflows-api-reference/events/#workflows.events.Event "Event \(workflows.events.Event\)")] | None` |  otherwise `None`.  
Examples:
```
@step
async defsynthesize(
    self, ctx: Context, ev: QueryEvent | RetrieveEvent
) -> StopEvent | None:
    events = ctx.collect_events(ev, [QueryEvent, RetrieveEvent])
    if events is None:
        return None
    query_ev, retrieve_ev = events
    # ... proceed with both inputs present ...

```

See Also

Source code in `workflows/context/context.py`
```
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
```
| ```
defcollect_events(
    self, ev: Event, expected: list[Type[Event]], buffer_id: str | None = None
) -> list[Event] | None:
"""
    Buffer events until all expected types are available, then return them.

    This utility is helpful when a step can receive multiple event types
    and needs to proceed only when it has a full set. The returned list is
    ordered according to `expected`.

    Args:
        ev (Event): The incoming event to add to the buffer.
        expected (list[Type[Event]]): Event types to collect, in order.
        buffer_id (str | None): Optional stable key to isolate buffers across
            steps or workers. Defaults to an internal key derived from the
            task name or expected types.

    Returns:
        list[Event] | None: The events in the requested order when complete,
        otherwise `None`.

    Examples:
        ```python
        @step
        async def synthesize(
            self, ctx: Context, ev: QueryEvent | RetrieveEvent
        ) -> StopEvent | None:
            events = ctx.collect_events(ev, [QueryEvent, RetrieveEvent])
            if events is None:
                return None
            query_ev, retrieve_ev = events
            # ... proceed with both inputs present ...
        ```

    See Also:
        - [Event][workflows.events.Event]
    """
    return self._running_broker.collect_events(ev, expected, buffer_id)

```
  
---|---  
###  from_dict `classmethod` [#](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.Context.from_dict "Permanent link")
```
from_dict(workflow: 'Workflow', data: [, ], serializer:  | None = None) -> 'Context[MODEL_T]'

```

Reconstruct a `Context` from a serialized payload.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`workflow` |  |  The workflow instance that will own this context. |  _required_  
`data` |  `dict[str, Any]` |  Payload produced by [to_dict](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.Context.to_dict "to_dict"). |  _required_  
`serializer` |  `BaseSerializer[](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.serializers.BaseSerializer "BaseSerializer \(workflows.context.serializers.BaseSerializer\)") | None` |  Serializer used to decode state and events. Defaults to JSON. |  `None`  
Returns:
Type | Description  
---|---  
`'Context[MODEL_T]'` |  Context[MODEL_T]: A context instance initialized with the persisted state and queues.  
Raises:
Type | Description  
---|---  
|  If the payload is missing required fields or is in an incompatible format.  
Examples:
```
ctx_dict = ctx.to_dict()
my_db.set("key", json.dumps(ctx_dict))

ctx_dict = my_db.get("key")
restored_ctx = Context.from_dict(my_workflow, json.loads(ctx_dict))
result = await my_workflow.run(..., ctx=restored_ctx)

```

Source code in `workflows/context/context.py`
```
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
```
| ```
@classmethod
deffrom_dict(
    cls,
    workflow: "Workflow",
    data: dict[str, Any],
    serializer: BaseSerializer | None = None,
) -> "Context[MODEL_T]":
"""Reconstruct a `Context` from a serialized payload.

    Args:
        workflow (Workflow): The workflow instance that will own this
            context.
        data (dict[str, Any]): Payload produced by
            [to_dict][workflows.context.context.Context.to_dict].
        serializer (BaseSerializer | None): Serializer used to decode state
            and events. Defaults to JSON.

    Returns:
        Context[MODEL_T]: A context instance initialized with the persisted
            state and queues.

    Raises:
        ContextSerdeError: If the payload is missing required fields or is
            in an incompatible format.

    Examples:
        ```python
        ctx_dict = ctx.to_dict()
        my_db.set("key", json.dumps(ctx_dict))

        ctx_dict = my_db.get("key")
        restored_ctx = Context.from_dict(my_workflow, json.loads(ctx_dict))
        result = await my_workflow.run(..., ctx=restored_ctx)
        ```
    """
    try:
        return cls(workflow, previous_context=data, serializer=serializer)
    except KeyError as e:
        msg = "Error creating a Context instance: the provided payload has a wrong or old format."
        raise ContextSerdeError(msg) frome

```
  
---|---  
###  get_result [#](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.Context.get_result "Permanent link")
```
get_result() -> RunResultT

```

Return the final result of the workflow run.
Deprecated
This method is deprecated and will be removed in a future release. Prefer awaiting the handler returned by `Workflow.run`, e.g.: `result = await workflow.run(..., ctx=ctx)`.
Examples:
```
# Preferred
result = await my_workflow.run(..., ctx=ctx)

# Deprecated
result_agent = ctx.get_result()

```

Returns:
Name | Type | Description  
---|---|---  
`RunResultT` |  `RunResultT` |  The value provided via a `StopEvent`.  
Source code in `workflows/context/context.py`
```
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
```
| ```
defget_result(self) -> RunResultT:
"""Return the final result of the workflow run.

    Deprecated:
        This method is deprecated and will be removed in a future release.
        Prefer awaiting the handler returned by `Workflow.run`, e.g.:
        `result = await workflow.run(..., ctx=ctx)`.

    Examples:
        ```python
        # Preferred
        result = await my_workflow.run(..., ctx=ctx)

        # Deprecated
        result_agent = ctx.get_result()
        ```

    Returns:
        RunResultT: The value provided via a `StopEvent`.
    """
    _warn_get_result()
    if self._running_broker._handler is None:
        raise WorkflowRuntimeError("Workflow handler is not set")
    return self._running_broker._handler.result()

```
  
---|---  
###  send_event [#](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.Context.send_event "Permanent link")
```
send_event(message: , step:  | None = None) -> None

```

Dispatch an event to one or all workflow steps.
If `step` is omitted, the event is broadcast to all step queues and non-matching steps will ignore it. When `step` is provided, the target step must accept the event type or a [WorkflowRuntimeError](https://developers.llamaindex.ai/python/workflows-api-reference/errors/#workflows.errors.WorkflowRuntimeError "WorkflowRuntimeError") is raised.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`message` |  |  The event to enqueue. |  _required_  
`step` |  `str | None` |  Optional step name to target. |  `None`  
Raises:
Type | Description  
---|---  
|  If the target step does not exist or does not accept the event type.  
Examples:
It's common to use this method to fan-out events:
```
@step
async defmy_step(self, ctx: Context, ev: StartEvent) -> WorkerEvent | GatherEvent:
    for i in range(10):
        ctx.send_event(WorkerEvent(msg=i))
    return GatherEvent()

```

You also see this method used from the caller side to send events into the workflow:
```
handler = my_workflow.run(...)
async for ev in handler.stream_events():
    if isinstance(ev, SomeEvent):
        handler.ctx.send_event(SomeOtherEvent(msg="Hello!"))

result = await handler

```

Source code in `workflows/context/context.py`
```
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
```
| ```
defsend_event(self, message: Event, step: str | None = None) -> None:
"""Dispatch an event to one or all workflow steps.

    If `step` is omitted, the event is broadcast to all step queues and
    non-matching steps will ignore it. When `step` is provided, the target
    step must accept the event type or a
    [WorkflowRuntimeError][workflows.errors.WorkflowRuntimeError] is raised.

    Args:
        message (Event): The event to enqueue.
        step (str | None): Optional step name to target.

    Raises:
        WorkflowRuntimeError: If the target step does not exist or does not
            accept the event type.

    Examples:
        It's common to use this method to fan-out events:

        ```python
        @step
        async def my_step(self, ctx: Context, ev: StartEvent) -> WorkerEvent | GatherEvent:
            for i in range(10):
                ctx.send_event(WorkerEvent(msg=i))
            return GatherEvent()
        ```

        You also see this method used from the caller side to send events into the workflow:

        ```python
        handler = my_workflow.run(...)
        async for ev in handler.stream_events():
            if isinstance(ev, SomeEvent):
                handler.ctx.send_event(SomeOtherEvent(msg="Hello!"))

        result = await handler
        ```
    """
    return self._running_broker.send_event(message, step)

```
  
---|---  
###  to_dict [#](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.Context.to_dict "Permanent link")
```
to_dict(serializer:  | None = None) -> [, ]

```

Serialize the context to a JSON-serializable dict.
Persists the global state store, event queues, buffers, accepted events, broker log, and running flag. This payload can be fed to [from_dict](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.Context.from_dict "from_dict


  
      classmethod
  ") to resume a run or carry state across runs.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`serializer` |  `BaseSerializer[](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.serializers.BaseSerializer "BaseSerializer \(workflows.context.serializers.BaseSerializer\)") | None` |  Value serializer used for state and event payloads. Defaults to [JsonSerializer](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.serializers.JsonSerializer "JsonSerializer"). |  `None`  
Returns:
Type | Description  
---|---  
`dict[str, Any]` |  dict[str, Any]: A dict suitable for JSON encoding and later  
`dict[str, Any]` |  restoration via `from_dict`.  
See Also
  * [InMemoryStateStore.to_dict](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.state_store.InMemoryStateStore.to_dict "to_dict")


Examples:
```
ctx_dict = ctx.to_dict()
my_db.set("key", json.dumps(ctx_dict))

ctx_dict = my_db.get("key")
restored_ctx = Context.from_dict(my_workflow, json.loads(ctx_dict))
result = await my_workflow.run(..., ctx=restored_ctx)

```

Source code in `workflows/context/context.py`
```
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
```
| ```
defto_dict(self, serializer: BaseSerializer | None = None) -> dict[str, Any]:
"""Serialize the context to a JSON-serializable dict.

    Persists the global state store, event queues, buffers, accepted events,
    broker log, and running flag. This payload can be fed to
    [from_dict][workflows.context.context.Context.from_dict] to resume a run
    or carry state across runs.

    Args:
        serializer (BaseSerializer | None): Value serializer used for state
            and event payloads. Defaults to
            [JsonSerializer][workflows.context.serializers.JsonSerializer].

    Returns:
        dict[str, Any]: A dict suitable for JSON encoding and later
        restoration via `from_dict`.

    See Also:
        - [InMemoryStateStore.to_dict][workflows.context.state_store.InMemoryStateStore.to_dict]

    Examples:
        ```python
        ctx_dict = ctx.to_dict()
        my_db.set("key", json.dumps(ctx_dict))

        ctx_dict = my_db.get("key")
        restored_ctx = Context.from_dict(my_workflow, json.loads(ctx_dict))
        result = await my_workflow.run(..., ctx=restored_ctx)
        ```
    """
    serializer = serializer or self._serializer

    # Serialize state using the state manager's method
    state_data = {}
    if self._state_store is not None:
        state_data = self._state_store.to_dict(serializer)

    # Get the broker state - either from the running broker or from the init snapshot
    if self._broker_run is not None:
        broker_state = self._broker_run._state
    else:
        # Deserialize the init snapshot to get a BrokerState, then re-serialize it
        # This ensures we always output the current format
        broker_state = BrokerState.from_serialized(
            self._init_snapshot, self._workflow, serializer
        )

    context = broker_state.to_serialized(serializer)
    context.state = state_data
    # mode="python" to support pickling over json if one so chooses. This should perhaps be moved into the serializers
    return context.model_dump(mode="python")

```
  
---|---  
###  wait_for_event `async` [#](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.Context.wait_for_event "Permanent link")
```
wait_for_event(event_type: [], waiter_event:  | None = None, waiter_id:  | None = None, requirements: [, ] | None = None, timeout: float | None = 2000) -> 

```

Wait for the next matching event of type `event_type`.
The runtime pauses by throwing an internal control-flow exception and replays the entire step when the event arrives, so keep this call near the top of the step and make any preceding work safe to repeat.
Optionally emits a `waiter_event` to the event stream once per `waiter_id` to inform callers that the workflow is waiting for external input. This helps to prevent duplicate waiter events from being sent to the event stream.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`event_type` |  `type[T]` |  Concrete event class to wait for. |  _required_  
`waiter_event` |  `Event[](https://developers.llamaindex.ai/python/workflows-api-reference/events/#workflows.events.Event "Event \(workflows.events.Event\)") | None` |  Optional event to write to the stream once when the wait begins. |  `None`  
`waiter_id` |  `str | None` |  Stable identifier to avoid emitting multiple waiter events for the same logical wait. |  `None`  
`requirements` |  `dict[str, Any] | None` |  Key/value filters that must be satisfied by the event via `event.get(key) == value`. |  `None`  
`timeout` |  `float | None` |  Max seconds to wait. `None` means no timeout. Defaults to 2000 seconds. |  `2000`  
Returns:
Name | Type | Description  
---|---|---  
The received event instance of the requested type.  
Raises:
Type | Description  
---|---  
`TimeoutError` |  If the timeout elapses.  
Examples:
```
@step
async defmy_step(self, ctx: Context, ev: StartEvent) -> StopEvent:
    response = await ctx.wait_for_event(
        HumanResponseEvent,
        waiter_event=InputRequiredEvent(msg="What's your name?"),
        waiter_id="user_name",
        timeout=60,
    )
    return StopEvent(result=response.response)

```

Source code in `workflows/context/context.py`
```
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
482
483
484
485
486
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
```
| ```
async defwait_for_event(
    self,
    event_type: Type[T],
    waiter_event: Event | None = None,
    waiter_id: str | None = None,
    requirements: dict[str, Any] | None = None,
    timeout: float | None = 2000,
) -> T:
"""Wait for the next matching event of type `event_type`.

    The runtime pauses by throwing an internal control-flow exception and replays
    the entire step when the event arrives, so keep this call near the top of the
    step and make any preceding work safe to repeat.

    Optionally emits a `waiter_event` to the event stream once per `waiter_id` to
    inform callers that the workflow is waiting for external input.
    This helps to prevent duplicate waiter events from being sent to the event stream.

    Args:
        event_type (type[T]): Concrete event class to wait for.
        waiter_event (Event | None): Optional event to write to the stream
            once when the wait begins.
        waiter_id (str | None): Stable identifier to avoid emitting multiple
            waiter events for the same logical wait.
        requirements (dict[str, Any] | None): Key/value filters that must be
            satisfied by the event via `event.get(key) == value`.
        timeout (float | None): Max seconds to wait. `None` means no
            timeout. Defaults to 2000 seconds.

    Returns:
        T: The received event instance of the requested type.

    Raises:
        asyncio.TimeoutError: If the timeout elapses.

    Examples:
        ```python
        @step
        async def my_step(self, ctx: Context, ev: StartEvent) -> StopEvent:
            response = await ctx.wait_for_event(
                HumanResponseEvent,
                waiter_event=InputRequiredEvent(msg="What's your name?"),
                waiter_id="user_name",
                timeout=60,

            return StopEvent(result=response.response)
        ```
    """
    return await self._running_broker.wait_for_event(
        event_type, waiter_event, waiter_id, requirements, timeout
    )

```
  
---|---  
###  write_event_to_stream [#](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.Context.write_event_to_stream "Permanent link")
```
write_event_to_stream(ev:  | None) -> None

```

Enqueue an event for streaming to [WorkflowHandler]](workflows.handler.WorkflowHandler).
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`Event[](https://developers.llamaindex.ai/python/workflows-api-reference/events/#workflows.events.Event "Event \(workflows.events.Event\)") | None` |  The event to stream. `None` can be used as a sentinel in some streaming modes. |  _required_  
Examples:
```
@step
async defmy_step(self, ctx: Context, ev: StartEvent) -> StopEvent:
    ctx.write_event_to_stream(ev)
    return StopEvent(result="ok")

```

Source code in `workflows/context/context.py`
```
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
```
| ```
defwrite_event_to_stream(self, ev: Event | None) -> None:
"""Enqueue an event for streaming to [WorkflowHandler]](workflows.handler.WorkflowHandler).

    Args:
        ev (Event | None): The event to stream. `None` can be used as a
            sentinel in some streaming modes.

    Examples:
        ```python
        @step
        async def my_step(self, ctx: Context, ev: StartEvent) -> StopEvent:
            ctx.write_event_to_stream(ev)
            return StopEvent(result="ok")
        ```
    """
    self._running_broker.write_event_to_stream(ev)

```
  
---|---  
##  DictState [#](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.state_store.DictState "Permanent link")
Bases: `DictLikeModel`
Dynamic, dict-like Pydantic model for workflow state.
Used as the default state model when no typed state is provided. Behaves like a mapping while retaining Pydantic validation and serialization.
Examples:
```
fromworkflows.context.state_storeimport DictState

state = DictState()
state["foo"] = 1
state.bar = 2  # attribute-style access works for nested structures

```

See Also

Source code in `workflows/context/state_store.py`
```
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
```
| ```
classDictState(DictLikeModel):
"""
    Dynamic, dict-like Pydantic model for workflow state.

    Used as the default state model when no typed state is provided. Behaves
    like a mapping while retaining Pydantic validation and serialization.

    Examples:
        ```python
        from workflows.context.state_store import DictState

        state = DictState()
        state["foo"] = 1
        state.bar = 2  # attribute-style access works for nested structures
        ```

    See Also:
        - [InMemoryStateStore][workflows.context.state_store.InMemoryStateStore]
    """

    def__init__(self, **params: Any):
        super().__init__(**params)

```
  
---|---  
##  InMemoryStateStore [#](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.state_store.InMemoryStateStore "Permanent link")
Bases: `Generic[MODEL_T]`
Async, in-memory, type-safe state manager for workflows.
This store holds a single Pydantic model instance representing global workflow state. When the generic parameter is omitted, it defaults to [DictState](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.state_store.DictState "DictState") for flexible, dictionary-like usage.
Thread-safety is ensured with an internal `asyncio.Lock`. Consumers can either perform atomic reads/writes via `get_state` and `set_state`, or make in-place, transactional edits via the `edit_state` context manager.
Examples:
Typed state model:
```
frompydanticimport BaseModel
fromworkflows.context.state_storeimport InMemoryStateStore

classMyState(BaseModel):
    count: int = 0

store = InMemoryStateStore(MyState())
async with store.edit_state() as state:
    state.count += 1

```

Dynamic state with `DictState`:
```
fromworkflows.context.state_storeimport InMemoryStateStore, DictState

store = InMemoryStateStore(DictState())
await store.set("user.profile.name", "Ada")
name = await store.get("user.profile.name")

```

See Also

Source code in `workflows/context/state_store.py`
```
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
205
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
```
| ```
classInMemoryStateStore(Generic[MODEL_T]):
"""
    Async, in-memory, type-safe state manager for workflows.

    This store holds a single Pydantic model instance representing global
    workflow state. When the generic parameter is omitted, it defaults to
    [DictState][workflows.context.state_store.DictState] for flexible,
    dictionary-like usage.

    Thread-safety is ensured with an internal `asyncio.Lock`. Consumers can
    either perform atomic reads/writes via `get_state` and `set_state`, or make
    in-place, transactional edits via the `edit_state` context manager.

    Examples:
        Typed state model:

        ```python
        from pydantic import BaseModel
        from workflows.context.state_store import InMemoryStateStore

        class MyState(BaseModel):
            count: int = 0

        store = InMemoryStateStore(MyState())
        async with store.edit_state() as state:
            state.count += 1
        ```

        Dynamic state with `DictState`:

        ```python
        from workflows.context.state_store import InMemoryStateStore, DictState

        store = InMemoryStateStore(DictState())
        await store.set("user.profile.name", "Ada")
        name = await store.get("user.profile.name")
        ```

    See Also:
        - [Context.store][workflows.context.context.Context.store]
    """

    # These keys are set by pre-built workflows and
    # are known to be unserializable in some cases.
    known_unserializable_keys = ("memory",)

    state_type: Type[MODEL_T]

    def__init__(self, initial_state: MODEL_T):
        self._state = initial_state
        self._lock = asyncio.Lock()
        self.state_type = type(initial_state)

    async defget_state(self) -> MODEL_T:
"""Return a shallow copy of the current state model.

        Returns:
            MODEL_T: A `.model_copy()` of the internal Pydantic model.
        """
        return self._state.model_copy()

    async defset_state(self, state: MODEL_T) -> None:
"""Replace the current state model.

        Args:
            state (MODEL_T): New state of the same type as the existing model.

        Raises:
            ValueError: If the type differs from the existing state type.
        """
        if not isinstance(state, type(self._state)):
            raise ValueError(f"State must be of type {type(self._state)}")

        async with self._lock:
            self._state = state

    defto_dict(self, serializer: "BaseSerializer") -> dict[str, Any]:
"""Serialize the state and model metadata for persistence.

        For `DictState`, each individual item is serialized using the provided
        serializer since values can be arbitrary Python objects. For other
        Pydantic models, defers to the serializer (e.g. JSON) which can leverage
        model-aware encoding.

        Args:
            serializer (BaseSerializer): Strategy used to encode values.

        Returns:
            dict[str, Any]: A payload suitable for
            [from_dict][workflows.context.state_store.InMemoryStateStore.from_dict].
        """
        # Special handling for DictState - serialize each item in _data
        if isinstance(self._state, DictState):
            serialized_data = {}
            for key, value in self._state.items():
                try:
                    serialized_data[key] = serializer.serialize(value)
                except Exception as e:
                    if key in self.known_unserializable_keys:
                        warnings.warn(
                            f"Skipping serialization of known unserializable key: {key} -- "
                            "This is expected but will require this item to be set manually after deserialization.",
                            category=UnserializableKeyWarning,
                        )
                        continue
                    raise ValueError(
                        f"Failed to serialize state value for key {key}: {e}"
                    )

            return {
                "state_data": {"_data": serialized_data},
                "state_type": type(self._state).__name__,
                "state_module": type(self._state).__module__,
            }
        else:
            # For regular Pydantic models, rely on pydantic's serialization
            serialized_state = serializer.serialize(self._state)

            return {
                "state_data": serialized_state,
                "state_type": type(self._state).__name__,
                "state_module": type(self._state).__module__,
            }

    @classmethod
    deffrom_dict(
        cls, serialized_state: dict[str, Any], serializer: "BaseSerializer"
    ) -> "InMemoryStateStore[MODEL_T]":
"""Restore a state store from a serialized payload.

        Args:
            serialized_state (dict[str, Any]): The payload produced by
                [to_dict][workflows.context.state_store.InMemoryStateStore.to_dict].
            serializer (BaseSerializer): Strategy to decode stored values.

        Returns:
            InMemoryStateStore[MODEL_T]: A store with the reconstructed model.
        """
        if not serialized_state:
            # Return a default DictState manager
            return cls(DictState())  # type: ignore

        state_data = serialized_state.get("state_data", {})
        state_type = serialized_state.get("state_type", "DictState")

        # Deserialize the state data
        if state_type == "DictState":
            # Special handling for DictState - deserialize each item in _data
            _data_serialized = state_data.get("_data", {})
            deserialized_data = {}
            for key, value in _data_serialized.items():
                try:
                    deserialized_data[key] = serializer.deserialize(value)
                except Exception as e:
                    raise ValueError(
                        f"Failed to deserialize state value for key {key}: {e}"
                    )

            state_instance = DictState(_data=deserialized_data)
        else:
            state_instance = serializer.deserialize(state_data)

        return cls(state_instance)  # type: ignore

    @asynccontextmanager
    async defedit_state(self) -> AsyncGenerator[MODEL_T, None]:
"""Edit state transactionally under a lock.

        Yields the mutable model and writes it back on exit. This pattern avoids
        read-modify-write races and keeps updates atomic.

        Yields:
            MODEL_T: The current state model for in-place mutation.
        """
        async with self._lock:
            state = self._state

            yield state

            self._state = state

    async defget(self, path: str, default: Optional[Any] = Ellipsis) -> Any:
"""Get a nested value using dot-separated paths.

        Supports dict keys, list indices, and attribute access transparently at
        each segment.

        Args:
            path (str): Dot-separated path, e.g. "user.profile.name".
            default (Any): If provided, return this when the path does not
                exist; otherwise, raise `ValueError`.

        Returns:
            Any: The resolved value.

        Raises:
            ValueError: If the path is invalid and no default is provided or if
                the path depth exceeds limits.
        """
        segments = path.split(".") if path else []
        if len(segments)  MAX_DEPTH:
            raise ValueError(f"Path length exceeds {MAX_DEPTH} segments")

        async with self._lock:
            try:
                value: Any = self._state
                for segment in segments:
                    value = self._traverse_step(value, segment)
            except Exception:
                if default is not Ellipsis:
                    return default

                msg = f"Path '{path}' not found in state"
                raise ValueError(msg)

        return value

    async defset(self, path: str, value: Any) -> None:
"""Set a nested value using dot-separated paths.

        Intermediate containers are created as needed. Dicts, lists, tuples, and
        Pydantic models are supported where appropriate.

        Args:
            path (str): Dot-separated path to write.
            value (Any): Value to assign.

        Raises:
            ValueError: If the path is empty or exceeds the maximum depth.
        """
        if not path:
            raise ValueError("Path cannot be empty")

        segments = path.split(".")
        if len(segments)  MAX_DEPTH:
            raise ValueError(f"Path length exceeds {MAX_DEPTH} segments")

        async with self._lock:
            current = self._state

            # Navigate/create intermediate segments
            for segment in segments[:-1]:
                try:
                    current = self._traverse_step(current, segment)
                except (KeyError, AttributeError, IndexError, TypeError):
                    # Create intermediate object and assign it
                    intermediate: Any = {}
                    self._assign_step(current, segment, intermediate)
                    current = intermediate

            # Assign the final value
            self._assign_step(current, segments[-1], value)

    async defclear(self) -> None:
"""Reset the state to its type defaults.

        Raises:
            ValueError: If the model type cannot be instantiated from defaults
                (i.e., fields missing default values).
        """
        try:
            await self.set_state(self._state.__class__())
        except ValidationError:
            raise ValueError("State must have defaults for all fields")

    def_traverse_step(self, obj: Any, segment: str) -> Any:
"""Follow one segment into *obj* (dict key, list index, or attribute)."""
        if isinstance(obj, dict):
            return obj[segment]

        # attempt list/tuple index
        try:
            idx = int(segment)
            return obj[idx]
        except (ValueError, TypeError, IndexError):
            pass

        # fallback to attribute access (Pydantic models, normal objects)
        return getattr(obj, segment)

    def_assign_step(self, obj: Any, segment: str, value: Any) -> None:
"""Assign *value* to *segment* of *obj* (dict key, list index, or attribute)."""
        if isinstance(obj, dict):
            obj[segment] = value
            return

        # attempt list/tuple index assignment
        try:
            idx = int(segment)
            obj[idx] = value
            return
        except (ValueError, TypeError, IndexError):
            pass

        # fallback to attribute assignment
        setattr(obj, segment, value)

```
  
---|---  
###  get_state `async` [#](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.state_store.InMemoryStateStore.get_state "Permanent link")
```
get_state() -> MODEL_T

```

Return a shallow copy of the current state model.
Returns:
Name | Type | Description  
---|---|---  
`MODEL_T` |  `MODEL_T` |  A `.model_copy()` of the internal Pydantic model.  
Source code in `workflows/context/state_store.py`
```
105
106
107
108
109
110
111
```
| ```
async defget_state(self) -> MODEL_T:
"""Return a shallow copy of the current state model.

    Returns:
        MODEL_T: A `.model_copy()` of the internal Pydantic model.
    """
    return self._state.model_copy()

```
  
---|---  
###  set_state `async` [#](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.state_store.InMemoryStateStore.set_state "Permanent link")
```
set_state(state: MODEL_T) -> None

```

Replace the current state model.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`state` |  `MODEL_T` |  New state of the same type as the existing model. |  _required_  
Raises:
Type | Description  
---|---  
`ValueError` |  If the type differs from the existing state type.  
Source code in `workflows/context/state_store.py`
```
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
```
| ```
async defset_state(self, state: MODEL_T) -> None:
"""Replace the current state model.

    Args:
        state (MODEL_T): New state of the same type as the existing model.

    Raises:
        ValueError: If the type differs from the existing state type.
    """
    if not isinstance(state, type(self._state)):
        raise ValueError(f"State must be of type {type(self._state)}")

    async with self._lock:
        self._state = state

```
  
---|---  
###  to_dict [#](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.state_store.InMemoryStateStore.to_dict "Permanent link")
```
to_dict(serializer: ) -> [, ]

```

Serialize the state and model metadata for persistence.
For `DictState`, each individual item is serialized using the provided serializer since values can be arbitrary Python objects. For other Pydantic models, defers to the serializer (e.g. JSON) which can leverage model-aware encoding.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`serializer` |  |  Strategy used to encode values. |  _required_  
Returns:
Type | Description  
---|---  
`dict[str, Any]` |  dict[str, Any]: A payload suitable for  
`dict[str, Any]` |   
Source code in `workflows/context/state_store.py`
```
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
```
| ```
defto_dict(self, serializer: "BaseSerializer") -> dict[str, Any]:
"""Serialize the state and model metadata for persistence.

    For `DictState`, each individual item is serialized using the provided
    serializer since values can be arbitrary Python objects. For other
    Pydantic models, defers to the serializer (e.g. JSON) which can leverage
    model-aware encoding.

    Args:
        serializer (BaseSerializer): Strategy used to encode values.

    Returns:
        dict[str, Any]: A payload suitable for
        [from_dict][workflows.context.state_store.InMemoryStateStore.from_dict].
    """
    # Special handling for DictState - serialize each item in _data
    if isinstance(self._state, DictState):
        serialized_data = {}
        for key, value in self._state.items():
            try:
                serialized_data[key] = serializer.serialize(value)
            except Exception as e:
                if key in self.known_unserializable_keys:
                    warnings.warn(
                        f"Skipping serialization of known unserializable key: {key} -- "
                        "This is expected but will require this item to be set manually after deserialization.",
                        category=UnserializableKeyWarning,
                    )
                    continue
                raise ValueError(
                    f"Failed to serialize state value for key {key}: {e}"
                )

        return {
            "state_data": {"_data": serialized_data},
            "state_type": type(self._state).__name__,
            "state_module": type(self._state).__module__,
        }
    else:
        # For regular Pydantic models, rely on pydantic's serialization
        serialized_state = serializer.serialize(self._state)

        return {
            "state_data": serialized_state,
            "state_type": type(self._state).__name__,
            "state_module": type(self._state).__module__,
        }

```
  
---|---  
###  from_dict `classmethod` [#](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.state_store.InMemoryStateStore.from_dict "Permanent link")
```
from_dict(serialized_state: [, ], serializer: ) -> [MODEL_T]

```

Restore a state store from a serialized payload.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`serialized_state` |  `dict[str, Any]` |  The payload produced by [to_dict](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.state_store.InMemoryStateStore.to_dict "to_dict"). |  _required_  
`serializer` |  |  Strategy to decode stored values. |  _required_  
Returns:
Type | Description  
---|---  
`InMemoryStateStore[](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.state_store.InMemoryStateStore "InMemoryStateStore \(workflows.context.state_store.InMemoryStateStore\)")[MODEL_T]` |  InMemoryStateStore[MODEL_T]: A store with the reconstructed model.  
Source code in `workflows/context/state_store.py`
```
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
205
206
207
208
209
210
211
212
213
214
```
| ```
@classmethod
deffrom_dict(
    cls, serialized_state: dict[str, Any], serializer: "BaseSerializer"
) -> "InMemoryStateStore[MODEL_T]":
"""Restore a state store from a serialized payload.

    Args:
        serialized_state (dict[str, Any]): The payload produced by
            [to_dict][workflows.context.state_store.InMemoryStateStore.to_dict].
        serializer (BaseSerializer): Strategy to decode stored values.

    Returns:
        InMemoryStateStore[MODEL_T]: A store with the reconstructed model.
    """
    if not serialized_state:
        # Return a default DictState manager
        return cls(DictState())  # type: ignore

    state_data = serialized_state.get("state_data", {})
    state_type = serialized_state.get("state_type", "DictState")

    # Deserialize the state data
    if state_type == "DictState":
        # Special handling for DictState - deserialize each item in _data
        _data_serialized = state_data.get("_data", {})
        deserialized_data = {}
        for key, value in _data_serialized.items():
            try:
                deserialized_data[key] = serializer.deserialize(value)
            except Exception as e:
                raise ValueError(
                    f"Failed to deserialize state value for key {key}: {e}"
                )

        state_instance = DictState(_data=deserialized_data)
    else:
        state_instance = serializer.deserialize(state_data)

    return cls(state_instance)  # type: ignore

```
  
---|---  
###  edit_state `async` [#](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.state_store.InMemoryStateStore.edit_state "Permanent link")
```
edit_state() -> AsyncGenerator[MODEL_T, None]

```

Edit state transactionally under a lock.
Yields the mutable model and writes it back on exit. This pattern avoids read-modify-write races and keeps updates atomic.
Yields:
Name | Type | Description  
---|---|---  
`MODEL_T` |  `AsyncGenerator[MODEL_T, None]` |  The current state model for in-place mutation.  
Source code in `workflows/context/state_store.py`
```
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
```
| ```
@asynccontextmanager
async defedit_state(self) -> AsyncGenerator[MODEL_T, None]:
"""Edit state transactionally under a lock.

    Yields the mutable model and writes it back on exit. This pattern avoids
    read-modify-write races and keeps updates atomic.

    Yields:
        MODEL_T: The current state model for in-place mutation.
    """
    async with self._lock:
        state = self._state

        yield state

        self._state = state

```
  
---|---  
###  get `async` [#](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.state_store.InMemoryStateStore.get "Permanent link")
```
get(path: , default: Optional[] = Ellipsis) -> 

```

Get a nested value using dot-separated paths.
Supports dict keys, list indices, and attribute access transparently at each segment.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`path` |  Dot-separated path, e.g. "user.profile.name". |  _required_  
`default` |  If provided, return this when the path does not exist; otherwise, raise `ValueError`. |  `Ellipsis`  
Returns:
Name | Type | Description  
---|---|---  
`Any` |  The resolved value.  
Raises:
Type | Description  
---|---  
`ValueError` |  If the path is invalid and no default is provided or if the path depth exceeds limits.  
Source code in `workflows/context/state_store.py`
```
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
```
| ```
async defget(self, path: str, default: Optional[Any] = Ellipsis) -> Any:
"""Get a nested value using dot-separated paths.

    Supports dict keys, list indices, and attribute access transparently at
    each segment.

    Args:
        path (str): Dot-separated path, e.g. "user.profile.name".
        default (Any): If provided, return this when the path does not
            exist; otherwise, raise `ValueError`.

    Returns:
        Any: The resolved value.

    Raises:
        ValueError: If the path is invalid and no default is provided or if
            the path depth exceeds limits.
    """
    segments = path.split(".") if path else []
    if len(segments)  MAX_DEPTH:
        raise ValueError(f"Path length exceeds {MAX_DEPTH} segments")

    async with self._lock:
        try:
            value: Any = self._state
            for segment in segments:
                value = self._traverse_step(value, segment)
        except Exception:
            if default is not Ellipsis:
                return default

            msg = f"Path '{path}' not found in state"
            raise ValueError(msg)

    return value

```
  
---|---  
###  set `async` [#](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.state_store.InMemoryStateStore.set "Permanent link")
```
set(path: , value: ) -> None

```

Set a nested value using dot-separated paths.
Intermediate containers are created as needed. Dicts, lists, tuples, and Pydantic models are supported where appropriate.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`path` |  Dot-separated path to write. |  _required_  
`value` |  Value to assign. |  _required_  
Raises:
Type | Description  
---|---  
`ValueError` |  If the path is empty or exceeds the maximum depth.  
Source code in `workflows/context/state_store.py`
```
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
```
| ```
async defset(self, path: str, value: Any) -> None:
"""Set a nested value using dot-separated paths.

    Intermediate containers are created as needed. Dicts, lists, tuples, and
    Pydantic models are supported where appropriate.

    Args:
        path (str): Dot-separated path to write.
        value (Any): Value to assign.

    Raises:
        ValueError: If the path is empty or exceeds the maximum depth.
    """
    if not path:
        raise ValueError("Path cannot be empty")

    segments = path.split(".")
    if len(segments)  MAX_DEPTH:
        raise ValueError(f"Path length exceeds {MAX_DEPTH} segments")

    async with self._lock:
        current = self._state

        # Navigate/create intermediate segments
        for segment in segments[:-1]:
            try:
                current = self._traverse_step(current, segment)
            except (KeyError, AttributeError, IndexError, TypeError):
                # Create intermediate object and assign it
                intermediate: Any = {}
                self._assign_step(current, segment, intermediate)
                current = intermediate

        # Assign the final value
        self._assign_step(current, segments[-1], value)

```
  
---|---  
###  clear `async` [#](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.state_store.InMemoryStateStore.clear "Permanent link")
```
clear() -> None

```

Reset the state to its type defaults.
Raises:
Type | Description  
---|---  
`ValueError` |  If the model type cannot be instantiated from defaults (i.e., fields missing default values).  
Source code in `workflows/context/state_store.py`
```
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
```
| ```
async defclear(self) -> None:
"""Reset the state to its type defaults.

    Raises:
        ValueError: If the model type cannot be instantiated from defaults
            (i.e., fields missing default values).
    """
    try:
        await self.set_state(self._state.__class__())
    except ValidationError:
        raise ValueError("State must have defaults for all fields")

```
  
---|---  
##  BaseSerializer [#](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.serializers.BaseSerializer "Permanent link")
Bases: 
Interface for value serialization used by the workflow context and state store.
Implementations must encode arbitrary Python values into a string and be able to reconstruct the original values from that string.
See Also

Source code in `workflows/context/serializers.py`
```
17
18
19
20
21
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
```
| ```
classBaseSerializer(ABC):
"""
    Interface for value serialization used by the workflow context and state store.

    Implementations must encode arbitrary Python values into a string and be able
    to reconstruct the original values from that string.

    See Also:
        - [JsonSerializer][workflows.context.serializers.JsonSerializer]
        - [PickleSerializer][workflows.context.serializers.PickleSerializer]
    """

    @abstractmethod
    defserialize(self, value: Any) -> str: ...

    @abstractmethod
    defdeserialize(self, value: str) -> Any: ...

```
  
---|---  
##  JsonSerializer [#](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.serializers.JsonSerializer "Permanent link")
Bases: 
JSON-first serializer that understands Pydantic models and LlamaIndex components.
Behavior: - Pydantic models are encoded as JSON with their qualified class name so they can be faithfully reconstructed. - LlamaIndex components (objects exposing `class_name` and `to_dict`) are serialized to their dict form alongside the qualified class name. - Dicts and lists are handled recursively.
Fallback for unsupported objects is to attempt JSON encoding directly; if it fails, a `ValueError` is raised.
Examples:
```
s = JsonSerializer()
payload = s.serialize({"x": 1, "y": [2, 3]})
data = s.deserialize(payload)
assert data == {"x": 1, "y": [2, 3]}

```

See Also

Source code in `workflows/context/serializers.py`
```
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
```
| ```
classJsonSerializer(BaseSerializer):
"""
    JSON-first serializer that understands Pydantic models and LlamaIndex components.

    Behavior:
    - Pydantic models are encoded as JSON with their qualified class name so they
      can be faithfully reconstructed.
    - LlamaIndex components (objects exposing `class_name` and `to_dict`) are
      serialized to their dict form alongside the qualified class name.
    - Dicts and lists are handled recursively.

    Fallback for unsupported objects is to attempt JSON encoding directly; if it
    fails, a `ValueError` is raised.

    Examples:
        ```python
        s = JsonSerializer()
        payload = s.serialize({"x": 1, "y": [2, 3]})
        data = s.deserialize(payload)
        assert data == {"x": 1, "y": [2, 3]}
        ```

    See Also:
        - [BaseSerializer][workflows.context.serializers.BaseSerializer]
        - [PickleSerializer][workflows.context.serializers.PickleSerializer]
    """

    defserialize_value(self, value: Any) -> Any:
"""
        Events with a wrapper type that includes type metadata, so that they can be reserialized into the original Event type.
        Traverses dicts and lists recursively.

        Args:
            value (Any): The value to serialize.

        Returns:
            Any: The serialized value. A dict, list, string, number, or boolean.
        """
        # This has something to do with BaseComponent from llama_index.core. Is it still needed?
        if hasattr(value, "class_name"):
            retval = {
                "__is_component": True,
                "value": value.to_dict(),
                "qualified_name": get_qualified_name(value),
            }
            return retval

        if isinstance(value, BaseModel):
            return {
                "__is_pydantic": True,
                "value": value.model_dump(mode="json"),
                "qualified_name": get_qualified_name(value),
            }

        if isinstance(value, dict):
            return {k: self.serialize_value(v) for k, v in value.items()}

        if isinstance(value, list):
            return [self.serialize_value(item) for item in value]

        return value

    defserialize(self, value: Any) -> str:
"""Serialize an arbitrary value to a JSON string.

        Args:
            value (Any): The value to encode.

        Returns:
            str: JSON string.

        Raises:
            ValueError: If the value cannot be encoded to JSON.
        """
        try:
            serialized_value = self.serialize_value(value)
            return json.dumps(serialized_value)
        except Exception:
            raise ValueError(f"Failed to serialize value: {type(value)}: {value!s}")

    defdeserialize_value(self, data: Any) -> Any:
"""Helper to deserialize a single dict or other json value from its discriminator fields back into a python class.

        Args:
            data (Any): a dict, list, string, number, or boolean

        Returns:
            Any: The deserialized value.
        """
        if isinstance(data, dict):
            if data.get("__is_pydantic") and data.get("qualified_name"):
                module_class = import_module_from_qualified_name(data["qualified_name"])
                return module_class.model_validate(data["value"])
            elif data.get("__is_component") and data.get("qualified_name"):
                module_class = import_module_from_qualified_name(data["qualified_name"])
                return module_class.from_dict(data["value"])
            return {k: self.deserialize_value(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.deserialize_value(item) for item in data]
        return data

    defdeserialize(self, value: str) -> Any:
"""Deserialize a JSON string into Python objects.

        Args:
            value (str): JSON string.

        Returns:
            Any: The reconstructed value.
        """
        data = json.loads(value)
        return self.deserialize_value(data)

```
  
---|---  
###  serialize_value [#](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.serializers.JsonSerializer.serialize_value "Permanent link")
```
serialize_value(value: ) -> 

```

Events with a wrapper type that includes type metadata, so that they can be reserialized into the original Event type. Traverses dicts and lists recursively.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`value` |  The value to serialize. |  _required_  
Returns:
Name | Type | Description  
---|---|---  
`Any` |  The serialized value. A dict, list, string, number, or boolean.  
Source code in `workflows/context/serializers.py`
```
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
```
| ```
defserialize_value(self, value: Any) -> Any:
"""
    Events with a wrapper type that includes type metadata, so that they can be reserialized into the original Event type.
    Traverses dicts and lists recursively.

    Args:
        value (Any): The value to serialize.

    Returns:
        Any: The serialized value. A dict, list, string, number, or boolean.
    """
    # This has something to do with BaseComponent from llama_index.core. Is it still needed?
    if hasattr(value, "class_name"):
        retval = {
            "__is_component": True,
            "value": value.to_dict(),
            "qualified_name": get_qualified_name(value),
        }
        return retval

    if isinstance(value, BaseModel):
        return {
            "__is_pydantic": True,
            "value": value.model_dump(mode="json"),
            "qualified_name": get_qualified_name(value),
        }

    if isinstance(value, dict):
        return {k: self.serialize_value(v) for k, v in value.items()}

    if isinstance(value, list):
        return [self.serialize_value(item) for item in value]

    return value

```
  
---|---  
###  serialize [#](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.serializers.JsonSerializer.serialize "Permanent link")
```
serialize(value: ) -> 

```

Serialize an arbitrary value to a JSON string.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`value` |  The value to encode. |  _required_  
Returns:
Name | Type | Description  
---|---|---  
`str` |  JSON string.  
Raises:
Type | Description  
---|---  
`ValueError` |  If the value cannot be encoded to JSON.  
Source code in `workflows/context/serializers.py`
```
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
```
| ```
defserialize(self, value: Any) -> str:
"""Serialize an arbitrary value to a JSON string.

    Args:
        value (Any): The value to encode.

    Returns:
        str: JSON string.

    Raises:
        ValueError: If the value cannot be encoded to JSON.
    """
    try:
        serialized_value = self.serialize_value(value)
        return json.dumps(serialized_value)
    except Exception:
        raise ValueError(f"Failed to serialize value: {type(value)}: {value!s}")

```
  
---|---  
###  deserialize_value [#](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.serializers.JsonSerializer.deserialize_value "Permanent link")
```
deserialize_value(data: ) -> 

```

Helper to deserialize a single dict or other json value from its discriminator fields back into a python class.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`data` |  a dict, list, string, number, or boolean |  _required_  
Returns:
Name | Type | Description  
---|---|---  
`Any` |  The deserialized value.  
Source code in `workflows/context/serializers.py`
```
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
```
| ```
defdeserialize_value(self, data: Any) -> Any:
"""Helper to deserialize a single dict or other json value from its discriminator fields back into a python class.

    Args:
        data (Any): a dict, list, string, number, or boolean

    Returns:
        Any: The deserialized value.
    """
    if isinstance(data, dict):
        if data.get("__is_pydantic") and data.get("qualified_name"):
            module_class = import_module_from_qualified_name(data["qualified_name"])
            return module_class.model_validate(data["value"])
        elif data.get("__is_component") and data.get("qualified_name"):
            module_class = import_module_from_qualified_name(data["qualified_name"])
            return module_class.from_dict(data["value"])
        return {k: self.deserialize_value(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [self.deserialize_value(item) for item in data]
    return data

```
  
---|---  
###  deserialize [#](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.serializers.JsonSerializer.deserialize "Permanent link")
```
deserialize(value: ) -> 

```

Deserialize a JSON string into Python objects.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`value` |  JSON string. |  _required_  
Returns:
Name | Type | Description  
---|---|---  
`Any` |  The reconstructed value.  
Source code in `workflows/context/serializers.py`
```
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
```
| ```
defdeserialize(self, value: str) -> Any:
"""Deserialize a JSON string into Python objects.

    Args:
        value (str): JSON string.

    Returns:
        Any: The reconstructed value.
    """
    data = json.loads(value)
    return self.deserialize_value(data)

```
  
---|---  
##  PickleSerializer [#](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.serializers.PickleSerializer "Permanent link")
Bases: 
Hybrid serializer: JSON when possible, Pickle as a safe fallback.
This serializer attempts JSON first for readability and portability, and transparently falls back to Pickle for objects that cannot be represented in JSON. Deserialization prioritizes Pickle and falls back to JSON.
Warning
Pickle can execute arbitrary code during deserialization. Only deserialize trusted payloads.
Note: Used to be called `JsonPickleSerializer` but it was renamed to `PickleSerializer`.
Examples:
```
s = PickleSerializer()
classFoo:
    def__init__(self, x):
        self.x = x
payload = s.serialize(Foo(1))  # will likely use Pickle
obj = s.deserialize(payload)
assert isinstance(obj, Foo)

```

Source code in `workflows/context/serializers.py`
```
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
205
```
| ```
classPickleSerializer(JsonSerializer):
"""
    Hybrid serializer: JSON when possible, Pickle as a safe fallback.

    This serializer attempts JSON first for readability and portability, and
    transparently falls back to Pickle for objects that cannot be represented in
    JSON. Deserialization prioritizes Pickle and falls back to JSON.

    Warning:
        Pickle can execute arbitrary code during deserialization. Only
        deserialize trusted payloads.

    Note: Used to be called `JsonPickleSerializer` but it was renamed to `PickleSerializer`.

    Examples:
        ```python
        s = PickleSerializer()
        class Foo:
            def __init__(self, x):
                self.x = x
        payload = s.serialize(Foo(1))  # will likely use Pickle
        obj = s.deserialize(payload)
        assert isinstance(obj, Foo)
        ```
    """

    defserialize(self, value: Any) -> str:
"""Serialize with JSON preference and Pickle fallback.

        Args:
            value (Any): The value to encode.

        Returns:
            str: Encoded string (JSON or base64-encoded Pickle bytes).
        """
        try:
            return super().serialize(value)
        except Exception:
            return base64.b64encode(pickle.dumps(value)).decode("utf-8")

    defdeserialize(self, value: str) -> Any:
"""Deserialize with Pickle preference and JSON fallback.

        Args:
            value (str): Encoded string.

        Returns:
            Any: The reconstructed value.

        Notes:
            Use only with trusted payloads due to Pickle security implications.
        """
        try:
            return pickle.loads(base64.b64decode(value))
        except Exception:
            return super().deserialize(value)

```
  
---|---  
###  serialize [#](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.serializers.PickleSerializer.serialize "Permanent link")
```
serialize(value: ) -> 

```

Serialize with JSON preference and Pickle fallback.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`value` |  The value to encode. |  _required_  
Returns:
Name | Type | Description  
---|---|---  
`str` |  Encoded string (JSON or base64-encoded Pickle bytes).  
Source code in `workflows/context/serializers.py`
```
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
```
| ```
defserialize(self, value: Any) -> str:
"""Serialize with JSON preference and Pickle fallback.

    Args:
        value (Any): The value to encode.

    Returns:
        str: Encoded string (JSON or base64-encoded Pickle bytes).
    """
    try:
        return super().serialize(value)
    except Exception:
        return base64.b64encode(pickle.dumps(value)).decode("utf-8")

```
  
---|---  
###  deserialize [#](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.serializers.PickleSerializer.deserialize "Permanent link")
```
deserialize(value: ) -> 

```

Deserialize with Pickle preference and JSON fallback.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`value` |  Encoded string. |  _required_  
Returns:
Name | Type | Description  
---|---|---  
`Any` |  The reconstructed value.  
Notes
Use only with trusted payloads due to Pickle security implications.
Source code in `workflows/context/serializers.py`
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
204
205
```
| ```
defdeserialize(self, value: str) -> Any:
"""Deserialize with Pickle preference and JSON fallback.

    Args:
        value (str): Encoded string.

    Returns:
        Any: The reconstructed value.

    Notes:
        Use only with trusted payloads due to Pickle security implications.
    """
    try:
        return pickle.loads(base64.b64decode(value))
    except Exception:
        return super().deserialize(value)

```
  
---|---
