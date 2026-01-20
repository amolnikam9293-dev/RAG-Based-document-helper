# Errors
##  WorkflowValidationError [#](https://developers.llamaindex.ai/python/workflows-api-reference/errors/#workflows.errors.WorkflowValidationError "Permanent link")
Bases: `Exception`
Raised when the workflow configuration or step signatures are invalid.
Source code in `workflows/errors.py`
```
classWorkflowValidationError(Exception):
"""Raised when the workflow configuration or step signatures are invalid."""

```
  
---  
##  WorkflowTimeoutError [#](https://developers.llamaindex.ai/python/workflows-api-reference/errors/#workflows.errors.WorkflowTimeoutError "Permanent link")
Bases: `Exception`
Raised when a workflow run exceeds the configured timeout.
Source code in `workflows/errors.py`
```
classWorkflowTimeoutError(Exception):
"""Raised when a workflow run exceeds the configured timeout."""

```
  
---  
##  WorkflowRuntimeError [#](https://developers.llamaindex.ai/python/workflows-api-reference/errors/#workflows.errors.WorkflowRuntimeError "Permanent link")
Bases: `Exception`
Raised for runtime errors during step execution or event routing.
Source code in `workflows/errors.py`
```
13
14
```
| ```
classWorkflowRuntimeError(Exception):
"""Raised for runtime errors during step execution or event routing."""

```
  
---|---  
##  WorkflowDone [#](https://developers.llamaindex.ai/python/workflows-api-reference/errors/#workflows.errors.WorkflowDone "Permanent link")
Bases: `Exception`
Internal control-flow exception used to terminate workers at run end.
Source code in `workflows/errors.py`
```
17
18
```
| ```
classWorkflowDone(Exception):
"""Internal control-flow exception used to terminate workers at run end."""

```
  
---|---  
##  WorkflowCancelledByUser [#](https://developers.llamaindex.ai/python/workflows-api-reference/errors/#workflows.errors.WorkflowCancelledByUser "Permanent link")
Bases: `Exception`
Raised when a run is cancelled via the handler or programmatically.
Source code in `workflows/errors.py`
```
21
22
```
| ```
classWorkflowCancelledByUser(Exception):
"""Raised when a run is cancelled via the handler or programmatically."""

```
  
---|---  
##  WorkflowStepDoesNotExistError [#](https://developers.llamaindex.ai/python/workflows-api-reference/errors/#workflows.errors.WorkflowStepDoesNotExistError "Permanent link")
Bases: `Exception`
Raised when addressing a step that does not exist in the workflow.
Source code in `workflows/errors.py`
```
25
26
```
| ```
classWorkflowStepDoesNotExistError(Exception):
"""Raised when addressing a step that does not exist in the workflow."""

```
  
---|---  
##  WorkflowConfigurationError [#](https://developers.llamaindex.ai/python/workflows-api-reference/errors/#workflows.errors.WorkflowConfigurationError "Permanent link")
Bases: `Exception`
Raised when a logical configuration error is detected pre-run.
Source code in `workflows/errors.py`
```
29
30
```
| ```
classWorkflowConfigurationError(Exception):
"""Raised when a logical configuration error is detected pre-run."""

```
  
---|---  
##  ContextSerdeError [#](https://developers.llamaindex.ai/python/workflows-api-reference/errors/#workflows.errors.ContextSerdeError "Permanent link")
Bases: `Exception`
Raised when serializing/deserializing a `Context` fails.
Source code in `workflows/errors.py`
```
33
34
```
| ```
classContextSerdeError(Exception):
"""Raised when serializing/deserializing a `Context` fails."""

```
  
---|---
