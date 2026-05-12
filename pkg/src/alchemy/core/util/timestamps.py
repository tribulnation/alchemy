import time
from datetime import UTC, datetime

class timestamp:
  @staticmethod
  def parse(value: datetime | int | float | str) -> datetime:
    if isinstance(value, datetime):
      return value
    if isinstance(value, int | float):
      return datetime.fromtimestamp(value / 1e3, UTC)
    try:
      return datetime.fromtimestamp(int(value) / 1e3, UTC)
    except ValueError:
      return datetime.fromisoformat(value.replace('Z', '+00:00'))
  
  @staticmethod
  def dump(dt: datetime) -> int:
    return int(1e3*dt.timestamp())
  
  @staticmethod
  def now() -> int:
    return int(time.time() * 1e3)
