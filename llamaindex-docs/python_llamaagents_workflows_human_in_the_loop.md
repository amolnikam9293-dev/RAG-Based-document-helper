[Skip to content](https://developers.llamaindex.ai/python/llamaagents/workflows/human_in_the_loop/#_top)
# Human in the Loop
Since workflows are so flexible, there are many possible ways to implement human-in-the-loop patterns.
The easiest way to implement a human-in-the-loop is to use the `InputRequiredEvent` and `HumanResponseEvent` events during event streaming.
```


from workflows.events import InputRequiredEvent, HumanResponseEvent






classHumanInTheLoopWorkflow(Workflow):




@step




asyncdefstep1(self, ev: StartEvent) -> InputRequiredEvent:




returnInputRequiredEvent(prefix="Enter a number: ")





@step




asyncdefstep2(self, ev: HumanResponseEvent) -> StopEvent:




returnStopEvent(result=ev.response)





# workflow should work with streaming



workflow =HumanInTheLoopWorkflow()





handler = workflow.run()




asyncfor event in handler.stream_events():




ifisinstance(event, InputRequiredEvent):




# here, we can handle human input however you want




# this means using input(), websockets, accessing async state, etc.




# here, we just use input()




response =input(event.prefix)




handler.ctx.send_event(HumanResponseEvent(response=response))





final_result =await handler


```

Here, the workflow will wait until the `HumanResponseEvent` is emitted.
If needed, you can also subclass these two events to add custom payloads.
## Stopping/Resuming Between Human Responses
[Section titled “Stopping/Resuming Between Human Responses”](https://developers.llamaindex.ai/python/llamaagents/workflows/human_in_the_loop/#stoppingresuming-between-human-responses)
Also note that you can break out of the loop, and resume it later. This is useful if you want to pause the workflow to wait for a human response, but continue the workflow later.
```


handler = workflow.run()




asyncfor event in handler.stream_events():




ifisinstance(event, InputRequiredEvent):




# Serialize the context, store it anywhere as a JSON blob




ctx_dict = handler.ctx.to_dict()




await handler.cancel_run()




break




...



# now we handle the human response once it comes in



response =input(event.prefix)





restored_ctx = Context.from_dict(workflow, ctx_dict)




handler = workflow.run=restored_ctx)




# Send the event to resume the workflow



handler.ctx.send_event(HumanResponseEvent(response=response))




# now we resume the workflow streaming with our restored context



asyncfor event in handler.stream_events():




continue





final_result =await handler


```

