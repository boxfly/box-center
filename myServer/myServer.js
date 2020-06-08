
var http = require("http"); 
var url = require("url");  
var app ={
	imgSrc:"https://iph.href.lu/100x100",
	imgs:["http://placehold.it/20x20","http://placekitten.com/g/100/200"],
	videos:[
	"https://lmp4.vjshi.com/2016-03-09/2015-ec1b3b3e5e831d7bb4dd16bdff9759fc.mp4?v=nizhuanrennizhuan",
	"https://lmp4.vjshi.com/2017-06-25/7ed6e8119a1dc16485086e4efb7b2f43.mp4?v=nizhuanrennizhuan", 
	],
} 
   
var ss=[]
Array(20).fill(1).map((e,i)=>{ 
	ss.push({  choose:false},) 
})
var DATA ={
	"page_a":{},
	"page_b":{},
	"page_c":{},
}
http.createServer(function(request, response) { 
  var path= url.parse(request.url).path;  //console.log(path) 
  var query = url.parse(request.url,true).query;   
  var ret = query
  
  if(query.queryType == 0){
	  
  }
  if(path.indexOf(query.page)>-1){
	 ret = DATA[query.page]
  }
  if(path.indexOf("getDownloadUrl")>-1){
	  var img = `${imgSrc}?text=${count}`
	      count++
		  ret =  {"code":"200","message":"get download url success!","data":img}
		  // https://mirrors.huaweicloud.com/nginx/nginx-1.9.2.zip
  }
    
 response.writeHead(200, {"Content-Type": "application/json;charset=UTF-8"}); 
 response.write(JSON.stringify(ret)); 
 response.end(); 
}).listen(1234); 


var desc = `
\n https://shipin.vjshi.com/free
\n npm install  querystring
\n nodejs start listen 1234 port! 
\n http://127.0.0.1:1234/wz/data?id=1
`
console.log(desc);