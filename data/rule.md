# Peraturan dalam bahasa Id

  ## Urutan kalkulasi (dari paling superior)
  1. atom\
     INT | FLOAT
     LPARENT expresion RPARENT
  2. power\
     atom (POW factor)*
  3. factor\
     (POSITIVE | NEGATIVE) power*
  4. term\
     factor ((MUL | DIV) factor)*
  5. expresion\
     factor ((PLUS | MINUS)) factor)*

  ## visualisasi grammar
  Expression (PLUS <+> |MINUS <–>)
  │
  ├── Term (kosong jadi di skip)
  │   └── Factor (angka/INT 25)
  │       └── 25
  │
  ├── + (25 + 18 = 43)
  │
  └── Term (MUL <*> | DIV </> )
      ├── Factor (INT 6)
      │   └── 6
      ├── * (6 × 3 = 18)
      └── Factor (INT 3)
          └── 3