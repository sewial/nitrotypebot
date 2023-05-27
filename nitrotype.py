from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import time
import random

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager"
options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"]) #ignores messy errors
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options, desired_capabilities=caps)

def login(u, p):
    ubox = driver.find_element(by=By.XPATH, value="/html/body/div/div/div/main/div/section/div[2]/div/div[3]/form/div[1]/div[1]/div[2]/input")
    pbox = driver.find_element(by=By.XPATH, value="/html/body/div/div/div/main/div/section/div[2]/div/div[3]/form/div[1]/div[2]/div[2]/input")
    ubox.send_keys(u)
    pbox.send_keys(p)
    driver.find_element(by=By.XPATH, value="/html/body/div/div/div/main/div/section/div[2]/div/div[3]/form/button").click()

def typing(wpm):
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    yes = str(soup.find_all("span", class_="dash-word"))
    n = 0
    text = ""
    for i in yes:
        try:
            if yes[n+1] == "<":
                if yes[n-1] == ">":
                    text += i
        except:
            pass
        n += 1
    wrong = random.randint(0, 5) #generates random wrong characters
    for x in range(wrong):
        try:
            text = text[:len(text)-(x*3+1)] + "~" + text[len(text)-(x*3+1):]
        except:
            pass
    box = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div/main/div/section/div/div[3]/div[1]/div[1]/div[2]/input")
    if wpm >= 100:
        delay = float(8.7/wpm)
    elif wpm >= 70 and wpm <= 99:
        delay = float(9.3/wpm)
    else:
        delay = float(9.7/wpm)
    for i in text:
        time.sleep(delay + (delay/random.randint(12, 14)) - (delay/random.randint(12, 14)))
        if i.isspace():
            box.send_keys(Keys.SPACE)
        else:
            box.send_keys(i)

def loop(l, wpm):
    for x in range(l):
        try:
            driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[1]/div[1]/div[3]/div/div/button").click() #battle pass
        except:
            pass
        #wait for input box to exist
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/main/div/section/div/div[3]/div[1]/div[1]/div[2]/div[1]")))
        typing(wpm)    
        try:
            driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[1]/div[1]/div[3]/div/div[2]/button").click() #close reward popup
        except:
            pass
        time.sleep(3)
        try:
            #in case of disqualification
            driver.find_element(by=By.XPATH, value="/html/body/div[3]/div/div[1]/div/div/div/div[2]/button").click()
            print("Race failed")
        except:
            print(f"Finished race {x+1}")
        driver.get("https://www.nitrotype.com/race")
        
def qs(s):
    try:
        return int(input(s))
    except:
        print("Enter a whole number")
        qs(s)

u = input("Username: ")
p = input("Password: ")
wpm = qs("WPM: ")
l = qs("How many races? ")
driver.get("https://www.nitrotype.com/login")
login(u, p)
time.sleep(1)
driver.get("https://www.nitrotype.com/race")
loop(l, wpm)
driver.quit()
