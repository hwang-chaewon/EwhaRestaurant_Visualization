# -*- coding: utf-8 -*-
"""google_crawling_ver4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JriJ4nTIhF52c8e25aTrgLDQbqk3Vu-n
"""

# Commented out IPython magic to ensure Python compatibility.
#기본적으로 필요한 라이브러리
import numpy as np
import pandas as pd
# %config IPCompleter.greedy=True
import requests

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import tqdm
from tqdm.notebook import tqdm

'''options = webdriver.ChromeOptions()
#options.add_argument('headless')    # 웹 브라우저를 띄우지 않는 headless chrome 옵션 적용
#options.add_argument('disable-gpu')    # GPU 사용 안함
options.add_argument('lang=ko_KR')    # 언어 설정
driver = webdriver.Chrome("chromedriver", options=options) #  옵션 적용'''

import os

path_dir = 'C:/Users/user/OneDrive - 이화여자대학교/3-1/05 파이썬과데이터분석'
#csv파일이 있는 폴더 경로 입력

for dirname, _, filenames in os.walk(path_dir):
    for filename in filenames:
        print(os.path.join(dirname, filename))

df = pd.read_csv("C:/Users/user/OneDrive - 이화여자대학교/3-1/05 파이썬과데이터분석/shops_seoul.csv", encoding='cp949')
#encoding은 한글을 읽기 위한 인코딩

df.columns.tolist()

df.head()

columns = ['상호명', '상권업종대분류명','상권업종소분류명', 
           '시도명', '시군구명', '행정동명', '지번주소','도로명주소', 
           '경도', '위도']
print(df.shape)
df=df[columns].copy()
df = df.loc[df['시군구명'] == '서대문구']
df = df.loc[df['상권업종대분류명'] =="음식"]
dong=sorted(set(list((df['행정동명']))))
print(dong)
dong_list=[]
for i in range(len(dong)): 
    dong_list.append(df.loc[df.행정동명==dong[i]])
    i+=1
dong_list[0]

# 이름과 주소를 입력하면 식당이름, 별점, 리뷰데이터를 리스트로 반환하는 함수
# 크롬창을 실행하는 함수 안에 넣어서 쓰는 함수, 크롤링 창 띄어진 후 실행하는 함수
def get_review_data(name, address): # name 은 검색어
    #driver = webdriver.Chrome("chromedriver", options=options) #  옵션 적용
    #driver.get("https://www.google.co.kr/maps/")
    # 검색창을 찾아서 검색하는 문단
    time.sleep(1)
    search_box = driver.find_element(By.ID, "searchboxinput")
    search_box.clear()
    search_box.send_keys(address+' '+name)
    search_box.send_keys(Keys.ENTER)
    time.sleep(3)
    
    try: # 목록이 여러개 있을 시 첫번째 선택 (바로 식당 리뷰로 넘어가지 않는 경우)
        driver.find_element(By.CLASS_NAME, 'hfpxzc').click()
        time.sleep(1)
    except:
        pass
    
    try: # 식당 이름 수집(혹시나 검색 결과가 다를 경우)
        shop = driver.find_element(By.CLASS_NAME, 'fontHeadlineLarge').text
    except: # 식당 리뷰로 바로 넘어가는 경우, 입력받은 식당 이름으로 받기
        shop = name     
        
    try: # 식당 주소 수집(나중에 확인용)
        address_element = driver.find_element(By.XPATH, "//button[contains(@aria-label,'주소')]")
        address_val = address_element.get_attribute('aria-label')
    except:
        address_val = '주소 존재하지 않음'
     
    try: # 리뷰 창으로 넘어가는 코드
        driver.find_element(By.XPATH, "//button[contains(@aria-label,'리뷰')]").click()
    except: # 리뷰가 없을 경우, 별점 0, 검색결과없음으로 감
        result = [shop, address_val, 0.0, '검색 결과 없음']
        #print(result)
        return result

    # 별점 정보 수집
    time.sleep(2)
    star = driver.find_element(By.CLASS_NAME, "fontDisplayLarge").text
    star = float(star)    
    #print(star)
           
    # 전체 화면 높이와 스크롤 바 위치 확인
    prev_height = driver.execute_script(
        "return document.querySelector('div.m6QErb.DxyBCb.kA9KIf.dS8AEf').scrollHeight")
    scroll = driver.find_element(By.CSS_SELECTOR, "div.m6QErb.DxyBCb.kA9KIf.dS8AEf")
    
    time.sleep(1)

    while True: # 무한 스크롤 코드
        driver.execute_script('arguments[0].scrollBy(0,{});'.format(prev_height), scroll)
        time.sleep(2)
        curr_height = driver.execute_script( # 현재 화면 높이 갖고 오기
            "return document.querySelector('div.m6QErb.DxyBCb.kA9KIf.dS8AEf').scrollHeight")
    
        if(curr_height == prev_height): # 현재 화면 높이와 내가 위치한 높이가 같으면 스크롤이 다 된것
            break
        else: # 아니면 현재 높이를 이전 높이에 대입하여 다음 비교에 사용함
            prev_height = curr_height
    
    # 리뷰 더 보기 버튼 클릭 부분
    buttons = driver.find_elements(By.XPATH, "//button[contains(@aria-label,'더보기')]")
    for n in range(len(buttons)):
        try:
            buttons[n].click()
        except:
            pass
    
    # 리뷰 텍스트 수집
    time.sleep(1)
    review_list = driver.find_elements(By.CLASS_NAME, "wiI7pd")
           
    for i in range(len(review_list)):
        review_list[i] = review_list[i].text
        #print("리뷰완료",i)
    result = [shop, address_val, star, review_list]
    
    return result

