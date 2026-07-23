from dataclasses import dataclass

@dataclass
class Error:
  """Baseplate/blueprint untuk class error"""
  name: str
  details: str
  
  def as_string(self) -> str:
    """Berfungsi agar kalau pengen di print lebih rapi"""
    return f'{self.name}: {self.details}'
    

class IllegalCharError(Error):
  def __init__(self, details: str) -> None:
    super().__init__('Illegal Character', details)
  
 
def main() -> None:
 er: IllegalCharError = IllegalCharError('test')
 print(er.string())
  
if __name__ == '__main__':
  main()