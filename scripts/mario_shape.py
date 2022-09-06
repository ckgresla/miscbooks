height = int(input("Tree Height- "))
shape = int(input("Which shape would you like to print (1 or 2)?- "))

for i in range(0, height+1):
  o = height-i

  # Shape 1 
  left_spc = ' ' * o
  left_hash = '#' * i 
  right_hash = '#' * i 
  right_spc = ' ' * o
  
  if shape == 1:
    print(left_spc, left_hash,' ', right_hash, right_spc)  

  # Shape 2  
  left_spc_2 = ' ' * i
  left_hash_2 = '#' * o 
  right_hash_2 = '#' * o 
  right_spc_2 = ' ' * i
  if shape == 2:
    print(left_hash_2, left_spc_2, left_spc_2, left_hash_2)  

  

