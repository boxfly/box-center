import os
ABS_PATH = os.path.dirname(os.path.abspath(__file__))
res_dir = os.path.join(ABS_PATH, '采集结果')
if not os.path.exists(res_dir):
    os.mkdir(res_dir)
import urllib.request

response=urllib.request.urlopen('https://www.qq.com')
print(response)
