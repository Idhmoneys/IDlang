from idlang.errors import Error
from idlang.tokens import Token
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
  
  def success(self, value: Token) -> Self:
    self.node = value
    return self
  
  def failure(self, error: Error) -> Self:
    self.error = error
    return self


    
class RuntimeResult:
  def __init__(self):
    self.node: None|Token = None
    self.error: None|Error = None
    
  def __repr__(self) -> str:
    return f'{self.node= }, {self.error= }'
    
  #====================================================#

  def register(self, result: Any) -> Self:
    if result.error:
      self.error: Error = result.error
    return result.value
    
  def success(self, value: Token) -> Self:
    self.value: Token = value
    return self
    
  def failure(self, error: Error) -> Self:
    self.error: Error = error
    return self
  