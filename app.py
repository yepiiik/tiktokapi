from flask import Flask

from modules import parser

app = Flask(__name__)

@app.route("api/music_statistic/<int:music_id>")
def music_statistic(music_id):
    musicStat = parser.AsyncMusicStatistic(music_id=music_id)
    musicStat.get()
    views = musicStat.sorted_df['playCount'].sum()
    print(views)
    return str(views)


if __name__ == '__main__':
    app.run('127.0.0.1', '80')