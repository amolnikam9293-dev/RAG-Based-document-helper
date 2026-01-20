# Index
##  ToolSelection [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.ToolSelection "Permanent link")
Bases: `BaseModel`
Tool selection.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`tool_id` |  Tool ID to select. |  _required_  
`tool_name` |  Tool name to select. |  _required_  
`tool_kwargs` |  `Dict[str, Any]` |  Keyword arguments for the tool. |  _required_  
Source code in `llama_index/core/llms/llm.py`
```
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
```
| ```
class ToolSelection(BaseModel):
"""Tool selection."""

    tool_id: str = Field(description="Tool ID to select.")
    tool_name: str = Field(description="Tool name to select.")
    tool_kwargs: Dict[str, Any] = Field(description="Keyword arguments for the tool.")

    @field_validator("tool_kwargs", mode="wrap")
    @classmethod
    def ignore_non_dict_arguments(cls, v: Any, handler: Any) -> Dict[str, Any]:
        try:
            return handler(v)
        except ValidationError:
            return handler({})

```
  
---|---  
##  LLM [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM "Permanent link")
Bases: `BaseLLM`
The LLM class is the main class for interacting with language models.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`system_prompt` |  `str | None` |  System prompt for LLM calls. |  `None`  
`messages_to_prompt` |  `MessagesToPromptType | None` |  Function to convert a list of messages to an LLM prompt. |  `None`  
`completion_to_prompt` |  `CompletionToPromptType | None` |  Function to convert a completion to an LLM prompt. |  `None`  
`output_parser` |  `BaseOutputParser[](https://developers.llamaindex.ai/python/framework-api-reference/output_parsers/#llama_index.core.types.BaseOutputParser "llama_index.core.types.BaseOutputParser") | None` |  Output parser to parse, validate, and correct errors programmatically. |  `None`  
`pydantic_program_mode` |  |  `<PydanticProgramMode.DEFAULT: 'default'>`  
`query_wrapper_prompt` |  `BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "llama_index.core.prompts.BasePromptTemplate") | None` |  Query wrapper prompt for LLM calls. |  `None`  
Attributes:
Name | Type | Description  
---|---|---  
`system_prompt` |  `Optional[str]` |  System prompt for LLM calls.  
`messages_to_prompt` |  `Callable` |  Function to convert a list of messages to an LLM prompt.  
`completion_to_prompt` |  `Callable` |  Function to convert a completion to an LLM prompt.  
`output_parser` |  `Optional[BaseOutputParser[](https://developers.llamaindex.ai/python/framework-api-reference/output_parsers/#llama_index.core.types.BaseOutputParser "llama_index.core.types.BaseOutputParser")]` |  Output parser to parse, validate, and correct errors programmatically.  
`pydantic_program_mode` |  |  Pydantic program mode to use for structured prediction.  
Source code in `llama_index/core/llms/llm.py`
```
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
610
611
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
689
690
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
797
798
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
870
871
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
```
| ```
class LLM(BaseLLM):
"""
    The LLM class is the main class for interacting with language models.

    Attributes:
        system_prompt (Optional[str]):
            System prompt for LLM calls.
        messages_to_prompt (Callable):
            Function to convert a list of messages to an LLM prompt.
        completion_to_prompt (Callable):
            Function to convert a completion to an LLM prompt.
        output_parser (Optional[BaseOutputParser]):
            Output parser to parse, validate, and correct errors programmatically.
        pydantic_program_mode (PydanticProgramMode):
            Pydantic program mode to use for structured prediction.

    """

    system_prompt: Optional[str] = Field(
        default=None, description="System prompt for LLM calls."
    )
    messages_to_prompt: MessagesToPromptCallable = Field(
        description="Function to convert a list of messages to an LLM prompt.",
        default=None,
        exclude=True,
    )
    completion_to_prompt: CompletionToPromptCallable = Field(
        description="Function to convert a completion to an LLM prompt.",
        default=None,
        exclude=True,
    )
    output_parser: Optional[BaseOutputParser] = Field(
        description="Output parser to parse, validate, and correct errors programmatically.",
        default=None,
        exclude=True,
    )
    pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT

    # deprecated
    query_wrapper_prompt: Optional[BasePromptTemplate] = Field(
        description="Query wrapper prompt for LLM calls.",
        default=None,
        exclude=True,
    )

    # -- Pydantic Configs --

    @field_validator("messages_to_prompt")
    @classmethod
    def set_messages_to_prompt(
        cls, messages_to_prompt: Optional[MessagesToPromptType]
    ) -> MessagesToPromptType:
        return messages_to_prompt or generic_messages_to_prompt

    @field_validator("completion_to_prompt")
    @classmethod
    def set_completion_to_prompt(
        cls, completion_to_prompt: Optional[CompletionToPromptType]
    ) -> CompletionToPromptType:
        return completion_to_prompt or default_completion_to_prompt

    @model_validator(mode="after")
    def check_prompts(self) -> "LLM":
        if self.completion_to_prompt is None:
            self.completion_to_prompt = default_completion_to_prompt
        if self.messages_to_prompt is None:
            self.messages_to_prompt = generic_messages_to_prompt
        return self

    # -- Utils --

    def _log_template_data(
        self, prompt: BasePromptTemplate, **prompt_args: Any
    ) -> None:
        template_vars = {
            k: v
            for k, v in ChainMap(prompt.kwargs, prompt_args).items()
            if k in prompt.template_vars
        }
        with self.callback_manager.event(
            CBEventType.TEMPLATING,
            payload={
                EventPayload.TEMPLATE: prompt.get_template(llm=self),
                EventPayload.TEMPLATE_VARS: template_vars,
                EventPayload.SYSTEM_PROMPT: self.system_prompt,
                EventPayload.QUERY_WRAPPER_PROMPT: self.query_wrapper_prompt,
            },
        ):
            pass

    def _get_prompt(self, prompt: BasePromptTemplate, **prompt_args: Any) -> str:
        formatted_prompt = prompt.format(
            llm=self,
            messages_to_prompt=self.messages_to_prompt,
            completion_to_prompt=self.completion_to_prompt,
            **prompt_args,
        )
        if self.output_parser is not None:
            formatted_prompt = self.output_parser.format(formatted_prompt)
        return self._extend_prompt(formatted_prompt)

    def _get_messages(
        self, prompt: BasePromptTemplate, **prompt_args: Any
    ) -> List[ChatMessage]:
        messages = prompt.format_messages(llm=self, **prompt_args)
        if self.output_parser is not None:
            messages = self.output_parser.format_messages(messages)
        return self._extend_messages(messages)

    def _parse_output(self, output: str) -> str:
        if self.output_parser is not None:
            return str(self.output_parser.parse(output))

        return output

    def _extend_prompt(
        self,
        formatted_prompt: str,
    ) -> str:
"""Add system and query wrapper prompts to base prompt."""
        extended_prompt = formatted_prompt

        if self.system_prompt:
            extended_prompt = self.system_prompt + "\n\n" + extended_prompt

        if self.query_wrapper_prompt:
            extended_prompt = self.query_wrapper_prompt.format(
                query_str=extended_prompt
            )

        return extended_prompt

    def _extend_messages(self, messages: List[ChatMessage]) -> List[ChatMessage]:
"""Add system prompt to chat message list."""
        if self.system_prompt:
            messages = [
                ChatMessage(role=MessageRole.SYSTEM, content=self.system_prompt),
                *messages,
            ]
        return messages

    # -- Structured outputs --

    @dispatcher.span
    def structured_predict(
        self,
        output_cls: Type[Model],
        prompt: PromptTemplate,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        **prompt_args: Any,
    ) -> Model:
r"""
        Structured predict.

        Args:
            output_cls (BaseModel):
                Output class to use for structured prediction.
            prompt (PromptTemplate):
                Prompt template to use for structured prediction.
            llm_kwargs (Optional[Dict[str, Any]]):
                Arguments that are passed down to the LLM invoked by the program.
            prompt_args (Any):
                Additional arguments to format the prompt with.

        Returns:
            BaseModel: The structured prediction output.

        Examples:
            ```python
            from pydantic import BaseModel

            class Test(BaseModel):
                \"\"\"My test class.\"\"\"
                name: str

            from llama_index.core.prompts import PromptTemplate

            prompt = PromptTemplate("Please predict a Test with a random name related to {topic}.")
            output = llm.structured_predict(Test, prompt, topic="cats")
            print(output.name)


        """
        from llama_index.core.program.utils import get_program_for_llm

        dispatcher.event(
            LLMStructuredPredictStartEvent(
                output_cls=output_cls, template=prompt, template_args=prompt_args
            )
        )
        program = get_program_for_llm(
            output_cls,
            prompt,
            self,
            pydantic_program_mode=self.pydantic_program_mode,
        )

        result = program(llm_kwargs=llm_kwargs, **prompt_args)
        assert not isinstance(result, list)

        dispatcher.event(LLMStructuredPredictEndEvent(output=result))
        return result

    @dispatcher.span
    async def astructured_predict(
        self,
        output_cls: Type[Model],
        prompt: PromptTemplate,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        **prompt_args: Any,
    ) -> Model:
r"""
        Async Structured predict.

        Args:
            output_cls (BaseModel):
                Output class to use for structured prediction.
            prompt (PromptTemplate):
                Prompt template to use for structured prediction.
            llm_kwargs (Optional[Dict[str, Any]]):
                Arguments that are passed down to the LLM invoked by the program.
            prompt_args (Any):
                Additional arguments to format the prompt with.

        Returns:
            BaseModel: The structured prediction output.

        Examples:
            ```python
            from pydantic import BaseModel

            class Test(BaseModel):
                \"\"\"My test class.\"\"\"
                name: str

            from llama_index.core.prompts import PromptTemplate

            prompt = PromptTemplate("Please predict a Test with a random name related to {topic}.")
            output = await llm.astructured_predict(Test, prompt, topic="cats")
            print(output.name)


        """
        from llama_index.core.program.utils import get_program_for_llm

        dispatcher.event(
            LLMStructuredPredictStartEvent(
                output_cls=output_cls, template=prompt, template_args=prompt_args
            )
        )

        program = get_program_for_llm(
            output_cls,
            prompt,
            self,
            pydantic_program_mode=self.pydantic_program_mode,
        )

        result = await program.acall(llm_kwargs=llm_kwargs, **prompt_args)
        assert not isinstance(result, list)

        dispatcher.event(LLMStructuredPredictEndEvent(output=result))
        return result

    def _structured_stream_call(
        self,
        output_cls: Type[Model],
        prompt: PromptTemplate,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        **prompt_args: Any,
    ) -> Generator[
        Union[Model, List[Model], "FlexibleModel", List["FlexibleModel"]], None, None
    ]:
        from llama_index.core.program.utils import get_program_for_llm

        program = get_program_for_llm(
            output_cls,
            prompt,
            self,
            pydantic_program_mode=self.pydantic_program_mode,
        )
        return program.stream_call(llm_kwargs=llm_kwargs, **prompt_args)

    @dispatcher.span
    def stream_structured_predict(
        self,
        output_cls: Type[Model],
        prompt: PromptTemplate,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        **prompt_args: Any,
    ) -> Generator[Union[Model, "FlexibleModel"], None, None]:
r"""
        Stream Structured predict.

        Args:
            output_cls (BaseModel):
                Output class to use for structured prediction.
            prompt (PromptTemplate):
                Prompt template to use for structured prediction.
            llm_kwargs (Optional[Dict[str, Any]]):
                Arguments that are passed down to the LLM invoked by the program.
            prompt_args (Any):
                Additional arguments to format the prompt with.

        Returns:
            Generator: A generator returning partial copies of the model or list of models.

        Examples:
            ```python
            from pydantic import BaseModel

            class Test(BaseModel):
                \"\"\"My test class.\"\"\"
                name: str

            from llama_index.core.prompts import PromptTemplate

            prompt = PromptTemplate("Please predict a Test with a random name related to {topic}.")
            stream_output = llm.stream_structured_predict(Test, prompt, topic="cats")
            for partial_output in stream_output:
                # stream partial outputs until completion
                print(partial_output.name)


        """
        dispatcher.event(
            LLMStructuredPredictStartEvent(
                output_cls=output_cls, template=prompt, template_args=prompt_args
            )
        )

        result = self._structured_stream_call(
            output_cls, prompt, llm_kwargs, **prompt_args
        )
        for r in result:
            dispatcher.event(LLMStructuredPredictInProgressEvent(output=r))
            assert not isinstance(r, list)
            yield r

        dispatcher.event(LLMStructuredPredictEndEvent(output=r))

    async def _structured_astream_call(
        self,
        output_cls: Type[Model],
        prompt: PromptTemplate,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        **prompt_args: Any,
    ) -> AsyncGenerator[
        Union[Model, List[Model], "FlexibleModel", List["FlexibleModel"]], None
    ]:
        from llama_index.core.program.utils import get_program_for_llm

        program = get_program_for_llm(
            output_cls,
            prompt,
            self,
            pydantic_program_mode=self.pydantic_program_mode,
        )

        return await program.astream_call(llm_kwargs=llm_kwargs, **prompt_args)

    @dispatcher.span
    async def astream_structured_predict(
        self,
        output_cls: Type[Model],
        prompt: PromptTemplate,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        **prompt_args: Any,
    ) -> AsyncGenerator[Union[Model, "FlexibleModel"], None]:
r"""
        Async Stream Structured predict.

        Args:
            output_cls (BaseModel):
                Output class to use for structured prediction.
            prompt (PromptTemplate):
                Prompt template to use for structured prediction.
            llm_kwargs (Optional[Dict[str, Any]]):
                Arguments that are passed down to the LLM invoked by the program.
            prompt_args (Any):
                Additional arguments to format the prompt with.

        Returns:
            Generator: A generator returning partial copies of the model or list of models.

        Examples:
            ```python
            from pydantic import BaseModel

            class Test(BaseModel):
                \"\"\"My test class.\"\"\"
                name: str

            from llama_index.core.prompts import PromptTemplate

            prompt = PromptTemplate("Please predict a Test with a random name related to {topic}.")
            stream_output = await llm.astream_structured_predict(Test, prompt, topic="cats")
            async for partial_output in stream_output:
                # stream partial outputs until completion
                print(partial_output.name)


        """

        async def gen() -> AsyncGenerator[Union[Model, "FlexibleModel"], None]:
            dispatcher.event(
                LLMStructuredPredictStartEvent(
                    output_cls=output_cls, template=prompt, template_args=prompt_args
                )
            )

            result = await self._structured_astream_call(
                output_cls, prompt, llm_kwargs, **prompt_args
            )
            async for r in result:
                dispatcher.event(LLMStructuredPredictInProgressEvent(output=r))
                assert not isinstance(r, list)
                yield r

            dispatcher.event(LLMStructuredPredictEndEvent(output=r))

        return gen()

    # -- Prompt Chaining --

    @dispatcher.span
    def predict(
        self,
        prompt: BasePromptTemplate,
        **prompt_args: Any,
    ) -> str:
"""
        Predict for a given prompt.

        Args:
            prompt (BasePromptTemplate):
                The prompt to use for prediction.
            prompt_args (Any):
                Additional arguments to format the prompt with.

        Returns:
            str: The prediction output.

        Examples:
            ```python
            from llama_index.core.prompts import PromptTemplate

            prompt = PromptTemplate("Please write a random name related to {topic}.")
            output = llm.predict(prompt, topic="cats")
            print(output)


        """
        dispatcher.event(
            LLMPredictStartEvent(template=prompt, template_args=prompt_args)
        )
        self._log_template_data(prompt, **prompt_args)

        if self.metadata.is_chat_model:
            messages = self._get_messages(prompt, **prompt_args)
            chat_response = self.chat(messages)
            output = chat_response.message.content or ""
        else:
            formatted_prompt = self._get_prompt(prompt, **prompt_args)
            response = self.complete(formatted_prompt, formatted=True)
            output = response.text
        parsed_output = self._parse_output(output)
        dispatcher.event(LLMPredictEndEvent(output=parsed_output))
        return parsed_output

    @dispatcher.span
    def stream(
        self,
        prompt: BasePromptTemplate,
        **prompt_args: Any,
    ) -> TokenGen:
"""
        Stream predict for a given prompt.

        Args:
            prompt (BasePromptTemplate):
                The prompt to use for prediction.
            prompt_args (Any):
                Additional arguments to format the prompt with.

        Yields:
            str: Each streamed token.

        Examples:
            ```python
            from llama_index.core.prompts import PromptTemplate

            prompt = PromptTemplate("Please write a random name related to {topic}.")
            gen = llm.stream(prompt, topic="cats")
            for token in gen:
                print(token, end="", flush=True)


        """
        self._log_template_data(prompt, **prompt_args)

        dispatcher.event(
            LLMPredictStartEvent(template=prompt, template_args=prompt_args)
        )
        if self.metadata.is_chat_model:
            messages = self._get_messages(prompt, **prompt_args)
            chat_response = self.stream_chat(messages)
            stream_tokens = stream_chat_response_to_tokens(chat_response)
        else:
            formatted_prompt = self._get_prompt(prompt, **prompt_args)
            stream_response = self.stream_complete(formatted_prompt, formatted=True)
            stream_tokens = stream_completion_response_to_tokens(stream_response)

        if prompt.output_parser is not None or self.output_parser is not None:
            raise NotImplementedError("Output parser is not supported for streaming.")

        return stream_tokens

    @dispatcher.span
    async def apredict(
        self,
        prompt: BasePromptTemplate,
        **prompt_args: Any,
    ) -> str:
"""
        Async Predict for a given prompt.

        Args:
            prompt (BasePromptTemplate):
                The prompt to use for prediction.
            prompt_args (Any):
                Additional arguments to format the prompt with.

        Returns:
            str: The prediction output.

        Examples:
            ```python
            from llama_index.core.prompts import PromptTemplate

            prompt = PromptTemplate("Please write a random name related to {topic}.")
            output = await llm.apredict(prompt, topic="cats")
            print(output)


        """
        dispatcher.event(
            LLMPredictStartEvent(template=prompt, template_args=prompt_args)
        )
        self._log_template_data(prompt, **prompt_args)

        if self.metadata.is_chat_model:
            messages = self._get_messages(prompt, **prompt_args)
            chat_response = await self.achat(messages)
            output = chat_response.message.content or ""
        else:
            formatted_prompt = self._get_prompt(prompt, **prompt_args)
            response = await self.acomplete(formatted_prompt, formatted=True)
            output = response.text

        parsed_output = self._parse_output(output)
        dispatcher.event(LLMPredictEndEvent(output=parsed_output))
        return parsed_output

    @dispatcher.span
    async def astream(
        self,
        prompt: BasePromptTemplate,
        **prompt_args: Any,
    ) -> TokenAsyncGen:
"""
        Async stream predict for a given prompt.

        Args:
        prompt (BasePromptTemplate):
            The prompt to use for prediction.
        prompt_args (Any):
            Additional arguments to format the prompt with.

        Yields:
            str: An async generator that yields strings of tokens.

        Examples:
            ```python
            from llama_index.core.prompts import PromptTemplate

            prompt = PromptTemplate("Please write a random name related to {topic}.")
            gen = await llm.astream(prompt, topic="cats")
            async for token in gen:
                print(token, end="", flush=True)


        """
        self._log_template_data(prompt, **prompt_args)

        dispatcher.event(
            LLMPredictStartEvent(template=prompt, template_args=prompt_args)
        )
        if self.metadata.is_chat_model:
            messages = self._get_messages(prompt, **prompt_args)
            chat_response = await self.astream_chat(messages)
            stream_tokens = await astream_chat_response_to_tokens(chat_response)
        else:
            formatted_prompt = self._get_prompt(prompt, **prompt_args)
            stream_response = await self.astream_complete(
                formatted_prompt, formatted=True
            )
            stream_tokens = await astream_completion_response_to_tokens(stream_response)

        if prompt.output_parser is not None or self.output_parser is not None:
            raise NotImplementedError("Output parser is not supported for streaming.")

        return stream_tokens

    @dispatcher.span
    def predict_and_call(
        self,
        tools: List["BaseTool"],
        user_msg: Optional[Union[str, ChatMessage]] = None,
        chat_history: Optional[List[ChatMessage]] = None,
        verbose: bool = False,
        **kwargs: Any,
    ) -> "AgentChatResponse":
"""
        Predict and call the tool.

        By default uses a ReAct agent to do tool calling (through text prompting),
        but function calling LLMs will implement this differently.

        """
        from llama_index.core.agent.workflow import ReActAgent
        from llama_index.core.chat_engine.types import AgentChatResponse
        from llama_index.core.memory import Memory
        from llama_index.core.tools.calling import call_tool_with_selection
        from llama_index.core.workflow import Context
        from workflows.context.state_store import DictState

        agent = ReActAgent(
            tools=tools,
            llm=self,
            verbose=verbose,
            formatter=kwargs.get("react_chat_formatter"),
            output_parser=kwargs.get("output_parser"),
            tool_retriever=kwargs.get("tool_retriever"),
        )

        memory = kwargs.get("memory", Memory.from_defaults())

        if isinstance(user_msg, ChatMessage) and isinstance(user_msg.content, str):
            pass
        elif isinstance(user_msg, str):
            user_msg = ChatMessage(content=user_msg, role=MessageRole.USER)

        llm_input = []
        if chat_history:
            llm_input.extend(chat_history)
        if user_msg:
            llm_input.append(user_msg)

        ctx: Context[DictState] = Context(agent)

        try:
            resp = asyncio_run(
                agent.take_step(
                    ctx=ctx, llm_input=llm_input, tools=tools or [], memory=memory
                )
            )
            tool_outputs = []
            for tool_call in resp.tool_calls:
                tool_output = call_tool_with_selection(
                    tool_call=tool_call,
                    tools=tools or [],
                    verbose=verbose,
                )
                tool_outputs.append(tool_output)
            output_text = "\n\n".join(
                [tool_output.content for tool_output in tool_outputs]
            )
            return AgentChatResponse(
                response=output_text,
                sources=tool_outputs,
            )
        except Exception as e:
            output = AgentChatResponse(
                response="An error occurred while running the tool: " + str(e),
                sources=[],
            )

        return output

    @dispatcher.span
    async def apredict_and_call(
        self,
        tools: List["BaseTool"],
        user_msg: Optional[Union[str, ChatMessage]] = None,
        chat_history: Optional[List[ChatMessage]] = None,
        verbose: bool = False,
        **kwargs: Any,
    ) -> "AgentChatResponse":
"""Predict and call the tool."""
        from llama_index.core.agent.workflow import ReActAgent
        from llama_index.core.chat_engine.types import AgentChatResponse
        from llama_index.core.memory import Memory
        from llama_index.core.tools.calling import acall_tool_with_selection
        from llama_index.core.workflow import Context
        from workflows.context.state_store import DictState

        agent = ReActAgent(
            tools=tools,
            llm=self,
            verbose=verbose,
            formatter=kwargs.get("react_chat_formatter"),
            output_parser=kwargs.get("output_parser"),
            tool_retriever=kwargs.get("tool_retriever"),
        )

        memory = kwargs.get("memory", Memory.from_defaults())

        if isinstance(user_msg, ChatMessage) and isinstance(user_msg.content, str):
            pass
        elif isinstance(user_msg, str):
            user_msg = ChatMessage(content=user_msg, role=MessageRole.USER)

        llm_input = []
        if chat_history:
            llm_input.extend(chat_history)
        if user_msg:
            llm_input.append(user_msg)

        ctx: Context[DictState] = Context(agent)

        try:
            resp = await agent.take_step(
                ctx=ctx, llm_input=llm_input, tools=tools or [], memory=memory
            )
            tool_outputs = []
            for tool_call in resp.tool_calls:
                tool_output = await acall_tool_with_selection(
                    tool_call=tool_call,
                    tools=tools or [],
                    verbose=verbose,
                )
                tool_outputs.append(tool_output)

            output_text = "\n\n".join(
                [tool_output.content for tool_output in tool_outputs]
            )
            return AgentChatResponse(
                response=output_text,
                sources=tool_outputs,
            )
        except Exception as e:
            output = AgentChatResponse(
                response="An error occurred while running the tool: " + str(e),
                sources=[],
            )

        return output

    def as_structured_llm(
        self,
        output_cls: Type[BaseModel],
        **kwargs: Any,
    ) -> "StructuredLLM":
"""Return a structured LLM around a given object."""
        from llama_index.core.llms.structured_llm import StructuredLLM

        return StructuredLLM(llm=self, output_cls=output_cls, **kwargs)

```
  
