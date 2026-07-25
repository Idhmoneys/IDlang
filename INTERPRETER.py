import NODES
from   ERRORS  import RuntimeError
from   VALUES  import Number
from   TOKENS  import Token
from   RESULT  import RuntimeResult
from   CONTEXT import Context

class Interpreter:
  def visit(self, node: NODES, context: Context) -> str|int|None|Number|RuntimeError:
    method: str = f'visit_{type(node).__name__}' 
    # type bakal keluarin class nya, contoh <class 'NODES.NumberNode'>
    # __name__ bakal keluarin nama class nya, contoh BinaryOpNode
    method: callable = getattr(self, method, self.no_visit)
    # fungsi getattr mirip kayak . nya class/object, kayak self.var
    # getattr(self, result, self.no_visit) = self.{result}
    # kalau ga ketemu maka default nya self.no_visit
    return method(node, context)
  
  @staticmethod
  def no_visit(node: NODES) -> RuntimeError:
    result: RuntimeResult = RuntimeResult()
    return result.failure(RuntimeError(f'Tidak menemukan {type(node).__name__} visit method'))
    
  #====================================================#
  
  @staticmethod
  def visit_NumberNode(node: NODES, context: Context) -> Number:
    RTresult: RuntimeResult = RuntimeResult()
    return RTresult.success(Number(node.token.value))
  
  
  def visit_BinaryOpNode(self, node: NODES, context: Context) -> int|None:
    RTresult:     RuntimeResult = RuntimeResult()
    left_number:  Number        = RTresult.register(self.visit(node.left_node, context))
    operator:     Token         = node.op_token
    right_number: Number        = RTresult.register(self.visit(node.right_node, context))
    
    if RTresult.error:
      return RTresult
    
    match operator.type:
      case Token.TT_PLUS:
        result, error = left_number.add(right_number)
      case Token.TT_MINUS:
        result, error =  left_number.subtract(right_number)
      case Token.TT_MUL:
        result, error = left_number.multiply(right_number)
      case Token.TT_DIV:
        result, error = left_number.divide(right_number)
      case Token.TT_POW:
        result, error = left_number.power(right_number)
      case Token.TT_MOD:
        result, error = left_number.mod(right_number)
    
    if error:
      return RTresult.failure(error)
    return RTresult.success(result)
  
  
  def visit_UnaryOpNode(self, node: NODES, context: Context) -> Number:
    RTresult: RuntimeResult = RuntimeResult()
    number:          Number = RTresult.register(self.visit(node.node, context))
    operator:         Token = node.op_token.type
    
    if RTresult.error:
      return RTresult
    
    if operator == Token.TT_MINUS:
      number, error = number.multiply(Number(-1))
      
    return RTresult.success(number)
    
  
  def visit_VariableAccessNode(self, node: NODES, context: Context) -> RuntimeError|str|int|None:
    RTresult: RuntimeResult = RuntimeResult()
    variable_name: Token = node.variable.value
    value: str|int|None = context.symbol_table.take(variable_name)
    if value is None:
      return RTresult.failure(RuntimeError(f"Kata kunci '{variable_name}' tidak terdefinisikan."))
    return RTresult.success(value)
    
  def visit_VariableAssignNode(self, node: NODES, context: Context):
    RTresult: RuntimeResult = RuntimeResult()
    variable_name: Token = node.variable_name.value
    value: str|int|None = RTresult.register(self.visit(node.variable_value, context))
    
    if RTresult.error:
      return RTresult
    context.symbol_table.make(variable_name, value)
    
    return RTresult.success(value)