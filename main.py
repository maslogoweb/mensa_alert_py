# coding: UTF-8
import requests
from bs4 import BeautifulSoup
from flask import *
import re

app = Flask(__name__)


@app.route('/getschedules')
def getschedules():
    try:
        target_url = 'https://mensa.jp/exam/'

        r = requests.get(target_url)  # requestsを使って、webから取得
        soup = BeautifulSoup(r.content, 'html.parser')  # 要素を抽出
        all_date = soup.find_all("li", class_="date")
        result = []
        for date in all_date:

            # prefecture
            pattern = r'([\u30e0-\u9fcf]{2,3}[都,道,府,県])'
            matches = re.finditer(pattern, str(date), flags=re.MULTILINE)
            for match in matches:
                prefecture = str(match.groups()[0])
                print(prefecture)
                break

            # datetime
            pattern = r'日時 ： (.*)<br'
            matches = re.finditer(pattern, str(date), flags=re.MULTILINE)
            for match in matches:
                datetime = str(match.groups()[0])
                print(datetime)
                break

            result.append({'prefecture': prefecture, 'datetime': datetime})

        all_link = soup.find_all("li", class_="link")
        for i, link in enumerate(all_link):
            # state
            pattern = r'alt="(.*)" src'
            matches = re.finditer(pattern, str(link), flags=re.MULTILINE)
            for match in matches:
                state = str(match.groups()[0])
                print(state)
                break

            result[i]['state'] = state
    except:
        result = 'error'

    result = jsonify({'result': result})
    return result

if __name__ == "__main__":
    app.run(debug=True)
