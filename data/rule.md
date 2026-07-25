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
  5. expresion\
     unary ((PLUS | MINUS)) unary)*\
     KEYWORD:buat IDENTIFIER KEYWORD:sebagai expresion
