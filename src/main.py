import time

import pyautogui as pya
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By

if __name__ == "__main__":
    browser = Firefox()
    browser.get("https://monkeytype.com")
    reject_all = browser.find_element(By.XPATH, '//div[text()="Reject all"]')
    reject_all.click()

    first = True
    while True:
        soup = BeautifulSoup(browser.page_source, "lxml")

        word_div = soup.find("div", {"id": "words"})

        if not word_div:
            break
        else:
            words = word_div.find_all("div", {"class": "word"})

            text = ""
            for word in words:
                letters = word.find_all("letter", class_=False)
                if letters:
                    for letter in letters:
                        text += letter.text
                    text += " "

        if first:
            pya.click(1000, 500)
            first = False
        pya.write(text)
