from LEXER import Lexer
from PARSER import Parser
import argparse

def main() -> None:
  # SETTING ARGPARSE NYA
  parser: argparse = argparse.ArgumentParser()
  parser.add_argument('file')
  path: dict[str] = parser.parse_args()
  
  # BUKA FILE NYA
  with open(path.file, 'r') as f:
    file = f.readlines()
    
    # LOOP UNTUK SETIAP BARIS DI FILE NYA
    for line in file:
      line = line.strip()
      
      lexer = Lexer(line)
      tokens = lexer.create_tokens()
      
      parser: Parser = Parser(tokens)
      ast = parser.parse()
      print(f'ast: {ast}')
      
def test():
  while True:
    ui = input('>> ')
    
    lexer: Lexer = Lexer(ui)
    tokens = lexer.create_tokens()
    
    parser: Parser = Parser(tokens)
    ast = parser.parse()
    print(ast)
  
if __name__ == '__main__':
  test()