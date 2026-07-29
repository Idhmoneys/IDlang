"""
    Parser adalah tempat/file
    untuk menguraikan, menganalisis, dan menterjemahkan
    data mentah mejadi struktur data yang terstruktur.

    ### Class:
        Parser
    ### Import:
    ```python
    from TOKENS import Token
    from RESULT import ParseResult
    from ERRORS import IllegalCharError, SyntaxError
    from NODES import BinaryOpNode, UnaryOpNode, NumberNode, VariableAssignNode, VariableAccessNode

    from typing import Callable, Self
    ```

    ### Contoh kode:
    ```python
    from idlang.parser import Parser

    # kode sebelumnya...

    parser: Parser = Parser()
    result = parser.parse(token)

    # kode setelahnya
    ```
"""


from idlang.tokens import Token
from idlang.nodes import BinaryOpNode, UnaryOpNode, NumberNode, VariableAssignNode, VariableAccessNode, IfNode
from idlang.errors import IllegalCharError, SyntaxError
from idlang.result import ParseResult
from typing import Callable, Self

#====================================================#

class Parser:
  """
    komponen atau alat dalam sistem komputer
    yang berfungsi untuk menguraikan, menganalisis,
    dan menerjemahkan data mentah atau kode program
    menjadi struktur data yang terstruktur.

    ---
    ### Function:
    ```python
    # ====DunderMethod==========
    def __init__(self, tokens: list[Token]) -> None:

    # ====Helper================
    def advance(self) -> None:
    def parse(self) -> ParseResult:

    # ====Parsing===============
    def expression(self) -> ParseResult:
    def comparasion(self) -> ParseResult:
    ```
  """


  def __init__(self, tokens: list[Token]) -> None:
    self.tokens: list[Token] = tokens # isinya (operator) atau (tipe token + value token)
    self.index: int = -1
    self.advance() # berfungsi untuk memajukan index sekarang, yang tadinya -1 jadi 0


  def advance(self) -> None:
    """Memajukan token sekarang"""
    self.index += 1
    self.current_token: Token | None = self.tokens[self.index] if self.index < len(self.tokens) else None


  def parse(self) -> ParseResult:
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


  def expression(self) -> ParseResult:
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


  def comparasion(self) -> ParseResult:
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


  def arithmetic(self) -> ParseResult:
    return self.binary_operation(self.term, (Token.TT_PLUS, Token.TT_MINUS))


  def term(self) -> ParseResult:
    """term adalah langkah kedua dari parser"""
    return self.binary_operation(self.unary, (Token.TT_MUL, Token.TT_DIV))


  def unary(self) -> ParseResult:
    token: Token = self.current_token
    result: ParseResult = ParseResult()
    
    if token.type in (Token.TT_PLUS, Token.TT_MINUS):
      self.advance()
      unary: Node = result.register(self.unary())
      if result.error:
        return result
      # ^ ini ga bakal nge override karna yang function pake keyword self
      # | gunanya panggil diri sendiri supaya bisa ngedeteksi unary beruntun kayak --5
      return result.success(UnaryOpNode(token, unary))
    
    return self.power()


  def power(self) -> ParseResult:
    return self.binary_operation(self.factor, (Token.TT_POW, ), self.unary)


  def factor(self) -> ParseResult:
    """factor adalah langkah paling akhir dari parser"""
    token:  Token       = self.current_token
    result: ParseResult = ParseResult()
    
    if token.type in (Token.TT_INT, Token.TT_FLOAT):
      self.advance()
      return result.success(NumberNode(token))
      
    elif token.type == Token.IDENTIFIER:
      self.advance()
      return result.success(VariableAccessNode(token))
    
    elif token.type == Token.TT_LPARENT:
      self.advance()
      expr: ParseResult = result.register(self.expression())

      if result.error:
        return result

      if self.current_token.type == Token.TT_RPARENT:
        self.advance()
        return result.success(expr)

      return result.failure(SyntaxError("Membutuhkan ')'."))

    elif token.equal_to(Token.KEYWORD, 'kalau'):
        if_result = result.register(self.if_expression())
        if result.error:
          return result
        return result.success(if_result)

    return result.failure(SyntaxError(result))

  def if_expression(self) -> ParseResult:
      Presult: ParseResult = ParseResult()
      cases: list[ParseResult|None] = []
      else_cases: list[ParseResult|None] = []

      if not self.current_token.equal_to(Token.KEYWORD, 'kalau'):
          return SyntaxError("Mengharapkan 'kalau'")

      self.advance()
      condition = Presult.register(self.expression())
      if Presult.error:
          return Presult

      if self.current_token.type != Token.COLON:
          return Presult.failure(SyntaxError("Membutuhkan ':'"))

      self.advance()
      expression = Presult.register(self.expression())
      if Presult.error:
          return Presult


      cases.append((condition, expression))
      while self.current_token is not None and self.current_token.equal_to(Token.KEYWORD, 'selain'):
          self.advance()
          if not self.current_token.equal_to(Token.KEYWORD, 'itu'):
              return Presult.failure(SyntaxError("Mengharapkan 'itu' setelah 'selain'"))

          self.advance()
          if self.current_token.equal_to(Token.KEYWORD, 'kalau'):
              self.advance()

              condition = Presult.register(self.expression())
              if Presult.error:
                  return Presult

              if self.current_token.type != Token.COLON:
                  return Presult.failure(SyntaxError("Membutuhkan ':'"))
              self.advance()

              expression = Presult.register(self.expression())
              if Presult.error:
                  return Presult

              cases.append((condition, expression))
          elif self.current_token.type == Token.COLON:
              self.advance()
              expression = Presult.register(self.expression())
              if Presult.error:
                  return Presult
              else_cases.append(expression)
              return Presult.success(IfNode(cases, else_cases))
          else:
             return Presult.failure(SyntaxError(f"karakter yang tidak diketahui '{self.current_token}'"))
      return Presult.success(IfNode(cases, else_cases))


  #====================================================#


  def binary_operation(self, func: Callable[[], ParseResult], ops: str|tuple[str], func2: Callable[[], ParseResult]=None) -> ParseResult:
    if not func2:
      func2 = func

    result: ParseResult = ParseResult()
    left = result.register(func()) # ini bakal manggil function terus terusan sampe nyentuh valuenya factor

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
