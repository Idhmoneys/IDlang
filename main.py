import id_

def main():
  while True:
    text = input('id: ')
    result, error = id_.run('<stdin>', text)
    
    if error: 
      print(error.as_string())
    else: 
      print(result)

if __name__ == "__main__":
  main()