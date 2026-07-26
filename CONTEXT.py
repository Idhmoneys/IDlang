from SYMBOL_TABLE import SymbolTable
from typing import Self

class Context:
  """
    Tempat untuk menympan semua context di file
  
    Attributes:
        display_name (str)            : Tampilan text, contohnya '<idlang>'
        parent (None|Self)            : Context nya context, gunanya saat ada file berkelipatan bisa di track.
        parent_entry_pos (None|Self)  : Posisi awal parent.
        symbol_table (SymbolTable)    : Tempat penyimpanan variabel.
  """

  # ====DunderMethod==========================
  def __init__(self, display_name: str, parent: Self|None=None, parent_entry_pos: Self|None=None) -> None:
    self.display_name:     str          = display_name
    self.parent:           None|Self    = parent
    self.parent_entry_pos: None|Self    = parent_entry_pos
    
    
    # ====SymbolTable=========================
    self.symbol_table:     SymbolTable  = SymbolTable()