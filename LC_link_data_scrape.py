import os
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time


index=1
QDATA_folder="Qdata"
linkfileLC="leetcode.txt"

with open("./Qdata/leetcode.txt","r") as file:
    for line in file:
        url=line.strip()        

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

driver.quit()