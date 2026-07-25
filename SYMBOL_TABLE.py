from typing import Self
from TOKENS import Token
class SymbolTable:
  def __init__(self) -> None:
    self.symbols: dict[str, int|str] = {}
    self.parent : Self = None
  
  def take(self, variable: str) -> Token:
    """Mengambil nilai dari suatu variable"""
    value: Token = self.symbols.get(variable, None)
    if value is None and self.parent:
      return self.parent.get(variable)
      
    return value
  
  def make(self, name: str, value: int|str) -> None:
    """Membuat variable baru"""
    self.symbols[name] = value
    
  def delete(self, name: str) -> None:
    """Menghapus sebuah variable"""
    del self.symbol[name]