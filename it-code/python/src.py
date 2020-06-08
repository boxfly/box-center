# -*- coding: utf-8 -*-
# @Time    : 2020-04-11 15:32
# @Author  : 须枫
# @Email   : sunganyu@htomail.com
# @File    : 多多爆款提取同行id.py
# @Software: PyCharm

from gevent import monkey
import os
import pandas as pd
import time
import copy
import multiprocessing
import re
from collections import defaultdict

monkey.patch_all(thread=False, select=False)
import grequests
import requests
import ujson
import configparser  # 引入模块
import signal
from sys import exit

ROUTER_BATCH = 50
stop_task = False
RES_VER = ''
import platform
from leguang_reboot import ping, reboot_router, ROUTER_HOST, BAIDU_HOST


def list_unique(orig):
    temp = list(set(orig))
    temp.sort(key=orig.index)
    return temp


sys_str = platform.system()
if sys_str == "Windows":
    from pdd_collect_register import init_register

    RES_VER = init_register()
    if not RES_VER:
        time.sleep(10)
        exit()
    res = ping(ROUTER_HOST)
    if not res:
        print('未识别到路由器。')
        RES_VER = 'SUCCESS'


def ctrl_c_handler(signum, frame):
    print()
    print("用户手动中止！")
    global stop_task
    stop_task = True


signal.signal(signal.SIGINT, ctrl_c_handler)

DATE_PATTERN = r'20\d{2}-\d{2}-\d{2}'

KEY_WORDS_FILE = '多多爆款采集关键词.txt'
CONFIG_FILE = '爆款采集配置.inf'
DANGER_WORDS_FILE = '违禁词.txt'
DANGER_WORDS_LIST = []
GOODS_MAIN_PAGE = 'http://mobile.yangkeduo.com/goods.html'
PDD_CAT1_MAP_FILE = '拼多多一级类目.json'
# 66代理订单号,购买地址：http://www.66daili.cn
PROXY_ORDER_ID = ''

# 搜索排序方式: [1]销量由高到低，[3]综合排序，[4]价格由高到低, [-4]价格由低到高
SORT_TYPE = 3

# 采集页数
SEARCH_PAGES = 50

# 过滤价格范围，对低价和最高价，单位元
MIN_PRICE = 1.0
MAX_PRICE = 99999.9

# 过滤销量范围，整数
MIN_SALES = 0
MAX_SALES = 999999

# 是否过滤旗舰店和专营店, [1]是,[0]否
FILTER_SPECIAL_SHOPS = 0

# 是否过滤标题违禁词,[1]是,[0]否
FILTER_DANGER_WORDS = 0

QUERY_GOODS_LIST_PATH = 'https://api.pinduoduo.com/api/jinbao/h5_weak_auth/goods/query_goodslist_v2'
HEADERS = {
    'Host': 'api.pinduoduo.com',
    'Content-Type': 'text/plain;charset=UTF-8',
    'Accept': '*/*'
}

ABS_PATH = os.path.dirname(os.path.abspath(__file__))
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
    'cookie': 'api_uid=CiU8PV7E00Q19wBDYBbKAg==;'
              'msec=1800000;'
              'ua=Mozilla%2F5.0%20(Linux%3B%20Android%206.0%3B%20Nexus%205%20Build%2FMRA58N)%20AppleWebKit%2F537.'
              '36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F80.0.3987.149%20Mobile%20Safari%2F537.36; '
              'webp=1; pdd_user_id=; pdd_user_uin=; PDDAccessToken='
}
from bs4 import BeautifulSoup


def process_goods_resp(response):
    if response is None:
        return response
    if response.status_code in [200, 206]:
        soup = BeautifulSoup(response.text, 'lxml')
        script_tags = soup.select('script')
        for s in script_tags:
            script_code = s.getText()
            if 'window.rawData' in script_code:
                code_lines = script_code.split('\n')
                for line in code_lines:
                    if 'window.rawData' in line:
                        line = line.replace('window.rawData=', '')
                        line = line.strip(';').strip()
                        try:
                            window_raw_data = ujson.loads(line)
                        except Exception as e:
                            print(e)
                            pass
                        else:
                            if window_raw_data:
                                store = window_raw_data.get('store', None)
                                if store:
                                    return store.get('initDataObj', None)
                        break
                break