options = webdriver.ChromeOptions()
#options.add_argument('headless')    # 웹 브라우저를 띄우지 않는 headless chrome 옵션 적용
#options.add_argument('disable-gpu')    # GPU 사용 안함
options.add_argument('lang=ko_KR')    # 언어 설정
driver = webdriver.Chrome("chromedriver", options=options) #  옵션 적용

driver.get("https://www.google.co.kr/maps/")

search_box = driver.find_element(By.ID, "searchboxinput")
search_box.clear()
search_box.send_keys("위샐러듀 이대점")
search_box.send_keys(Keys.ENTER)

address_element = driver.find_element(By.XPATH, "//button[contains(@aria-label,'주소')]")
address_val = address_element.get_attribute('aria-label')
address_val

buttons = driver.find_elements(By.CLASS_NAME, "w8nwRe")
for n in range(len(buttons)):
    try:
        buttons[n].click()
    except:
        pass

review_list = driver.find_elements(By.CLASS_NAME, "wiI7pd")
review_list[1].text

for i in range(len(review_list)):
    review_list[i] = review_list[i].text
        #print("리뷰완료",i)
review_list

driver.find_element(By.CLASS_NAME, 'hfpxzc').click()

prev_height = driver.execute_script(
        "return document.querySelector('#pane > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf').scrollHeight")
scroll = driver.find_element(By.CSS_SELECTOR, "div.m6QErb.DxyBCb.kA9KIf.dS8AEf")
print(prev_height)

while True: # 무한 스크롤 코드
    driver.execute_script('arguments[0].scrollBy(0,{});'.format(prev_height), scroll)
    time.sleep(2)
    curr_height = driver.execute_script( # 현재 화면 높이 갖고 오기
        "return document.body.scrollHeight")
    
    if(curr_height == prev_height): # 현재 화면 높이와 내가 위치한 높이가 같으면 스크롤이 다 된것
        break
    else: # 아니면 현재 높이를 이전 높이에 대입하여 다음 비교에 사용함
        prev_height = curr_height

# 크롬 드라이버로 크롬 창 열기
options = webdriver.ChromeOptions()
#options.add_argument('headless')    # 웹 브라우저를 띄우지 않는 headless chrome 옵션 적용
#options.add_argument('disable-gpu')    # GPU 사용 안함
options.add_argument('lang=ko_KR')    # 언어 설정
driver = webdriver.Chrome("chromedriver", options=options) #  옵션 적용

# 정보 받을 리스트 생성
a = []

# 추출한 데이터에서 하나씩 리뷰 수집
for dong in dong_list:
    for i, keyword in enumerate(tqdm(dong['상호명'].tolist())):
        name = dong.상호명.values[i]
        address = dong.행정동명.values[i]
        driver.get("https://www.google.co.kr/maps/")
        a.append(get_review_data(name,address))
        print("_____________________________")
        print('<',a[i][0],'>')
        print('별점: ', a[i][1])
        print('방문자 리뷰')
        print(a[i][2])

driver.close()
print("검색 완료")

result = pd.DataFrame(a)
result

# result.to_csv('파일 경로', encoding='utf-8-sig') 저장하기
result.to_csv('C:/Users/user/OneDrive - 이화여자대학교/3-1/05 파이썬과데이터분석/google_result.csv', encoding='utf-8-sig')

for dong in dong_list:
    print(dong.행정동명,len(dong))

a[:116]

dong_list[0]

