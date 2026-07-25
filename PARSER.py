from TOKENS import Token
from NODES import BinaryOpNode, UnaryOpNode, NumberNode
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
    self.current_token: str = self.tokens[self.index] if self.index < len(self.tokens) else None
    
  def parse(self) -> None:
    """
    Memulai parsernya, dengan memanggil fungsi paling awal ()
    dan di fungsi itu akan memanggil fungsi level berikutnya
    begitu terus sampai di tier maximal
    TODO: bikin parse nya
    """
    result: Node = self.expression()
    
    
    if not result.error and self.current_token.type != Token.TT_EOF:
      return result.failure(SyntaxError("Mengharapkan '+', '-', '*', atau '/'."))
    
    return result
  
  #====================================================#
  
  def expression(self) -> Node:
    """expression adalah langkah paling awal dalam parser"""
    return self.binary_operation(self.term, (Token.TT_PLUS, Token.TT_MINUS))
  
  def term(self) -> Node:
    """term adalah langkah kedua dari parser"""
    return self.binary_operation(self.factor, (Token.TT_MUL, Token.TT_DIV))
  
  def factor(self) -> Node:
    """factor adalah langkah paling akhir dari parser"""
    token:  str         = self.current_token
    result: ParseResult = ParseResult()
    
   
    if token.type in (Token.TT_PLUS, Token.TT_MINUS):
      self.advance()
      factor: Node = result.register(self.factor())
      # ^ ini ga bakal nge override karna yang function pake keyword self
      # | gunanya panggil diri sendiri supaya bisa ngedeteksi unary beruntun kayak --5
      return result.success(UnaryOpNode(token, factor))
    
    elif token.type in (Token.TT_INT, Token.TT_FLOAT):
      self.advance()
      return result.success(NumberNode(token))
    
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
  
  def binary_operation(self, func: callable, ops: str) -> NumberNode|UnaryOpNode|BinaryOpNode:
    result: ParseResult = ParseResult()
    left: Node = result.register(func()) # ini bakal manggil function terus terusan sampe nyentuh valuenya factor
    
    
    if result.error:
      return result
   
    while self.current_token.type in ops:
      op_token: str = self.current_token
    
      self.advance()
      right:  Node  = result.register(func()) # sama kayak yang left, return value nya int plus|minus (kayak 1, 5, 67, -10)
    
      if result.error:
        return result
      
      left :  Node  = BinaryOpNode(left, op_token, right) # ubah nilai leftnya jadi node kalau udah dapet int nya
    return result.success(left)
    # BinaryOpNode: left=int, op_token=operation(+, -, *, /), right=int
