import NODES
from ERRORS import NoVisitMethod
from VALUES import Number
from TOKENS import Token

class Interpreter:
  def visit(self, node: NODES) -> Number|NoVisitMethod|int|None:
    method: str = f'visit_{type(node).__name__}' 
    # type bakal keluarin class nya, contoh <class 'NODES.NumberNode'>
    # __name__ bakal keluarin nama class nya, contoh BinaryOpNode
    method: callable = getattr(self, method, self.no_visit)
    # fungsi getattr mirip kayak . nya class/object, kayak self.var
    # getattr(self, result, self.no_visit) = self.{result}
    # kalau ga ketemu maka default nya self.no_visit
    return method(node)
  
  @staticmethod
  def no_visit(node: NODES) -> NoVisitMethod:
    return NoVisitMethod(f'No visit {type(node).__name__} method found').as_string()
    
  ##############################################
  
  def visit_NumberNode(self, node: NODES) -> Number:
    return Number(node.token.value)
    
  def visit_BinaryOpNode(self, node: NODES) -> int|None:
    left_number: Number  = self.visit(node.left_node)
    operator: Token = node.op_token
    right_number: Number = self.visit(node.right_node)
    
    match operator.type:
      case Token.TT_PLUS:
        return left_number.add(right_number)
      case Token.TT_MINUS:
        return left_number.subtract(right_number)
      case Token.TT_MUL:
        return left_number.multiply(right_number)
      case Token.TT_DIV:
        return left_number.divide(right_number)
      case _:
        return None
        
  def visit_UnaryOpNode(self, node) -> Number:
    number: Number = self.visit(node.node)
    operator: Token = node.op_token.type
    
    if operator == Token.TT_MINUS:
      number: Number = number.multiply(Number(-1))
      
    return number