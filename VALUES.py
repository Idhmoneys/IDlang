from typing import Self
from ERRORS import RuntimeError

class Number:
  def __init__(self, value: int|float) -> None:
    self.value: int|float = value
  
  def __repr__(self) -> str:
    return f'{self.value}'
    
  def add(self, other: Self|None) -> tuple["Number | None", RuntimeError | None]:
    if isinstance(other, Number):
      return Number(self.value + other.value), None
    return None, RuntimeError(f"'{self.value}' + '{other.value}'")
      # None = Errornya
      
  def subtract(self, other: Self|None) -> tuple["Number | None", RuntimeError | None]:
    if isinstance(other, Number):
      return Number(self.value - other.value), None
    return None, RuntimeError(f"'{self.value}' - '{other.value}'")
      
  def multiply(self, other: Self|None) -> tuple["Number | None", RuntimeError | None]:
    if isinstance(other, Number):
      return Number(self.value * other.value), None
    return None, RuntimeError(f"'{self.value}' * '{other.value}'")
      
  def divide(self, other: Self|None|int|float) -> tuple["Number | None", RuntimeError | None]:
    if isinstance(other, Number):
      if other.value == 0:
        return None, RuntimeError("Tidak bisa membagikan angka dengan angka '0'")
      return Number(self.value / other.value), None
    return None, RuntimeError(f"'{self.value}' / '{other.value}'")
      
  def power(self, other: Self|None) -> tuple["Number | None", RuntimeError | None]:
    if isinstance(other, Number):
      return Number(self.value ** other.value), None
    return None, RuntimeError(f"'{self.value}' ^ '{other.value}'")
      
  def mod(self, other: Self|None) -> tuple["Number | None", RuntimeError | None]:
    if isinstance(other, Number):
      return Number(self.value % other.value), None
    return None, RuntimeError(f"'{self.value}' % '{other.value}'")
    
  def greater_than(self, other: Self|None) -> tuple["Number | None", RuntimeError | None]:
    if isinstance(other, Number):
      return Number(int(self.value > other.value)), None
    return None, RuntimeError(f"'{self.value}' > '{other.value}'")
      
  def greater_than_equal(self, other: Self|None) -> tuple["Number | None", RuntimeError | None]:
    if isinstance(other, Number):
      return Number(int(self.value >= other.value)), None
    return None, RuntimeError(f"'{self.value}' >= '{other.value}'")
      
  def less_than(self, other: Self|None) -> tuple["Number | None", RuntimeError | None]:
    if isinstance(other, Number):
      return Number(int(self.value < other.value)), None
    return None, RuntimeError(f"'{self.value}' < '{other.value}'")
      
  def less_than_equal(self, other: Self|None) -> tuple["Number | None", RuntimeError | None]:
    if isinstance(other, Number):
      return Number(int(self.value <= other.value)), None
    return None, RuntimeError(f"'{self.value}' <= '{other.value}'")
      
  def is_equal(self, other: Self|None) -> tuple["Number | None", RuntimeError | None]:
    if isinstance(other, Number):
      return Number(int(self.value == other.value)), None
    return None, RuntimeError(f"'{self.value}' == '{other.value}'")
      
  def not_equal(self, other: Self|None) -> tuple["Number | None", RuntimeError | None]:
    if isinstance(other, Number):
      return Number(int(self.value != other.value)), None
    return None, RuntimeError(f"'{self.value}' != '{other.value}'")
      
  def notted(self) -> tuple["Number | None", RuntimeError | None]:
    return Number(0 if self.value > 0 else 1), None
  
    
  def and_(self, other: Self|None) -> tuple["Number | None", RuntimeError | None]:
    if isinstance(other, Number):
      return Number(int(self.value and other.value)), None
    return None, RuntimeError(f"'{self.value}' and '{other.value}'")
      
  def or_(self, other: Self|None) -> tuple["Number | None", RuntimeError | None]:
    if isinstance(other, Number):
      return Number(int(self.value or other.value)), None
    return None, RuntimeError(f"'{self.value}' or '{other.value}'")