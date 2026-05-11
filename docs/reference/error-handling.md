# Error Handling

Typed Clients should distinguish between failure modes clearly.

## Common Error Categories

- `NetworkError`: connection failures, timeouts, transport errors
- `AuthError`: missing credentials, invalid signatures, rejected authentication
- `ApiError`: the remote API returned an application-level error
- `ValidationError`: the response shape did not match the expected schema
- `BadRequest`: invalid request or rejected client input
- `RateLimited`: Alchemy rate-limit response
- `LogicError`: local SDK logic error

## Recommended Pattern

```python
from alchemy import ApiError, AuthError, NetworkError, RateLimited, ValidationError

try:
  ...
except ValidationError:
  ...
except RateLimited:
  ...
except AuthError:
  ...
except ApiError:
  ...
except NetworkError:
  ...
```

## Operational Guidance

- retry transient network failures carefully
- do not blindly retry authentication failures
- log validation failures because they often signal upstream API changes
- include request identifiers from the exchange when available
