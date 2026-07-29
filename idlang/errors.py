from dataclasses import dataclass

@dataclass
class Error:
  """
    #### Baseplate/blueprint untuk class error

    Attributes:
        name     (str): tampilan nama error nya.
        details  (str): tampilan detail error nya.
  """
  name: str
  details: str
  
  def as_string(self) -> str:
    """
			Mengeprint hasil dari error nya

			return: 
				```python
				f'{RED}{self.name}:{RESET} {self.details}'
				```
		"""
    RED = '\033[1;31m'
    RESET = '\033[0m'
    return f'{RED}{self.name}:{RESET} {self.details}'


class IllegalCharError(Error):
  """Tempat error untuk karakter yang tidak dekutahi, biasanya ada di lexer"""
  def __init__(self, details: str) -> None:
    super().__init__('Karakter Illegal', details)
    
class SyntaxError(Error):
  """Tempat error untuk syntax, biasanya saat typo"""
  def __init__(self, details: str) -> None:
    super().__init__('Kesalahan Syntax', details)
    
class RuntimeError(Error):
  """Tempat error untuk kesalahan yang sedang dilakukan"""
  def __init__(self, details: str='') -> None:
    super().__init__('Kesalahan Saat Beroperasi', details)

 

def main() -> None:
 er: IllegalCharError = IllegalCharError('test')
 print(er.as_string())
  
if __name__ == '__main__':
  main()