---|---  
###  structured_predict [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM.structured_predict "Permanent link")
```
structured_predict(output_cls: [], prompt: , llm_kwargs: Optional[[, ]] = None, **prompt_args: ) -> 

```

Structured predict.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`output_cls` |  `BaseModel` |  Output class to use for structured prediction. |  _required_  
`prompt` |  |  Prompt template to use for structured prediction. |  _required_  
`llm_kwargs` |  `Optional[Dict[str, Any]]` |  Arguments that are passed down to the LLM invoked by the program. |  `None`  
`prompt_args` |  Additional arguments to format the prompt with.  
Returns:
Name | Type | Description  
---|---|---  
`BaseModel` |  `Model` |  The structured prediction output.  
Examples:
```
from pydantic import BaseModel

class Test(BaseModel):
    \"\"\"My test class.\"\"\"
    name: str

from llama_index.core.prompts import PromptTemplate

prompt = PromptTemplate("Please predict a Test with a random name related to {topic}.")
output = llm.structured_predict(Test, prompt, topic="cats")
print(output.name)

```

Source code in `llama_index/core/llms/llm.py`
```
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
```
| ```
@dispatcher.span
def structured_predict(
    self,
    output_cls: Type[Model],
    prompt: PromptTemplate,
    llm_kwargs: Optional[Dict[str, Any]] = None,
    **prompt_args: Any,
) -> Model:
r"""
    Structured predict.

    Args:
        output_cls (BaseModel):
            Output class to use for structured prediction.
        prompt (PromptTemplate):
            Prompt template to use for structured prediction.
        llm_kwargs (Optional[Dict[str, Any]]):
            Arguments that are passed down to the LLM invoked by the program.
        prompt_args (Any):
            Additional arguments to format the prompt with.

    Returns:
        BaseModel: The structured prediction output.

    Examples:
        ```python
        from pydantic import BaseModel

        class Test(BaseModel):
            \"\"\"My test class.\"\"\"
            name: str

        from llama_index.core.prompts import PromptTemplate

        prompt = PromptTemplate("Please predict a Test with a random name related to {topic}.")
        output = llm.structured_predict(Test, prompt, topic="cats")
        print(output.name)
        ```

    """
    from llama_index.core.program.utils import get_program_for_llm

    dispatcher.event(
        LLMStructuredPredictStartEvent(
            output_cls=output_cls, template=prompt, template_args=prompt_args
        )
    )
    program = get_program_for_llm(
        output_cls,
        prompt,
        self,
        pydantic_program_mode=self.pydantic_program_mode,
    )

    result = program(llm_kwargs=llm_kwargs, **prompt_args)
    assert not isinstance(result, list)

    dispatcher.event(LLMStructuredPredictEndEvent(output=result))
    return result

```
  
