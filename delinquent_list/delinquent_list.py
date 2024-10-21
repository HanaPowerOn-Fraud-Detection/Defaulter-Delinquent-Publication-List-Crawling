import requests
from bs4 import BeautifulSoup
import pandas as pd

# url = "https://www.nts.go.kr/nts/ad/openInfo/selectList.do"
# request = requests.get(url)
# soup = BeautifulSoup(request.text, 'html.parser')

# # 테이블 선택
# table = soup.find("table")
# print(table)

# # 헤더 추출 (실제 데이터를 기준으로 맞추기 위해 두 번째 헤더 행만 추출)
# headers = []
# for th in table.find_all('th'):
#     headers.append(th.get_text(strip=True).replace("\n", ""))

# print(headers)


headers = ['No', '공개년도', '법인명', '대표자', '업종', '법인소재지', '대표자 주소', '총 체납액', '세목', '납기', '체납건수', '체납요지']
rows = []

# 페이지 수 설정 (예: 1부터 10까지 크롤링)
for page in range(1, 11):  # 1부터 10 페이지까지
    url = "https://www.nts.go.kr/nts/ad/openInfo/selectList.do"
    
    # POST 요청을 위한 데이터 준비
    data = {
        'currPage': page,
        'maxSn': 20,
        'tcd': 1,
        'pageIndex': 20,
        'search_order': 1,
        'minSn': (page - 1) * 20,  # 페이지에 따라 minSn 계산
    }
    
    # POST 요청
    request = requests.post(url, data=data)
    
    # 요청이 성공적으로 이루어졌는지 확인
    if request.status_code == 200:
        soup = BeautifulSoup(request.text, 'html.parser')
        table = soup.find("table")
        
        if table:  # 테이블이 존재하는지 확인
            for tr in table.find('tbody').find_all('tr'):
                cells = tr.find_all('td')
                row = [cell.get_text(strip=True) for cell in cells]
                rows.append(row)
        else:
            print(f"Page {page}: No table found")
    else:
        print(f"Failed to retrieve page {page}: {request.status_code}")

df = pd.DataFrame(rows, columns=headers)
print(df)

df.to_csv('delinquent_list.csv', index=False, encoding='utf-8-sig')
