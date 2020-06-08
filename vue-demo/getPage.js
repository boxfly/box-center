/* eslint-disable  */
var fs = require('fs')
 
PAGE_URL = ""

fs.writeFile('./imgs.md', '1.js', function (error) {
    if (error) {
      console.log('写入失败')
    } else {
      console.log('写入成功了')
    }
  })

  
var request = require('request');
request(PAGE_URL, function (error, response, body) {
    console.log(response)  
  if (!error&& response.statusCode == 200) {
    console.log(body) 
  }else{
    console.log(error)   
  }
});