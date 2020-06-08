import json
import requests
headers={
"Host": "www.dianping.com",
"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
}
r = requests.get('http://httpbin.org/get?desc=this-is-a-test-return-desc',  
    headers =headers,
    params={'id':11,'names':123456 })
json_data = json.loads(r.text)
print(json_data['args'])
###
### http://httpbin.org/get?desc=this-is-a-test-return-desc
### C:\Users\User\AppData\Local\Programs\Python\Python37\Scripts
### pip --timeout=900 install requests -i http://pypi.douban.com/simple --trusted-host=pypi.douban.com
###
res = requests.post('http://httpbin.org/post?desc=this-is-a-test-return-desc',  
    headers =headers,
    json={'id':11,'names':123456 })
json_data = json.loads(res.text)
print(json_data['args'])
print(json_data['data'])
