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
url='https://www.premierleague.com/players'
driver.get(url)

# Accept on Cookies
time.sleep(6) # Wait to load page

accept_cookies = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/div[5]/button[1]')
accept_cookies.click()

# seasons
seasons =  ["https://www.premierleague.com/players?se=418&cl=-1",
            "https://www.premierleague.com/players?se=363&cl=-1",
            "https://www.premierleague.com/players?se=274&cl=-1",
            "https://www.premierleague.com/players?se=210&cl=-1"]



players_links = set()


for season in seasons:
    while True:
        try:
            driver.get(season)
            time.sleep(4)
            # Scroll down
            current_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 	# Scroll step
                time.sleep(3) 	# Wait to load page
                try:
                    new_height = driver.execute_script("return document.body.scrollHeight") # Calculate new scroll height
                except:
                    print("Failed: ", new_height)
                if new_height == current_height: # Compare with last scroll height
                    break
                current_height = new_height
                
            print("scorlled till",current_height)
            time.sleep(10)

            # Get players
            players = driver.find_elements(By.XPATH,'/html/body/main/div[2]/div[1]/div/div/table/tbody/tr')
            print("Number of players",len(players))

            for player in players:
                attr = player.find_elements(By.TAG_NAME, 'td')
                name, position, nationality = attr

                player_link = name.find_element(By.TAG_NAME, 'a').get_attribute('href')
                parsed_link = ''
                stop = 0
                for c in player_link:
                    parsed_link += c
                    if c.isdigit(): stop = 1
                    if c == '/' and stop:
                        break
                players_links.add((name.text, nationality.text, parsed_link))
            break

        except:
            print('Trying ', season)

# linksdf = pd.DataFrame(players_links)
# linksdf.to_csv(r'out/PlayersLinks.csv',index=False)

players_list = []
clubPlayers_list = []
for name, nationality, url in players_links:
    while True:
        try:
            driver.get(url)
            time.sleep(4)

            player_dict = {}

            player_id = driver.find_element(By.XPATH, '/html/body/main/div[3]/nav/div/section[2]/table/tbody').get_attribute('data-player')
            player_dict['playerID'] = player_id

            player_dict['playerName'] = name
            player_dict['nationality'] = nationality

            personal_info = driver.find_element(By.CLASS_NAME, 'personalLists')
            data = personal_info.find_elements(By.TAG_NAME, 'li')
            birth = weight = height = ''

            for info in data:
                info = info.text.split('\n')
                if len(info) != 2: continue
                field, value = info
                if field == 'Date of Birth': birth = value.split(' ')[0]
                elif field == 'Height': height = value[:-2]

            weight = ''
            try:
                weight = personal_info.find_element(By.CLASS_NAME, 'u-hide').find_elements(By.TAG_NAME, 'div')
                weight = (weight[1].get_attribute('innerHTML'))[:-2]
            except:
                pass

            player_dict['birthDate'] = birth
            player_dict['height'] = height
            player_dict['weight'] = weight

            position = ''
            player_intro = driver.find_element(By.CLASS_NAME, 'playerIntro').find_elements(By.TAG_NAME, 'div')
            for i in range(len(player_intro)):
                if player_intro[i].text == 'Position':
                    position = player_intro[i+1].text
                    break
            player_dict['position'] = position

            players_list.append(player_dict)

            ### Now Scrapping ClubPlayers table:

            career = driver.find_elements(By.XPATH, '/html/body/main/div[3]/div/div/div[3]/table/tbody/tr')

            for entry in career:
                ClubPlayers_dict = {}

                info = entry.find_elements(By.TAG_NAME, 'td')
                season = info[0].text
                club = info[1].text.replace(' (Loan)', '').replace('&', 'and').replace(' U21', '').replace(' U18', '')

                if season == '2021/2022':
                    ClubPlayers_dict['clubName'] = club
                    ClubPlayers_dict['playerID'] = player_id
                    ClubPlayers_dict['season'] = '2021/22'
                    clubPlayers_list.append(ClubPlayers_dict)
                elif season == '2020/2021':
                    ClubPlayers_dict['clubName'] = club
                    ClubPlayers_dict['playerID'] = player_id
                    ClubPlayers_dict['season'] = '2020/21'
                    clubPlayers_list.append(ClubPlayers_dict)
                elif season == '2019/2020':
                    ClubPlayers_dict['clubName'] = club
                    ClubPlayers_dict['playerID'] = player_id
                    ClubPlayers_dict['season'] = '2019/20'
                    clubPlayers_list.append(ClubPlayers_dict)
                elif season == '2018/2019':
                    ClubPlayers_dict['clubName'] = club
                    ClubPlayers_dict['playerID'] = player_id
                    ClubPlayers_dict['season'] = '2018/19'
                    clubPlayers_list.append(ClubPlayers_dict)
            
            print(player_dict)
            print(clubPlayers_list[-2:])
            break
              
        except:
            print('Trying ', url, ' again.')

# Create a DataFrame and Export CSV
playersDF = pd.DataFrame(players_list)
playersDF.to_csv(r'Data/PlayersTable.csv',index=False)

clubplayersDF = pd.DataFrame(clubPlayers_list)
clubplayersDF.drop_duplicates(inplace = True, ignore_index = True)
clubplayersDF.to_csv(r'Data/ClubPlayersTable.csv',index=False)

driver.close()