def up_div(a, b):
    c = a // b
    d = a % b
    if d:
        return c + 1
    else:
        return c


pdd_cat_1_map = defaultdict(str)
COLUMNS = ['关键词', '结果数量', '店铺id', '店铺商品数', '店铺销量', '宝贝id', '宝贝链接', '宝贝标题', '宝贝价格', '宝贝销量', '多多一级类目', '上架时间']
PDD_GOODS_URL_PREFIX = 'http://yangkeduo.com/goods.html?goods_id='


def init_pdd_cat_map():
    global pdd_cat_1_map
    cat_map = {}
    try:
        with open(PDD_CAT1_MAP_FILE, 'r') as rf:
            cat_map = ujson.load(rf)
    except UnicodeDecodeError:
        with open(PDD_CAT1_MAP_FILE, 'r', encoding='utf-8') as rf:
            cat_map = ujson.load(rf)
    finally:
        for cat in cat_map:
            pdd_cat_1_map.update({
                str(cat['id']): cat['stapleName'][0]
            })


# 要兼容gbk编码
def get_key_words():
    _keyword_list = []
    keyword_lines = []
    try:
        with open(KEY_WORDS_FILE, 'r', encoding='utf-8-sig') as rf:
            keyword_lines = rf.readlines()
    except UnicodeDecodeError:
        with open(KEY_WORDS_FILE, 'r', encoding='gbk') as rf:
            keyword_lines = rf.readlines()
    for l in keyword_lines:
        m = l.replace("\r", '').replace("\n", '')
        if len(m):
            _keyword_list.append(m)
    _keyword_list = list_unique(_keyword_list)
    return _keyword_list


def get_cfg():
    config = configparser.ConfigParser()
    try:
        config.read(CONFIG_FILE, encoding='gbk')
    except UnicodeDecodeError:
        config.read(CONFIG_FILE, encoding='utf-8-sig')

    # 66代理订单号,购买地址：http://www.66daili.cn
    global PROXY_ORDER_ID
    PROXY_ORDER_ID = config['DEFAULT']["PROXY_ORDER_ID"]
    if PROXY_ORDER_ID:
        print('66代理订单号：{}'.format(PROXY_ORDER_ID))
    # 搜索排序方式: [1]销量由高到低，[3]综合排序，[4]价格由高到低, [-4]价格由低到高
    global SORT_TYPE
    SORT_TYPE = int(config['DEFAULT']["SORT_TYPE"])
    if SORT_TYPE not in [1, 3, 4, -4]:
        print('排序方式未正确识别，默认用"综合排序".')
        SORT_TYPE = 3
    sort_map = {
        '1': '销量由高到低',
        '3': '综合排序',
        '4': '价格由高到低',
        '-4': '价格由低到高'
    }
    print("排序方式：{}".format(sort_map[str(SORT_TYPE)]))

    # 采集页数
    global SEARCH_PAGES
    SEARCH_PAGES = int(float(config['DEFAULT']["SEARCH_PAGES"]))
    if SEARCH_PAGES < 1 or SEARCH_PAGES > 300:
        print('采集页数超范围，默认50页.')
        SEARCH_PAGES = 50
    print("采集页数：{} 页".format(SEARCH_PAGES))

    # 过滤价格范围，对低价和最高价，单位元
    global MIN_PRICE
    global MAX_PRICE
    MIN_PRICE = float(config['DEFAULT']["MIN_PRICE"]) or MIN_PRICE
    MAX_PRICE = float(config['DEFAULT']["MAX_PRICE"]) or MAX_PRICE
    if MIN_PRICE < 0:
        MAX_PRICE = 0
    if MAX_PRICE < MIN_PRICE:
        MAX_PRICE = None
    print("\n过滤价格范围：{}-{} 元".format(MIN_PRICE, MAX_PRICE))

    # 过滤销量范围，整数
    global MIN_SALES
    global MAX_SALES
    MIN_SALES = int(float(config['DEFAULT']["MIN_SALES"])) or MIN_SALES
    MAX_SALES = int(float(config['DEFAULT']["MAX_SALES"])) or MAX_SALES
    if MIN_SALES < 0:
        MIN_SALES = 0
    if MAX_SALES < MIN_SALES:
        MAX_SALES = None
    print("过滤销量范围：{}-{}".format(MIN_SALES, MAX_SALES))
    # 是否过滤旗舰店和专营店, [1]是,[0]否
    global FILTER_SPECIAL_SHOPS
    FILTER_SPECIAL_SHOPS = int(config['DEFAULT']["FILTER_SPECIAL_SHOPS"]) or FILTER_SPECIAL_SHOPS
    print("是否过滤旗舰店和专营店：{}".format(FILTER_SPECIAL_SHOPS))
    # 是否过滤标题违禁词,[1]是,[0]否
    global FILTER_DANGER_WORDS
    FILTER_DANGER_WORDS = int(config['DEFAULT']["FILTER_DANGER_WORDS"]) or FILTER_DANGER_WORDS
    print("是否过滤标题违禁词：{}".format(FILTER_DANGER_WORDS))
    pass


