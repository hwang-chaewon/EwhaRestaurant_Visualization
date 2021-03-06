# -*- coding: utf-8 -*-
"""네이버크롤링_후반부_최종.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1d5VXQfxiWyGMXACWR9rLaXtsJQfNy3dc
"""

import pandas as pd
import numpy as np
from tqdm import tqdm_notebook
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import requests
from bs4 import BeautifulSoup

df = pd.read_csv('shops.csv', sep=',') ##################컴퓨터에 저장된 파일이름으로 바꿔야 함####################
columns = ['상호명', '상권업종대분류명','상권업종소분류명', 
           '시도명', '시군구명', '행정동명', '도로명주소', 
           '경도', '위도']
df=df[columns].copy()
df = df.loc[df['시군구명'] == '서대문구']
df_ = df.loc[df['상권업종대분류명'] =="음식"]

dong=sorted(set(list((df_['행정동명']))))
dong_list=[]
for i in range(len(dong)): 
    dong_list.append(df_.loc[df.행정동명==dong[i]])
    i+=1


print(dong)
a = input('url을 구할 동을 입력하세요: ')
k = dong.index(a)

df = pd.read_csv(str(dong[k]) + '.csv', sep=',', encoding = 'utf-8-sig')
print(str(dong[k]),'의 리뷰를 수집합니다.')

"""### 셀 설명
-**visitor_review_num_list**: 상점마다의 방문자 리뷰 수를 요소로 가지는 리스트 변수  
-**visitor_review_rate_list**: 상점마다의 방문자 리뷰 별점을 요소로 가지는 리스트 변수  
-**visitor_review_text_list**: 상점마다의 방문자 리뷰 텍스트를 요소로 가지는 리스트 변수  

-해당 상점의 방문자 리뷰 수, 방문자 리뷰 별점, 방문자 리뷰 텍스트를 크롤링 할 수 있는 경우, 크롤링하여 각 리스트에 저장합니다.  
-크롤링할 수 없는 경우, null값을 넣어줍니다.  
"""

visitor_review_num_list = []
visitor_review_rate_list = []
visitor_text_list = []
chromedriver = 'C:/crawling/chromedriver.exe'##################컴퓨터에 저장된 위치로 바꿔야 함####################
driver = webdriver.Chrome(chromedriver) 

e = 0 #################30단위로 끊어서 해주기####################

for i, url in enumerate(tqdm_notebook(df['naver_map_url'][e:e+30])):
    req = requests.get(url + '/review/visitor', headers = {
"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
})

    req.encoding = 'utf-8'
    source = req.text
    soup = BeautifulSoup(source, 'html.parser')
    driver.get(url + '/review/visitor')
    time.sleep(2)


    # 간단 정보 가져오기
    store_name = driver.find_element_by_css_selector("#_title > span._3XamX").text
    print("_____________________________")
    print('<',store_name,'>')
    
    try:
        # 방문자 리뷰 수
        visitor_review_num = driver.find_element_by_css_selector("#app-root > div > div > div > div:nth-child(7) > div:nth-child(2) > div.place_section.cXO6M > h2 > span.place_section_count").text
        print('방문자 리뷰 수: ',visitor_review_num)
        visitor_review_num_list.append(visitor_review_num)
    except:
        print(f"{i}행 리뷰수 문제가 발생")
        visitor_review_num_list.append('null')
        
    try:    
        # 방문자 별점 점수
        visitor_review_rate = driver.find_element_by_css_selector("#app-root > div > div > div > div:nth-child(7) > div:nth-child(2) > div.place_section._11ptV > div > div > div._2oZg_ > span._1fvo3.Sv1wj > em").text
        print('별점: ',visitor_review_rate)
        visitor_review_rate_list.append(visitor_review_rate)
    except:
        print(f"{i}행 별점 문제가 발생")
        visitor_review_rate_list.append('null')
        
    
    while True:
        try:
            driver.find_element(By.CLASS_NAME, "_3iTUo").click()
            time.sleep(1)
        except: 
            break
                
    # 끝까지 내렸으니 리뷰 수집해서 리스트에 넣기
    review_text_lists = driver.find_elements(By.CLASS_NAME, "WoYOw")
    if review_text_lists == []:
        review_text = 'null'
    else:
        review_text = []
        for i in review_text_lists:
            review_text.append(i.text)
            
    print(type(review_text))
    print(review_text)
    visitor_text_list.append(review_text)
driver.quit()

"""### 셀 설명
-**<i>visitor_review_num_list</i>** 의 정보를 받아 **<i>naver_visitor_review_num</i>** 열에 저장합니다.  

-**<i>visitor_review_rate_list</i>** 의 정보를 받아 **<i>naver_visitor_review_rate</i>** 열에 저장합니다.  

-**<i>visitor_review_text_list</i>** 의 정보를 받아 **<i>naver_visitor_review_text</i>** 열에 저장합니다.  
-저장 시 리뷰 텍스트가 없을 경우 null 값으로 변경해주고 기존 인덱스를 제거해줍니다.

-크롤링한 정보들을 행정동명_naver_result.csv파일로 저장합니다.
"""

df['naver_visitor_review_num'] = visitor_review_num_list  
df['naver_visitor_review_rate'] = visitor_review_rate_list
df['naver_visitor_review_text'] = visitor_text_list
df['naver_visitor_review_text'].replace('[]','null')
df.drop(df.columns[0], axis=1, inplace = True)
df.to_csv(str(dong[k]) + "_naver_result.csv", encoding="utf-8-sig")