# -*- coding: utf-8 -*- 
import math
print({
    "<=x":  math.floor(4.12),
    "<=x":  math.trunc(4.12),
    ">=x":  math.ceil(4.12),
    "sum":math.fsum((1,2,3,4)),
    "1": math.copysign(2,-3),
    "sin(30)":math.sin(math.pi/6),
    "degrees":math.degrees(math.pi/4),
    "abs":math.fabs(-0.03),
    "sqrt":math.sqrt(100),
    "pow":math.pow(2,2),
    "log2":math.log2(4),
    "log":math.log(10,10),
    "hypot":math.hypot(3,4),
}) 

print({
    "reverse": "hello"[::-1],
    "replace": "replace".replace("ce", 'se'),
    "format": 'http://api.cn?' \
                    'orderid={}'.format(math.e),
                    
})
import time
print({
    "YYYY-mm-dd": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) ,                   
})

import json  
obj = {"a": 1, "b": 2}
obj['a'] ='obj.a is not work'
print({
    "obj.a":obj['a'],
    "json_data ":json.loads(json.dumps({"a": 1, "b": 2}))
})
with open('data.json', 'w') as f:
    json.dump(json.loads(json.dumps({"a": 1, "b": 2})), f)
with open('data.json', 'r') as f:
    print(json.load(f))