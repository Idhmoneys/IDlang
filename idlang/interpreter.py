"""
	Interpreter adalah tempat untuk mengkalkulasi hasil tokenitizer lexer dan parser.

	Class:
		Interpreter

	Contoh kode:
		```python
		from INTERPRETER import Interpreter
		from typing import Any
		# import lainnya...

		interpreter: Interpreter = Interpreter()

		# kode setting lexer & parser nya...

		result: Any = interpreter.visit(ast.node, context)
		```
"""

from idlang.tokens  import Token
from idlang.value   import Number
from idlang.context import Context
from idlang.errors  import RuntimeError
from idlang.result  import RuntimeResult
from idlang.nodes   import NumberNode, UnaryOpNode, BinaryOpNode, VariableAccessNode, VariableAssignNode, IfNode
from typing import Callable

# ====Typedef===================================
Node = NumberNode|UnaryOpNode|BinaryOpNode|VariableAssignNode|VariableAccessNode

# ====MainClass==================================
class Interpreter:
  """
    Interpreter adalah operasi melaksanakan token
    
    Function:
        visit (Node, Context): Untuk pindah ke function lain sesuai Node nya
        
        visit_NumberNode   (Node, Context): Mengembalikan nilai dari Node
        visit_UnaryOpNode  (Node, Context): Untuk mengubah Number positif bisa jadi negatif dan sebaliknya
        visit_BinaryOpNode (Node, Context): Melakukan operasi ke Number|Token.KEYWORD
        visit_VariableAccessNode (Node, Context): Mengembalikan nilai dari variable yang tersimpan
        visit_VariableAssignNode (Node, Context): Menambah variable baru ke penyimpanan
  """
  
  def visit(self, node: Node, context: Context) -> RuntimeResult:
    method: str = f'visit_{type(node).__name__}' 
    # type bakal keluarin class nya, contoh <class 'NODES.NumberNode'>
    # __name__ bakal keluarin nama class nya, contoh BinaryOpNode
    method: Callable = getattr(self, method, self.no_visit)
    # fungsi getattr mirip kayak . nya class/object, kayak self.var
    # getattr(self, result, self.no_visit) = self.{result}
    # kalau ga ketemu maka default nya self.no_visit
    return method(node, context)

	
  @staticmethod
  def no_visit(node: Node, context: Context) -> RuntimeResult:
    result: RuntimeResult = RuntimeResult()
    return result.failure(RuntimeError(f'Tidak menemukan {type(node).__name__} visit method'))

		
  #====================================================#

	
  @staticmethod
  def visit_NumberNode(node: Node, context: Context) -> RuntimeResult:
    RTresult: RuntimeResult = RuntimeResult()
    return RTresult.success(Number(node.token.value))


  def visit_BinaryOpNode(self, node: Node, context: Context) -> RuntimeResult:
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
      case Token.DE:
        result, error = left_number.is_equal(right_number)
      case Token.NE:
        result, error = left_number.not_equal(right_number)
      case Token.GT:
        result, error = left_number.greater_than(right_number)
      case Token.GTE:
        result, error = left_number.greater_than_equal(right_number)
      case Token.LT:
        result, error = left_number.less_than(right_number)
      case Token.LTE:
        result, error = left_number.less_than_equal(right_number)
      case _:
        if operator.equal_to(Token.KEYWORD, 'dan'):
          result, error = left_number.and_(right_number)
        if operator.equal_to(Token.KEYWORD, 'atau'):
          result, error = left_number.or_(right_number)
    
    if error:
      return RTresult.failure(error)
    return RTresult.success(result)


  def visit_UnaryOpNode(self, node: Node, context: Context) -> RuntimeResult:
    RTresult: RuntimeResult = RuntimeResult()
    number:          Number = RTresult.register(self.visit(node.node, context))
    operator:         str = node.op_token.type
    
    if RTresult.error:
      return RTresult
    
    if operator == Token.TT_MINUS:
      number, error = number.multiply(Number(-1))
      
    if operator == Token.KEYWORD and node.op_token.value == 'tidak':
      number, error = number.notted()
      
    if RTresult.error:
      return RTresult
      
    return RTresult.success(number)


  def visit_VariableAccessNode(self, node: VariableAccessNode, context: Context) -> RuntimeResult:
    RTresult: RuntimeResult = RuntimeResult()
    variable_name: Token = node.variable.value
    value: RuntimeResult = context.symbol_table.take(variable_name)
    if value is None:
      return RTresult.failure(RuntimeError(f"Kata kunci '{variable_name}' tidak terdefinisikan."))
    return RTresult.success(value)


  def visit_VariableAssignNode(self, node: VariableAssignNode, context: Context) -> RuntimeResult:
    RTresult: RuntimeResult = RuntimeResult()
    variable_name = node.variable_name.value
    value = RTresult.register(self.visit(node.variable_value, context))

    if RTresult.error:
      return RTresult
    context.symbol_table.make(variable_name, value)

    return RTresult.success(value)


  def visit_IfNode(self, node: IfNode, context: Context):
    RTresult = RuntimeResult()
    for condition, expression in node.if_cases:
      condition_value = RTresult.register(self.visit(condition, context=context))
      if RTresult.error:
        return RTresult

      if not condition_value.is_true():
        continue

      expr = RTresult.register(self.visit(expression, context))
      if RTresult.error:
        return RTresult
      
      return RTresult.success(expr)
    if node.else_cases:
      expr = RTresult.register(self.visit(node.else_cases[0], context))
      if RTresult.error:
        return RTresult
      return RTresult.success(expr)
  
    return RTresult.success(None)