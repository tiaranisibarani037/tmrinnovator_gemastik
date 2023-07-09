import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import pyautogui
import csv

option = webdriver.ChromeOptions()
option.add_argument("start-maximized")


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=option)
url = 'https://www.google.com/maps/place/Pantai+Lumban+Bul-bul+Balige'
driver.get(url)

content = driver.page_source
soup = BeautifulSoup(content, 'lxml')

span = soup.find('div', {'role':'main'}).find_all('h1', {'class':'DUwDvf fontHeadlineLarge'})
location = span[0].text
print(location)

time.sleep(2)

def ulasan():
    review = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[2]')
    review.click()
    time.sleep(4)

ulasan()

banyak_Rev = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div[2]/div/div[2]/div[2]')
Rev = banyak_Rev.text
print('Terdapat', Rev)

x = int(float(Rev.split()[0].replace('.', '')))
print(x)

i = 0

hasil_ulasan = []
stars = []

start_time = time.time()


while i < x :
    elapsed_time= time.time()
    pyautogui.moveTo(331, 626)
    pyautogui.scroll(-20000)
    pyautogui.time.sleep(1)   

    current_time = time.time()
    elapsed_time = current_time - start_time

    
    i +=1
    if (elapsed_time > 300):
        content = driver.page_source
        soup = BeautifulSoup(content, 'lxml')

        review_all = soup.findAll('div', {'class':'MyEned'})
        teks = ['nothing']  
        # print('-',review_all)           
        for element in review_all:
            hasil_ulasan.append(element.text)
            teks[0] = element.text                    
            print (teks)
        bintang = soup.findAll('span', {'class':'kvMYJc'})
        total = [t_bin['aria-label']for t_bin in bintang]
        for star in total:
            num = int(star.split()[0])
            stars.append(num)

        break

data_frame = pd.DataFrame(list(zip(hasil_ulasan, stars)), columns = ['Nama Tempat','Ulasan', 'Rating'])
print(data_frame)

filename = 'set-data-bulbul.csv'

data_frame.to_csv(filename, index=False, encoding='utf-8')
print('Berhasil membuat file csv')