---|---  
###  astructured_predict `async` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM.astructured_predict "Permanent link")
```
astructured_predict(output_cls: [], prompt: , llm_kwargs: Optional[[, ]] = None, **prompt_args: ) -> 

```

Async Structured predict.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`output_cls` |  `BaseModel` |  Output class to use for structured prediction. |  _required_  
`prompt` |  |  Prompt template to use for structured prediction. |  _required_  
`llm_kwargs` |  `Optional[Dict[str, Any]]` |  Arguments that are passed down to the LLM invoked by the program. |  `None`  
`prompt_args` |  Additional arguments to format the prompt with.  
Returns:
Name | Type | Description  
---|---|---  
`BaseModel` |  `Model` |  The structured prediction output.  
Examples:
```
from pydantic import BaseModel

class Test(BaseModel):
    \"\"\"My test class.\"\"\"
    name: str

from llama_index.core.prompts import PromptTemplate

prompt = PromptTemplate("Please predict a Test with a random name related to {topic}.")
output = await llm.astructured_predict(Test, prompt, topic="cats")
print(output.name)

```

Source code in `llama_index/core/llms/llm.py`
```
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
```
| ```
@dispatcher.span
async def astructured_predict(
    self,
    output_cls: Type[Model],
    prompt: PromptTemplate,
    llm_kwargs: Optional[Dict[str, Any]] = None,
    **prompt_args: Any,
) -> Model:
r"""
    Async Structured predict.

    Args:
        output_cls (BaseModel):
            Output class to use for structured prediction.
        prompt (PromptTemplate):
            Prompt template to use for structured prediction.
        llm_kwargs (Optional[Dict[str, Any]]):
            Arguments that are passed down to the LLM invoked by the program.
        prompt_args (Any):
            Additional arguments to format the prompt with.

    Returns:
        BaseModel: The structured prediction output.

    Examples:
        ```python
        from pydantic import BaseModel

        class Test(BaseModel):
            \"\"\"My test class.\"\"\"
            name: str

        from llama_index.core.prompts import PromptTemplate

        prompt = PromptTemplate("Please predict a Test with a random name related to {topic}.")
        output = await llm.astructured_predict(Test, prompt, topic="cats")
        print(output.name)
        ```

    """
    from llama_index.core.program.utils import get_program_for_llm

    dispatcher.event(
        LLMStructuredPredictStartEvent(
            output_cls=output_cls, template=prompt, template_args=prompt_args
        )
    )

    program = get_program_for_llm(
        output_cls,
        prompt,
        self,
        pydantic_program_mode=self.pydantic_program_mode,
    )

    result = await program.acall(llm_kwargs=llm_kwargs, **prompt_args)
    assert not isinstance(result, list)

    dispatcher.event(LLMStructuredPredictEndEvent(output=result))
    return result

```
  
---|---  
###  stream_structured_predict [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM.stream_structured_predict "Permanent link")
```
stream_structured_predict(output_cls: [], prompt: , llm_kwargs: Optional[[, ]] = None, **prompt_args: ) -> Generator[Union[, FlexibleModel], None, None]

```

Stream Structured predict.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`output_cls` |  `BaseModel` |  Output class to use for structured prediction. |  _required_  
`prompt` |  |  Prompt template to use for structured prediction. |  _required_  
`llm_kwargs` |  `Optional[Dict[str, Any]]` |  Arguments that are passed down to the LLM invoked by the program. |  `None`  
`prompt_args` |  Additional arguments to format the prompt with.  
Returns:
Name | Type | Description  
---|---|---  
`Generator` |  `None` |  A generator returning partial copies of the model or list of models.  
Examples:
```
from pydantic import BaseModel

class Test(BaseModel):
    \"\"\"My test class.\"\"\"
    name: str

from llama_index.core.prompts import PromptTemplate

prompt = PromptTemplate("Please predict a Test with a random name related to {topic}.")
stream_output = llm.stream_structured_predict(Test, prompt, topic="cats")
for partial_output in stream_output:
    # stream partial outputs until completion
    print(partial_output.name)

```

Source code in `llama_index/core/llms/llm.py`
```
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
```
| ```
@dispatcher.span
def stream_structured_predict(
    self,
    output_cls: Type[Model],
    prompt: PromptTemplate,
    llm_kwargs: Optional[Dict[str, Any]] = None,
    **prompt_args: Any,
) -> Generator[Union[Model, "FlexibleModel"], None, None]:
r"""
    Stream Structured predict.

    Args:
        output_cls (BaseModel):
            Output class to use for structured prediction.
        prompt (PromptTemplate):
            Prompt template to use for structured prediction.
        llm_kwargs (Optional[Dict[str, Any]]):
            Arguments that are passed down to the LLM invoked by the program.
        prompt_args (Any):
            Additional arguments to format the prompt with.

    Returns:
        Generator: A generator returning partial copies of the model or list of models.

    Examples:
        ```python
        from pydantic import BaseModel

        class Test(BaseModel):
            \"\"\"My test class.\"\"\"
            name: str

        from llama_index.core.prompts import PromptTemplate

        prompt = PromptTemplate("Please predict a Test with a random name related to {topic}.")
        stream_output = llm.stream_structured_predict(Test, prompt, topic="cats")
        for partial_output in stream_output:
            # stream partial outputs until completion
            print(partial_output.name)
        ```

    """
    dispatcher.event(
        LLMStructuredPredictStartEvent(
            output_cls=output_cls, template=prompt, template_args=prompt_args
        )
    )

    result = self._structured_stream_call(
        output_cls, prompt, llm_kwargs, **prompt_args
    )
    for r in result:
        dispatcher.event(LLMStructuredPredictInProgressEvent(output=r))
        assert not isinstance(r, list)
        yield r

    dispatcher.event(LLMStructuredPredictEndEvent(output=r))

```
  
---|---  
###  astream_structured_predict `async` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM.astream_structured_predict "Permanent link")
```
astream_structured_predict(output_cls: [], prompt: , llm_kwargs: Optional[[, ]] = None, **prompt_args: ) -> AsyncGenerator[Union[, FlexibleModel], None]

```

Async Stream Structured predict.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`output_cls` |  `BaseModel` |  Output class to use for structured prediction. |  _required_  
`prompt` |  |  Prompt template to use for structured prediction. |  _required_  
`llm_kwargs` |  `Optional[Dict[str, Any]]` |  Arguments that are passed down to the LLM invoked by the program. |  `None`  
`prompt_args` |  Additional arguments to format the prompt with.  
Returns:
Name | Type | Description  
---|---|---  
`Generator` |  `AsyncGenerator[Union[Model, FlexibleModel], None]` |  A generator returning partial copies of the model or list of models.  
Examples:
```
from pydantic import BaseModel

class Test(BaseModel):
    \"\"\"My test class.\"\"\"
    name: str

from llama_index.core.prompts import PromptTemplate

prompt = PromptTemplate("Please predict a Test with a random name related to {topic}.")
stream_output = await llm.astream_structured_predict(Test, prompt, topic="cats")
async for partial_output in stream_output:
    # stream partial outputs until completion
    print(partial_output.name)

```

