import requests
from bs4 import BeautifulSoup


def search_news_test():
    keyword = "海洋"
    try:
        params = {
            'tn': 'news',
            'rtt': 4,
            'bsst': 1,
            'cl': 2,
            'medium': 0,
            'wd': keyword}
        r = requests.get("http://www.baidu.com/s", params=params)
        print(r.request.url)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, 'html.parser', from_encoding='utf-8')

        for item in soup.find_all(name='h3', attrs={'class': 'news-title_1YtI1'}):
            print(item.a['href'])  # Urls

        for item in soup.find_all(name='span', attrs={'class': 'c-color-gray c-font-normal c-gap-right'}):
            print(item.text)  # Source

        for item in soup.find_all(name='span', attrs={'class': 'c-color-gray2 c-font-normal'}):
            print(item.text)  # Time

    except:
        print("Error!")


if __name__ == '__main__':
    search_news_test()