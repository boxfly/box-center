var request = require('request');
request('http://httpbin.org/get?id=1', function (error, response, body) {
  if (!error && response.statusCode == 200) {
	console.log(body) // 请求成功的处理逻辑
  }
});
request({ url: "http://httpbin.org/post",method: "POST",json: true,
	headers: { "content-type": "application/json",},
	body: JSON.stringify({ data:"data"})
}, function(error, response, body) {
	if (!error && response.statusCode == 200) {
		console.log(body)
	}
}); 
request.post({url:'http://httpbin.org/post', form:{ key:'value'}}, function(error, response, body) {
	if (!error && response.statusCode == 200) {
		console.log(body)
	}
})