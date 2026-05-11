from dataclasses import dataclass, field
from typing_extensions import Any

import httpx
from typed_core.http import HttpClient


@dataclass
class HttpMixin:
  """Compatibility mixin backed by the shared typed-core HTTP client."""
  base_url: str
  http: HttpClient = field(kw_only=True, default_factory=HttpClient)

  async def __aenter__(self):
    await self.http.__aenter__()
    return self

  async def __aexit__(self, exc_type, exc_value, traceback):
    await self.http.__aexit__(exc_type, exc_value, traceback)

  async def request(
    self, method: str, url: str, /, *,
    json: Any | None = None,
    params: dict[str, Any] | None = None,
  ) -> httpx.Response:
    """Send an HTTP request relative to this mixin base URL."""
    return await self.http.request(
      method, self.base_url + url, json=json, params=params,
    )
