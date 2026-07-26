from TOKENS import Token
from NODES import BinaryOpNode, UnaryOpNode, NumberNode, VariableAssignNode, VariableAccessNode
from ERRORS import IllegalCharError, SyntaxError
from RESULT import ParseResult

#====================================================#

Node = NumberNode | UnaryOpNode | BinaryOpNode

#====================================================#

class Parser:
  """
  komponen atau alat dalam sistem komputer 
  yang berfungsi untuk menguraikan, menganalisis, 
  dan menerjemahkan data mentah atau kode program 
  menjadi struktur data yang terstruktur. 
  """
  
  def __init__(self, tokens: list[Token]) -> None:
    self.tokens: list[Token] = tokens # isinya (operator) atau (tipe token + value token)
    self.index: int = -1
    self.advance() # berfungsi untuk memajukan index sekarang, yang tadinya -1 jadi 0
    
  def advance(self) -> None:
    """Memajukan token sekarang"""
    self.index += 1
    self.current_token: Token | None = self.tokens[self.index] if self.index < len(self.tokens) else None
    
  def parse(self) -> Node:
    """
    Memulai parsernya, dengan memanggil fungsi paling awal ()
    dan di fungsi itu akan memanggil fungsi level berikutnya
    begitu terus sampai di tier maximal
    TODO: bikin parse nya
    """
    Presult: ParseResult = ParseResult()
    result: Node = Presult.register(self.expression())
    if not Presult.error and self.current_token.type != Token.TT_EOF:
      return Presult.failure(SyntaxError("Mengharapkan '+', '-', '*', atau '/'."))
    
    return Presult.success(result)
  
  #====================================================#
  
  def expression(self) -> Node:
    """expression adalah langkah paling awal dalam parser"""
    result = ParseResult()
    if self.current_token.equal_to(Token.KEYWORD, 'buat'):
      keyword = self.current_token
      result.register(self.advance())
      
      if self.current_token.type != Token.IDENTIFIER:
        return result.failure(SyntaxError(f"Mengharapkan identifier setelah '{keyword}'."))
      variable_name = self.current_token
      
      self.advance()
      
      if not self.current_token.equal_to(Token.KEYWORD, 'sebagai'):
        return result.failure(SyntaxError(f"Mengharapkan 'sebagai' setelah '{variable_name.value}'."))
      
      self.advance()
      value = result.register(self.expression())
      
      if result.error:
        return result
      
      return result.success(VariableAssignNode(variable_name, value))
      
    node = result.register(self.binary_operation(self.comparasion, ((Token.KEYWORD, 'dan'), (Token.KEYWORD, 'atau'))))
    
    if result.error:
      return result
    
    return result.success(node)
    
    
  def comparasion(self):
    Presult = ParseResult()
    if self.current_token.equal_to(Token.KEYWORD, 'tidak'):
      op_token = self.current_token
      self.advance()
      
      value = Presult.register(self.comparasion())
      if Presult.error:
        return Presult
      return Presult.success(UnaryOpNode(op_token, value))
    
    value = Presult.register(self.binary_operation(
      self.arithmetic, 
      (Token.LT, Token.LTE, Token.DE, Token.NE, Token.GT, Token.GTE),
      self.arithmetic
    ))
    if Presult.error:
      return Presult.failure(SyntaxError('Mengharapkan sebuah nilai.'))
    return Presult.success(value)
      
  def arithmetic(self):
    return self.binary_operation(self.term, (Token.TT_PLUS, Token.TT_MINUS))
  
  def term(self) -> Node:
    """term adalah langkah kedua dari parser"""
    return self.binary_operation(self.unary, (Token.TT_MUL, Token.TT_DIV))
  
  def unary(self) -> Node:
    token: Token = self.current_token
    result: ParseResult = ParseResult()
    
    if token.type in (Token.TT_PLUS, Token.TT_MINUS):
      self.advance()
      unary: Node = result.register(self.unary())
      # ^ ini ga bakal nge override karna yang function pake keyword self
      # | gunanya panggil diri sendiri supaya bisa ngedeteksi unary beruntun kayak --5
      return result.success(UnaryOpNode(token, unary))
    
    return self.power()
    
  def power(self):
    return self.binary_operation(self.factor, (Token.TT_POW, ), self.unary)
  
  def factor(self) -> Node:
    """factor adalah langkah paling akhir dari parser"""
    token:  str         = self.current_token
    result: ParseResult = ParseResult()
    
    if token.type in (Token.TT_INT, Token.TT_FLOAT):
      self.advance()
      return result.success(NumberNode(token))
      
    elif token.type == Token.IDENTIFIER:
      self.advance()
      return result.success(VariableAccessNode(token))
    
    elif token.type == Token.TT_LPARENT:
      self.advance()
      expr: Node = result.register(self.expression())
    
      if result.error:
        return result
      
      if self.current_token.type == Token.TT_RPARENT:
        self.advance()
        return result.success(expr)
      
      return result.failure(SyntaxError("Membutuhkan ')'."))
    
    return result.failure(SyntaxError("Mengharapkan sebuah nilai."))

  #====================================================#
  
  def binary_operation(self, func: callable, ops: str, func2: callable=None) -> Node:
    if not func2:
      func2 = func
    
    result: ParseResult = ParseResult()
    left: Node = result.register(func()) # ini bakal manggil function terus terusan sampe nyentuh valuenya factor
    
    if result.error:
      return result
    while self.current_token.type in ops or (self.current_token.type, self.current_token.value) in ops:
      op_token: Token = self.current_token
      self.advance()
      right:  Node  = result.register(func2()) # sama kayak yang left, return value nya int plus|minus (kayak 1, 5, 67, -10)
      
      if result.error:
        return result
      
      left :  Node  = BinaryOpNode(left, op_token, right) # ubah nilai leftnya jadi node kalau udah dapet int nya
    return result.success(left)
    # BinaryOpNode: left=int, op_token=operation(+, -, *, /), right=int
