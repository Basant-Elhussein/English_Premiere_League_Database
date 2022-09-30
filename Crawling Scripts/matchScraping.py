import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options

# Open browser
options = Options()
options.binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')
driver = webdriver.Firefox(executable_path=r'C:\Users\Basant\AppData\Local\Programs\Python\Python37/geckodriver.exe', options=options)
url='https://www.premierleague.com/clubs'
driver.get(url)

# Accept on Cookies
time.sleep(6) # Wait to load page

accept_cookies = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/div[5]/button[1]')
accept_cookies.click()


# Seasons
seasons = [{"season" : "2021/22", "url" : "https://www.premierleague.com/results?co=1&se=418&cl=-1"},
{"season" : "2020/21", "url" : "https://www.premierleague.com/results?co=1&se=363&cl=-1"},
{"season" : "2019/20", "url" : "https://www.premierleague.com/results?co=1&se=274&cl=-1"},
{"season" : "2018/19", "url" : "https://www.premierleague.com/results?co=1&se=210&cl=-1"}]


matches_per_season = {}
for season in seasons:
    while True:
        try:
            driver.get(season['url'])
            time.sleep(3)

            # Scroll down
            current_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 	# Scroll step
                time.sleep(4) 	# Wait to load page
                try:
                    new_height = driver.execute_script("return document.body.scrollHeight") # Calculate new scroll height
                except:
                    print("Failed: ", new_height)
                if new_height == current_height: # Compare with last scroll height
                    break
                current_height = new_height
            
            time.sleep(5)
            # Get matches urls
            matches = driver.find_elements(By.CLASS_NAME, 'postMatch')
            print('found')
            matches_urls = []
            for match in matches:
                matches_urls.append('https:' + match.get_attribute('data-href'))
            
            matches_per_season[season['season']] = matches_urls
            print(season['season'], ': ', len(matches_urls))
            break
        except:
            print('Trying ', season['season'])


matches_list = []

for season, urls in matches_per_season.items():
    for url in urls:
        while True:
            try:
                driver.get(url)
                time.sleep(3)

                stats_btn = driver.find_element(By.XPATH, '/html/body/main/div/section[2]/div[2]/div[2]/div[1]/div/div/ul/li[3]')
                stats_btn.click()

                home = driver.find_element(By.XPATH, '/html/body/main/div/section[2]/div[2]/section/div[3]/div/div/div[1]/div[1]/a[2]/span[1]')
                away = driver.find_element(By.XPATH, '/html/body/main/div/section[2]/div[2]/section/div[3]/div/div/div[1]/div[3]/a[2]/span[1]')
                stadium = driver.find_element(By.XPATH, '/html/body/main/div/section[2]/div[2]/section/div[1]/div/div[1]/div[3]') 
                date = driver.find_element(By.CLASS_NAME, 'matchDate')

                score = driver.find_element(By.XPATH, '/html/body/main/div/section[2]/div[2]/section/div[3]/div/div/div[1]/div[2]/div/div')
                score = score.text.split('-')
                stats = driver.find_elements(By.XPATH, '/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr')
                stats_info = {}
                for stat in stats:
                    info = stat.find_elements(By.TAG_NAME, 'td')
                    home_score, attr, away_score = info
                    stats_info[attr.text] = (home_score.text, away_score.text)
                
                match_dict = {
                    'season': season,
                    'homeClub': home.text,
                    'awayClub': away.text,
                    'stadium': stadium.text.split(',')[0],
                    'date': date.text,
                    'homePossessions': stats_info['Possession %'][0],
                    'homeRCards': stats_info['Red cards'][0] if 'Red cards' in stats_info else '0',
                    'awayRCards': stats_info['Red cards'][1] if 'Red cards' in stats_info else '0',
                    'homeYCards': stats_info['Yellow cards'][0] if 'Yellow cards' in stats_info else '0',
                    'awayYCards': stats_info['Yellow cards'][1] if 'Yellow cards' in stats_info else '0',
                    'homeGoals': score[0],
                    'awayGoals': score[1],
                    'homeFouls': stats_info['Fouls conceded'][0] if 'Fouls conceded' in stats_info else '0',
                    'awayFouls': stats_info['Fouls conceded'][1] if 'Fouls conceded' in stats_info else '0',
                    'homeShots': stats_info['Shots'][0],
                    'awayShots': stats_info['Shots'][1]
                }
                matches_list.append(match_dict)
                print(match_dict)
                break

            except:
                print('Trying ', season, ' ', url)

df = pd.DataFrame(matches_list)
df.to_csv(r'out/MatchesTable.csv',index=False)