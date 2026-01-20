# Retry policy
##  RetryPolicy [#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.RetryPolicy "Permanent link")
Bases: `Protocol`
Policy interface to control step retries after failures.
Implementations decide whether to retry and how long to wait before the next attempt based on elapsed time, number of attempts, and the last error.
See Also

Source code in `workflows/retry_policy.py`
```
 9
10
11
12
13
14
15
16
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
34
35
```
| ```
@runtime_checkable
classRetryPolicy(Protocol):
"""
    Policy interface to control step retries after failures.

    Implementations decide whether to retry and how long to wait before the next
    attempt based on elapsed time, number of attempts, and the last error.

    See Also:
        - [ConstantDelayRetryPolicy][workflows.retry_policy.ConstantDelayRetryPolicy]
        - [step][workflows.decorators.step]
    """

    defnext(
        self, elapsed_time: float, attempts: int, error: Exception
    ) -> float | None:
"""
        Decide if another retry should occur and the delay before it.

        Args:
            elapsed_time (float): Seconds since the first failure.
            attempts (int): Number of attempts made so far.
            error (Exception): The last exception encountered.

        Returns:
            float | None: Seconds to wait before retrying, or `None` to stop.
        """

```
  
---|---  
###  next [#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.RetryPolicy.next "Permanent link")
```
next(elapsed_time: float, attempts: , error: Exception) -> float | None

```

Decide if another retry should occur and the delay before it.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`elapsed_time` |  `float` |  Seconds since the first failure. |  _required_  
`attempts` |  Number of attempts made so far. |  _required_  
`error` |  `Exception` |  The last exception encountered. |  _required_  
Returns:
Type | Description  
---|---  
`float | None` |  float | None: Seconds to wait before retrying, or `None` to stop.  
Source code in `workflows/retry_policy.py`
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
```
| ```
defnext(
    self, elapsed_time: float, attempts: int, error: Exception
) -> float | None:
"""
    Decide if another retry should occur and the delay before it.

    Args:
        elapsed_time (float): Seconds since the first failure.
        attempts (int): Number of attempts made so far.
        error (Exception): The last exception encountered.

    Returns:
        float | None: Seconds to wait before retrying, or `None` to stop.
    """

```
  
---|---  
##  ConstantDelayRetryPolicy [#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.ConstantDelayRetryPolicy "Permanent link")
Retry at a fixed interval up to a maximum number of attempts.
Examples:
```
@step(retry_policy=ConstantDelayRetryPolicy(delay=5, maximum_attempts=10))
async defflaky(self, ev: StartEvent) -> StopEvent:
    ...

```

Source code in `workflows/retry_policy.py`
```
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
```
| ```
classConstantDelayRetryPolicy:
"""Retry at a fixed interval up to a maximum number of attempts.

    Examples:
        ```python
        @step(retry_policy=ConstantDelayRetryPolicy(delay=5, maximum_attempts=10))
        async def flaky(self, ev: StartEvent) -> StopEvent:

        ```
    """

    def__init__(self, maximum_attempts: int = 3, delay: float = 5) -> None:
"""
        Initialize the policy.

        Args:
            maximum_attempts (int): Maximum consecutive attempts. Defaults to 3.
            delay (float): Seconds to wait between attempts. Defaults to 5.
        """
        self.maximum_attempts = maximum_attempts
        self.delay = delay

    defnext(
        self, elapsed_time: float, attempts: int, error: Exception
    ) -> float | None:
"""Return the fixed delay while attempts remain; otherwise `None`."""
        if attempts >= self.maximum_attempts:
            return None

        return self.delay

```
  
---|---  
###  next [#](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.ConstantDelayRetryPolicy.next "Permanent link")
```
next(elapsed_time: float, attempts: , error: Exception) -> float | None

```

Return the fixed delay while attempts remain; otherwise `None`.
Source code in `workflows/retry_policy.py`
```
60
61
62
63
64
65
66
67
```
| ```
defnext(
    self, elapsed_time: float, attempts: int, error: Exception
) -> float | None:
"""Return the fixed delay while attempts remain; otherwise `None`."""
    if attempts >= self.maximum_attempts:
        return None

    return self.delay

```
  
---|---
