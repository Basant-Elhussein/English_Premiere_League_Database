import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options

#Open browser
options = Options()
options.binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')
driver = webdriver.Firefox(executable_path=r'C:\Users\Basant\AppData\Local\Programs\Python\Python37/geckodriver.exe', options=options)
url='https://www.premierleague.com/clubs'
driver.get(url)

# Accept on Cookies
time.sleep(5) # Wait to load page

accept_cookies = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/div[5]/button[1]')
accept_cookies.click()

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

# Get clubs
clubs = driver.find_elements(By.XPATH,'/html/body/main/div[2]/div/div/div[3]/div/table/tbody/tr')
print("Number of clubs",len(clubs))

clubs_list = []
stadium_links = []

# Loop in clubs for each club
for club in clubs:
	attr = club.find_elements(By.TAG_NAME,'td')
	[team, stadium] = attr #Object Destruction

	club_link = team.find_element(By.TAG_NAME, 'a').get_attribute('href')
	stadium_link = stadium.find_element(By.TAG_NAME, 'a').get_attribute('href')

	stadium_dict = {
		"stadiumName" : stadium.text,
		"website": stadium_link
	}

	club_dict = {
				"clubName": team.text,
				"website": club_link,
				"homeStadium": stadium.text
	}

	stadium_links.append(stadium_dict)
	clubs_list.append(club_dict)

updated_clubs_list = []

for club in clubs_list:
	print(club)
	club_link = club["website"]
	while True:
		try:
			driver.get(club_link)
			time.sleep(4)
			try:
				official_website = driver.find_element(By.CLASS_NAME, 'website')
				official_website_link = official_website.find_element(By.TAG_NAME, 'a').get_attribute('href')
				club["website"] = official_website_link
				updated_clubs_list.append(club)
				print('done')
			except:
				print('no website')
			break	
		except:
			print('Trying ', club_link, ' again.')




print(len(updated_clubs_list))
print(len(stadium_links))
print(updated_clubs_list[0])
print(stadium_links[0])

# Create a DataFrame and Export CSV
df = pd.DataFrame(updated_clubs_list)
df.to_csv(r'out/ClubsTable.csv',index=False)

linksdf = pd.DataFrame(stadium_links)
linksdf.to_csv(r'out/StadiumLinks.csv',index=False)

driver.close()