from LEXER import Lexer
from PARSER import Parser
from INTERPRETER import Interpreter
import NODES
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
      tokens, error = lexer.create_tokens()
      
      if error:
        print(error)
        break
      
      parser: Parser = Parser(tokens)
      ast = parser.parse()
      
      interpreter = Interpreter()
      print(interpreter.visit(ast))

#====================================================#

def REPL():
  while True:
    
    user_input    = input('>> ')
    
    lexer: Lexer  = Lexer(user_input)
    tokens, error = lexer.create_tokens()
    
    if error:
      print(error)
      continue
    
    parser: Parser = Parser(tokens)
    
    ast: NODES     = parser.parse() # ast -> Abstract Syntax Tree
    
    
    if ast.error:
      print(ast.error.as_string())
      continue
    
    interpreter: Interpreter = Interpreter()
    result: any    = interpreter.visit(ast.node)
    
    if result.error:
      print(result.error.as_string())
      continue
    
    print(result.value)

  
if __name__ == '__main__':
  REPL()