from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome()

# Define the base URL and pattern for the pages
base_url = "https://leetcode.com/problemset/all/?page="

# List to store all extracted hrefs
all_hrefs = []
problem_urls=[]

driver.get(base_url)

# Loop through the pages
for i in range(1, 56):
    # Construct the URL for the current page
    #url = base_url + str(page_number)
    #driver.get(url)

    # To wait a few seconds to give time for the page to load
    time.sleep(7)

    # Scroll to the bottom of the page to load all elements
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # time.sleep(7)

    # Extract page source using BeautifulSoup
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    time.sleep(7)

    # Find all <a> elements
    a_elements = soup.find_all('a')

    # Extract the href attribute and add to the set
    # hrefs = [a['href'] for a in a_elements if 'leetcode.com/problems/' in a.get('href', '')]
    # all_hrefs.update(hrefs)
    for a in a_elements:
        href=a.get('href')
        if href and href.startswith('/problems/') and  not href.endswith('/solution'):
            problem_url="https://leetcode.com"+href
            problem_urls.append(problem_url)
            
    if i != 55: # Because last page will not have next button
            X_PATH = "/html/body/div[1]/div/div[2]/div[1]/div[1]/div[5]/div[3]/nav/button[10]"
            element = driver.find_element("xpath",X_PATH)
            element.click() 
            time.sleep(7)

# Create a new text file
all_hrefs=list(set(problem_urls))
filename = "leetcode.txt"
with open(filename, "w") as file:
    # Write the href attribute of each <a> element to the file
    for href in all_hrefs:
        try:
            file.write(href + "\n")
        except:
            pass

# Quit the webdriver
driver.quit()
