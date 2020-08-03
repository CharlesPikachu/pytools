'''
Function:
    特朗普推特数据下载
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import json
import requests


'''下载'''
def download():
    tweets = []
    for year in range(2009, 2021):
        url = f'http://www.trumptwitterarchive.com/data/realdonaldtrump/{year}.json'
        response = requests.get(url)
        response_json = response.json()
        for item in response_json:
            tweets.append(item)
    with open('trump_tweets.json', 'w', encoding='utf-8') as fp:
        json.dump(tweets, fp)


'''run'''
if __name__ == '__main__':
    download()