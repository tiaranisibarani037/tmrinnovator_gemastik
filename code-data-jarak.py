import csv
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pyautogui
import keyboard
import pandas as pd

option = webdriver.ChromeOptions()
option.add_argument("start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
url = 'https://www.google.com/maps/place/Pantai+Lumban+Bul-bul+Balige'
driver.get(url)

content = driver.page_source
soup = BeautifulSoup(content, 'lxml')

span = soup.find('div', {'role':'main'}).find_all('h1', {'class':'DUwDvf fontHeadlineLarge'})
location = span[0].text
print(location)
start = input('search area? (y/n) : ')
sleep(2)

pencarian = []
result = []
lokasi = []
while start.lower() == 'y':        
    def choose():
        rute = driver.find_element(By.XPATH, '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[1]/button')
        rute.click()
        sleep(2)

    def area(a):
        _area = driver.find_element(By.XPATH, '/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[2]/div[1]/div/input')
        _area.send_keys(a) 
        sleep(1)                      
        _area.send_keys(Keys.RETURN)
        sleep(3)
    def close():
        tutup = driver.find_element(By.XPATH, '//*[@id="omnibox-directions"]/div/div[2]/div/button')
        tutup.click()
        sleep(1)

    choose()
    
    search = input('bandara/pelabuhan/rumah sakit : ')
    area(search)
    pencarian.append(search.title())

    distance = driver.find_element(By.XPATH, '//*[@id="section-directions-trip-0"]/div[1]/div/div[1]/div[2]/div')
    hasil = distance.text
    result.append(hasil)
    lokasi.append(location)
    print('jarak terdekat ke : ',hasil)
    
    start = input('others? (y/n) : ')
    close()


nama_file = input("Enter your file name(e.g., data_jarak.csv) :")

data = list(zip(lokasi,pencarian, result))

with open(nama_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Lokasi','Tujuan','Jarak'])
    writer.writerows(data)

print('Data berhasil disimpan dalam file CSV:', nama_file)
