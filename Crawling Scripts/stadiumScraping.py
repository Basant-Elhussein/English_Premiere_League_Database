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


# Open Stadiums Links
stadiums = pd.read_csv('out\StadiumLinks.csv')
stadiums = stadiums.to_dict('records')

stadiums_list = []

for stadium in stadiums:
    print(stadium['website'])
    while True:
        try:
            driver.get(stadium['website'])
            time.sleep(3)

            try:
                toggle = driver.find_element(By.XPATH, '/html/body/main/div[3]/div[2]/div/ul/li[2]')
                toggle.click()
            except:
                break

            article = driver.find_element(By.XPATH, '/html/body/main/div[3]/div[3]/div[2]')
            stadium_info = article.find_elements(By.TAG_NAME, 'p')

            stadium_dict = {
                'stadiumName': stadium['stadiumName']
            }
            for info in stadium_info:
                field = info.text.split(':')[0]
                words = info.text.split(' ')
                # print(field)
                if field == 'Record PL attendance': stadium_dict['recordLeagueAttendance'] = words[3].replace(',', '')
                elif field == 'Capacity': stadium_dict['capacity'] = words[1].replace(',', '')
                elif field == 'Stadium address':
                    address = info.text.split(':')[1].split(',')
                    stadium_dict['zipCode'] = address[-1]
                    stadium_dict['area'] = ', '.join(address[:-2])
                    stadium_dict['city'] = address[-2]
                elif field == 'Pitch size':
                    stadium_dict['lengthMeter'] = words[2][:-1]
                    stadium_dict['WidthMeter'] = words[4][:-1]
                elif field == 'Built':
                    stadium_dict['buildingDate'] = words[1]
            
            print('done ', stadium['stadiumName'])

            target = ['stadiumName', 'recordLeagueAttendance', 'capacity',
            'area', 'city', 'zipCode', 'lengthMeter', 'WidthMeter', 'buildingDate']
            
            ordered_stadium_dict = {}
            for t in target:
                ordered_stadium_dict[t] = stadium_dict[t] if t in stadium_dict else ''
            
            stadiums_list.append(ordered_stadium_dict)
            break
        except:
            print('Trying again.')

df = pd.DataFrame(stadiums_list)
df.to_csv(r'out/StadiumsTable.csv', index=False)
