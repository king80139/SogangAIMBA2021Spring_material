from bs4 import BeautifulSoup
from selenium import webdriver
import time
import datetime as dt
import pandas as pd
import re

# 키워드 지정하기
# 크롤링할 주제의 키워드를 리스트 안에 넣어줍니다.
keyword_list = ["서울대", "연세대", "고려대", "서강대", "성균관대", "한양대", "낙성대"]

# 순서대로 각 키워드 검색 결과 크롤링하기
for keyword in keyword_list:
    # 아래 option은 selenium을 통해 크롤링을 실행할 때 창을 열지 않고 진행하도록 하기 위함입니다.
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
    )
    # 아래 path에 필요한 chromedriver의 경로를 작성해줍니다.
    path = "/Users/ssakoon/Downloads/chromedriver"
    # 위에서 설정한 option과 경로를 바탕으로 selenium.webdriver로 Chrome 브라우저를 지정해줍니다.
    browser = webdriver.Chrome(path, chrome_options=options)

    # 크롤링할 날짜 지정하기
    startdate, untildate, enddate = dt.date(year=2021, month=3, day=1), dt.date(year=2021, month=3, day=2), dt.date(
        year=2021, month=3, day=18)
    keyword = keyword
    language = "ko"

    df = pd.DataFrame(columns=["date", "contents"])

    # 크롤링 부분
    dates = []
    contents = []
    while not enddate == startdate:  # 끝날짜와 시작날짜가 같지 않다면
        url = 'https://twitter.com/search?l=' + language + '&q=' + keyword + \
              '%20since%3A' + str(startdate) + '%20until%3A' + str(untildate)
        browser.get(url)
        time.sleep(1)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')

        lastHeight = browser.execute_script(
            "return document.body.scrollHeight")
        while True:
            cleaner = re.compile('<.*?>')
            unicode_list = re.compile(r'''[\\u]%d{4,5}''')
            key_enter = re.compile(r'''[\n]''')

            # 스크롤 내리기
            browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            newHeight = browser.execute_script(
                "return document.body.scrollHeight")
            # 끝까지 내렸을때의 페이지의 길이로 lastHeight 갱신
            if newHeight != lastHeight:
                lastHeight = newHeight

            else:
                html = browser.page_source
                soup = BeautifulSoup(html, 'html.parser')
                contents = soup.find_all("div", {
                    "class": "css-901oao r-jwli3a r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0"})
                contents_rtl = soup.find_all(
                    "p", {"class": "TweetTextSize js-tweet-text tweet-text tweet-text-rtl"})
                contents_total = contents + contents_rtl

                tw = []
                for t in contents_total:
                    t = re.sub(cleaner, "", str(t))
                    t = re.sub(unicode_list, "", t)
                    tw.append(t)

                dates = [startdate] * len(tw)

                startdate = untildate
                untildate += dt.timedelta(days=1)

                daily_df = pd.DataFrame({"date": dates, "contents": tw})
                # display(daily_df)

                df = pd.concat([df, daily_df], axis=0, sort=True)
                break
            df = df.reset_index(drop=True)

    df.to_excel("SogangAIMBA_multiTwitter.xlsx", index = True)