import numpy as np

#A
M = np.arange(5,21)
print(M)

#B
M = M.reshape(4,4)
print(M)

#C
M[1:3, 1:3] = 0
print(M)

#D
M = M @ M
print(M)

#E
v = M[0]
print(np.sqrt(v@v))