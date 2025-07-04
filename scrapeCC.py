from selenium import webdriver
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome()

# Define the base URL and pattern for the pages
base_url = "https://codechef.com/practice?page="

# List to store all extracted hrefs
all_hrefs = []
problem_urls=[]

# Loop through the pages
for page_number in range(0, 211):
    # Construct the URL for the current page
    url = base_url + str(page_number)
    driver.get(url)

    # To wait a few seconds to give time for the page to load
    time.sleep(5)

    # Scroll to the bottom of the page to load all elements
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

    # Extract page source using BeautifulSoup
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    time.sleep(5)

    # Find all <a> elements
    table_elements = soup.select('td.MuiTableCell-root.MuiTableCell-body[data-colindex="0"]')
    # Extract the href attribute and add to the set
    # hrefs = [a['href'] for a in a_elements if 'leetcode.com/problems/' in a.get('href', '')]
    # all_hrefs.update(hrefs)
    for a in table_elements:
        href=a.div.text
        #if href and href.startswith('/problems/') and  not href.endswith('/solution'):
        problem_url="https://codechef.com/problems/"+href
        problem_urls.append(problem_url)

# Create a new text file
all_hrefs=list(set(problem_urls))
filename = "codechef.txt"
with open(filename, "w") as file:
    # Write the href attribute of each <a> element to the file
    for href in all_hrefs:
        try:
            file.write(href + "\n")
        except:
            pass

# Quit the webdriver
driver.quit()
