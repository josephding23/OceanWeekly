import requests
import pandas as pd
from lxml import etree
import re
from mongo_data.mongo_database import get_wechat_table
from datetime import datetime
from wechat_articles.util import *


def save_html(html_str, page_name):
    file_path = "html/lufa/{}.html".format(page_name)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_str)


def crawl_wechat_articles():
    import time
    UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'

    header = {
        "User-Agent": UserAgent
    }

    wechat_table = get_wechat_table()

    for article_info in wechat_table.find({'Other': {'$exists': False}}):
        if not within_one_week(article_info['CreateTime']):
            continue
        time.sleep(5)

        url = article_info['Link']
        response = requests.get(url, headers=header, verify=False)
        html_str = response.content.decode()

        html = etree.HTML(html_str)

        title = html.xpath("//*[@id=\"activity-name\"]/text()")
        title = [i.replace("\n", "").replace(" ", "") for i in title]

        source = html.xpath("//*[@id=\"js_name\"]/text()")
        source = [i.replace("\n", "").replace(" ", "") for i in source]

        other = html.xpath("//*[@id=\"js_content\"]//text()")

        title = ''.join(title)
        other = '\n'.join(other)
        cleaned_other = other.replace('\n', '').replace('\r', '').replace(' ', '')

        p1 = re.compile(r'\s*[（|(]20\d+[）|)]\s*[\u4e00-\u9fa5]*[\d]*[\u4e00-\u9fa5]+[\d]+号', re.S)
        anhao = re.search(p1, other)
        if anhao:
            anhao = anhao.group().replace("\n", "")
        else:
            anhao = ""

        p3 = re.compile('<div class="rich_media_content " id="js_content">.*?</div>', re.S)
        html = re.search(p3, html_str)
        if html:
            html = re.search(p3, html_str).group().replace("\n", "")

        else:
            html = html_str.replace("\n", "")

        additional_info = {
                 'TitleCrawled': title,
                 'Source': source,
                 'Other': other,
                 'CleanedOther': cleaned_other,
                 'AnHao': anhao,
                 'Html': html
             }
        print(additional_info)

        wechat_table.update_one(
            {'aid': article_info['aid']},
            {'$set': additional_info}
        )


def clean_other():
    wechat_table = get_wechat_table()
    for article_info in wechat_table.find({'CleanedOther': {'$exists': False}}):
        raw_other = article_info['Other']
        cleaned_other = raw_other.replace('\n', '').replace('\r', '').replace(' ', '')
        wechat_table.update_one(
            {'aid': article_info['aid']},
            {'$set': {'CleanedOther': cleaned_other}
        })


if __name__ == '__main__':
    clean_other()