Source code in `llama_index/core/llms/llm.py`
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
```
| ```
@dispatcher.span
async def astream_structured_predict(
    self,
    output_cls: Type[Model],
    prompt: PromptTemplate,
    llm_kwargs: Optional[Dict[str, Any]] = None,
    **prompt_args: Any,
) -> AsyncGenerator[Union[Model, "FlexibleModel"], None]:
r"""
    Async Stream Structured predict.

    Args:
        output_cls (BaseModel):
            Output class to use for structured prediction.
        prompt (PromptTemplate):
            Prompt template to use for structured prediction.
        llm_kwargs (Optional[Dict[str, Any]]):
            Arguments that are passed down to the LLM invoked by the program.
        prompt_args (Any):
            Additional arguments to format the prompt with.

    Returns:
        Generator: A generator returning partial copies of the model or list of models.

    Examples:
        ```python
        from pydantic import BaseModel

        class Test(BaseModel):
            \"\"\"My test class.\"\"\"
            name: str

        from llama_index.core.prompts import PromptTemplate

        prompt = PromptTemplate("Please predict a Test with a random name related to {topic}.")
        stream_output = await llm.astream_structured_predict(Test, prompt, topic="cats")
        async for partial_output in stream_output:
            # stream partial outputs until completion
            print(partial_output.name)
        ```

    """

    async def gen() -> AsyncGenerator[Union[Model, "FlexibleModel"], None]:
        dispatcher.event(
            LLMStructuredPredictStartEvent(
                output_cls=output_cls, template=prompt, template_args=prompt_args
            )
        )

        result = await self._structured_astream_call(
            output_cls, prompt, llm_kwargs, **prompt_args
        )
        async for r in result:
            dispatcher.event(LLMStructuredPredictInProgressEvent(output=r))
            assert not isinstance(r, list)
            yield r

        dispatcher.event(LLMStructuredPredictEndEvent(output=r))

    return gen()

```
  
---|---  
###  predict [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM.predict "Permanent link")
```
predict(prompt: , **prompt_args: ) -> 

```

Predict for a given prompt.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`prompt` |  |  The prompt to use for prediction. |  _required_  
`prompt_args` |  Additional arguments to format the prompt with.  
Returns:
Name | Type | Description  
---|---|---  
`str` |  The prediction output.  
Examples:
```
from llama_index.core.prompts import PromptTemplate

prompt = PromptTemplate("Please write a random name related to {topic}.")
output = llm.predict(prompt, topic="cats")
print(output)

```

Source code in `llama_index/core/llms/llm.py`
```
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
610
611
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
```
| ```
@dispatcher.span
def predict(
    self,
    prompt: BasePromptTemplate,
    **prompt_args: Any,
) -> str:
"""
    Predict for a given prompt.

    Args:
        prompt (BasePromptTemplate):
            The prompt to use for prediction.
        prompt_args (Any):
            Additional arguments to format the prompt with.

    Returns:
        str: The prediction output.

    Examples:
        ```python
        from llama_index.core.prompts import PromptTemplate

        prompt = PromptTemplate("Please write a random name related to {topic}.")
        output = llm.predict(prompt, topic="cats")
        print(output)
        ```

    """
    dispatcher.event(
        LLMPredictStartEvent(template=prompt, template_args=prompt_args)
    )
    self._log_template_data(prompt, **prompt_args)

    if self.metadata.is_chat_model:
        messages = self._get_messages(prompt, **prompt_args)
        chat_response = self.chat(messages)
        output = chat_response.message.content or ""
    else:
        formatted_prompt = self._get_prompt(prompt, **prompt_args)
        response = self.complete(formatted_prompt, formatted=True)
        output = response.text
    parsed_output = self._parse_output(output)
    dispatcher.event(LLMPredictEndEvent(output=parsed_output))
    return parsed_output

```
  
---|---  
###  stream [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM.stream "Permanent link")
```
stream(prompt: , **prompt_args: ) -> TokenGen

```

Stream predict for a given prompt.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`prompt` |  |  The prompt to use for prediction. |  _required_  
`prompt_args` |  Additional arguments to format the prompt with.  
Yields:
Name | Type | Description  
---|---|---  
`str` |  `TokenGen` |  Each streamed token.  
Examples:
```
from llama_index.core.prompts import PromptTemplate

prompt = PromptTemplate("Please write a random name related to {topic}.")
gen = llm.stream(prompt, topic="cats")
for token in gen:
    print(token, end="", flush=True)

```

Source code in `llama_index/core/llms/llm.py`
```
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
```
| ```
@dispatcher.span
def stream(
    self,
    prompt: BasePromptTemplate,
    **prompt_args: Any,
) -> TokenGen:
"""
    Stream predict for a given prompt.

    Args:
        prompt (BasePromptTemplate):
            The prompt to use for prediction.
        prompt_args (Any):
            Additional arguments to format the prompt with.

    Yields:
        str: Each streamed token.

    Examples:
        ```python
        from llama_index.core.prompts import PromptTemplate

        prompt = PromptTemplate("Please write a random name related to {topic}.")
        gen = llm.stream(prompt, topic="cats")
        for token in gen:
            print(token, end="", flush=True)
        ```

    """
    self._log_template_data(prompt, **prompt_args)

    dispatcher.event(
        LLMPredictStartEvent(template=prompt, template_args=prompt_args)
    )
    if self.metadata.is_chat_model:
        messages = self._get_messages(prompt, **prompt_args)
        chat_response = self.stream_chat(messages)
        stream_tokens = stream_chat_response_to_tokens(chat_response)
    else:
        formatted_prompt = self._get_prompt(prompt, **prompt_args)
        stream_response = self.stream_complete(formatted_prompt, formatted=True)
        stream_tokens = stream_completion_response_to_tokens(stream_response)

    if prompt.output_parser is not None or self.output_parser is not None:
        raise NotImplementedError("Output parser is not supported for streaming.")

    return stream_tokens

```
  
---|---  
###  apredict `async` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM.apredict "Permanent link")
```
apredict(prompt: , **prompt_args: ) -> 

```

Async Predict for a given prompt.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`prompt` |  |  The prompt to use for prediction. |  _required_  
`prompt_args` |  Additional arguments to format the prompt with.  
Returns:
Name | Type | Description  
---|---|---  
`str` |  The prediction output.  
Examples:
```
from llama_index.core.prompts import PromptTemplate

prompt = PromptTemplate("Please write a random name related to {topic}.")
output = await llm.apredict(prompt, topic="cats")
print(output)

```

Source code in `llama_index/core/llms/llm.py`
```
681
682
683
684
685
686
687
688
689
690
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
```
| ```
@dispatcher.span
async def apredict(
    self,
    prompt: BasePromptTemplate,
    **prompt_args: Any,
) -> str:
"""
    Async Predict for a given prompt.

    Args:
        prompt (BasePromptTemplate):
            The prompt to use for prediction.
        prompt_args (Any):
            Additional arguments to format the prompt with.

    Returns:
        str: The prediction output.

    Examples:
        ```python
        from llama_index.core.prompts import PromptTemplate

        prompt = PromptTemplate("Please write a random name related to {topic}.")
        output = await llm.apredict(prompt, topic="cats")
        print(output)
        ```

    """
    dispatcher.event(
        LLMPredictStartEvent(template=prompt, template_args=prompt_args)
    )
    self._log_template_data(prompt, **prompt_args)

    if self.metadata.is_chat_model:
        messages = self._get_messages(prompt, **prompt_args)
        chat_response = await self.achat(messages)
        output = chat_response.message.content or ""
    else:
        formatted_prompt = self._get_prompt(prompt, **prompt_args)
        response = await self.acomplete(formatted_prompt, formatted=True)
        output = response.text

    parsed_output = self._parse_output(output)
    dispatcher.event(LLMPredictEndEvent(output=parsed_output))
    return parsed_output

```
  
---|---  
###  astream `async` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM.astream "Permanent link")
```
astream(prompt: , **prompt_args: ) -> TokenAsyncGen

```

Async stream predict for a given prompt.
prompt (BasePromptTemplate): The prompt to use for prediction. prompt_args (Any): Additional arguments to format the prompt with.
Yields:
Name | Type | Description  
---|---|---  
`str` |  `TokenAsyncGen` |  An async generator that yields strings of tokens.  
Examples:
```
from llama_index.core.prompts import PromptTemplate

prompt = PromptTemplate("Please write a random name related to {topic}.")
gen = await llm.astream(prompt, topic="cats")
async for token in gen:
    print(token, end="", flush=True)

```

Source code in `llama_index/core/llms/llm.py`
```
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
```
| ```
@dispatcher.span
async def astream(
    self,
    prompt: BasePromptTemplate,
    **prompt_args: Any,
) -> TokenAsyncGen:
"""
    Async stream predict for a given prompt.

    Args:
    prompt (BasePromptTemplate):
        The prompt to use for prediction.
    prompt_args (Any):
        Additional arguments to format the prompt with.

    Yields:
        str: An async generator that yields strings of tokens.

    Examples:
        ```python
        from llama_index.core.prompts import PromptTemplate

        prompt = PromptTemplate("Please write a random name related to {topic}.")
        gen = await llm.astream(prompt, topic="cats")
        async for token in gen:
            print(token, end="", flush=True)
        ```

    """
    self._log_template_data(prompt, **prompt_args)

    dispatcher.event(
        LLMPredictStartEvent(template=prompt, template_args=prompt_args)
    )
    if self.metadata.is_chat_model:
        messages = self._get_messages(prompt, **prompt_args)
        chat_response = await self.astream_chat(messages)
        stream_tokens = await astream_chat_response_to_tokens(chat_response)
    else:
        formatted_prompt = self._get_prompt(prompt, **prompt_args)
        stream_response = await self.astream_complete(
            formatted_prompt, formatted=True
        )
        stream_tokens = await astream_completion_response_to_tokens(stream_response)

    if prompt.output_parser is not None or self.output_parser is not None:
        raise NotImplementedError("Output parser is not supported for streaming.")

    return stream_tokens

```
  
---|---  
###  predict_and_call [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM.predict_and_call "Permanent link")
```
predict_and_call(tools: [], user_msg: Optional[Union[, ]] = None, chat_history: Optional[[]] = None, verbose:  = False, **kwargs: ) -> 

```

Predict and call the tool.
By default uses a ReAct agent to do tool calling (through text prompting), but function calling LLMs will implement this differently.
Source code in `llama_index/core/llms/llm.py`
```
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
797
798
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
```
| ```
@dispatcher.span
def predict_and_call(
    self,
    tools: List["BaseTool"],
    user_msg: Optional[Union[str, ChatMessage]] = None,
    chat_history: Optional[List[ChatMessage]] = None,
    verbose: bool = False,
    **kwargs: Any,
) -> "AgentChatResponse":
"""
    Predict and call the tool.

    By default uses a ReAct agent to do tool calling (through text prompting),
    but function calling LLMs will implement this differently.

    """
    from llama_index.core.agent.workflow import ReActAgent
    from llama_index.core.chat_engine.types import AgentChatResponse
    from llama_index.core.memory import Memory
    from llama_index.core.tools.calling import call_tool_with_selection
    from llama_index.core.workflow import Context
    from workflows.context.state_store import DictState

    agent = ReActAgent(
        tools=tools,
        llm=self,
        verbose=verbose,
        formatter=kwargs.get("react_chat_formatter"),
        output_parser=kwargs.get("output_parser"),
        tool_retriever=kwargs.get("tool_retriever"),
    )

    memory = kwargs.get("memory", Memory.from_defaults())

    if isinstance(user_msg, ChatMessage) and isinstance(user_msg.content, str):
        pass
    elif isinstance(user_msg, str):
        user_msg = ChatMessage(content=user_msg, role=MessageRole.USER)

    llm_input = []
    if chat_history:
        llm_input.extend(chat_history)
    if user_msg:
        llm_input.append(user_msg)

    ctx: Context[DictState] = Context(agent)

    try:
        resp = asyncio_run(
            agent.take_step(
                ctx=ctx, llm_input=llm_input, tools=tools or [], memory=memory
            )
        )
        tool_outputs = []
        for tool_call in resp.tool_calls:
            tool_output = call_tool_with_selection(
                tool_call=tool_call,
                tools=tools or [],
                verbose=verbose,
            )
            tool_outputs.append(tool_output)
        output_text = "\n\n".join(
            [tool_output.content for tool_output in tool_outputs]
        )
        return AgentChatResponse(
            response=output_text,
            sources=tool_outputs,
        )
    except Exception as e:
        output = AgentChatResponse(
            response="An error occurred while running the tool: " + str(e),
            sources=[],
        )

    return output

