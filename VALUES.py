from typing import Self

class Number:
  def __init__(self, value: int|str) -> None:
    self.value: int|str = value
  
  def __repr__(self) -> str:
    return f'{self.value}'
    
  def add(self, other: Self|None) -> Self:
    if isinstance(other, Number):
      return Number(self.value + other.value)
      
  def subtract(self, other: Self|None) -> Self:
    if isinstance(other, Number):
      return Number(self.value - other.value)
      
  def multiply(self, other: Self|None) -> Self:
    if isinstance(other, Number):
      return Number(self.value * other.value)
      
  def divide(self, other: Self|None) -> Self:
    if isinstance(other, Number):
      return Number(self.value / other.value)