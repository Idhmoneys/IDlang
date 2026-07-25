import NODES
from ERRORS import NoVisitMethod
from VALUES import Number
from TOKENS import Token
from RESULT import RuntimeResult

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
    
  #====================================================#
  
  @staticmethod
  def visit_NumberNode(node: NODES) -> Number:
    result = RuntimeResult()
    return result.success(Number(node.token.value))
  
  
  def visit_BinaryOpNode(self, node: NODES) -> int|None:
    res = RuntimeResult()
    left_number: Number  = res.register(self.visit(node.left_node))
    operator: Token = node.op_token
    right_number: Number = res.register(self.visit(node.right_node))
    
    if res.error:
      return res
    
    match operator.type:
      case Token.TT_PLUS:
        result, error = left_number.add(right_number)
      case Token.TT_MINUS:
        result, error =  left_number.subtract(right_number)
      case Token.TT_MUL:
        result, error = left_number.multiply(right_number)
      case Token.TT_DIV:
        result, error = left_number.divide(right_number)
      case _:
        return None
    
    if error:
      return res.failure(error)
    return res.success(result)
  
  
  def visit_UnaryOpNode(self, node) -> Number:
    result = RuntimeResult()
    number: Number = result.register(self.visit(node.node))
    operator: Token = node.op_token.type
    
    if result.error:
      return result
    
    if operator == Token.TT_MINUS:
      number, error = number.multiply(Number(-1))
      
    return result.success(number)