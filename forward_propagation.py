import numpy as np
p = np.array([[0,0,0,1]]).T
A1 = np.array([[0,0,0,0],
               [0,0,0,0],
               [0,0,0,1],
               [0,0,1,0]])
A2 = np.array([[0,0,0,0],
               [0,0,0,1],
               [0,0,0,0],
               [0,1,0,0]])
A3 = np.array([[0,0,0,1],
               [0,0,0,0],
               [0,0,0,0],
               [1,0,0,0]])
A4 = np.array([[0,1,0,0],
               [1,0,0,0],
               [0,0,0,1],
               [0,0,1,0]])
q = 0.1 # infect
r = 0.1 # healing

for A in [A1,A2,A3,A4]:
    print(p)
    p = p + q*(1-p)*(A@p)
    print(p)
    p = p*(1-r)
print(p)