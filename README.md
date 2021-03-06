# EwhaRestaurant_visualization
이화여대 주변의 음식점 데이터 시각화 프로젝트

# 이화여대 주변 음식점 리뷰 데이터 시각화

## 목차
1. 소개
2. 프로젝트 설명
3. 파일 설명
4. 시작하기
5. 메뉴1
6. 메뉴2
7. 메뉴3
8. 메뉴4
9. 메뉴5
10. 실행 문제점
11. 고려 사항
---

## 1. 소개
본 프로젝트는 이화여대 주변 음식점에 대한 기본적인 데이터를 갖고 리뷰 데이터 및 관련 정보를 직접 크롤링하여 사용자가 정보를 쉽게 사용할 수 있도록 시각화 하는 것에 집중하였습니다.


## 2. 프로젝트 설명
최근 많은 양의 리뷰 데이터가 쌓이면서 음식점을 선택하는 데에 리뷰가 중요한 요소가 되어 사람들은 음식점을 고르는 데에 리뷰 데이터를 많이 참고하기 시작했습니다. 이러한 과정 속에서 방대한 양의 리뷰를 사용자가 읽어야 한다는 번거로움이 발생하고, 이러한 문제에 집중하여 리뷰 정보를 용이하게 확인할 수 있도록 하였습니다. 단순히 리뷰 데이터 뿐만 아니라 음식점의 위치 정보, 영업시간 및 배달여부 등 다양한 방면으로 음식점들에 대한 정보를 접할 수 있도록 프로그램을 구현하였습니다.

- 실행 환경 : 구글 코랩
- 개발 언어 : 파이썬



## 3. 파일 설명
### 디렉토리 Path
 - 데이터 디렉토리 : `/content/gdrive/MyDrive/파데분플젝/최종/데이터/`
 - 실행 코드 디렉토리 : `/content/gdrive/MyDrive/파데분플젝/최종/최종코드/`

### 데이터 목록
  - shops.csv : 음식점 기본 정보 데이터 파일
  - final_all.csv : 모든 식당들의 리뷰 데이터  파일
  - 음식점방문수.csv : 요일에 따른 방문자 수를 표시한 데이터 파일
  - 영업시간, 배달 crawling data 폴더 안 00동_result.csv : 행정동별 영업시간, 배달여부 데이터 파일

### 코드 목록
  - 이화여대 주변의 음식점 데이터 시각화 프로젝트.ipynb : 본 프로그램 실행 파일
  - Naver_crawling.ipynb : 네이버 플레이스 크롤링 코드 파일
  - google_crawling.ipynb : 구글맵 크롤링 코드 파일
  - 영업시간, 배달여부_Naver_crawling.ipynb : 네이버 플레이스에서 영업시간, 배달여부 크롤링 코드 파일
  - crawling데이터합치기.ipynb : 크롤링한 네이버, 구글 데이터 통합 코드 파일


## 4. 시작하기
![title](https://i.ibb.co/8sYntTN/01.png)  
첫 번째 코드블럭을 실행하여 폰트를 설치해 줍니다.

![title](https://i.ibb.co/YB2qqty/02.png)   
폰트 설치 후 런타임 - 런타임 다시 시작을 눌러줍니다.

![title](https://i.ibb.co/k4Jdk8T/03.png)   
데이터 파일 경로를 data_path에 입력해줍니다.

![title](https://i.ibb.co/xMbTyqJ/04.png)   
전체 실행을 한 후, 원하는 메뉴를 실행시키면 됩니다.


## 5. 메뉴1 : '음식점 위치, 리뷰 평점, 도로명 주소' 데이터 시각화
![title](https://i.ibb.co/VQtdVkK/05.png)   
folium 라이브러리를 활용해 음식점 위치를 아이콘으로 시각화하여 사용자에게 보여줍니다. 사용자가 행정동명을 검색하면 해당 행정동명에 위치한 음식점을 사용자에 선택에 따라 2가지 모드(전체 뷰 모드, 검색 모드)로 보여줍니다. 전체 뷰 모드에서는 선택한 행정동명의 전체 음식점 분포를 확인 가능합니다. 검색 모드에서는 원하는 음식점의 현재 나와의 거리와 주소를 확인할 수 있습니다.


## 6. 메뉴2 : '영업시간, 배달 여부' 데이터 시각화
![title](https://i.ibb.co/26hvQrM/06.png)   
matplotlib.pyplot 라이브러리를 활용해 영업 시간을 시각화해주고, 배달 가능 여부를 알려줍니다. 가게의 영업 시간과 배달 여부를 사용자가 원하는 하에 연속적으로 확인할 수 있습니다.


## 7. 메뉴3 : '최다리뷰수, 최고리뷰평점의 음식점' 데이터 시각화
![title](https://i.ibb.co/C1xxwz8/07.png)   
![title](https://i.ibb.co/4MGRpgV/08.png)   
크롤링한 데이터 기반 음식점 요일별 방문자수, 최다리뷰수, 최고리뷰평점의 음식점 정보를 그래프(히트맵, 히스토그램)로 시각화하여 보여줍니다.


## 8. 메뉴4 : '리뷰텍스트' 정보 말뭉치 시각화
![title](https://i.ibb.co/5n0Z660/09.png)   
사용자에게 크롤링한 리뷰 데이터를 기반으로 한 해당 음식점의 리뷰 말뭉치를 생성하여 보여줍니다.


## 9. 메뉴5 : '리뷰 텍스트' 파이 차트 시각화
![title](https://i.ibb.co/6W6JGp9/10.png)   
크롤링한 리뷰 데이터를 기반으로 하여 사용자가 원하는 지역과 키워드 세 개를 입력하면, 키워드 세 개의 빈도수가 가장 높은 식당을 찾아 해당 키워드 각각이 전체 리뷰에서 몇 퍼센트를 차지하고 있는지 파이차트로 시각화하여 보여줍니다.


## 10. 실행 문제점
- 각 메뉴가 실행 될 때마다 데이터를 처리하기 때문에 다소 로딩 시간이 길 수 있습니다.
- 폰트와 라이브러리 설치가 제대로 되지 않을 시 프로그램 실행 과정에 문제가 발생할 수 있습니다.
- 모든 식당에 대한 정보의 양이 균일하지 않아 일부 리뷰가 없는 식당이 있을 수 있습니다.


## 11. 고려 사항
- 프로그램을 지속적으로 사용할 수 있도록 무한루프가 돌아가는 중입니다.
- 용이한 식당 검색을 위해 일부 키워드 검색을 구현하였습니다.
- 각 메뉴 내에서도 모드 설정을 두어 다양한 기능을 실행할 수 있도록 하였습니다.
- 관심 있는 지역만 검색할 수 있도록 행정동을 설정하여 메뉴를 실행할 수 있습니다.