def init_danger_words():
    global DANGER_WORDS_LIST
    if os.path.exists(DANGER_WORDS_FILE):
        with open(DANGER_WORDS_FILE, 'r') as rf:
            data = rf.readlines()
            danger_word_lines = []
            for _d in data:
                _d = _d.replace("\r", '').replace("\n", '')
                if len(_d):
                    danger_word_lines.append(_d)
            DANGER_WORDS_LIST = list(set(danger_word_lines))


def fetch_proxy():
    if not PROXY_ORDER_ID:
        print("未配置代理IP订单号")
        return None
    _66_proxy_url = 'http://api.66daili.cn/API/GetSecretProxy/?' \
                    'orderid={}&num=20&token=66daili&format=text' \
                    '&line_separator=win&protocol=http' \
                    '&region=domestic'.format(PROXY_ORDER_ID)
    _res = {}
    # noinspection PyBroadException
    try:
        _res = requests.get(_66_proxy_url)
    except Exception:
        import traceback
        # traceback.print_exc()
        print("请求代理出现异常,请检查网络！")
        time.sleep(1)
        return fetch_proxy()
    if _res.status_code == 200:
        data = _res.content.decode("utf-8")
        if ":" not in data:
            print('代理IP响应异常：{}'.format(data))
            if '秒后获取' in data:
                time.sleep(4)
                return fetch_proxy()
            return None
        return data.split("\r\n")[:-1]
    else:
        return None


