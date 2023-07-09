import csv
from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pyautogui

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

sleep(2)
stay = input("Do you want to search something nearby? (y/n): ")

results = {}  # Create a dictionary to store the results

while stay.lower() == 'y':
    telusuri = input("What are you looking for? ")
    print("This is the result for", telusuri)
    query = telusuri + ' di ' + location

    def nearby():
        sleep(2)
        near = driver.find_element(By.XPATH,'/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[3]/button')
        near.click()

    def search(a):
        cari = driver.find_element(By.XPATH, '//*[@id="searchboxinput"]')
        cari.send_keys(a)
        tekan = driver.find_element(By.XPATH, '//*[@id="searchbox-searchbutton"]')
        tekan.click()
        sleep(5)

    nearby()
    search(query)

    pyautogui.sleep(2)

    a = 0

    while True:
        pyautogui.moveTo(331, 626)
        pyautogui.scroll(-2000)
        pyautogui.sleep(1)

        content = driver.page_source
        soup = BeautifulSoup(content, 'lxml')

        names = soup.findAll('a', {'class':'hfpxzc'})
        resto = [name['aria-label'] for name in names]
        x = len(resto)

        if a == x:
            print(resto)
            results[telusuri] = resto  # Add the results to the dictionary with the search query as the key
            break
        else:
            a = x
            continue

    def close():
        sleep(3)
        tutup = driver.find_element(By.XPATH, '//*[@id="searchbox"]/div[3]/div/button')
        tutup.click()

    close()

    stay = input("Do you want to search for something else? (y/n): ")

print('Thank you')

# Prompt for saving the results into a CSV file
save_results = input("Do you want to save the results into a CSV file? (y/n): ")

if save_results.lower() == 'y':
    filename = input("Enter the filename for the CSV file (e.g., results.csv): ")

    # Get the custom column names from the user
    column_names = []
    for query in results.keys():
        column_name = input(f"Enter the column name for the search query '{query}': ")
        column_names.append(column_name)

    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write the header row
        writer.writerow(column_names)

        # Write the results row by row
        max_results = max(len(resto) for resto in results.values())  # Get the maximum number of results for any search query

        for i in range(max_results):
            row = []
            for query, resto in results.items():
                if i < len(resto):
                    result = resto[i]
                    row.append(result)
                else:
                    row.append('')
            writer.writerow(row)

    print("Results saved successfully!")
else:
    print("Results not saved.")
