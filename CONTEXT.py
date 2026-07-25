from SYMBOL_TABLE import SymbolTable
class Context:
  def __init__(self, fn: str) -> None:
    self.file_name:            str = fn
    self.symbol_table: SymbolTable = SymbolTable()