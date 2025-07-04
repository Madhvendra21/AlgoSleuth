import os
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time


index=2227
QDATA_folder="Qdata"
linkfileLC="leetcode.txt"
links=[] # for links of problems already scraped
premium_problems_links=[]
premium_problems=0

with open("./Qdata/indexLC.txt","r",encoding="utf-8") as file:
    for line in file:
        words=line.split()
        link="https://leetcode.com/problems/" + "-".join(words[1:]).lower() + "/"
        links.append(link.strip())

with open("./Qdata/premium_problems_LC.txt","r",encoding="utf-8") as file:
    for line in file:
        premium_problems_links.append(line.strip())

links.extend(premium_problems_links)
# for i in range(1,11):
#     print(links[i],'\n')

with open("./Qdata/leetcode.txt","r",encoding="utf-8") as file:
    for line in file:
        url=line.strip()

        if url in links:
            continue

        driver = webdriver.Chrome()

        driver.get(url)
        time.sleep(4)

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        time.sleep(4)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        try:
            Title=soup.find_all(class_="flex h-full items-center")
        except:
            print("Error with Title\n")

        try:
            Q_body=soup.find_all(class_="px-5 pt-4")
        except:
            print("Error101\n")

        if len(Title) == 0:
            premium_problems+=1
            with open("./Qdata/premium_problems_LC","a",encoding="utf-8") as file:
                file.write(url + '\n')
            # premium_problems_links.append(url)
            continue  

        folder_name = str(index)
        folder_path = "./" + QDATA_folder + "/" + folder_name

        os.mkdir(folder_path)

        file_name = str(index)+".txt"
        file_path = folder_path + "/" + file_name

        #print Title
        filename_index="./Qdata/indexLC.txt"
        for Title1 in Title:
            Title_text=Title1.text
            with open(filename_index,"a",encoding="utf-8") as file:
                file.write(Title_text+"\n")

        #print(Q_body)
        for body_text in Q_body:
            body_text_line=body_text.text
            with open(file_path, "a", encoding="utf-8") as file:
                file.write(body_text_line)
        
        index = index + 1

# with open("./Qdata/premium_problems_LC","a",encoding="utf-8") as file:
#     for line in premium_problems_links:
#         file.write(premium_problems_links + '\n')

print("Premium Problems=",premium_problems,'\n')

driver.quit()