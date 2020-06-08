import pdb 
import operator  #https://blog.csdn.net/zhtysw/article/details/80510113
print({
    "max":max([1,2,3]),
    "maxByOperator": max(enumerate([1,2,3]), key=operator.itemgetter(1))[1]
})  
pdb.set_trace()
itemgetter = operator.itemgetter
print({
    "index":itemgetter(1)('ABCDEFG'),
    "indexOf":"index".index("index")>-1,
    "slice":itemgetter(slice(2,None))('ABCDEFG'),
    "values":list(map(itemgetter(1), [('apple', 3), ('banana', 2),('orange', 1)])),
}) 
l = list("hello")
l.reverse() 
print("".join(l))  