```
  
---|---  
###  apredict_and_call `async` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM.apredict_and_call "Permanent link")
```
apredict_and_call(tools: [], user_msg: Optional[Union[, ]] = None, chat_history: Optional[[]] = None, verbose:  = False, **kwargs: ) -> 

```

Predict and call the tool.
Source code in `llama_index/core/llms/llm.py`
```
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
870
871
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
```
| ```
@dispatcher.span
async def apredict_and_call(
    self,
    tools: List["BaseTool"],
    user_msg: Optional[Union[str, ChatMessage]] = None,
    chat_history: Optional[List[ChatMessage]] = None,
    verbose: bool = False,
    **kwargs: Any,
) -> "AgentChatResponse":
"""Predict and call the tool."""
    from llama_index.core.agent.workflow import ReActAgent
    from llama_index.core.chat_engine.types import AgentChatResponse
    from llama_index.core.memory import Memory
    from llama_index.core.tools.calling import acall_tool_with_selection
    from llama_index.core.workflow import Context
    from workflows.context.state_store import DictState

    agent = ReActAgent(
        tools=tools,
        llm=self,
        verbose=verbose,
        formatter=kwargs.get("react_chat_formatter"),
        output_parser=kwargs.get("output_parser"),
        tool_retriever=kwargs.get("tool_retriever"),
    )

    memory = kwargs.get("memory", Memory.from_defaults())

    if isinstance(user_msg, ChatMessage) and isinstance(user_msg.content, str):
        pass
    elif isinstance(user_msg, str):
        user_msg = ChatMessage(content=user_msg, role=MessageRole.USER)

    llm_input = []
    if chat_history:
        llm_input.extend(chat_history)
    if user_msg:
        llm_input.append(user_msg)

    ctx: Context[DictState] = Context(agent)

    try:
        resp = await agent.take_step(
            ctx=ctx, llm_input=llm_input, tools=tools or [], memory=memory
        )
        tool_outputs = []
        for tool_call in resp.tool_calls:
            tool_output = await acall_tool_with_selection(
                tool_call=tool_call,
                tools=tools or [],
                verbose=verbose,
            )
            tool_outputs.append(tool_output)

        output_text = "\n\n".join(
            [tool_output.content for tool_output in tool_outputs]
        )
        return AgentChatResponse(
            response=output_text,
            sources=tool_outputs,
        )
    except Exception as e:
        output = AgentChatResponse(
            response="An error occurred while running the tool: " + str(e),
            sources=[],
        )

    return output

```
  
---|---  
###  as_structured_llm [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM.as_structured_llm "Permanent link")
```
as_structured_llm(output_cls: [BaseModel], **kwargs: ) -> StructuredLLM

```

Return a structured LLM around a given object.
Source code in `llama_index/core/llms/llm.py`
```
922
923
924
925
926
927
928
929
930
```
| ```
def as_structured_llm(
    self,
    output_cls: Type[BaseModel],
    **kwargs: Any,
) -> "StructuredLLM":
"""Return a structured LLM around a given object."""
    from llama_index.core.llms.structured_llm import StructuredLLM

    return StructuredLLM(llm=self, output_cls=output_cls, **kwargs)

```
  
---|---  
##  stream_completion_response_to_tokens [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.stream_completion_response_to_tokens "Permanent link")
```
stream_completion_response_to_tokens(completion_response_gen: CompletionResponseGen) -> TokenGen

```

Convert a stream completion response to a stream of tokens.
Source code in `llama_index/core/llms/llm.py`
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
108
```
| ```
def stream_completion_response_to_tokens(
    completion_response_gen: CompletionResponseGen,
) -> TokenGen:
"""Convert a stream completion response to a stream of tokens."""

    def gen() -> TokenGen:
        for response in completion_response_gen:
            yield response.delta or ""

    return gen()

```
  
---|---  
##  stream_chat_response_to_tokens [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.stream_chat_response_to_tokens "Permanent link")
```
stream_chat_response_to_tokens(chat_response_gen: ChatResponseGen) -> TokenGen

```

Convert a stream completion response to a stream of tokens.
Source code in `llama_index/core/llms/llm.py`
```
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
```
| ```
def stream_chat_response_to_tokens(
    chat_response_gen: ChatResponseGen,
) -> TokenGen:
"""Convert a stream completion response to a stream of tokens."""

    def gen() -> TokenGen:
        for response in chat_response_gen:
            yield response.delta or ""

    return gen()

```
  
---|---  
##  astream_completion_response_to_tokens `async` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.astream_completion_response_to_tokens "Permanent link")
```
astream_completion_response_to_tokens(completion_response_gen: CompletionResponseAsyncGen) -> TokenAsyncGen

```

Convert a stream completion response to a stream of tokens.
Source code in `llama_index/core/llms/llm.py`
```
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
```
| ```
async def astream_completion_response_to_tokens(
    completion_response_gen: CompletionResponseAsyncGen,
) -> TokenAsyncGen:
"""Convert a stream completion response to a stream of tokens."""

    async def gen() -> TokenAsyncGen:
        async for response in completion_response_gen:
            yield response.delta or ""

    return gen()

```
  
---|---  
##  astream_chat_response_to_tokens `async` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.astream_chat_response_to_tokens "Permanent link")
```
astream_chat_response_to_tokens(chat_response_gen: ChatResponseAsyncGen) -> TokenAsyncGen

```

Convert a stream completion response to a stream of tokens.
Source code in `llama_index/core/llms/llm.py`
```
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
```
| ```
async def astream_chat_response_to_tokens(
    chat_response_gen: ChatResponseAsyncGen,
) -> TokenAsyncGen:
"""Convert a stream completion response to a stream of tokens."""

    async def gen() -> TokenAsyncGen:
        async for response in chat_response_gen:
            yield response.delta or ""

    return gen()

```
  
---|---  
options: members: - LLM show_source: false inherited_members: true
##  MessageRole [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.MessageRole "Permanent link")
Bases: `str`, `Enum`
Message role.
Source code in `llama_index/core/base/llms/types.py`
```
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
```
| ```
class MessageRole(str, Enum):
"""Message role."""

    SYSTEM = "system"
    DEVELOPER = "developer"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"
    TOOL = "tool"
    CHATBOT = "chatbot"
    MODEL = "model"

```
  
---|---  
##  TextBlock [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.TextBlock "Permanent link")
Bases: `BaseModel`
A representation of text data to directly pass to/from the LLM.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`block_type` |  `Literal['text']` |  `'text'`  
`text` |  _required_  
Source code in `llama_index/core/base/llms/types.py`
```
52
53
54
55
56
```
| ```
class TextBlock(BaseModel):
"""A representation of text data to directly pass to/from the LLM."""

    block_type: Literal["text"] = "text"
    text: str

```
  
---|---  
##  ImageBlock [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ImageBlock "Permanent link")
Bases: `BaseModel`
A representation of image data to directly pass to/from the LLM.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`block_type` |  `Literal['image']` |  `'image'`  
`image` |  `bytes | None` |  `None`  
`path` |  `Annotated[Path, PathType] | None` |  `None`  
`url` |  `AnyUrl | str | None` |  `None`  
`image_mimetype` |  `str | None` |  `None`  
`detail` |  `str | None` |  `None`  
Source code in `llama_index/core/base/llms/types.py`
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
```
| ```
class ImageBlock(BaseModel):
"""A representation of image data to directly pass to/from the LLM."""

    block_type: Literal["image"] = "image"
    image: bytes | IOBase | None = None
    path: FilePath | None = None
    url: AnyUrl | str | None = None
    image_mimetype: str | None = None
    detail: str | None = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("url", mode="after")
    @classmethod
    def urlstr_to_anyurl(cls, url: str | AnyUrl | None) -> AnyUrl | None:
"""Store the url as Anyurl."""
        if isinstance(url, AnyUrl):
            return url
        if url is None:
            return None

        return AnyUrl(url=url)

    @field_serializer("image")
    def serialize_image(self, image: bytes | IOBase | None) -> bytes | None:
"""Serialize the image field."""
        if isinstance(image, bytes):
            return image
        if isinstance(image, IOBase):
            image.seek(0)
            return image.read()
        return None

    @model_validator(mode="after")
    def image_to_base64(self) -> Self:
"""
        Store the image as base64 and guess the mimetype when possible.

        In case the model was built passing image data but without a mimetype,
        we try to guess it using the filetype library. To avoid resource-intense
        operations, we won't load the path or the URL to guess the mimetype.
        """
        if not self.image or not isinstance(self.image, bytes):
            if not self.image_mimetype:
                path = self.path or self.url
                if path:
                    suffix = Path(str(path)).suffix.replace(".", "") or None
                    mimetype = filetype.get_type(ext=suffix)
                    if mimetype and str(mimetype.mime).startswith("image/"):
                        self.image_mimetype = str(mimetype.mime)

            return self

        try:
            # Check if self.image is already base64 encoded.
            # b64decode() can succeed on random binary data, so we
            # pass verify=True to make sure it's not a false positive
            decoded_img = base64.b64decode(self.image, validate=True)
        except BinasciiError:
            decoded_img = self.image
            self.image = base64.b64encode(self.image)

        self._guess_mimetype(decoded_img)
        return self

    def _guess_mimetype(self, img_data: bytes) -> None:
        if not self.image_mimetype:
            guess = filetype.guess(img_data)
            self.image_mimetype = guess.mime if guess else None

    def resolve_image(self, as_base64: bool = False) -> IOBase:
"""
        Resolve an image such that PIL can read it.

        Args:
            as_base64 (bool): whether the resolved image should be returned as base64-encoded bytes

        """
        data_buffer = (
            self.image
            if isinstance(self.image, IOBase)
            else resolve_binary(
                raw_bytes=self.image,
                path=self.path,
                url=str(self.url) if self.url else None,
                as_base64=as_base64,
            )
        )

        # Check size by seeking to end and getting position
        data_buffer.seek(0, 2)  # Seek to end
        size = data_buffer.tell()
        data_buffer.seek(0)  # Reset to beginning

        if size == 0:
            raise ValueError("resolve_image returned zero bytes")
        return data_buffer

```
  
---|---  
###  urlstr_to_anyurl `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ImageBlock.urlstr_to_anyurl "Permanent link")
```
urlstr_to_anyurl(url:  | AnyUrl | None) -> AnyUrl | None

```

Store the url as Anyurl.
Source code in `llama_index/core/base/llms/types.py`
```
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
```
| ```
@field_validator("url", mode="after")
@classmethod
def urlstr_to_anyurl(cls, url: str | AnyUrl | None) -> AnyUrl | None:
"""Store the url as Anyurl."""
    if isinstance(url, AnyUrl):
        return url
    if url is None:
        return None

    return AnyUrl(url=url)

```
  
---|---  
###  serialize_image [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ImageBlock.serialize_image "Permanent link")
```
serialize_image(image: bytes | IOBase | None) -> bytes | None

```

Serialize the image field.
Source code in `llama_index/core/base/llms/types.py`
```
82
83
84
85
86
87
88
89
90
```
| ```
@field_serializer("image")
def serialize_image(self, image: bytes | IOBase | None) -> bytes | None:
"""Serialize the image field."""
    if isinstance(image, bytes):
        return image
    if isinstance(image, IOBase):
        image.seek(0)
        return image.read()
    return None

```
  
