from time import sleep
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

sleep(2)

def ulasan():
    review = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[2]')
    review.click()
    sleep(4)

ulasan()

banyak_Rev = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div[2]/div/div[2]/div[2]')
Rev = banyak_Rev.text
print('Terdapat', Rev)

x = int(float(Rev.split()[0].replace('.', '')))
print(x)

i = 0

hasil_ulasan = []
stars = []


while i < 5 :
    pyautogui.moveTo(331, 626)
    pyautogui.scroll(-20000)
    pyautogui.sleep(1)   

    content = driver.page_source
    soup = BeautifulSoup(content, 'lxml')
                                         
    review_ = soup.findAll('span',{'class':'wiI7pd'})

    ulasan_teks = review_[i].text
    hasil_ulasan.append(ulasan_teks)

    bintang = soup.findAll('span', {'class':'kvMYJc'})
    total = [t_bin['aria-label']for t_bin in bintang]
    for star in total:
        num = int(star.split()[0])
        stars.append(num)

    i +=1
    # print(i)
    # if i == 1000:
    #     print('list ulasan = ', hasil_ulasan)
    #     print('list_bintang = ', stars[:i])
    # else:
    #     continue
# print(hasil_ulasan)
# print(stars[:i])
data_frame = pd.DataFrame(list(zip(hasil_ulasan, stars)), columns = ['Ulasan', 'Rating'])
print(data_frame)

filename = 'set-data-bulbul.csv'

data_frame.to_csv(filename, index=False, encoding='utf-8')
print('Berhasil membuat file csv')
