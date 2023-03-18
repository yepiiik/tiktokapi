import requests
import json
import time
import os

from fake_useragent import UserAgent

from modules.func import *


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
    count = 15

    # folder_path = 'data/{}/'.format(time.time())
    # os.mkdir(folder_path)

    video_count = 0
    comment_count = 0
    digg_count = 0
    play_count = 0
    share_count = 0
    round = 0

    music_id = '6848462047387060225'

    while True:
        random_ua = ua.random
        dict_prop['count'] = count
        dict_prop['cursor'] = cursor
        dict_prop['musicID'] = music_id
        dict_prop['browser_version'] = random_ua
        headers['x-tt-params'] = generateToken(dict_prop)
        headers['user-agent'] = random_ua
        response = requests.get(url, headers=headers, timeout=5)
        response_copy = response
        response.close()
        data = response_copy.json()
        
        if round % 10 == 0: time.sleep(3.0)

        try:
            for video in data['itemList']:
                video_count += 1
                comment_count += video['stats']['commentCount']
                digg_count += video['stats']['diggCount']
                play_count += video['stats']['playCount']
                share_count += video['stats']['shareCount']
        except:
            print("Out of range")

        # with open('{}cursor{}.json'.format(folder_path, cursor), 'w') as file:
        #     file.write(json.dumps(data))

        os.system('cls')
        print("Total Videos:\t\t{}\nComment Count:\t\t{}\nDigg Count:\t\t{}\nPlay Count:\t\t{}\nShare Count:\t\t{}\nCursor:\t\t{}\n".format(video_count, comment_count, digg_count, play_count, share_count, cursor))
        if cursor == int(data['cursor']): break
        cursor = int(data['cursor'])
        round += 1
