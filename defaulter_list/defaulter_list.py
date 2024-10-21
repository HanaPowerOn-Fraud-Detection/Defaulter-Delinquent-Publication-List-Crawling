import requests
from bs4 import BeautifulSoup
import pandas as pd


page = 1

headers = ['성명', '나이', '주소', '임차보증금반환채무', '이행기', '채무불이행기간', '이행일', '구상채무', '강제집행 횟수', '기준일']
rows = []

for i in range(5):
    page += i
    url = f"https://www.molit.go.kr/USR/WPGE0201/m_37180/DTL.jsp?page={page}&searchCriteria=null"
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')

    table = soup.find("table", {"class": "table"})

    for tr in table.find('tbody').find_all('tr'):
        cells = tr.find_all('td')
        row = [cell.get_text(strip=True) for cell in cells]
        rows.append(row)

df = pd.DataFrame(rows, columns=headers)

# 결과 출력
print(df)

# CSV 파일로 저장
df.to_csv('defaulter_list.csv', index=False, encoding='utf-8-sig')

