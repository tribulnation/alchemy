from typing_extensions import TypeVar, Generic, Any, TypedDict as _TypedDict, Annotated
from pydantic import with_config, ConfigDict, BeforeValidator
from datetime import datetime

from typed_core.exceptions import ValidationError
from .util.timestamps import timestamp as ts

@with_config(ConfigDict(extra='allow'))
class TypedDict(_TypedDict):
  ...

Timestamp = Annotated[datetime, BeforeValidator(ts.parse)]

T = TypeVar('T')

class validator(Generic[T]):

  def __init__(self, Type: Any):
    from pydantic import TypeAdapter
    self.adapter = TypeAdapter(Type)
    
  def json(self, data: str | bytes | bytearray) -> T:
    from pydantic import ValidationError as PydanticValidationError
    try:
      return self.adapter.validate_json(data)
    except PydanticValidationError as e:
      raise ValidationError(*e.args) from e

  def python(self, data: Any) -> T:
    from pydantic import ValidationError as PydanticValidationError
    try:
      return self.adapter.validate_python(data)
    except PydanticValidationError as e:
      raise ValidationError(*e.args) from e
    
  def __call__(self, data) -> T:
    if isinstance(data, str | bytes | bytearray):
      return self.json(data)
    else:
      return self.python(data)
