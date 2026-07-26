# Peraturan dalam bahasa Id

  ## Urutan kalkulasi (dari paling superior)
  1. factor\
     INT | FLOAT | IDENTIFIER\
     LPARENT expresion RPARENT
  2. power\
     factor (POW unary)*
  3. unary\
     (POSITIVE | NEGATIVE) power*
  4. term\
     unary ((MUL | DIV) unary)*
  5. arithmetic\
    unary ((PLUS | MINUS)) unary)*\
  6. comparasion
    (tidak) arithmetic
    arithmetic ((EQ|NE|GT|GTE|LT|LTE) arithmetic)
  6. expresion\
    comparasion ((dan|atau) comparasion)
    KEYWORD:buat IDENTIFIER KEYWORD:sebagai expresion

((2) == (2))
(((2) == (2)) dan ((3) == (3)))
(tidak (2 != 2))
