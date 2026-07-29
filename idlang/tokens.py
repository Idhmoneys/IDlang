"""Ini tokens"""
import string

####################################
# BIKIN TOKEN (TT = TOKEN TYPE)
####################################
class Token:
  """
  bagian-kecil hasil pecahan kode teks mentah 
  yang bisa digunakan untuk code lainnya
  
  Attribute:
      |====Constant========================|
      | DIGITS (str) : List angka.
      | LETTERS (str): List ascii letters.
      |====TokenType=======================|
      |  INT (str)        : Integer
      |  FLOAT (str)      : Float
      |  PLUS (str)       : Positif
      |  MINUS (str)      : Negatif
      |  MUL (str)        : Multiply
      |  DIV (str)        : Divide
      |  POW (str)        : Power
      |  LPARENT (str)    : '('
      |  RPARENT (str)    : ')'
      |  DOT (str)        : '.'
      |-------------------------------------|
      |  IDENTIFIER (str) : Identifikasi
      |  KEYWORD (str)    : Kata kunci
      |  EOF (str): Akhir file (End Of File)
      |=====================================|
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
  IDENTIFIER:     str   =   'IDENTIFIER'
  KEYWORD:        str   =   'KEYWORD'
  NOT:            str   =   'NOT'
  EQUAL:          str   =   'EQUAL'
  NE:             str   =   'NE'
  OR:             str   =   'OR'
  AND:            str   =   'AND'
  DE:             str   =   'DE' # DOUBLE EQUAL | ==
  LT:             str   =   'LT' # LESS THAN | <
  LTE:            str   =   'LTE' # LESS THAN EQUAL | <=
  GT:             str   =   'GT' # GREATER THAN | >
  GTE:            str   =   'GTE' # GREATER THAN EQUAL | >=
  COLON:          str   =   'COLON'
  
  # KEYWORD
  keyword = [
    'buat',
    'sebagai',
    'adalah',
    'bukan',
    'dan',
    'atau',
    'tidak',
    'kalau',
    'selain',
    'itu'
  ]
  
  # SYMBOL TABLE
  symbol_table = None
  
  
  def __init__(self, token_type: str, value: None|int|float =None) -> None:
    self.type:  str            = token_type
    self.value: None|int|float|str = value
    
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