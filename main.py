import grequests
import json
import time
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from fake_useragent import UserAgent

from modules.func import *


def stat_plot(df):
    if len(df) > 0:
        df.plot()
        plt.plot()
        plt.xlabel('Videos',fontsize=16)
        plt.ylabel('Views',fontsize=16)
        plt.legend()
        plt.show()


ua = UserAgent()
url = 'https://www.tiktok.com/api/music/item_list/'
headers = {
    'authority': 'www.tiktok.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'referer': 'https://www.tiktok.com/music/I-Feel-Bad-6790026525874849793?lang=en',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}


if __name__ == '__main__':
    dict_prop = {}
    with open('raw-x-tt-params.json', 'r') as file:
        dict_prop = json.loads(file.read())

    cursor = 0
    count = 30

    video_count = 0
    comment_count = 0
    digg_count = 0
    play_count = 0
    share_count = 0

    music_id = '7060154433442859010'

    stat_dict = {
        "commentCount": 0,
        "diggCount": 0,
        "playCount": 0,
        "shareCount": 0,
    }
    stat_df = pd.DataFrame(columns=stat_dict)

    rs = []
    try:
        while cursor < 3300:
            random_ua = ua.random
            dict_prop['count'] = count
            dict_prop['cursor'] = cursor
            dict_prop['musicID'] = music_id
            dict_prop['browser_version'] = random_ua
            headers['x-tt-params'] = generateToken(dict_prop)
            headers['user-agent'] = random_ua
            rs.append(grequests.get(url, headers=headers.copy()))

            cursor += count
        
        for r in grequests.map(rs, size=8):
            data = r.json()
            try:
                for video in data['itemList']:
                    video_count += 1
                    comment_count = video['stats']['commentCount']
                    digg_count = video['stats']['diggCount']
                    play_count = video['stats']['playCount']
                    share_count = video['stats']['shareCount']
                    stat_df.loc[len(stat_df)] = [comment_count, digg_count, play_count, share_count]
            except:
                print("Out of range")

    except:
        sorted_df = stat_df["playCount"].sort_values(ascending=False).reset_index()
        stat_plot(sorted_df)
        sorted_df.to_csv('data.csv')
        exit()

    sorted_df = stat_df["playCount"].sort_values(ascending=False).reset_index()
    stat_plot(sorted_df)
    sorted_df.to_csv('data.csv')

        