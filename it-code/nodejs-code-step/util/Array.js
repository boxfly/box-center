function log(e){console.log(e)}
function print(e){console.log(e)}
arr = [1,2,3]
for(key in arr) print(key);
for(value of arr) print(value);
print({
  "init arr ": [1,2,3,"a","b","c"],
  "reverse": Array(3).fill(1).map((e,i)=>i).reverse(),
  "slice": [1,2,3].slice(1) ,
  "splice": [1,2,3].splice(1,1,2) ,
  "concat":[].concat([1,2,3],[4,5,6]),
  "delete": arr.splice(0,1),
})
print(arr)

