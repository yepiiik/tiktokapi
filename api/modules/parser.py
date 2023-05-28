import grequests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import math
from progress.bar import IncrementalBar

from fake_useragent import UserAgent

from . import func


class AsyncMusicStatistic:
    def __init__(self, music_id, max_cursor=3300):
        self.ua = UserAgent()
        self.url = 'https://www.tiktok.com/api/music/item_list/'
        self.headers = {
            'authority': 'www.tiktok.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        }
        self.rs = []
        self.max_cursor = max_cursor
        self.music_id = music_id
    
    def get(self):
        self.rs.clear()
        self.stat_dict = {
            "commentCount": 0,
            "diggCount": 0,
            "playCount": 0,
            "shareCount": 0,
        }
        self.stat_df = pd.DataFrame(columns=self.stat_dict)
        cursor = 0
        count = 30

        video_count = 0
        comment_count = 0
        digg_count = 0
        play_count = 0
        share_count = 0

        dict_prop = {}
        with open('api/raw-x-tt-params.json', 'r') as file:
            dict_prop = json.loads(file.read())
        
        os.system("cls")
        print(f"Statistic for music: {self.music_id}")
        print("Making request, please wait (it maybe about 15-60 seconds depends on Internet speed)")

        while cursor < self.max_cursor:
            random_ua = self.ua.random
            dict_prop['count'] = count
            dict_prop['cursor'] = cursor
            dict_prop['musicID'] = self.music_id
            dict_prop['browser_version'] = random_ua
            self.headers['x-tt-params'] = func.generateToken(dict_prop)
            self.headers['user-agent'] = random_ua
            self.rs.append(grequests.get(self.url, headers=self.headers.copy()))
            cursor += count

        bar = IncrementalBar('Progress', max = len(self.rs))

        for r in grequests.map(self.rs, size=8):
            data = r.json()
            try:
                for video in data['itemList']:
                    video_count += 1
                    comment_count = video['stats']['commentCount']
                    digg_count = video['stats']['diggCount']
                    play_count = video['stats']['playCount']
                    share_count = video['stats']['shareCount']
                    self.stat_df.loc[len(self.stat_df)] = [comment_count, digg_count, play_count, share_count]
            except:
                print("Out of range")

            bar.next()
        bar.finish()
        
        self.__save_result()
        
    
    def stat_plot(self):
        if len(self.sorted_df) > 0:
            self.sorted_df.plot()
            plt.plot()
            plt.xlabel('Videos',fontsize=16)
            plt.ylabel('Views',fontsize=16)
            plt.legend()
            plt.show()

    def __save_result(self):
        self.sorted_df = self.stat_df["playCount"].sort_values(ascending=False).reset_index()
        self.sorted_df.to_csv(f"api/data/{self.music_id}.csv")
