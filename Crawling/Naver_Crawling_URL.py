# -*- coding: utf-8 -*-
"""네이버크롤링_전반부_최종.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1i0Rf_iLaSCchlZAuZuYAc3TqEOSZPh1l
"""

import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

"""### 셀 설명
-**shop.csv** 파일의 데이터 중 서대문구에 위치하고, 상권업종대분류명이 음식인 상점들의 데이터셋을 불러옵니다.  

-**<i>각 동의 DataFrame</i>** 을 만들어주고, 이들을 요소로 하는 list 변수인 <i>**dong_list**</i> 를 생성합니다.  

-**<i>dong</i>** 은 서대문구의 행정동명을 요소로 하는 list 변수입니다.
    
-url을 수집하고 싶은 동을 입력하면, **<i>dong</i>**에서 **<i>해당 동의 인덱스</i>** 를 찾아 해당 값을 **k** 에 저장합니다. 
"""

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

dong_list[k]['naver_keyword'] = [i for i in range(len(dong_list[k]))]
dong_list[k]['naver_map_url'] = ''

"""### 셀 설명
-**<i>dong_list</i>** 의 데이터셋을 기반으로 하여 네이버 맵에 *'행정동명 + 상호명'* 의 형태로 검색한뒤, 검색결과로부터 상점의 url을 불러와서 **<i>dong_list</i>**  DataFrame에 저장합니다.  

-이를 위해 새로운 2개의 열을 **<i>dong_list</i>** DataFrame에 생성합니다  
**'naver_keyword'**: 크롤링으로 네이버 맵 사이트에 검색시 입력할 글자(행정동명 + 상호명의 형태)  
**'naver_map_url'**: 크롤링으로 가져온 해당 상점의 url

-검색이 되지 않는 상점의 경우 null 값을 대입합니다.
"""

chromedriver = 'C:/crawling/chromedriver.exe'##################chromedriver 설치 위치에 따라 변경할 것####################
driver = webdriver.Chrome(chromedriver)

e = 0 ###끝날때마다 재설정해줄것, 막힘 방지 위해 100개씩 끊어서 한번 돌리면 e를 100씩 증가시키면 됨###


dong_list[k]['naver_keyword'][e:e+100] = dong_list[k]['행정동명'][e:e+100]+'%20'+dong_list[k]['상호명'][e:e+100]
dong_list[k]['naver_map_url'][e:e+100] = ''



for i, keyword in enumerate(dong_list[k]['naver_keyword'][e:e+100].tolist()):
    
    print("이번에 찾을 키워드 :", i, f"/ {dong_list[k][e:e+100].shape[0] - 1} 행", keyword)
    try:
        naver_map_search_url = f"https://m.map.naver.com/search2/search.naver?query={keyword}&sm=hty&style=v5"
        driver.get(naver_map_search_url)
        
        time.sleep(3.5)
        dong_list[k][e:e+100].iloc[i,-1] = driver.find_element_by_css_selector("#ct > div.search_listview._content._ctList > ul > li:nth-child(1) > div.item_info > a.a_item.a_item_distance._linkSiteview").get_attribute('data-cid')
    except Exception as e1:
        if "li:nth-child(1)" in str(e1):
            try:
                dong_list[k][e:e+100].iloc[i,-1] = driver.find_element_by_css_selector("#ct > div.search_listview._content._ctList > ul > li:nth-child(1) > div.item_info > a.a_item.a_item_distance._linkSiteview").get_attribute('data-cid')
                time.sleep(1)
            except Exception as e2:
                print(e2)
                dong_list[k][e:e+100].iloc[i,-1] = np.nan
                time.sleep(1)
        else:
            pass

driver.quit()

"""### 셀 설명
-상점의 url을 **<i>"https://m.place.naver.com/restaurant/" + dong_list[k]['naver_map_url']</i>** 형태로 **<i>'naver_map_url'</i>** 열에 저장해줍니다.  

-url이 수집되지 않은 상점의 경우, 해당 상점의 데이터를 제거합니다.  

-수집된 해당 동 상점들의 url이 포함된 <i>**dong_list**</i> DataFrame을 **<i>'행정동명.csv'</i>** 이름의 파일로 만들어줍니다.
"""

dong_list[k]['naver_map_url'] = "https://m.place.naver.com/restaurant/" + dong_list[k]['naver_map_url']
dong_list[k] = dong_list[k].loc[~dong_list[k]['naver_map_url'].isnull()]
dong_list[k].to_csv(str(dong[k]) + ".csv", mode='w')
print(str(dong[k] + '의 url 수집 완료'))