---|---  
###  image_to_base64 [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ImageBlock.image_to_base64 "Permanent link")
```
image_to_base64() -> 

```

Store the image as base64 and guess the mimetype when possible.
In case the model was built passing image data but without a mimetype, we try to guess it using the filetype library. To avoid resource-intense operations, we won't load the path or the URL to guess the mimetype.
Source code in `llama_index/core/base/llms/types.py`
```
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
```
| ```
@model_validator(mode="after")
def image_to_base64(self) -> Self:
"""
    Store the image as base64 and guess the mimetype when possible.

    In case the model was built passing image data but without a mimetype,
    we try to guess it using the filetype library. To avoid resource-intense
    operations, we won't load the path or the URL to guess the mimetype.
    """
    if not self.image or not isinstance(self.image, bytes):
        if not self.image_mimetype:
            path = self.path or self.url
            if path:
                suffix = Path(str(path)).suffix.replace(".", "") or None
                mimetype = filetype.get_type(ext=suffix)
                if mimetype and str(mimetype.mime).startswith("image/"):
                    self.image_mimetype = str(mimetype.mime)

        return self

    try:
        # Check if self.image is already base64 encoded.
        # b64decode() can succeed on random binary data, so we
        # pass verify=True to make sure it's not a false positive
        decoded_img = base64.b64decode(self.image, validate=True)
    except BinasciiError:
        decoded_img = self.image
        self.image = base64.b64encode(self.image)

    self._guess_mimetype(decoded_img)
    return self

```
  
---|---  
###  resolve_image [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ImageBlock.resolve_image "Permanent link")
```
resolve_image(as_base64:  = False) -> IOBase

```

Resolve an image such that PIL can read it.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`as_base64` |  `bool` |  whether the resolved image should be returned as base64-encoded bytes |  `False`  
Source code in `llama_index/core/base/llms/types.py`
```
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
```
| ```
def resolve_image(self, as_base64: bool = False) -> IOBase:
"""
    Resolve an image such that PIL can read it.

    Args:
        as_base64 (bool): whether the resolved image should be returned as base64-encoded bytes

    """
    data_buffer = (
        self.image
        if isinstance(self.image, IOBase)
        else resolve_binary(
            raw_bytes=self.image,
            path=self.path,
            url=str(self.url) if self.url else None,
            as_base64=as_base64,
        )
    )

    # Check size by seeking to end and getting position
    data_buffer.seek(0, 2)  # Seek to end
    size = data_buffer.tell()
    data_buffer.seek(0)  # Reset to beginning

    if size == 0:
        raise ValueError("resolve_image returned zero bytes")
    return data_buffer

```
  
---|---  
##  AudioBlock [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.AudioBlock "Permanent link")
Bases: `BaseModel`
A representation of audio data to directly pass to/from the LLM.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`block_type` |  `Literal['audio']` |  `'audio'`  
`audio` |  `bytes | None` |  `None`  
`path` |  `Annotated[Path, PathType] | None` |  `None`  
`url` |  `AnyUrl | str | None` |  `None`  
`format` |  `str | None` |  `None`  
Source code in `llama_index/core/base/llms/types.py`
```
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
```
| ```
class AudioBlock(BaseModel):
"""A representation of audio data to directly pass to/from the LLM."""

    block_type: Literal["audio"] = "audio"
    audio: bytes | IOBase | None = None
    path: FilePath | None = None
    url: AnyUrl | str | None = None
    format: str | None = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("url", mode="after")
    @classmethod
    def urlstr_to_anyurl(cls, url: str | AnyUrl) -> AnyUrl:
"""Store the url as Anyurl."""
        if isinstance(url, AnyUrl):
            return url
        return AnyUrl(url=url)

    @field_serializer("audio")
    def serialize_audio(self, audio: bytes | IOBase | None) -> bytes | None:
"""Serialize the audio field."""
        if isinstance(audio, bytes):
            return audio
        if isinstance(audio, IOBase):
            audio.seek(0)
            return audio.read()
        return None

    @model_validator(mode="after")
    def audio_to_base64(self) -> Self:
"""
        Store the audio as base64 and guess the mimetype when possible.

        In case the model was built passing audio data but without a mimetype,
        we try to guess it using the filetype library. To avoid resource-intense
        operations, we won't load the path or the URL to guess the mimetype.
        """
        if not self.audio or not isinstance(self.audio, bytes):
            return self

        try:
            # Check if audio is already base64 encoded
            decoded_audio = base64.b64decode(self.audio)
        except Exception:
            decoded_audio = self.audio
            # Not base64 - encode it
            self.audio = base64.b64encode(self.audio)

        self._guess_format(decoded_audio)

        return self

    def _guess_format(self, audio_data: bytes) -> None:
        if not self.format:
            guess = filetype.guess(audio_data)
            self.format = guess.extension if guess else None

    def resolve_audio(self, as_base64: bool = False) -> IOBase:
"""
        Resolve an audio such that PIL can read it.

        Args:
            as_base64 (bool): whether the resolved audio should be returned as base64-encoded bytes

        """
        data_buffer = (
            self.audio
            if isinstance(self.audio, IOBase)
            else resolve_binary(
                raw_bytes=self.audio,
                path=self.path,
                url=str(self.url) if self.url else None,
                as_base64=as_base64,
            )
        )
        # Check size by seeking to end and getting position
        data_buffer.seek(0, 2)  # Seek to end
        size = data_buffer.tell()
        data_buffer.seek(0)  # Reset to beginning

        if size == 0:
            raise ValueError("resolve_audio returned zero bytes")
        return data_buffer

```
  
---|---  
###  urlstr_to_anyurl `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.AudioBlock.urlstr_to_anyurl "Permanent link")
```
urlstr_to_anyurl(url:  | AnyUrl) -> AnyUrl

```

Store the url as Anyurl.
Source code in `llama_index/core/base/llms/types.py`
```
169
170
171
172
173
174
175
```
| ```
@field_validator("url", mode="after")
@classmethod
def urlstr_to_anyurl(cls, url: str | AnyUrl) -> AnyUrl:
"""Store the url as Anyurl."""
    if isinstance(url, AnyUrl):
        return url
    return AnyUrl(url=url)

```
  
---|---  
###  serialize_audio [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.AudioBlock.serialize_audio "Permanent link")
```
serialize_audio(audio: bytes | IOBase | None) -> bytes | None

```

Serialize the audio field.
Source code in `llama_index/core/base/llms/types.py`
```
177
178
179
180
181
182
183
184
185
```
| ```
@field_serializer("audio")
def serialize_audio(self, audio: bytes | IOBase | None) -> bytes | None:
"""Serialize the audio field."""
    if isinstance(audio, bytes):
        return audio
    if isinstance(audio, IOBase):
        audio.seek(0)
        return audio.read()
    return None

```
  
---|---  
###  audio_to_base64 [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.AudioBlock.audio_to_base64 "Permanent link")
```
audio_to_base64() -> 

```

Store the audio as base64 and guess the mimetype when possible.
In case the model was built passing audio data but without a mimetype, we try to guess it using the filetype library. To avoid resource-intense operations, we won't load the path or the URL to guess the mimetype.
Source code in `llama_index/core/base/llms/types.py`
```
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
```
| ```
@model_validator(mode="after")
def audio_to_base64(self) -> Self:
"""
    Store the audio as base64 and guess the mimetype when possible.

    In case the model was built passing audio data but without a mimetype,
    we try to guess it using the filetype library. To avoid resource-intense
    operations, we won't load the path or the URL to guess the mimetype.
    """
    if not self.audio or not isinstance(self.audio, bytes):
        return self

    try:
        # Check if audio is already base64 encoded
        decoded_audio = base64.b64decode(self.audio)
    except Exception:
        decoded_audio = self.audio
        # Not base64 - encode it
        self.audio = base64.b64encode(self.audio)

    self._guess_format(decoded_audio)

    return self

```
  
---|---  
###  resolve_audio [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.AudioBlock.resolve_audio "Permanent link")
```
resolve_audio(as_base64:  = False) -> IOBase

```

Resolve an audio such that PIL can read it.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`as_base64` |  `bool` |  whether the resolved audio should be returned as base64-encoded bytes |  `False`  
Source code in `llama_index/core/base/llms/types.py`
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
```
| ```
def resolve_audio(self, as_base64: bool = False) -> IOBase:
"""
    Resolve an audio such that PIL can read it.

    Args:
        as_base64 (bool): whether the resolved audio should be returned as base64-encoded bytes

    """
    data_buffer = (
        self.audio
        if isinstance(self.audio, IOBase)
        else resolve_binary(
            raw_bytes=self.audio,
            path=self.path,
            url=str(self.url) if self.url else None,
            as_base64=as_base64,
        )
    )
    # Check size by seeking to end and getting position
    data_buffer.seek(0, 2)  # Seek to end
    size = data_buffer.tell()
    data_buffer.seek(0)  # Reset to beginning

    if size == 0:
        raise ValueError("resolve_audio returned zero bytes")
    return data_buffer

```
  
---|---  
##  VideoBlock [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.VideoBlock "Permanent link")
Bases: `BaseModel`
A representation of video data to directly pass to/from the LLM.
Source code in `llama_index/core/base/llms/types.py`
```
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
```
| ```
class VideoBlock(BaseModel):
"""A representation of video data to directly pass to/from the LLM."""

    block_type: Literal["video"] = "video"
    video: bytes | IOBase | None = None
    path: FilePath | None = None
    url: AnyUrl | str | None = None
    video_mimetype: str | None = None
    detail: str | None = None
    fps: int | None = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("url", mode="after")
    @classmethod
    def urlstr_to_anyurl(cls, url: str | AnyUrl | None) -> AnyUrl | None:
"""Store the url as AnyUrl."""
        if isinstance(url, AnyUrl):
            return url
        if url is None:
            return None
        return AnyUrl(url=url)

    @field_serializer("video")
    def serialize_video(self, video: bytes | IOBase | None) -> bytes | None:
"""Serialize the video field."""
        if isinstance(video, bytes):
            return video
        if isinstance(video, IOBase):
            video.seek(0)
            return video.read()
        return None

    @model_validator(mode="after")
    def video_to_base64(self) -> "VideoBlock":
"""
        Store the video as base64 and guess the mimetype when possible.

        If video data is passed but no mimetype is provided, try to infer it.
        """
        if not self.video or not isinstance(self.video, bytes):
            if not self.video_mimetype:
                path = self.path or self.url
                if path:
                    suffix = Path(str(path)).suffix.replace(".", "") or None
                    mimetype = filetype.get_type(ext=suffix)
                    if mimetype and str(mimetype.mime).startswith("video/"):
                        self.video_mimetype = str(mimetype.mime)
            return self

        try:
            decoded_vid = base64.b64decode(self.video, validate=True)
        except BinasciiError:
            decoded_vid = self.video
            self.video = base64.b64encode(self.video)

        self._guess_mimetype(decoded_vid)
        return self

    def _guess_mimetype(self, vid_data: bytes) -> None:
        if not self.video_mimetype:
            guess = filetype.guess(vid_data)
            if guess and guess.mime.startswith("video/"):
                self.video_mimetype = guess.mime

    def resolve_video(self, as_base64: bool = False) -> IOBase:
"""
        Resolve a video file to a IOBase buffer.

        Args:
            as_base64 (bool): whether to return the video as base64-encoded bytes

        """
        data_buffer = (
            self.video
            if isinstance(self.video, IOBase)
            else resolve_binary(
                raw_bytes=self.video,
                path=self.path,
                url=str(self.url) if self.url else None,
                as_base64=as_base64,
            )
        )

        # Check size by seeking to end and getting position
        data_buffer.seek(0, 2)  # Seek to end
        size = data_buffer.tell()
        data_buffer.seek(0)  # Reset to beginning

        if size == 0:
            raise ValueError("resolve_video returned zero bytes")
        return data_buffer

