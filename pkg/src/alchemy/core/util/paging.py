from typing_extensions import AsyncIterable, AsyncIterator, TypeVar, Generic, Sequence, Awaitable, Callable
from dataclasses import dataclass

T = TypeVar('T')
S = TypeVar('S')

@dataclass
class PaginatedResponse(AsyncIterable[Sequence[T]], Awaitable[Sequence[T]], Generic[T, S]):
  init: S
  next: Callable[[S], Awaitable[tuple[Sequence[T], S | None]]]
  
  def __aiter__(self) -> AsyncIterator[Sequence[T]]:
    async def iterate():
      state = self.init
      while True:
        page, next_state = await self.next(state)
        yield page
        if next_state is None or next_state == '':
          break
        state = next_state
    return iterate().__aiter__()

  def __await__(self):
    async def sync():
      out: list[T] = []
      async for page in self:
        out.extend(page)
      return out
    return sync().__await__()
