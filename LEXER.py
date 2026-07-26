from TOKENS import Token # Ambil class dari file token
from ERRORS import IllegalCharError # Ambil class dari file errors
from POSITION import Position

class Lexer:
  """
    komponen program yang membaca kode teks mentah 
    dan memecahnya menjadi bagian-kecil bernama TOKEN -Google
    
    Attributes:
        text (str)          : Text dari user.
        file_name (str)     : Nama file yang sedang di gunakan.
        index (int)         : Index character text.
        position (Position) : Posisi text berada.
  """
  
  def __init__(self, fn, text: str) -> None:
    self.text:      str      = text
    self.file_name: str      = fn
    self.index:     int      = -1
    self.position:  Position = Position(fn, text, -1, 0, -1)
    self.advance()

  def advance(self) -> None:
    """Memajukan character sekarang"""
    self.position.pos_advance()
    self.index += 1
    self.current_character: str|None = self.text[self.index] if self.index < len(self.text) else None
  
  def create_tokens(self) -> (list[Token|None], None|IllegalCharError):
    """
      Membuat token untuk digunakan di tempat lain.
      
      Return:
          list[Token|None]: mengembalikan hasil dari tokenizer text
    """
    tokens: list[Token] = [] # penympanan token
    
    # MAIN LOOPS
    while self.current_character is not None:
      if self.current_character in ' \t': # cek apakah hurufnya spasi/tab
        self.advance()
      elif self.current_character in Token.DIGITS: # cek apakah hurufnya ada di digits
        tokens.append(self.generate_numbers())
      elif self.current_character in Token.LETTERS:
        word = self.generate_identifier()
        comparasion_result = self.generate_comparasion(word)
        tokens.append(comparasion_result)
      else:
        match self.current_character: # i lup match case :v
          case '+':
            tokens.append(Token(Token.TT_PLUS))
            self.advance()
          case '-':
            tokens.append(Token(Token.TT_MINUS))
            self.advance()
          case '*':
            tokens.append(Token(Token.TT_MUL))
            self.advance()
          case '/':
            tokens.append(Token(Token.TT_DIV))
            self.advance()
          case '^':
            tokens.append(Token(Token.TT_POW))
            self.advance()
          case '%':
            tokens.append(Token(Token.TT_MOD))
            self.advance()
          case '(':
            tokens.append(Token(Token.TT_LPARENT))
            self.advance()
          case ')':
            tokens.append(Token(Token.TT_RPARENT))
            self.advance()
          case '=':
            equal_result, error = self.generate_equal('=')
            if error:
              return [], error.as_string()
            tokens.append(equal_result)
            self.advance()
          case '<':
            equal_result, error = self.generate_equal('<')
            if error:
              return [], error.as_string()
            tokens.append(equal_result)
            self.advance()
          case '>':
            equal_result, error = self.generate_equal('>')
            if equal_result == '>>':
              if not tokens:
                return [], 'skip'
              tokens.append(Token(Token.TT_EOF))
              return tokens, None
            if error:
              return [], error.as_string()
            tokens.append(equal_result)
            self.advance()
          case '.':
            self.advance()
            if self.current_character is not None:
              return [], IllegalCharError(f"'{self.current_character}'").as_string()
            break
          case _:
            return [], IllegalCharError(f"'{self.current_character}'").as_string()
            
    if not tokens:
      return [], 'skip'
    tokens.append(Token(Token.TT_EOF))
    return tokens, None
  
  #====================================================#

  def generate_numbers(self) -> Token:
    """
      Menggabung kan character untuk menjadi angka.
      
      >>> lexer = Lexer(123)
      >>> num = lexer.generate_tokens() -> generate_numbers()
      >>> print(num)
          (INT:1, INT:2, INT:3)
      
      Return:
          Token: class token dari TOKENS.py
    """
    numbers:   str = ''
    dot_count: int = 0
    
    while self.current_character is not None and self.current_character in Token.DIGITS + '.':
      if self.current_character == '.':
        if dot_count == 1: # cek apakah udah ada . sebelumnya
          break
        dot_count += 1
      
      numbers += self.current_character
      self.advance()
      
    if dot_count == 1:
      return Token(Token.TT_FLOAT, float(numbers))
    return Token(Token.TT_INT, int(numbers))
    
    
  def generate_identifier(self) -> Token:
    """
      Menggabung kan character untuk menjadi token identifier.
      
      >>> lexer = Lexer(buat x sebagai 10)
      >>> idt = lexer.generate_tokens() -> generate_identifier()
      >>> print(idt)
          (KEYWORD:buat, IDENTIFIER:x, KEYWORD:sebagai, INT:10)
      
      Return:
          Token: class token dari TOKENS.py
    """
    identifier: str = ''
    
    letters_digits: str = Token.LETTERS + Token.DIGITS
    
    while self.current_character is not None and self.current_character in letters_digits + '_':
      identifier += self.current_character
      self.advance()
    
    if identifier in Token.keyword:
      return Token(Token.KEYWORD, identifier)
    return Token(Token.IDENTIFIER, identifier)
    
    
  def generate_comparasion(self, word):
    if word.equal_to(Token.KEYWORD, 'adalah'):
      return Token(Token.DE, 'adalah')
    elif word.equal_to(Token.KEYWORD, 'bukan'):
      return Token(Token.NE, 'bukan')
    elif word.equal_to(Token.KEYWORD, 'tidak'):
      return Token(Token.KEYWORD, 'tidak')
    elif word.equal_to(Token.KEYWORD, 'dan'):
      return Token(Token.KEYWORD, 'dan')
    elif word.equal_to(Token.KEYWORD, 'atau'):
      return Token(Token.KEYWORD, 'atau')
    else:
      return word
      
  
  def generate_equal(self, token):
    if token not in '<=>':
      return
    symbol = token
    
    self.advance()
    
    if self.current_character not in ('<', '=', '>'):
      if symbol == '<':
        return Token(Token.LT), None
      elif symbol == '>':
        return Token(Token.GT), None
      else:
        return None, IllegalCharError(f"'{self.current_character}'")
    elif symbol == '>' and self.current_character == '>':
      return '>>', None
    elif self.current_character != '=':
      return [], IllegalCharError(f"Mengharapkan '=' setelah {symbol}, namun mendapatkan {self.current_character}")
    if symbol == '<':
      return Token(Token.LTE), None
    elif symbol == '=':
      return Token(Token.DE), None
    elif symbol == '>' :
      return Token(Token.GTE), None
    elif symbol == '!' :
      return Token(Token.GTE), None
    
    return [], IllegalCharError(f'Membutuhkan operator setelah {symbol}')
      
    


# AREA TESTING
def main() -> None:
  lexer: Lexer = Lexer('bom', '   .')
  print(lexer.create_tokens())
  

if __name__ == '__main__':
  main()