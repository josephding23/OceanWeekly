import pymongo


def get_wechat_table():
    client = pymongo.MongoClient()
    return client.ocean_weekly.wechat_articles


def get_baidu_table():
    client = pymongo.MongoClient()
    return client.ocean_weekly.baidu_news