def extract_goods(res_data):
    if res_data['success']:
        _goods_list = res_data['result']['goodsList']
        satisfied_goods_list = []
        filter_special_shops_cnt = 0
        filter_price_cnt = 0
        filter_sales_cnt = 0
        filter_dander_words_cnt = 0
        for goods in _goods_list:
            goods_id = goods['goodsId']
            goods_name = goods['goodsName']
            mall_id = goods['mallId']
            mall_name = goods['mallName']
            sales_tip = goods['salesTip']
            merchant_type = goods['merchantType']
            cat_id_1 = goods['catIds'][0]
            min_group_price = goods['minGroupPrice']
            goods_image_url = goods['goodsImageUrl']
            s = re.search(DATE_PATTERN, goods_image_url, flags=0)
            if s:
                goods_c_date = s.group() or ''
            else:
                goods_c_date = ''
            if FILTER_SPECIAL_SHOPS and merchant_type in [3, 5]:
                filter_special_shops_cnt += 1
                continue
            min_group_price = float(min_group_price / 100.0)
            if not (MIN_PRICE <= min_group_price <= MAX_PRICE):
                filter_price_cnt += 1
                continue
            sales_tip = sales_tip.replace("+", '')
            if '万' in sales_tip:
                sales = int(float(sales_tip.split("万")[0]) * 10000)
            else:
                sales = int(sales_tip)
            if not (MIN_SALES <= sales <= MAX_SALES):
                filter_sales_cnt += 1
                continue
            if FILTER_DANGER_WORDS:
                is_danger = False
                for dw in DANGER_WORDS_LIST:
                    if dw in goods_name:
                        is_danger = True
                        break
                if is_danger:
                    filter_dander_words_cnt += 1
                    continue
            satisfied_goods_list.append({
                "goods_id": goods_id,
                "goods_name": goods_name,
                "mall_id": mall_id,
                "mall_name": mall_name,
                "sales_tip": sales_tip,
                "cat_id_1": cat_id_1,
                "min_group_price": min_group_price,
                "goods_c_date": goods_c_date
            })
        _time_tik = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("{} 当前页面共采集到{}条数据，过滤完成剩{}条".format(_time_tik, len(_goods_list), len(satisfied_goods_list)))
        print('店铺类型不满足：{}条，价格不满足：{}条，销量不满足：{}条，标题违禁词：{}条'.format(
            filter_special_shops_cnt, filter_price_cnt, filter_sales_cnt, filter_dander_words_cnt))
        return satisfied_goods_list
    else:
        return None


