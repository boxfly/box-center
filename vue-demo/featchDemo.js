fetch('https://httpbin.org/get?id=1', { 
	method: 'get',
	headers: {  'Accept': 'application/json',  'Content-Type': 'application/json' },  
}).then((res)=>{ 
if(res.ok){
res.json().then((data)=>{ 
 console.log(data); 
})
}else{ 
console.log(res.status); 
//查看获取状态
} 
}).catch((res)=>{ 
//输出一些错误信息
console.log(res.status); 
})
fetch('https://httpbin.org/post', { 
	method: 'post',
	headers: {  'Accept': 'application/json',  'Content-Type': 'application/json' },  
	body: JSON.stringify({ name: 'Hubot' }) 
	}).then((res)=>{ 
if(res.ok){
res.json().then((data)=>{ 
  console.log(data); 
})
}else{  console.log(res.status); 
} 
}).catch((res)=>{  
   console.log(res.status); 
})
