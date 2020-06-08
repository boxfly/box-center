# -*- coding: utf-8 -*-
import numpy as np
print(''' 
test array
''')
print({
  "init arr ": [1,2,3,"a","b","c"],
  "reverse": list(range(3))[::-1],
  "slice": list(range(3))[0:1],
  "concat":np.append([1,2,3],[4,5,6]),
})      

a = np.array([1,2,3,4,5])
slice = a[:3]
slice[0] = 100
print(a)