```
  
---|---  
###  urlstr_to_anyurl `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.VideoBlock.urlstr_to_anyurl "Permanent link")
```
urlstr_to_anyurl(url:  | AnyUrl | None) -> AnyUrl | None

```

Store the url as AnyUrl.
Source code in `llama_index/core/base/llms/types.py`
```
257
258
259
260
261
262
263
264
265
```
| ```
@field_validator("url", mode="after")
@classmethod
def urlstr_to_anyurl(cls, url: str | AnyUrl | None) -> AnyUrl | None:
"""Store the url as AnyUrl."""
    if isinstance(url, AnyUrl):
        return url
    if url is None:
        return None
    return AnyUrl(url=url)

```
  
---|---  
###  serialize_video [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.VideoBlock.serialize_video "Permanent link")
```
serialize_video(video: bytes | IOBase | None) -> bytes | None

```

Serialize the video field.
Source code in `llama_index/core/base/llms/types.py`
```
267
268
269
270
271
272
273
274
275
```
| ```
@field_serializer("video")
def serialize_video(self, video: bytes | IOBase | None) -> bytes | None:
"""Serialize the video field."""
    if isinstance(video, bytes):
        return video
    if isinstance(video, IOBase):
        video.seek(0)
        return video.read()
    return None

```
  
---|---  
###  video_to_base64 [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.VideoBlock.video_to_base64 "Permanent link")
```
video_to_base64() -> 'VideoBlock'

```

Store the video as base64 and guess the mimetype when possible.
If video data is passed but no mimetype is provided, try to infer it.
Source code in `llama_index/core/base/llms/types.py`
```
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
```
| ```
@model_validator(mode="after")
def video_to_base64(self) -> "VideoBlock":
"""
    Store the video as base64 and guess the mimetype when possible.

    If video data is passed but no mimetype is provided, try to infer it.
    """
    if not self.video or not isinstance(self.video, bytes):
        if not self.video_mimetype:
            path = self.path or self.url
            if path:
                suffix = Path(str(path)).suffix.replace(".", "") or None
                mimetype = filetype.get_type(ext=suffix)
                if mimetype and str(mimetype.mime).startswith("video/"):
                    self.video_mimetype = str(mimetype.mime)
        return self

    try:
        decoded_vid = base64.b64decode(self.video, validate=True)
    except BinasciiError:
        decoded_vid = self.video
        self.video = base64.b64encode(self.video)

    self._guess_mimetype(decoded_vid)
    return self

```
  
---|---  
###  resolve_video [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.VideoBlock.resolve_video "Permanent link")
```
resolve_video(as_base64:  = False) -> IOBase

```

Resolve a video file to a IOBase buffer.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`as_base64` |  `bool` |  whether to return the video as base64-encoded bytes |  `False`  
Source code in `llama_index/core/base/llms/types.py`
```
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
```
| ```
def resolve_video(self, as_base64: bool = False) -> IOBase:
"""
    Resolve a video file to a IOBase buffer.

    Args:
        as_base64 (bool): whether to return the video as base64-encoded bytes

    """
    data_buffer = (
        self.video
        if isinstance(self.video, IOBase)
        else resolve_binary(
            raw_bytes=self.video,
            path=self.path,
            url=str(self.url) if self.url else None,
            as_base64=as_base64,
        )
    )

    # Check size by seeking to end and getting position
    data_buffer.seek(0, 2)  # Seek to end
    size = data_buffer.tell()
    data_buffer.seek(0)  # Reset to beginning

    if size == 0:
        raise ValueError("resolve_video returned zero bytes")
    return data_buffer

```
  
---|---  
##  DocumentBlock [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.DocumentBlock "Permanent link")
Bases: `BaseModel`
A representation of a document to directly pass to the LLM.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`block_type` |  `Literal['document']` |  `'document'`  
`data` |  `bytes | None` |  `None`  
`path` |  `Annotated[Path, PathType] | str | None` |  `None`  
`url` |  `str | None` |  `None`  
`title` |  `str | None` |  `None`  
`document_mimetype` |  `str | None` |  `None`  
Source code in `llama_index/core/base/llms/types.py`
```
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
```
| ```
class DocumentBlock(BaseModel):
"""A representation of a document to directly pass to the LLM."""

    block_type: Literal["document"] = "document"
    data: bytes | IOBase | None = None
    path: Optional[Union[FilePath | str]] = None
    url: Optional[str] = None
    title: Optional[str] = None
    document_mimetype: Optional[str] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @model_validator(mode="after")
    def document_validation(self) -> Self:
        self.document_mimetype = self.document_mimetype or self._guess_mimetype()

        if not self.title:
            self.title = "input_document"

        # skip data validation if no byte is provided
        if not self.data or not isinstance(self.data, bytes):
            return self

        try:
            decoded_document = base64.b64decode(self.data, validate=True)
        except BinasciiError:
            self.data = base64.b64encode(self.data)

        return self

    @field_serializer("data")
    def serialize_data(self, data: bytes | IOBase | None) -> bytes | None:
"""Serialize the data field."""
        if isinstance(data, bytes):
            return data
        if isinstance(data, IOBase):
            data.seek(0)
            return data.read()
        return None

    def resolve_document(self) -> IOBase:
"""
        Resolve a document such that it is represented by a BufferIO object.
        """
        data_buffer = (
            self.data
            if isinstance(self.data, IOBase)
            else resolve_binary(
                raw_bytes=self.data,
                path=self.path,
                url=str(self.url) if self.url else None,
                as_base64=False,
            )
        )
        # Check size by seeking to end and getting position
        data_buffer.seek(0, 2)  # Seek to end
        size = data_buffer.tell()
        data_buffer.seek(0)  # Reset to beginning

        if size == 0:
            raise ValueError("resolve_document returned zero bytes")
        return data_buffer

    def _get_b64_string(self, data_buffer: IOBase) -> str:
"""
        Get base64-encoded string from a IOBase buffer.
        """
        data = data_buffer.read()
        return base64.b64encode(data).decode("utf-8")

    def _get_b64_bytes(self, data_buffer: IOBase) -> bytes:
"""
        Get base64-encoded bytes from a IOBase buffer.
        """
        data = data_buffer.read()
        return base64.b64encode(data)

    def guess_format(self) -> str | None:
        path = self.path or self.url
        if not path:
            return None

        return Path(str(path)).suffix.replace(".", "")

    def _guess_mimetype(self) -> str | None:
        if self.data:
            guess = filetype.guess(self.data)
            return str(guess.mime) if guess else None

        suffix = self.guess_format()
        if not suffix:
            return None

        guess = filetype.get_type(ext=suffix)
        return str(guess.mime) if guess else None

```
  
---|---  
###  serialize_data [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.DocumentBlock.serialize_data "Permanent link")
```
serialize_data(data: bytes | IOBase | None) -> bytes | None

```

Serialize the data field.
Source code in `llama_index/core/base/llms/types.py`
```
368
369
370
371
372
373
374
375
376
```
| ```
@field_serializer("data")
def serialize_data(self, data: bytes | IOBase | None) -> bytes | None:
"""Serialize the data field."""
    if isinstance(data, bytes):
        return data
    if isinstance(data, IOBase):
        data.seek(0)
        return data.read()
    return None

```
  
---|---  
###  resolve_document [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.DocumentBlock.resolve_document "Permanent link")
```
resolve_document() -> IOBase

```

Resolve a document such that it is represented by a BufferIO object.
Source code in `llama_index/core/base/llms/types.py`
```
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
```
| ```
def resolve_document(self) -> IOBase:
"""
    Resolve a document such that it is represented by a BufferIO object.
    """
    data_buffer = (
        self.data
        if isinstance(self.data, IOBase)
        else resolve_binary(
            raw_bytes=self.data,
            path=self.path,
            url=str(self.url) if self.url else None,
            as_base64=False,
        )
    )
    # Check size by seeking to end and getting position
    data_buffer.seek(0, 2)  # Seek to end
    size = data_buffer.tell()
    data_buffer.seek(0)  # Reset to beginning

    if size == 0:
        raise ValueError("resolve_document returned zero bytes")
    return data_buffer

```
  
---|---  
##  CacheControl [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.CacheControl "Permanent link")
Bases: `BaseModel`
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`type` |  _required_  
`ttl` |  `'5m'`  
Source code in `llama_index/core/base/llms/types.py`
```
435
436
437
```
| ```
class CacheControl(BaseModel):
    type: str
    ttl: str = Field(default="5m")

```
  
---|---  
##  CachePoint [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.CachePoint "Permanent link")
Bases: `BaseModel`
Used to set the point to cache up to, if the LLM supports caching.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`block_type` |  `Literal['cache']` |  `'cache'`  
`cache_control` |  |  _required_  
Source code in `llama_index/core/base/llms/types.py`
```
440
441
442
443
444
```
| ```
class CachePoint(BaseModel):
"""Used to set the point to cache up to, if the LLM supports caching."""

    block_type: Literal["cache"] = "cache"
    cache_control: CacheControl

```
  
---|---  
##  CitableBlock [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.CitableBlock "Permanent link")
Bases: `BaseModel`
Supports providing citable content to LLMs that have built-in citation support.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`block_type` |  `Literal['citable']` |  `'citable'`  
`title` |  _required_  
`source` |  _required_  
`content` |  `List[Annotated[Union[TextBlock[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.TextBlock "llama_index.core.base.llms.types.TextBlock"), ImageBlock[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ImageBlock "llama_index.core.base.llms.types.ImageBlock"), DocumentBlock[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.DocumentBlock "llama_index.core.base.llms.types.DocumentBlock")], FieldInfo]]` |  _required_  
Source code in `llama_index/core/base/llms/types.py`
```
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
```
| ```
class CitableBlock(BaseModel):
"""Supports providing citable content to LLMs that have built-in citation support."""

    block_type: Literal["citable"] = "citable"
    title: str
    source: str
    # TODO: We could maybe expand the types here,
    # limiting for now to known use cases
    content: List[
        Annotated[
            Union[TextBlock, ImageBlock, DocumentBlock],
            Field(discriminator="block_type"),
        ]
    ]

    @field_validator("content", mode="before")
    @classmethod
    def validate_content(cls, v: Any) -> Any:
        if isinstance(v, str):
            return [TextBlock(text=v)]

        return v

```
  
---|---  
##  CitationBlock [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.CitationBlock "Permanent link")
Bases: `BaseModel`
A representation of cited content from past messages.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`block_type` |  `Literal['citation']` |  `'citation'`  
`cited_content` |  |  _required_  
`source` |  _required_  
`title` |  _required_  
`additional_location_info` |  `Dict[str, int]` |  _required_  
Source code in `llama_index/core/base/llms/types.py`
```
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
```
| ```
class CitationBlock(BaseModel):
"""A representation of cited content from past messages."""

    block_type: Literal["citation"] = "citation"
    cited_content: Annotated[
        Union[TextBlock, ImageBlock], Field(discriminator="block_type")
    ]
    source: str
    title: str
    additional_location_info: Dict[str, int]

    @field_validator("cited_content", mode="before")
    @classmethod
    def validate_cited_content(cls, v: Any) -> Any:
        if isinstance(v, str):
            return TextBlock(text=v)

        return v

```
  
