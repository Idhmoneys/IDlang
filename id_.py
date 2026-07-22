############################
# CONST
############################

DIGITS = '0123456789'

############################
# ERROR 
############################

class Error:
  def __init__(self, pos_start, pos_end, error_name, details):
    self.pos_start = pos_start
    self.pos_end = pos_end
    self.error_name = error_name
    self.details = details
    
  def as_string(self):
    result = f'{self.error_name}: {self.details}\n'
    result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
    return result
    
class IllegalCharError(Error):
  def __init__(self, pos_start, pos_end, details):
    super().__init__(pos_start, pos_end, 'Illegal Character', details)
    
class InvalidSyntaxError(Error):
  def __init__(self, pos_start, pos_end, details=''):
    super().__init__(pos_start, pos_end, 'Invalid Syntax', details)

class RuntimeError(Error):
  def __init__(self, pos_start, pos_end, details, context):
    super().__init__(pos_start, pos_end, 'Runtime Error', details)
    self.context = context
    
  def as_string(self):
    result = self.generate_traceback()
    result += f'{self.error_name}: {self.details}\n'
    return result
    
  def generate_traceback(self):
    result = ''
    pos = self.pos_start
    ctx = self.context
    
    while ctx:
      result = f'File {pos.fn}, line {str(pos.ln)}, in {ctx.display_name}\n' + result
      pos = ctx.parent_entry_pos
      ctx = ctx.parent
      
    return 'Traceback (most recent call last):\n' + result

############################
# POSITION 
############################

class Position:
  def __init__(self, idx, ln, col, fn, ftxt):
    """
    idx = index
    ln = line number
    col = column
    fn = file name
    ftxt = file text
    """
    self.idx = idx
    self.ln = ln
    self.col = col
    self.fn = fn
    self.ftxt = ftxt
    
  def advance(self, current_char=None):
    self.idx += 1
    self.col += 1
    
    if current_char == "\n":
      self.ln += 1
      self.col = 0
    
    return self
    
  def copy(self):
    return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

############################
# TOKENS 
############################

# Tambah TT (token type)
TT_INT        = 'INT'
TT_FLOAT      = 'FLOAT'
TT_PLUS       = 'PLUS'
TT_MINUS      = 'MINUS'
TT_MUL        = 'MUL'
TT_DIV        = 'DIV'
TT_LPARENT    = 'LPARENT'
TT_RPARENT    = 'RPARENT'
TT_EOF        = 'EOF'

# BUAT CLASS NYA

class Token:
  def __init__(self, type_, value=None, pos_start=None, pos_end=None):
    self.type = type_
    self.value = value
    
    if pos_start:
      self.pos_start = pos_start
      self.pos_end = pos_start.copy()
      self.pos_end.advance()
      
    if pos_end:
      self.pos_end = pos_end
    
  def __repr__(self):
    if self.value is not None: return f'{self.type}:{self.value}'
    return f'{self.type}'
    
    
############################
# LEXER 
############################

class Lexer:
  def __init__(self, fn, text):
    self.fn = fn
    self.text = text
    self.pos = Position(-1, 0, -1, fn, text)
    self.current_char = None
    self.advance()
    
  def advance(self):
    self.pos.advance(self.current_char)
    self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

  def make_token(self):
    tokens = []
    
    while self.current_char is not None:
      if self.current_char in ' \t':
        self.advance()
      elif self.current_char in DIGITS:
        tokens.append(self.make_number())
      elif self.current_char == '+':
        tokens.append(Token(TT_PLUS, pos_start=self.pos))
        self.advance()
      elif self.current_char == '-':
        tokens.append(Token(TT_MINUS, pos_start=self.pos))
        self.advance()
      elif self.current_char == '*':
        tokens.append(Token(TT_MUL, pos_start=self.pos))
        self.advance()
      elif self.current_char == ':':
        tokens.append(Token(TT_DIV, pos_start=self.pos))
        self.advance()
      elif self.current_char == '(':
        tokens.append(Token(TT_LPARENT, pos_start=self.pos))
        self.advance()
      elif self.current_char == ')':
        tokens.append(Token(TT_RPARENT, pos_start=self.pos))
        self.advance()
      else:
        pos_start = self.pos.copy()
        char = self.current_char
        self.advance()
        return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")
        
    tokens.append(Token(TT_EOF, pos_start=self.pos))
    return tokens, None
    
  def make_number(self):
    num_str = ''
    dot_count = 0
    pos_start = self.pos.copy()
    
    while self.current_char is not None and self.current_char in DIGITS + '.':
      if self.current_char == '.':
        if dot_count == 1: break
        dot_count += 1
        num_str += '.'
      else:
        num_str += self.current_char
      self.advance()
        
    if dot_count == 0:
      return Token(TT_INT, int(num_str), pos_start, self.pos)
    else:
      return Token(TT_FLOAT, float(num_str), pos_start, self.pos)
      
