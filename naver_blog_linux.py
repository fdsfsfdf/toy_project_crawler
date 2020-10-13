#Step 1. 필요한 모듈과 라이브러리를 로딩합니다.
from bs4 import BeautifulSoup
from selenium import webdriver
from pyvirtualdisplay import Display
import time
import numpy
import pandas as pd    
import os
import math
import re
import random

def naver_blog():
    #Step 2. 사용자에게 검색어 키워드를 입력 받습니다.
    print("=" *80)
    print(" 네이버 블로그 크롤러")
    print("=" *80)

    def scroll_down(driver):
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(1)

    while(1):
        print(
        '''
        1.국내야간관광 2.국내관광
        ''')
        keyword_no = int(input("원하시는 검색어의 번호를 적어주세요: "))
        try : 
            if keyword_no < 3 and keyword_no > 0:
                break
        except :
            continue

    if keyword_no == 1:
        keyword = '국내야간관광'
    else:
        keyword = '국내관광'

    startDate = input('시작날짜 설정(기본값: 2017-01-01) : ')
    if startDate == '':
        startDate = '2017-01-01'
    endDate = input('종료날짜 설정(기본값: 2020-01-31) : ')
    if endDate == '':
        endDate = '2020-01-31'


    cnt = int(input('크롤링 할 건수는 몇건입니까?: '))
    page_cnt = math.ceil(cnt/7)

    f_dir = input("파일을 저장할 폴더명만 쓰세요(기본경로:/home/ubuntu/temp):")
    if f_dir == '' :
        f_dir = "/home/ubuntu/temp"
        
    print("\n")

    n = time.localtime()
    s = '%04d-%02d-%02d-%02d-%02d-%02d' % (n.tm_year, n.tm_mon, n.tm_mday, n.tm_hour, n.tm_min, n.tm_sec)
    # day = time.strftime('%Y-%m-%d')
#     os.chdir(f_dir)
#     os.makedirs(f_dir+s+'-'+keyword)
#     os.chdir(f_dir+s+'-'+ keyword)

    # ff_dir=f_dir+s+'-'+keyword
    fc_name=s+keyword+'-'+startDate+'-'+endDate+'.csv'
    fx_name=s+keyword+'-'+startDate+'-'+endDate+'.xls'
        
    s_time = time.time( )

    #Step 4. 웹사이트 접속 후 해당 메뉴로 이동합니다.
    # options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    # options.add_argument('window-size=1920x1080')
    # options.add_argument("--disable-gpu")
    
    display = Display(visible=0, size=(1920, 1080))
    display.start()
    path = '/home/ubuntu/chromedriver'
    driver = webdriver.Chrome(path)
    # args = ["hide_console", ]
    # driver = webdriver.Chrome(path,options=options,service_args=args)

    # chrome_path = "c:/temp/chromedriver_240/chromedriver.exe"
    # driver = webdriver.Chrome(path)
    # query_url = f'https://section.blog.naver.com/Search/Post.nhn?pageNo=1&rangeType=ALL&orderBy=sim&keyword={keyword}'

    query_url = f'https://section.blog.naver.com/Search/Post.nhn?pageNo=1&rangeType=PERIOD&orderBy=sim&startDate={startDate}&endDate={endDate}&keyword={keyword}'
    driver.get(query_url)
    # driver.maximize_window()
    time.sleep(1)

    scroll_down(driver)   #현재화면의 가장 아래로 스크롤다운합니다
    scroll_down(driver)
    scroll_down(driver)

    count = 0
    blog_text2=[]
    for x in range(1,page_cnt + 1) :
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        # main_window = driver.current_window_handle
        
        blog_cnt = 1
        scroll_down(driver)

        for i in range(7):

            if count >= cnt :
                break
            print(f'-------{count}---------')
            print(f'-------!!!!{blog_cnt}!!!!---------')
            time.sleep(random.random())
            try :
                driver.find_element_by_xpath(f'//*[@id="content"]/section/div[2]/div[{blog_cnt}]/div/div[1]/div/a[1]/strong').click()
            except :
                blog_cnt += 1
                count += 1
                continue
                                           
            last_tab = driver.window_handles[-1]
            driver.switch_to.window(window_name=last_tab)

            html = driver.page_source
            soup2 = BeautifulSoup(html, 'html.parser')


            driver.switch_to.frame('mainFrame')
            html = driver.page_source
            soup2 = BeautifulSoup(html, 'html.parser')    
            # print(html)

            scroll_down(driver)
            scroll_down(driver)        
            blog_text = soup2.find('div',id = 'whole-body').get_text()
            blog_text = re.sub('[a-zA-Z]','',blog_text)
            blog_text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\{\};_\\‘|\(\)\[\]\<\>`\'…》]','',blog_text)
            # print(blog_text)
            blog_text2.append(blog_text)
            blog_cnt += 1
            count += 1
            driver.close()   
            first_tab = driver.window_handles[0]
            driver.switch_to.window(window_name=first_tab)
            time.sleep(1)
            
        x+=1
        if x % 10 == 1:
            driver.find_element_by_link_text('다음').click()
        else: 
            driver.find_element_by_link_text('%s' %x).click() # 다음 페이지번호 클릭
        
            
    #step 6. csv , xls 형태로 저장하기              
    blog_df = pd.DataFrame()
    blog_df['text']=blog_text2


    # # csv 형태로 저장하기
    blog_df.to_csv(fc_name,encoding="utf-8-sig",index=True)

    # # 엑셀 형태로 저장하기
    blog_df.to_excel(fx_name ,index=True)

    e_time = time.time( )
    t_time = e_time - s_time

    print("=" *80)
    print(f"작업 완료. 작업 시간 : {t_time}")
    print("=" *80)
    driver.close( )


naver_blog()
