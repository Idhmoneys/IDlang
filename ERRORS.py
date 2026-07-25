from dataclasses import dataclass

@dataclass
class Error:
  """Baseplate/blueprint untuk class error"""
  name: str
  details: str
  
  def as_string(self) -> str:
    RED = '\033[1;31m'
    RESET = '\033[0m'
    """Berfungsi agar kalau pengen di print lebih rapi"""
    return f'{RED}{self.name}:{RESET} {self.details}'


class IllegalCharError(Error):
  def __init__(self, details: str) -> None:
    super().__init__('Karakter Illegal', details)
    
class SyntaxError(Error):
  def __init__(self, details: str) -> None:
    super().__init__('Kesalahan Syntax', details)
    
class RuntimeError(Error):
  def __init__(self, details: str='') -> None:
    super().__init__('Kesalahan Saat Beroperasi', details)
  
class NoVisitMethod(Error):
  def __init__(self, details: str) -> None:
    super().__init__('Tidak Ada Visit Method', details)

 
def main() -> None:
 er: IllegalCharError = IllegalCharError('test')
 print(er.string())
  
if __name__ == '__main__':
  main()