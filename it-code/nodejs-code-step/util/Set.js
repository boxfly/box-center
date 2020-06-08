# -*- coding: utf-8 -*-
print(''' 
set 
交集 并集
''')

set1 = set([1, 2, 3]) 
set2 = set([2, 3, 4]) 
print(set1)
print([set1 == {1,2,3},set1  & set2  == {2,3},],set1  | set2  == {1,2,3,4})
