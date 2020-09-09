# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import json


def crawl_wechat_test():

    url = "https://mp.weixin.qq.com/cgi-bin/appmsg"

    cookie_str = 'appmsglist_action_3565742034=card; ' \
                 'pgv_pvid=1414382316; pgv_pvi=1853451264; ' \
                 'RK=LaRw/zBpGo; ' \
                 'ptcz=1900128ecc5e530fb35c7f75d68617b24feace79db19d6c197d29311d4148acf; ' \
                 'tvfe_boss_uuid=aa56c4a5e831c3d1; ' \
                 'o_cookie=963723408; ' \
                 'pac_uid=1_963723408; ' \
                 'XWINDEXGREY=0; iip=0; ' \
                 '_ga=GA1.2.106070508.1597891261; ' \
                 '_qpsvr_localtk=0.7113230734667237; ' \
                 'uin=o0963723408; ' \
                 'ua_id=q8v7WdhkDzjCspr9AAAAALhwCeSyRFZXNcnSQtde6CA=; ' \
                 'pgv_si=s176842752; ' \
                 'sig=h01d6caddf90268c59f35ee91a2b0862a7e4b9518d466374fdfc8830ee31b913791975978433ad25ee8; ' \
                 'xid=; ' \
                 'mm_lang=zh_CN; ' \
                 'skey=@e4sVsLbfM; ' \
                 'uuid=65475409c608a533876ea5e8a13b0174; ' \
                 'rand_info=CAESIC1Aafsbbc9uj7h+xHSfyaFXEhcCY3FBfu29TuhL2rgg; ' \
                 'slave_bizuin=3565742034; data_bizuin=3565742034; ' \
                 'bizuin=3565742034; ' \
                 'data_ticket=qOzri1jmM6rmy3QSlucZweXlmbr+yijnzLnTqhEbAR5tCUoCfYwrOEFiP3cjE8xk; ' \
                 'slave_sid=YkJ5WVRXbUQySjJvenNHejRYV3NmQWhDc1h5TlNySUhIZnJxaGFINnB6XzVVVDZKa1pxRUZhV3JndDNoUUlONG1EWHlYbVFndV9KVm8zaE4zVDJKZ0pYel9CVnRlelNvaEtwOHRNQUgzVVN0cm9jcnZNaVQ5aGRCSzlDN1hKbGR3WDJuZlpJVTB3RXk0U1JC; ' \
                 'slave_user=gh_9b02dcc0030e; ' \
                 'openid2ticket_o0ueI1BhhdEV3eXk6qWPMmMpEgWw=spKHQXg+N9GEl/B5NI95trfYXngrs0qN3vt6wgBBsrM='

    UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'

    headers = {
        "Cookie": cookie_str,
        "User-Agent": UserAgent
    }

    data = {
        "token": "1811081321",
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1",
        "action": "list_ex",
        "begin": "0",
        "count": "5",
        "query": "",
        "fakeid": "MzI5OTEwNTE0NA==",
        "type": "9",
    }

    content_list = []
    for i in range(20):
        data["begin"] = i * 5
        time.sleep(3)
        content = requests.get(url, headers=headers, params=data, verify=False)
        # content.encoding = 'utf-8'
        content_json = content.json()

        for item in content_json["app_msg_list"]:
            items = [item["title"],
                     item["link"],
                     str(item["create_time"]),
                     str(item["update_time"]),
                     item["digest"],
                     item['aid']
                     ]

            print(items)

            content_list.append(items)

        name = ['title', 'link', 'create_time', 'update_time', 'digest', 'aid']
        test = pd.DataFrame(columns=name, data=content_list)
        test.to_csv("test.csv", mode='a', encoding='utf-8')
        print("保存成功")


if __name__ == '__main__':
    crawl_wechat_test()