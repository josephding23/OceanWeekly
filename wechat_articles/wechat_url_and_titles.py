# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import json
from mongo_data.mongo_database import get_wechat_table
from wechat_articles.util import *


def crawl_wechat():

    url = "https://mp.weixin.qq.com/cgi-bin/appmsg"

    cookie_str = 'appmsglist_action_3565742034=card; pgv_pvid=1414382316; pgv_pvi=1853451264; RK=LaRw/zBpGo; ptcz=1900128ecc5e530fb35c7f75d68617b24feace79db19d6c197d29311d4148acf; tvfe_boss_uuid=aa56c4a5e831c3d1; o_cookie=963723408; pac_uid=1_963723408; XWINDEXGREY=0; iip=0; _ga=GA1.2.106070508.1597891261; _qpsvr_localtk=0.7113230734667237; uin=o0963723408; ua_id=q8v7WdhkDzjCspr9AAAAALhwCeSyRFZXNcnSQtde6CA=; pgv_si=s176842752; sig=h01d6caddf90268c59f35ee91a2b0862a7e4b9518d466374fdfc8830ee31b913791975978433ad25ee8; xid=; mm_lang=zh_CN; skey=@e4sVsLbfM; rewardsn=; wxtokenkey=777; uuid=3acd78bac358be0f3b7a2bcf619f3388; rand_info=CAESIMbUAL42W+468f2QIKs5WcQrIwY3JAeujoTQojkL9o7R; slave_bizuin=3565742034; data_bizuin=3565742034; bizuin=3565742034; data_ticket=579Y+2mZHtiaZp1j9fw7d4T+lPxkMB3S/mnw7/lejd7vDpLNyp/aPZbPzBEPaBqP; slave_sid=aDdLMU9ZUUlWNnh6Z3NEMG82ZnVjX1BKQ2lvSmVYMmEzNDN2QmN4XzlnWUI4RzV6a2Q1dXlpMjZfSXlubnZfQ2RHZzRkUUlDUUxzaDZPSkZkQ3hnal9rUjdUUGxOTWxVeDZqN2JXNGR0YXpLQVBFMXpSSmNWZzE3VlIyQ1JzckhLQm93Ykxpd1FlYUZGajN1; slave_user=gh_9b02dcc0030e; openid2ticket_o0ueI1BhhdEV3eXk6qWPMmMpEgWw=ZBJ1u/MIEeUHnuhsuj3I+0YVyoX1Iop9t0+k6gt/czc='
    UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'

    headers = {
        "Cookie": cookie_str,
        "User-Agent": UserAgent
    }
    data = {
        "token": "213910677",
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1",
        "action": "list_ex",
        "begin": "0",
        "count": "5",
        "query": "",
        "fakeid": "MzU2NDc1MjAzOQ==",
        "type": "9",
    }

    wechat_table = get_wechat_table()

    for i in range(20):
        data["begin"] = i * 5
        time.sleep(5)
        content = requests.get(url, headers=headers, params=data, verify=False)
        # content.encoding = 'utf-8'
        content_json = content.json()

        for item in content_json["app_msg_list"]:
            create_time = item["create_time"]
            if not within_one_week(create_time):
                print(create_time)
                return
            if wechat_table.count({'aid': item['aid']}) == 0:
                article_info = {
                    'aid': item['aid'],
                    'Title': item["title"],
                    'Link': item["link"],
                    'CreateTime': item["create_time"],
                    'UpdateTime': item["update_time"],
                    'Digest': item["digest"],
                }
                wechat_table.insert_one(article_info)
                print('new article:')
                print(article_info)

            else:
                print(f"{item['aid']} already exists!")

            # article_time = datetime.fromtimestamp(item["create_time"])
            # print(article_time, print(article_time > earliest_time))

        print(f'Page {i} finished')


def drop_late():
    wechat_table = get_wechat_table()

    for article_info in wechat_table.find():
        if not within_one_week(article_info['CreateTime']):
            wechat_table.delete_one({'aid': article_info['aid']})
            print(f"{article_info['aid']} deleted")


if __name__ == '__main__':
    crawl_wechat()