from ERRORS import Error
from TOKENS import Token
from typing import Self

class ParseResult:
  def __init__(self) -> None:
    self.node:  None|Token  = None
    self.error: None|Error  = None
    
  def __repr__(self) -> str:
    return f'{self.node= }, {self.error= }'
  
  #====================================================#
  
  def register(self, node: any) -> Token:
    if isinstance(node, ParseResult):
      self.error: Error|None = node.error if node.error else self.error
      return node.node
    return node
  
  def success(self, value: any) -> Self:
    self.node: Token = value
    return self
  
  def failure(self, error: any) -> Self:
    self.error: Error = error
    return self
    
class RuntimeResult:
  def __init__(self):
    self.node = None
    self.error = None
    
  def __repr__(self) -> str:
    return f'{self.node= }, {self.error= }'
    
  #====================================================#

  def register(self, result):
    self.error = result.error if result.error else self.error
    return result.value
    
  def success(self, value):
    self.value = value
    return self
    
  def failure(self, error):
    self.error = error
    return self
  