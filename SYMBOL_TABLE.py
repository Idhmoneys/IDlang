from typing import Self, Any
from TOKENS import Token
class SymbolTable:
  def __init__(self) -> None:
    self.symbols: dict[str, int|str|float]      = {}
    self.parent : dict[str, int|str|float]|None = None
  
  def take(self, variable: str) -> int|str|None:
    """Mengambil nilai dari suatu variable"""
    value: int|str|None = self.symbols.get(variable, None)
    if value is None and self.parent:
      return self.parent.get(variable)
      
    return value
  
  def make(self, name: str, value: int|str) -> None:
    """Membuat variable baru"""
    self.symbols[name] = value
    
  def delete(self, name: str) -> None:
    """Menghapus sebuah variable"""
    del self.symbols[name]