############################
# NODES 
############################

class NumberNode:
  def __init__(self, token):
    self.token = token
    
    self.pos_start = self.token.pos_start
    self.pos_end = self.token.pos_end
    
  def __repr__(self):
    return f'{self.token}'
    
class BinaryOpNode: # Op -> operation
  def __init__(self, left_node, op_token, right_node):
    self.left_node = left_node
    self.op_token = op_token
    self.right_node = right_node
    
    self.pos_start = self.left_node.pos_start
    self.pos_end = self.right_node.pos_end
    
  def __repr__(self):
    return f'({self.left_node}, {self.op_token}, {self.right_node})'
    
class UnaryOpNode:
  def __init__(self, op_token, node):
    self.op_token = op_token
    self.node = node
    
    self.pos_start = self.op_token.pos_start
    self.pos_end = self.op_token.pos_end
    
  def __repr__(self):
    return f'({self.op_token}, {self.node})'

############################
# PARSE RESULT 
############################

class ParseResult:
  def __init__(self):
    self.error = None
    self.node = None
    
  def register(self, res):
    if isinstance(res, ParseResult):
      if res.error: self.error = res.error
      return res.node
      
    return res
  
  def success(self, node):
    self.node = node
    return self
    
  def failure(self, error):
    self.error = error
    return self

############################
# PARSER 
############################

class Parser:
  def __init__(self, tokens):
    self.tokens = tokens
    self.token_idx = -1
    self.advance()
    
  def advance(self):
    self.token_idx += 1
    if self.token_idx < len(self.tokens):
      self.current_token = self.tokens[self.token_idx]
    return self.current_token
    
  def parse(self):
    res = self.expr()
    if not res.error and self.current_token.type != TT_EOF:
      return res.failure(InvalidSyntaxError(
        self.current_token.pos_start,
        self.current_token.pos_end,
        "Expected '+', '-', '*', or ':'"
      ))
    return res
    
  def factor(self):
    res = ParseResult()
    token = self.current_token
    
    if token.type in (TT_PLUS, TT_MINUS):
      res.register(self.advance())
      factor = res.register(self.factor())
      if res.error: return res
      return res.success(UnaryOpNode(token, factor))
    
    elif token.type in (TT_INT, TT_FLOAT):
      res.register(self.advance())
      return res.success(NumberNode(token))
      
    elif token.type == TT_LPARENT:
      res.register(self.advance())
      expr = res.register(self.expr())
      if res.error: return res
      if self.current_token.type == TT_RPARENT:
        res.register(self.advance())
        return res.success(expr)
      else:
        return res.failure(InvalidSyntaxError(
          self.current_token.pos_start, self.current_token.pos_end, "Expected ')'"
        ))
      
    return res.failure(InvalidSyntaxError(
      token.pos_start, token.pos_end, "Expected int or float"
    ))
    
  def term(self):
    return self.binary_op(self.factor, (TT_MUL, TT_DIV))
    
  def expr(self):
    return self.binary_op(self.term, (TT_PLUS, TT_MINUS))
    
  def binary_op(self, func, ops):
    res = ParseResult()
    left = res.register(func())
    if res.error: return res 
    
    while self.current_token.type in ops:
      op_token = self.current_token
      res.register(self.advance())
      right = res.register(func())
      if res.error: return res 
      left = BinaryOpNode(left, op_token, right)
    return res.success(left)

