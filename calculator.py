import re

class Node:
  def __init__(self, value):
    self.value = value
    self.left = None
    self.right = None
    
def add_operator_to_output(new_node, output):
  new_node.right = output.pop(0)
  new_node.left = output.pop(0)
  output.insert(0, new_node)
 
def parse(expr):
  output = []
  operators = []
 
  prec = {'(': 0, '^': 4, '*': 3, '/': 3, '+': 2, '-': 2}

  for i in range(len(expr)):
    if expr[i].isnumeric():
      output.insert(0, Node(expr[i]))
    elif expr[i] in prec.keys():
      if len(operators) > 0:
        while expr[i] in '*/+-' and prec[expr[i]] <= prec[operators[0]] or \
              expr[i] == '^' and prec[expr[i]] < prec[operators[0]]:
          add_operator_to_output(Node(operators.pop(0)), output)
          if len(operators) == 0:
            break
      operators.insert(0, expr[i])
    elif expr[i] == '(':
      operators.insert(0, expr[i])
    elif expr[i] == ')':
      while len(operators) > 0:
        top = operators.pop(0)
        if top == '(':
          break
        else:
          add_operator_to_output(Node(top), output)
    else:
      print('Unknown operator')
      break
    
  if i < len(expr)-1:
    # Return None if parsing failed
    return None
    
  while len(operators) > 0:
    add_operator_to_output(Node(operators.pop(0)), output)
      
  return output
    
def operation(op):
  ops = {'+': lambda a,b: a+b,
         '-': lambda a,b: a-b,
         '*': lambda a,b: a*b,
         '/': lambda a,b: a/b,
         '^': lambda a,b: a**b}
         
  return ops[op]
    
def evaluate(ast):
  if ast == None:
    return None
  else:
    if ast.value.isnumeric():
      return int(ast.value)
    else:
      return operation(ast.value)(evaluate(ast.left), evaluate(ast.right))
      
  return None
 
def get_tokens(s):
  whitespace = re.compile('\s+')
  s = re.sub(whitespace, '', s)
 
  tokens = re.compile('\d+|[()\^*/+-]|.+')
  return re.findall(tokens, s)

main_loop = True

while main_loop:
  expr = input('>')
  tokens = get_tokens(expr)
  
  if len(tokens) == 0:
    continue
  elif tokens[0] == 'quit':
    break
  
  output = parse(tokens)
  
  if output == None:
    break
   
  ast = output[0]
  print(evaluate(ast))