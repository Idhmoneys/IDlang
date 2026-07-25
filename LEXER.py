from TOKENS import Token # Ambil class dari file token
from ERRORS import IllegalCharError # Ambil class dari file errors

class Lexer:
  """
    komponen program yang membaca kode teks mentah 
    dan memecahnya menjadi bagian-kecil bernama TOKEN -Google
  """
  
  def __init__(self, text: str)-> None:
    self.text:  str   = text
    self.index: int   = -1
    self.advance()

  def advance(self) -> None:
    """Memajukan character sekarang"""
    self.index += 1
    self.current_character: str|None = self.text[self.index] if self.index < len(self.text) else None
  
  def create_tokens(self) -> list[Token|None] & None|IllegalCharError:
    """Membuat token untuk digunakan di tempat lain"""
    tokens: list[Token] = [] # penympanan token
    
    # MAIN LOOPS
    while self.current_character is not None:
      if self.current_character in ' \t': # cek apakah hurufnya spasi/tab
        self.advance()
      elif self.current_character in Token.DIGITS: # cek apakah hurufnya ada di digits
        tokens.append(self.generate_numbers())
      elif self.current_character in Token.LETTERS:
        tokens.append(self.generate_identifier())
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
          case '>':
            if not tokens:
              return tokens, 'skip'
            self.advance()
            if self.current_character == '>':
              break
              # return tokens, 'skip'
            return [], IllegalCharError('>, mungkin maksudmu >>?').as_string()
          case '.':
            self.advance()
            if self.current_character is not None:
              return [], IllegalCharError(f"'{self.current_character}'").as_string()
            break
          case _:
            return [], IllegalCharError(self.current_character).as_string()
            
    if not tokens:
      return [], 'skip'
    tokens.append(Token(Token.TT_EOF))
    return tokens, None
  
  #====================================================#

  def generate_numbers(self) -> Token:
    """
    Menggabung kan character untuk menjad angka, mirip split(' ')
    Contoh: 123, 1.5, 67
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
    """Berfungsi untuk menggabungkan character menjadi kalimat/kata/string"""
    identifier: str = ''
    
    letters_digits: str = Token.LETTERS + Token.DIGITS
    
    while self.current_character is not None and self.current_character in letters_digits + '_':
      identifier += self.current_character
      self.advance()
    
    if identifier in Token.keyword:
      return Token(Token.KEYWORD, identifier)
    return Token(Token.IDENTIFIER, identifier)


# AREA TESTING
def main() -> None:
  lexer: Lexer = Lexer('   .')
  print(lexer.create_tokens())
  

if __name__ == '__main__':
  main()