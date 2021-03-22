from bs4 import BeautifulSoup
from selenium import webdriver
import time
import datetime as dt
import pandas as pd
import re


# 키워드 지정하기
# 크롤링할 주제의 키워드를 리스트 안에 넣어줍니다.
keyword = '서강대학교'
startdate = dt.date(year=2020, month=11, day=14)
untildate = startdate + dt.timedelta(days=1)

# 아래 path에 필요한 chromedriver의 경로를 작성해줍니다.
path = "/Users/ssakoon/Downloads/chromedriver"
# 위에서 설정한 option과 경로를 바탕으로 selenium.webdriver로 Chrome 브라우저를 지정해줍니다.
browser = webdriver.Chrome(path)
language = "ko"

# url패턴으로 타겟 url로 접속해 html구조 알아내기
url = 'https://twitter.com/search?l='+language+'&q='+keyword+'%20since%3A'+str(startdate)+'%20until%3A'+str(untildate)
browser.get(url)
time.sleep(1)

html = browser.page_source  # 접속한 url의 html구조 가져오기 (단, 로딩된 데이터만!)
soup = BeautifulSoup(html, 'html.parser')  # BeautifulSoup으로 html구조 파싱


# 원하는 메세지가 있는 html의 구조를 파악해 가져와 내용 담기
contents = soup.find_all("div", {
                         "class": "css-901oao r-1fmj7o5 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0"})

# html 구조에서 정규표현식을 이용해 원하는 정보만 가져오도록 설정합니다.
# html 태그 제거
cleaner = re.compile('<.*?>')
# unicode 특수문자 제거
unicode_list = re.compile(r'''[\\u]%d{4,5}''')
tw = []
for t in contents:
    t = re.sub(cleaner, "", str(t))
    t = re.sub(unicode_list, "", t)
    tw.append(t)
dates = [startdate]*len(tw)

# 담아온 내용 DataFrame에 담기
daily_df = pd.DataFrame({"date": dates, "contents": tw})

daily_df = daily_df.reset_index(drop=True)
daily_df.to_excel("SogangAIMBA_SimpleCrawling_demo.xlsx", index=False)
