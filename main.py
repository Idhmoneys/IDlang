from LEXER import Lexer
from PARSER import Parser
from INTERPRETER import Interpreter
from CONTEXT import Context
from SYMBOL_TABLE import SymbolTable
from VALUES import Number
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
      error = None
      line = line.strip()
      
      lexer: Lexer  = Lexer(line)
      tokens, error = lexer.create_tokens()
      
      if error == 'skip':
        continue
      elif error:
        print(error)
        return
      
      parser: Parser = Parser(tokens)
      
      ast: NODES     = parser.parse() # ast -> Abstract Syntax Tree
      
      
      if ast.error:
        print(ast.error.as_string())
        return
      
      interpreter: Interpreter = Interpreter()
      result: any    = interpreter.visit(ast.node)
      
      if result.error:
        print(result.error.as_string())
        return
      
      print(result.value)

#====================================================#

def REPL() -> None:
  # GLOBAL
  global_symbol_table = SymbolTable()
  global_symbol_table.make('kosong', Number(0))
  global_symbol_table.make('salah', Number(0))
  global_symbol_table.make('benar', Number(1))
  # CONST
  context: Context = Context('<idlang>')
  context.symbol_table.parent = global_symbol_table.symbols
  # MAIN LOOP
  while True:
    
    user_input: input = input('Idlang: ')
    
    lexer: Lexer  = Lexer(user_input)
    tokens, error = lexer.create_tokens()
    
    if error == 'skip':
      continue
    
    if error:
      print(error)
      continue
    
    parser: Parser = Parser(tokens)
    
    ast: NODES     = parser.parse() # ast -> Abstract Syntax Tree
    
    
    if ast.error:
      print(ast.error.as_string())
      continue
    
    interpreter: Interpreter = Interpreter()
    result: any    = interpreter.visit(ast.node, context)
    
    if result.error:
      print(result.error.as_string())
      continue
    
    print(result.value)

  
if __name__ == '__main__':
  try:
    REPL()
  except KeyboardInterrupt:
    print('\nSuccessfuly Exited')