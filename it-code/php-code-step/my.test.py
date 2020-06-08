YANGKEDUO_HEADERS = {
    'authority': 'mobile.yangkeduo.com',
    'upgrade-insecure-requests': '1',
    'sec-fetch-user': '?1',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit'
                  '/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Mobile Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml'
              ';q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cookie': 'api_uid=CiSwEF6a8aWrmABLEyoXAg==; _nano_fp=XpdJnqPaX5maXqTbnC_wRf6RPqJV4qmqkuI2TMnW; ua=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F83.0.4103.61%20Safari%2F537.36; webp=1; PDDAccessToken=5D2VQ5XMRMQVO4MQZ4JB5HQC2C2RVNPECUNOIFDIGCVB2KVMNWFA1139315; pdd_user_id=7739430543251; pdd_user_uin=T4TTT6VEOICQLAOAJMZYACK4G4_GEXDA'
}
GOODS_MAIN_PAGE = 'http://mobile.yangkeduo.com/goods.html'
import requests
import json
 

#print(YANGKEDUO_HEADERS['Cookie']) 
#home_page_req = requests.get('http://yangkeduo.com',  headers=YANGKEDUO_HEADERS,verify=False)
# YANGKEDUO_HEADERS['Cookie'] = home_page_req.headers['Set-Cookie']
#print('-----') 
#print(YANGKEDUO_HEADERS['Cookie']) 
req = requests.get(GOODS_MAIN_PAGE, params=(('goods_id', str("7985561525")),), timeout=2,  headers=YANGKEDUO_HEADERS)
#print(req.text) 
# print(req.text.encode('gbk', 'ignore').decode('gbk'))
print(req.text.find('  window.rawData='))
a = req.text[req.text.find('  window.rawData=')+18:]
b=  a[:a.find(' </script>')-3]
b=b.replace(";","")
# print(b.encode('gbk', 'ignore').decode('gbk'))
json_data = json.loads(b.encode('utf-8').decode('gbk'))

#task = []
#req = grequests.request("GET", url=GOODS_MAIN_PAGE, params=(('goods_id', str("7985561525")),), headers=YANGKEDUO_HEADERS)
#task.append(req)
#resp = grequests.map(task)
#print(resp[0].text.encode('gbk', 'ignore').decode('gbk'))
 