def mk_res_dir():
    res_dir = os.path.join(ABS_PATH, '采集结果')
    if not os.path.exists(res_dir):
        os.mkdir(res_dir)
    date_str = time.strftime("%Y-%m-%d", time.localtime())
    date_res_dir = os.path.join(res_dir, date_str)
    if not os.path.exists(date_res_dir):
        os.mkdir(date_res_dir)
    return date_res_dir


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        multiprocessing.freeze_support()
        init_pdd_cat_map()
        _res_dir = mk_res_dir()
        init_danger_words()
        get_cfg()
        keyword_list = get_key_words()
        time_tik = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("\n{} 共读取到{}个关键词,下面开始采集...".format(time_tik, len(keyword_list)))
        page_range = list(range(SEARCH_PAGES))
        proxy_list = []

        router_ping_res = ping(ROUTER_HOST)
        if (RES_VER == 'PRO' or sys_str != 'Windows') and router_ping_res:
            use_proxy = False
        else:
            use_proxy = True
        # 普通版本，使用66代理

        for keyword in keyword_list:
            keyword_file = keyword.replace('/', '')
            csv_path = os.path.join(_res_dir, '{}.csv'.format(keyword_file))
            txt_path = os.path.join(_res_dir, '{}.txt'.format(keyword_file))
            if os.path.exists(csv_path):
                print("关键词[{}]今日已缓存，已在采集结果中".format(keyword))
                continue
            df = pd.DataFrame(columns=COLUMNS)
            pdd_links = []
            time_tik = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print('{} 开始采集关键字:{}'.format(time_tik, keyword))
            payload_data = {
                "keyword": keyword,
                "sortType": SORT_TYPE,
                "pageNum": 1,
                "pageSize": 100,
                "rangeItems": [{"rangeId": 1, "rangeFrom": 100, "rangeTo": 99999900}],
                "hasCoupon": None,
                "merchantTypeList": None,
                "listId": "0"
            }
            if sys_str == 'Windows' and RES_VER != 'PRO':
                proxy_list = fetch_proxy() or []
            elif RES_VER == 'PRO' or sys_str != 'Windows':
                proxy_list = [None] * 100
            remained_tasks = copy.deepcopy(page_range)
            if len(proxy_list):
                while True:
                    if stop_task:
                        break
                    if not len(remained_tasks):
                        time_tik = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        print("{} 当前关键词任务完成".format(time_tik))
                        break
                    task_cnt = min(len(proxy_list), len(remained_tasks))
                    g_req_tasks = []
                    for t in range(task_cnt):
                        PROXIES = {
                            "http": proxy_list[t],
                            "https": proxy_list[t]
                        }
                        payload_data.update({
                            "pageNum": 1 + remained_tasks[t]
                        })
                        req = grequests.post(QUERY_GOODS_LIST_PATH,
                                             params=(
                                                 ('pdduid', '0'),
                                                 ('__json', '1')
                                             ),
                                             timeout=3,
                                             headers=HEADERS,
                                             data=ujson.dumps(payload_data),
                                             proxies=PROXIES
                                             )
                        g_req_tasks.append(req)
                    time_tik = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    print("{} 请求发出".format(time_tik))
                    try:
                        resp = grequests.map(g_req_tasks, size=100, gtimeout=30)
                    except Exception:
                        print("请求超时！")
                    else:
                        time_tik = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        print("{} 请收到回复".format(time_tik))
                        for res in resp:
                            if not res:
                                continue
                            res_content = ujson.loads(res.content)
                            if res.status_code == 200:
                                req_body = ujson.loads(res.request.body)
                                page_num = req_body['pageNum']
                                time_tik = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                                print("{} 成功解析第{}页".format(time_tik, page_num))
                                remained_tasks.remove(page_num - 1)
                                goods_list = extract_goods(res_content)
                                if goods_list and len(goods_list):
                                    for pdd_goods in goods_list:
                                        cat_name = pdd_cat_1_map[str(pdd_goods['cat_id_1'])]
                                        goods_url = PDD_GOODS_URL_PREFIX + str(pdd_goods['goods_id'])
                                        if goods_url not in pdd_links:
                                            pdd_links.append(goods_url)
                                            new = pd.DataFrame({COLUMNS[0]: keyword,
                                                                COLUMNS[2]: pdd_goods['mall_id'],
                                                                COLUMNS[5]: pdd_goods['goods_id'],
                                                                COLUMNS[6]: goods_url,
                                                                COLUMNS[7]: pdd_goods['goods_name'],
                                                                COLUMNS[8]: '%.2f' % pdd_goods['min_group_price'],
                                                                COLUMNS[9]: pdd_goods['sales_tip'],
                                                                COLUMNS[10]: cat_name,
                                                                COLUMNS[11]: pdd_goods['goods_c_date'],
                                                                },
                                                               index=[1])
                                            df = df.append(new, ignore_index=True)
                            else:
                                pass
                    if use_proxy:
                        proxy_list = fetch_proxy() or []
                    else:
                        if len(remained_tasks):
                            res = reboot_router()
                            if res:
                                reboot_success = False
                                for i in range(15):
                                    time.sleep(1)
                                    if stop_task:
                                        print()
                                        break
                                else:
                                    time_out = 0
                                    while True:
                                        if stop_task:
                                            print()
                                            break
                                        ping_res = ping(BAIDU_HOST)
                                        if stop_task:
                                            print()
                                            break
                                        if ping_res:
                                            time_tik = time.strftime("%H:%M:%S", time.localtime())
                                            print()
                                            print("{} 网络连接已恢复！".format(time_tik))
                                            reboot_success = True
                                            time.sleep(1)
                                            break
                                        else:
                                            time.sleep(1)
                                            time_tik = time.strftime("%H:%M:%S", time.localtime())
                                            print("{} 正在等候网络连接恢复。".format(time_tik), end='\r')
                                            time_out += 1
                                        if time_out >= 60:
                                            print("网络连接超时！")
                                            break
                                    if not reboot_success:
                                        break

                                proxy_list = [None] * 100
                            else:
                                break
                        else:
                            break

                df[COLUMNS[1]] = df.shape[0]
                shop_detail_task = df.head(50)[COLUMNS[5]].tolist()
                remain_shop_ids = copy.deepcopy(shop_detail_task)
                while True:
                    if stop_task:
                        break
                    if not len(shop_detail_task):
                        break
                    if use_proxy:
                        proxy_list = fetch_proxy() or []
                    else:
                        res = reboot_router()
                        if res:
                            reboot_success = False
                            for i in range(15):
                                time.sleep(1)
                                if stop_task:
                                    print()
                                    break
                            else:
                                time_out = 0
                                while True:
                                    if stop_task:
                                        print()
                                        break
                                    ping_res = ping(BAIDU_HOST)
                                    if stop_task:
                                        print()
                                        break
                                    if ping_res:
                                        time_tik = time.strftime("%H:%M:%S", time.localtime())
                                        print()
                                        print("{} 网络连接已恢复！".format(time_tik))
                                        reboot_success = True
                                        time.sleep(1)
                                        break
                                    else:
                                        time.sleep(1)
                                        time_tik = time.strftime("%H:%M:%S", time.localtime())
                                        print("{} 正在等候网络连接恢复。".format(time_tik), end='\r')
                                        time_out += 1
                                    if time_out >= 60:
                                        print("网络连接超时！")
                                        break
                                if not reboot_success:
                                    break

                            proxy_list = [None] * ROUTER_BATCH
                        else:
                            break
                    task_cnt = min(len(proxy_list), len(shop_detail_task))
                    g_req_tasks = []
                    home_page_req = requests.get('http://yangkeduo.com',
                                                 headers=YANGKEDUO_HEADERS,
                                                 verify=False)
                    YANGKEDUO_HEADERS['Cookie'] = home_page_req.headers['Set-Cookie']

                    for t in range(task_cnt):
                        PROXIES = {
                            "http": proxy_list[t],
                            "https": proxy_list[t]
                        }
                        sample_goods_id = remain_shop_ids.pop()
                        req = grequests.get(GOODS_MAIN_PAGE,
                                            params=(('goods_id', str(sample_goods_id)),),
                                            timeout=2,
                                            headers=YANGKEDUO_HEADERS,
                                            proxies=PROXIES
                                            )
                        g_req_tasks.append(req)
                    time_tik = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    print("{} 请求发出".format(time_tik))

                    try:
                        resp = grequests.map(g_req_tasks, size=100, gtimeout=180)
                    except TimeoutError:
                        print('请求超时！')
                    else:
                        time_tik = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        print("{} 请求收到回复".format(time_tik))
                        resp = [process_goods_resp(res) for res in resp]
                        for init_data_obj in resp:
                            if not init_data_obj:
                                continue
                            mall_info = init_data_obj.get('mall', None)
                            if not mall_info:
                                continue
                            goods_id = init_data_obj['goods']['goodsID']
                            shop_goods_count = mall_info['goodsNum']
                            shop_sales_tip = mall_info['salesTip']
                            mall_id = mall_info['mallID']
                            print('店铺[id = {}]商品数：{}'.format(int(mall_id), shop_goods_count))
                            df.loc[df[COLUMNS[5]] == goods_id, COLUMNS[3]] = shop_goods_count
                            df.loc[df[COLUMNS[5]] == goods_id, COLUMNS[4]] = shop_sales_tip
                            if goods_id and goods_id in shop_detail_task:
                                shop_detail_task.remove(goods_id)
                        remain_shop_ids = copy.deepcopy(shop_detail_task)

                csv_data = df.to_csv(index=False)
                csv_data = csv_data.replace('\r\n', '\n')
                csv_data = csv_data.encode('gbk', 'ignore')
                with open(csv_path, 'wb') as f:
                    f.write(csv_data)
            else:
                import webbrowser

                webbrowser.open("http://www.66daili.cn/?dev=S8WWW")
                break
            time.sleep(3)

    except Exception:
        import traceback

        traceback.print_exc()
        time.sleep(1000)
    else:
        print("采集完成,可以关闭窗口！")
    while True:
        pass
