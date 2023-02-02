import time
from queue import Queue
from threading import Thread

import pyautogui as pya
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By

TEXT_QUEUE = Queue()
"""Queue for passing typing text between browser and typing thread."""

def typing_thread():
    """
    Thread responsible for beep-boop-BOPping them buttons. HEHHEH.
    """

    while True:
        text = TEXT_QUEUE.get(block=True)
        if text != "STOP_YOU_FUCKING_ASSHOLE":
            pya.write(text)
        else:
            break

def browser_thread():
    """
    Thread controlling selenium browser. Reads page HTML, parses characters and
    writes them to a queue to be read by the typing thread. SOUCKA.
    """

    browser = Firefox()
    browser.get("https://monkeytype.com")
    reject_all = browser.find_element(By.XPATH, '//div[text()="Reject all"]')
    reject_all.click()
    pya.click(1000, 500) # Click the approximate center of the 🅱creen. 

    while True:
        soup = BeautifulSoup(browser.page_source, "lxml")
        word_div = soup.find("div", {"id": "words"})

        if not word_div:
            TEXT_QUEUE.put("STOP_YOU_FUCKING_ASSHOLE")
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
        TEXT_QUEUE.put(text)
        time.sleep(1.45)

def main():
    b_thread = Thread(target=browser_thread)
    t_thread = Thread(target=typing_thread)
    b_thread.start()
    t_thread.start()
    b_thread.join()
    t_thread.join()

if __name__ == "__main__":
    main()
