from dataclasses import dataclass
from TOKENS import Token

@dataclass
class UnaryOpNode:
  op_token : Token
  node     : Token
  
  def __repr__(self) -> str:
    return f'{self.op_token}: {self.node}'

 
@dataclass
class NumberNode:
  token: Token
  
  def __repr__(self) -> str:
    return f'{self.token}'


@dataclass
class BinaryOpNode:
  left_node  : UnaryOpNode|NumberNode
  op_token   : Token
  right_node : UnaryOpNode|NumberNode
  
  def __repr__(self) -> str:
    return f'({self.left_node}, {self.op_token}, {self.right_node})'
    
@dataclass
class VariableAssignNode:
  variable_name : Token
  variable_value: Token
  

@dataclass
class VariableAccessNode:
  variable: Token = Token