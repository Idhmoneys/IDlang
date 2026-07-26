from dataclasses import dataclass

@dataclass
class Position:
  """
    Class yang mengetrack posisi

    Attributes:
        fn (str)           : File name.
        ftxt (str)         : File text.
        ln (int)           : Line number.
        pos_index (int)    : index.
        pos_column (int)   : column.
  """
  
  # ====INIT==========================
  
  fn: str
  ftxt: str
  pos_ln: int
  pos_index: int
  pos_column: int
  
  # ====FUNCTION=======================
  
  def pos_advance(self, current_char: None|str=None):
    """
      Memajukan posisi index, column, dan line number
      
      Parameter:
          current_char (str|None): character text sekarang
    """
    self.pos_index += 1
    self.pos_column += 1
    
    if current_char == '\n':
      self.pos_ln += 1
      self.pos_column = 0
  
  
  def pos_copy(self):
    """
      Mencopy semua atribut posisi sekarang
      
      >>> pos_start_copy = position.pos_copy()
      
      Return:
        Self: mengembalikan semua atribut posisi sekarang
    """
    return Position(self.fn, self.ftxt, self.pos_ln, self.pos_index, self.pos_column)

  # =====================================




def main():
  help(Position)
  print(Position('a', 'b', 1, 2, 3))

if __name__ == '__main__':
  main()