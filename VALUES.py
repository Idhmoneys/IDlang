from typing import Self
from ERRORS import RuntimeError

class Number:
  def __init__(self, value: int|str) -> None:
    self.value: int|str = value
  
  def __repr__(self) -> str:
    return f'{self.value}'
    
  def add(self, other: Self|None) -> Self:
    if isinstance(other, Number):
      return Number(self.value + other.value), None
      # None = Errornya
      
  def subtract(self, other: Self|None) -> Self:
    if isinstance(other, Number):
      return Number(self.value - other.value), None
      
  def multiply(self, other: Self|None) -> Self:
    if isinstance(other, Number):
      return Number(self.value * other.value), None
      
  def divide(self, other: Self|None) -> Self:
    if isinstance(other, Number):
      if other.value == 0:
        return None, RuntimeError("Tidak bisa membagikan angka dengan angka '0'")
      return Number(self.value / other.value), None