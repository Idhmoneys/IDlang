"""
	Context adalah tempat untuk menyimpan kondisi file
	seperti display_name (tampilan nama), symbol_table (variable), dll.

	file CONTEXT mempunyai class Context yang berfungsi untuk menyimpan data.

---
	contoh fungsi:
	```python
	from CONTEXT import Context
	
	context = Context()
	
	context.symbol_table.make(name='x', value=Number(10)) # membuat variable
	nilai_x = context.symbol_table.take(variable='x') # mengambil nilai variable
	```
"""

from idlang.symbol_table import SymbolTable
from typing import Self


class Context:
  """
    #### Tempat untuk menyimpan semua context di file
  
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