---|---  
##  ThinkingBlock [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ThinkingBlock "Permanent link")
Bases: `BaseModel`
A representation of the content streamed from reasoning/thinking processes by LLMs
Source code in `llama_index/core/base/llms/types.py`
```
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
```
| ```
class ThinkingBlock(BaseModel):
"""A representation of the content streamed from reasoning/thinking processes by LLMs"""

    block_type: Literal["thinking"] = "thinking"
    content: Optional[str] = Field(
        description="Content of the reasoning/thinking process, if available",
        default=None,
    )
    num_tokens: Optional[int] = Field(
        description="Number of token used for reasoning/thinking, if available",
        default=None,
    )
    additional_information: Dict[str, Any] = Field(
        description="Additional information related to the thinking/reasoning process, if available",
        default_factory=dict,
    )

```
  
---|---  
##  ChatMessage [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "Permanent link")
Bases: `BaseModel`
Chat message.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`role` |  |  `<MessageRole.USER: 'user'>`  
`blocks` |  `list[Annotated[Union[TextBlock[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.TextBlock "llama_index.core.base.llms.types.TextBlock"), ImageBlock[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ImageBlock "llama_index.core.base.llms.types.ImageBlock"), AudioBlock[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.AudioBlock "llama_index.core.base.llms.types.AudioBlock"), DocumentBlock[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.DocumentBlock "llama_index.core.base.llms.types.DocumentBlock"), CachePoint[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.CachePoint "llama_index.core.base.llms.types.CachePoint"), CitableBlock[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.CitableBlock "llama_index.core.base.llms.types.CitableBlock"), CitationBlock[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.CitationBlock "llama_index.core.base.llms.types.CitationBlock")], FieldInfo]]` |  Built-in mutable sequence. If no argument is given, the constructor creates a new empty list. The argument must be an iterable if specified. |  `<dynamic>`  
Source code in `llama_index/core/base/llms/types.py`
```
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
610
611
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
```
| ```
class ChatMessage(BaseModel):
"""Chat message."""

    role: MessageRole = MessageRole.USER
    additional_kwargs: dict[str, Any] = Field(default_factory=dict)
    blocks: list[ContentBlock] = Field(default_factory=list)

    def __init__(self, /, content: Any | None = None, **data: Any) -> None:
"""
        Keeps backward compatibility with the old `content` field.

        If content was passed and contained text, store a single TextBlock.
        If content was passed and it was a list, assume it's a list of content blocks and store it.
        """
        if content is not None:
            if isinstance(content, str):
                data["blocks"] = [TextBlock(text=content)]
            elif isinstance(content, list):
                data["blocks"] = content

        super().__init__(**data)

    @model_validator(mode="after")
    def legacy_additional_kwargs_image(self) -> Self:
"""
        Provided for backward compatibility.

        If `additional_kwargs` contains an `images` key, assume the value is a list
        of ImageDocument and convert them into image blocks.
        """
        if documents := self.additional_kwargs.get("images"):
            documents = cast(list[ImageDocument], documents)
            for doc in documents:
                img_base64_bytes = doc.resolve_image(as_base64=True).read()
                self.blocks.append(ImageBlock(image=img_base64_bytes))
        return self

    @property
    def content(self) -> str | None:
"""
        Keeps backward compatibility with the old `content` field.

        Returns:
            The cumulative content of the TextBlock blocks, None if there are none.

        """
        content_strs = []
        for block in self.blocks:
            if isinstance(block, TextBlock):
                content_strs.append(block.text)

        ct = "\n".join(content_strs) or None
        if ct is None and len(content_strs) == 1:
            return ""
        return ct

    @content.setter
    def content(self, content: str) -> None:
"""
        Keeps backward compatibility with the old `content` field.

        Raises:
            ValueError: if blocks contains more than a block, or a block that's not TextBlock.

        """
        if not self.blocks:
            self.blocks = [TextBlock(text=content)]
        elif len(self.blocks) == 1 and isinstance(self.blocks[0], TextBlock):
            self.blocks = [TextBlock(text=content)]
        else:
            raise ValueError(
                "ChatMessage contains multiple blocks, use 'ChatMessage.blocks' instead."
            )

    def __str__(self) -> str:
        return f"{self.role.value}: {self.content}"

    @classmethod
    def from_str(
        cls,
        content: str,
        role: Union[MessageRole, str] = MessageRole.USER,
        **kwargs: Any,
    ) -> Self:
        if isinstance(role, str):
            role = MessageRole(role)
        return cls(role=role, blocks=[TextBlock(text=content)], **kwargs)

    def _recursive_serialization(self, value: Any) -> Any:
        if isinstance(value, BaseModel):
            value.model_rebuild()  # ensures all fields are initialized and serializable
            return value.model_dump()  # type: ignore
        if isinstance(value, dict):
            return {
                key: self._recursive_serialization(value)
                for key, value in value.items()
            }
        if isinstance(value, list):
            return [self._recursive_serialization(item) for item in value]

        if isinstance(value, bytes):
            return base64.b64encode(value).decode("utf-8")

        return value

    @field_serializer("additional_kwargs", check_fields=False)
    def serialize_additional_kwargs(self, value: Any, _info: Any) -> Any:
        return self._recursive_serialization(value)

```
  
---|---  
###  content `property` `writable` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage.content "Permanent link")
```
content:  | None

```

Keeps backward compatibility with the old `content` field.
Returns:
Type | Description  
---|---  
`str | None` |  The cumulative content of the TextBlock blocks, None if there are none.  
###  legacy_additional_kwargs_image [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage.legacy_additional_kwargs_image "Permanent link")
```
legacy_additional_kwargs_image() -> 

```

Provided for backward compatibility.
If `additional_kwargs` contains an `images` key, assume the value is a list of ImageDocument and convert them into image blocks.
Source code in `llama_index/core/base/llms/types.py`
```
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
```
| ```
@model_validator(mode="after")
def legacy_additional_kwargs_image(self) -> Self:
"""
    Provided for backward compatibility.

    If `additional_kwargs` contains an `images` key, assume the value is a list
    of ImageDocument and convert them into image blocks.
    """
    if documents := self.additional_kwargs.get("images"):
        documents = cast(list[ImageDocument], documents)
        for doc in documents:
            img_base64_bytes = doc.resolve_image(as_base64=True).read()
            self.blocks.append(ImageBlock(image=img_base64_bytes))
    return self

```
  
---|---  
##  LogProb [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.LogProb "Permanent link")
Bases: `BaseModel`
LogProb of a token.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`logprob` |  `float` |  Convert a string or number to a floating point number, if possible. |  `<dynamic>`  
`bytes` |  `List[int]` |  Built-in mutable sequence. If no argument is given, the constructor creates a new empty list. The argument must be an iterable if specified. |  `<dynamic>`  
Source code in `llama_index/core/base/llms/types.py`
```
648
649
650
651
652
653
```
| ```
class LogProb(BaseModel):
"""LogProb of a token."""

    token: str = Field(default_factory=str)
    logprob: float = Field(default_factory=float)
    bytes: List[int] = Field(default_factory=list)

```
  
---|---  
##  ChatResponse [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatResponse "Permanent link")
Bases: `BaseModel`
Chat response.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`message` |  |  _required_  
`raw` |  `Any | None` |  `None`  
`delta` |  `str | None` |  `None`  
`logprobs` |  `List[List[LogProb[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.LogProb "llama_index.core.base.llms.types.LogProb")]] | None` |  `None`  
Source code in `llama_index/core/base/llms/types.py`
```
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
```
| ```
class ChatResponse(BaseModel):
"""Chat response."""

    message: ChatMessage
    raw: Optional[Any] = None
    delta: Optional[str] = None
    logprobs: Optional[List[List[LogProb]]] = None
    additional_kwargs: dict = Field(default_factory=dict)

    def __str__(self) -> str:
        return str(self.message)

```
  
---|---  
##  CompletionResponse [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.CompletionResponse "Permanent link")
Bases: `BaseModel`
Completion response.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`text` |  _required_  
`raw` |  `Any | None` |  `None`  
`logprobs` |  `List[List[LogProb[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.LogProb "llama_index.core.base.llms.types.LogProb")]] | None` |  `None`  
`delta` |  `str | None` |  `None`  
Fields
text: Text content of the response if not streaming, or if streaming, the current extent of streamed text. additional_kwargs: Additional information on the response(i.e. token counts, function calling information). raw: Optional raw JSON that was parsed to populate text, if relevant. delta: New text that just streamed in (only relevant when streaming).
Source code in `llama_index/core/base/llms/types.py`
```
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
689
690
691
692
693
694
695
```
| ```
class CompletionResponse(BaseModel):
"""
    Completion response.

    Fields:
        text: Text content of the response if not streaming, or if streaming,
            the current extent of streamed text.
        additional_kwargs: Additional information on the response(i.e. token
            counts, function calling information).
        raw: Optional raw JSON that was parsed to populate text, if relevant.
        delta: New text that just streamed in (only relevant when streaming).
    """

    text: str
    additional_kwargs: dict = Field(default_factory=dict)
    raw: Optional[Any] = None
    logprobs: Optional[List[List[LogProb]]] = None
    delta: Optional[str] = None

    def __str__(self) -> str:
        return self.text

```
  
---|---  
##  LLMMetadata [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.LLMMetadata "Permanent link")
Bases: `BaseModel`
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`context_window` |  Total number of tokens the model can be input and output for one response. |  `3900`  
`num_output` |  Number of tokens the model can output when generating a response. |  `256`  
`is_chat_model` |  `bool` |  Set True if the model exposes a chat interface (i.e. can be passed a sequence of messages, rather than text), like OpenAI's /v1/chat/completions endpoint. |  `False`  
`is_function_calling_model` |  `bool` |  Set True if the model supports function calling messages, similar to OpenAI's function calling API. For example, converting 'Email Anya to see if she wants to get coffee next Friday' to a function call like `send_email(to: string, body: string)`. |  `False`  
`model_name` |  The model's name used for logging, testing, and sanity checking. For some models this can be automatically discerned. For other models, like locally loaded models, this must be manually specified. |  `'unknown'`  
`system_role` |  |  The role this specific LLM providerexpects for system prompt. E.g. 'SYSTEM' for OpenAI, 'CHATBOT' for Cohere |  `<MessageRole.SYSTEM: 'system'>`  
Source code in `llama_index/core/base/llms/types.py`
```
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
```
| ```
class LLMMetadata(BaseModel):
    model_config = ConfigDict(
        protected_namespaces=("pydantic_model_",), arbitrary_types_allowed=True
    )
    context_window: int = Field(
        default=DEFAULT_CONTEXT_WINDOW,
        description=(
            "Total number of tokens the model can be input and output for one response."
        ),
    )
    num_output: int = Field(
        default=DEFAULT_NUM_OUTPUTS,
        description="Number of tokens the model can output when generating a response.",
    )
    is_chat_model: bool = Field(
        default=False,
        description=(
            "Set True if the model exposes a chat interface (i.e. can be passed a"
            " sequence of messages, rather than text), like OpenAI's"
            " /v1/chat/completions endpoint."
        ),
    )
    is_function_calling_model: bool = Field(
        default=False,
        # SEE: https://openai.com/blog/function-calling-and-other-api-updates
        description=(
            "Set True if the model supports function calling messages, similar to"
            " OpenAI's function calling API. For example, converting 'Email Anya to"
            " see if she wants to get coffee next Friday' to a function call like"
            " `send_email(to: string, body: string)`."
        ),
    )
    model_name: str = Field(
        default="unknown",
        description=(
            "The model's name used for logging, testing, and sanity checking. For some"
            " models this can be automatically discerned. For other models, like"
            " locally loaded models, this must be manually specified."
        ),
    )
    system_role: MessageRole = Field(
        default=MessageRole.SYSTEM,
        description="The role this specific LLM provider"
        "expects for system prompt. E.g. 'SYSTEM' for OpenAI, 'CHATBOT' for Cohere",
    )

```
  
---|---