############################
# RUNTIME RESULT 
############################

class RuntimeResult:
  def __init__(self):
    self.value: None = None
    self.error: None = None
    
  def register(self, result):
    self.error = result.error if result.error else self.error
    return result.value
    
  def success(self, value):
    self.value = value
    return self
    
  def failure(self, error):
    self.error = error
    return self

############################
# VALUES 
############################

class Number:
  def __init__(self, value):
    self.value = value
    self.set_pos()
    self.set_context()
    
  def set_pos(self, pos_start=None, pos_end=None):
    self.pos_start = pos_start
    self.pos_end   = pos_end
    return self
    
  def set_context(self, context=None):
    self.context = context
    return self
    
  def added_to(self, other):
    if isinstance(other, Number):
      return Number(self.value + other.value).set_context(self.context), None
      
  def subbed_by(self, other):
    if isinstance(other, Number):
      return Number(self.value - other.value).set_context(self.context), None
      
  def multiply_by(self, other):
    if isinstance(other, Number):
      return Number(self.value * other.value).set_context(self.context), None
      
  def divided_by(self, other):
    if isinstance(other, Number):
      if other.value == 0:
        return None, RuntimeError(
        other.pos_start, other.pos_end, 'Division by zero', self.context
        )
      return Number(self.value / other.value).set_context(self.context), None
      
  def __repr__(self):
    return str(self.value)

############################
# CONTEXT  
############################

class Context:
  """HOLD THE CURRENT FUNCTION OF THE PROGRAM"""
  def __init__(self, display_name, parent=None, parent_entry_pos=None):
    self.display_name       = display_name
    self.parent             = parent
    self.parent_entry_pos   = parent_entry_pos

############################
# INTERPRETER 
############################

class Interpreter:
  def visit(self, node, context):
    method_name = f'visit_{type(node).__name__}'
    method = getattr(self, method_name, self.no_visit_method)
    return method(node, context)
    
  def no_visit_method(self, node, context):
    raise Exception(f'No visit {type(node).__name__} method defined')
    
  ###########################
  
  def visit_NumberNode(self, node, context):
    return RuntimeResult().success(
      Number(node.token.value).set_context(context).set_pos(node.pos_start, node.pos_end)
    )
    
  def visit_BinaryOpNode(self, node, context):
    res = RuntimeResult()
    left  = res.register(self.visit(node.left_node, context))
    if res.error: return res
    right = res.register(self.visit(node.right_node, context))
    if res.error: return res
    
    if node.op_token.type == TT_PLUS:
      result, error = left.added_to(right)
    elif node.op_token.type == TT_MINUS:
      result, error = left.subbed_by(right)
    elif node.op_token.type == TT_MUL:
      result, error = left.multiply_by(right)
    elif node.op_token.type == TT_DIV:
      result, error = left.divided_by(right)
      
    if error: 
      return res.failure(error)
    else:
      return res.success(result.set_pos(node.pos_start, node.pos_end))
    
  def visit_UnaryOpNode(self, node, context):
    result = RuntimeResult()
    number = result.register(self.visit(node.node, context))
    if result.error: return result
    
    error = None
    
    if node.op_token.type == TT_MINUS:
      number, error = number.multiply_by(Number(-1))
    
    if error:
      return result.failure(error)
    else:
      return result.success(number.set_pos(node.pos_start, node.pos_end))

############################
# RUN 
############################

def run(fn, text):
  # GENERATE TOKENS
  lexer: Lexer = Lexer(fn, text)
  tokens, error = lexer.make_token()
  if error: return None, error
  
  # GENERATE AST
  parser: Parser = Parser(tokens)
  ast = parser.parse()
  if ast.error: return None, ast.error
  
  # RUN PROGRAM
  interpreter: Interpreter = Interpreter()
  context = Context('<program>')
  result = interpreter.visit(ast.node, context)
  
  return result.value, result.error