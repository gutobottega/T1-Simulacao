x = 1
a = 1826663
c = 858765198
M = 2**32
for i in range(100000):
    x = (a*x + c) % M
    with open("pseudoaleatorio1.txt", "a") as file:
        file.write(str(x/M) + "\n")
      
x = 2  
for i in range(100000):
    x = (a*x + c) % M
    with open("pseudoaleatorio2.txt", "a") as file:
        file.write(str(x/M) + "\n")
        
x = 3  
for i in range(100000):
    x = (a*x + c) % M
    with open("pseudoaleatorio3.txt", "a") as file:
        file.write(str(x/M) + "\n")
        
x = 4   
for i in range(100000):
    x = (a*x + c) % M
    with open("pseudoaleatorio4.txt", "a") as file:
        file.write(str(x/M) + "\n")
        
x = 5
for i in range(100000):
    x = (a*x + c) % M
    with open("pseudoaleatorio5.txt", "a") as file:
        file.write(str(x/M) + "\n")