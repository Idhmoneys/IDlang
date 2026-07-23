from dataclasses import dataclass

@dataclass
class UnaryOpNode:
  op_token: str
  node: str
  
  def __repr__(self):
    return f'{self.op_token}: {self.node}'

@dataclass
class BinaryOpNode:
  left_node: UnaryOpNode
  op_token: str
  right_node: UnaryOpNode
  
  def __repr__(self):
    return f'({self.left_node}, {self.op_token}, {self.right_node})'
  
@dataclass
class NumberNode:
  token: str
  
  def __repr__(self) -> None:
    return f'{self.token}'