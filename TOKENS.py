import string

####################################
# BIKIN TOKEN (TT = TOKEN TYPE)
####################################
class Token:
  """
  bagian-kecil hasil pecahan kode teks mentah 
  yang bisa digunakan untuk code lainnya
  """

  
  # CONSTANTA
  DIGITS:       str  = '0123456789'
  LETTERS:       str  = string.ascii_letters
  
  # TOKEN TYPE
  TT_INT:         str   =   'INT'
  TT_FLOAT:       str   =   'FLOAT'
  TT_PLUS:        str   =   'PLUS'
  TT_MINUS:       str   =   'MINUS'
  TT_MUL:         str   =   'MUL'
  TT_DIV:         str   =   'DIV'
  TT_POW:         str   =   'POW'
  TT_MOD:         str   =   'MOD'
  TT_LPARENT:     str   =   'LPARENT'
  TT_RPARENT:     str   =   'RPARENT'
  TT_DOT:         str   =   'DOT'
  TT_EOF:         str   =   'EOF'
  IDENTIFIER:  str   =   'IDENTIFIER'
  KEYWORD:     str   =   'KEYWORD'
  
  # KEYWORD
  keyword = [
    'buat',
    'sebagai'
  ]
  
  # SYMBOL TABLE
  symbol_table = None
  
  
  def __init__(self, token_type: str, value: None|int|float =None) -> None:
    self.type:  str            = token_type
    self.value: None|int|float = value
    
  def __repr__(self) -> str:
    """Mengembalikan string yang rapi saat class ini di print"""
    if self.value is None:
      return f'{self.type}'
    return f'{self.type}:{self.value}'
    
  def equal_to(self, type_: str, value: None|int|float) -> bool:
    return self.type == type_ and self.value == value
    
    
def main() -> int:
  token: Token = Token('TT_DOT')
  print('%s' % (token))
  return 0
    
if __name__ == '__main__':
  main()