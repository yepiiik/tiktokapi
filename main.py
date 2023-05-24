import grequests
import json
import time
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from fake_useragent import UserAgent

from modules.func import *

from modules import parser


if __name__ == '__main__':
    music_id = '7191094822155963179'

    musicStat = parser.AsyncMusicStatistic(music_id=music_id)
    musicStat.get()
    musicStat.stat_plot()

        