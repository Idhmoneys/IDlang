from ERRORS import Error
from TOKENS import Token
from typing import Self, Any

class ParseResult:
  def __init__(self) -> None:
    self.node:  None|Token  = None
    self.error: None|Error  = None
    
  def __repr__(self) -> str:
    return f'{self.node= }, {self.error= }'
  
  #====================================================#
  
  def register(self, node: Token) -> Token | None:
    if not isinstance(node, ParseResult):
      return node
    if node.error:
      self.error = node.error
    return node.node
  
  def success(self, value: Any) -> Self:
    self.node = value
    return self
  
  def failure(self, error: Any) -> Self:
    self.error = error
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
  