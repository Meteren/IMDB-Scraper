from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from lxml import etree 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 
import threading 
import multiprocessing as mp
from multiprocessing import Process, Queue


def Timer():
    time.sleep(1)

def scrape_page(link,q1,q2,path,type): 
    HEADERS ={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    print(link)
    myList = []
    did_win = 0
    is_nominated = 0
    Timer() 
    try:
        resp = requests.get(link,headers = HEADERS)
        sp = BeautifulSoup(resp.text, 'lxml')
        dom = etree.HTML(str(sp))
    except:
        print('Something went wrong! Check your internet connection.')
        time.sleep(60)
        
    if type == 0:
        try:
            genres = sp.find('div', class_ = path)
            for i in genres:
                a = i.findAll('a')
                for _ in a:
                    myList.append(_.text.strip())
        except:
            pass
        
        finally:
            q1.put(myList)
    
    elif type == 2:
        try:
            text = dom.xpath(path)[0].text
            if 'Oscar' in text:
                if 'Won' in text:
                     did_win = 1
                     is_nominated = 1
                if 'Nominated' in text:
                    did_win = 0
                    is_nominated = 1
            else:
                 did_win = 0
                 is_nominated = 0
            q1.put(did_win)
            q2.put(is_nominated)
        except:
            print('exception')
            did_win = 0
            is_nominated = 0
            q1.put(did_win)
            q2.put(is_nominated)
            pass

    print(q1)
    print(q2)
    

if __name__ == "__main__": 
    path = "/Users/shubn/Downloads/chromedriver/chromedriver.exe"
    HEAD = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    cService = webdriver.ChromeService(executable_path = path)
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_experimental_option("detach", True)

    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument(f'user-agent={HEAD}')
    chrome_options.add_argument('--disable-features=TranslateUI')
    chrome_options.add_argument('--disable-translate')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    #chrome_options.add_argument("--window-size=1366,728")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-browser-side-navigation")
    chrome_options.add_argument("--no-sandbox")

    
    driver = webdriver.Chrome(service = cService,options = chrome_options)
           
    URL = "https://www.imdb.com/search/title/?title_type=feature&genres=!short,!documentary&user_rating=5,10&release_date=1929-05-16,2023-03-13&sort=user_rating,desc&num_votes=20000,"


    #options = webdriver.ChromeOptions() 
    #options.headless = True 
    #with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) as driver: 
	#driver.get(url)

    driver.get(URL)

    for i in range(19):
        try:
            button = driver.find_element('xpath','//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/div[2]/div/span/button')
            driver.execute_script('arguments[0].click()',button)
        except:
            pass
        try:
            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/div[2]/div/span/button')))
        except:
            pass
    containers = driver.find_elements(By.CLASS_NAME,'ipc-metadata-list-summary-item__tc')

    is_nominated = []
    is_awarded = []
    movie_titles = []
    movie_links = []
    release_years = []
    ratings = []
    runtimes = []
    age_restrictions = []
    ratings_amount = []
    genres = []
    dramas = []
    actions = []
    adventures = []
    animations = []
    biographies = []
    comedies = []
    crimes = []
    dramas = []
    families = []
    fantasies = []
    film_noir = []
    game_shows = []
    histories = []
    horrors = []
    musics = []
    musicals = []
    mysteries = []
    news = []
    reality_tvs = []
    romances = []
    sci_fis = []
    sports = []
    talk_shows = []
    thrillers = []
    wars = []
    westerns = []

    genres_list = {'Action':actions,'Adventure':adventures,'Animation':animations,'Biography':biographies,
              'Comedy':comedies,'Crime':crimes,'Drama':dramas,'Family':families,
              'Fantasy': fantasies,'Film-Noir':film_noir,
              'Game-Show':game_shows,'History':histories,'Horror':horrors,'Music':musics,
              'Musical':musicals,'Mystery':mysteries,'News':news,
              'Reality-TV':reality_tvs,'Romance':romances,'Sci-Fi':sci_fis,
              'Sport':sports,'Talk-Show':talk_shows,'Thriller':thrillers,
              'War':wars,'Western':westerns}


    #top movies list generation
    for i in range(len(containers)):
        link = driver.find_element('xpath','//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/ul/li[{}]/div[1]/div/div/div[1]/div[2]/div[1]/a'
                               .format(i+1)).get_attribute('href')
        movie_links.append(link)
        row = driver.find_element('xpath','//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/ul/li[{}]/div[1]/div/div/div[1]/div[2]/div[2]'
                                       .format(i+1)).find_elements(By.TAG_NAME,'span')
        print(len(movie_links))
    
        try:
            release_years.append(row[0].text.strip())
        except:
            releas_years.append('?')
            pass
        try:
            runtimes.append(row[1].text.strip())
        except:
            runtimes.append('?')
            pass
        try:
            age_restrictions.append(row[2].text.strip())    
        except:
            age_restrictions.append('?')
            pass

        print(release_years)
        print(runtimes)
        print(age_restrictions)

        try:
            rating = driver.find_element('xpath','//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/ul/li[{}]/div[1]/div/div/div[1]/div[2]/span/div/span'.
                                     format(i+1)).text.strip()
            ratings.append(rating[0:3])
            print(ratings)
        except:
            ratings.append('')

        try:
            rating_amount = driver.find_element('xpath','//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/ul/li[{}]/div[1]/div/div/div[2]/div[2]'.
                                            format(i+1)).text.strip()
            ratings_amount.append(rating_amount[5:])
            print(ratings_amount)
        except:
            ratings_amount.append('')
            pass
        try:
            movie_title = driver.find_element('xpath','//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/ul/li[{}]/div[1]/div/div/div[1]/div[2]/div[1]/a/h3'.
                                      format(i+1)).text.strip()
            
            movie_titles.append(movie_title[movie_title.find('.')+1:].strip())
        except:
            movie_titles.append('?')
            pass
        
        print(movie_titles)
    
    values = {'genre':['ipc-chip-list--baseAlt ipc-chip-list',0],
             'director':['//*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[4]/ul/li[1]/div/ul/li/a',1],
             'is awarded':['//*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[1]/div/ul/li/a[1]',2]}
    
    processes = [] 
    
    for link in movie_links:
        q1 = Queue()
        q2 = Queue()
        for key,value in values.items():
            if key == 'genre':
                try:
                    p = mp.Process(target=scrape_page, args=(link,q1,q2,value[0],value[1]))
                    p.start()
                    processes.append(p)
                    genres.append(q1.get())
                    print(genres)
                except:
                    print('Something went wrong! Try to check your internet connection...')
                    time.sleep(60)
                    pass
                 
            if key == 'is awarded':
                try:
                    p = mp.Process(target=scrape_page, args=(link,q1,q2,value[0],value[1]))
                    p.start()
                    processes.append(p)
                    is_awarded.append(q1.get())
                    is_nominated.append(q2.get())
                    print(is_awarded)
                    print(is_nominated)
                except:
                    print('Something went wrong! Try to check your internet connection.')
                    time.sleep(60)
                    pass
                
            for p in processes:
                try:
                    p.join()
                except:
                    pass
                    
            
                
    #genre distribution
    for row in genres:
        dict = {'Action':0,'Adventure':0,'Animation':0,'Biography':0,
                  'Comedy':0,'Crime':0,'Drama':0,'Family':0,
                  'Fantasy': 0,'Film-Noir':0,
                  'Game-Show':0,'History':0,'Horror':0,'Music':0,
                  'Musical':0,'Mystery':0,'News':0,
                  'Reality-TV':0,'Romance':0,'Sci-Fi':0,
                  'Sport':0,'Talk-Show':0,'Thriller':0,
                  'War':0,'Western':0}
    
        for genre in row:
            for key,value in dict.items():
                if genre == key:
                    dict[key] = 1
    
        for key1,value1 in genres_list.items():
            for key2,value2 in dict.items():
                if key1 == key2:
                   value1.append(value2)


    data={
        'MovieName':movie_titles,'Release Year':release_years,'Age Restriction':age_restrictions,'Runtime':runtimes,'Rating': ratings,'Rating Amount':ratings_amount,'Action':actions,'Adventure':adventures,'Animation':animations,'Biography':biographies,'Comedy':comedies,'Crime':crimes,
        'Drama':dramas,'Family':families,'Fantasy':fantasies,'Film-Noir':film_noir,'Game-Show':game_shows,'History':histories,'Horror':horrors,'Music':musics,'Musical':musicals,'Mystery':mysteries,'News':news,'Reality':reality_tvs,'Romance':romances,'Sci-Fi':sci_fis,'Sport':sports,'Talk_Show':talk_shows,'Thriller':thrillers,'War':wars,'Western':westerns,
        'Is Awarded':is_awarded,'Is Nominated':is_nominated}

    df = pd.DataFrame(data)

    try:
        df.to_csv('movies.csv',index=False)
    except:
        print('Something went wrong!')
    else:
        print('Sucessfully converted.')
    finally:
        print('Exiting program')

















