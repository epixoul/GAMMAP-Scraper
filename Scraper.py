import ctypes
import json
import os
import sys
import threading
import time

import dotenv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

global driver


def modifier():
    global driver
    try:
        dotenv.load_dotenv()
        inst_path = os.getenv('Inst_Path')
        global result, options, firefox_drive, driver
        result = {"EGS": {},
                  "STEAM": {},
                  "GOG": {},
                  "ORIGIN": {},
                  "BTLNET": {},
                  "RSTG": {},
                  "MST": {},
                  "XBOX": {},
                  "UBISOFT": {},
                  "AZG": {},
                  "EAG": {},
                  "ITCH": {}
                  }
        os.chdir(os.getenv("Inst_Path") + r"\source")
        try:
            with open("games.json", "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            f.close()
        except Exception as e:
            print(e)
        firefox_drive = inst_path + r"\drivers" + fr"\{os.getenv(os.getenv("Desired_Driver"))}"
        options = webdriver.FirefoxOptions()
        options.add_argument("--start-minimized")
        driver = webdriver.Firefox(service=Service(firefox_drive), options=options)
        driver.minimize_window()
        print("-To avoid getting your IP banned, timer set to 10s.\n"
              "-Please wait for the fetching process to finish.\n")
    except Exception as e:
        print(e)


def egs_fetch():
    global j_file
    dotenv.load_dotenv()
    egs_url = os.getenv("EGS_Url")
    print("\n----------EGS(Epic Games) Fetch----------")
    try:
        driver.get(egs_url)
        driver.execute_script("return document.readyState")
        time.sleep(3)
        tabs = driver.window_handles
        driver.switch_to.window(tabs[0])
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        for container in soup.find_all("div", class_="css-1a6kj04"):
            title = container.select_one(".css-rgqwpc")
            price = container.select("div.css-l24hbj span")

            if title and price:
                result["EGS"][title.text.strip()] = price.pop(-1).getText(strip=True)
        for index, i in enumerate(result["EGS"]):
            print(f"{index}.", i)
            print("Current price:", result["EGS"][i])
        with open("games.json", "r", encoding="utf-8") as j_file:
            data = json.load(j_file)
        data["EGS"] = result["EGS"]
        with open("games.json", "w", encoding="utf-8") as j_file:
            json.dump(data, j_file, ensure_ascii=False, indent=2)
    except Exception as err:
        print(err)


def steam_fetch_loop(url, offset):
    global price_divs, j_file
    price_list = []
    try:
        driver.switch_to.new_window('tab')
        driver.get(url)
        driver.execute_script("return document.readyState")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        price_containers = soup.select("div._3EdZTDIisUpowxwm6uJ7Iq:has(.ImpressionTrackedElement)")
        title_list = soup.find_all("div", class_=lambda c: c and "StoreSaleWidgetTitle" in c)
        for container in price_containers:
            price_divs = container.find_all("div")
            for price in price_divs:
                if price.text.strip().endswith("€") and len(price.text.strip()) < 10:
                    price = price.text[-1] + price.text[:-1]
                    price_list.append(price.strip().replace(",", "."))
        for i, title in enumerate(title_list, start=1):
            print(f"{i + offset * 12 - 1}. {title.text.strip()}")
            print(f"Current Price: {price_list[i * 2 - 1]}")
            if title_list and price_list:
                result["STEAM"][title.text.strip()] = price_list[i * 2 - 1]
        with open("games.json", "r", encoding="utf-8") as j_file:
            data = json.load(j_file)
        data["STEAM"].update(result["STEAM"])
        with open("games.json", "w", encoding="utf-8") as j_file:
            json.dump(data, j_file, ensure_ascii=False, indent=2)
    except Exception as e:
        print(e)


def steam_fetch():
    try:
        dotenv.load_dotenv()
        steam_url = os.getenv("STEAM_Url")
        print("\n----------STEAM(Steam) Fetch----------")

        driver.get(steam_url)
        driver.execute_script("return document.readyState")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        for i in range(0, 10):
            thread = threading.Thread(target=steam_fetch_loop, args=(steam_url + str(i * 12), i))
            thread.start()
            thread.join()
    except Exception as e:
        print(e)


def destruct():
    global j_file
    try:
        j_file.close()
        input("\n-Now you can see the list items on \"games.json\" file.\n"
              "-Further info on : \" https://github.com/epixoul/GAMMAP-Scraper \".\n"
              "-Press \"Enter\" to close the terminal.")
        driver.quit()
        os.system("taskkill /F /IM firefox.exe")
        # os.system("taskkill /F /IM chrome.exe")
        # os.system("taskkill /F /IM msedge.exe")
        # os.system("taskkill /F /IM iexplore.exe")
    except Exception as err:
        print(err)


def root_exec():
    dotenv.load_dotenv()
    try:
        os.chdir(str(os.getenv("Inst_Path")))
    except Exception as err:
        print(err)
    modifier()
    egs_fetch()
    steam_fetch()
    destruct()


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as err:
        print(err)
        return False


def run_as_admin(script_path, args=" asadmin"):
    script_path = os.path.abspath(script_path)
    params = f'"{script_path}" {args}'
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)


if __name__ == "__main__":
    if not is_admin():
        run_as_admin("Scraper.py")
        sys.exit()
    else:
        print("Scraper is running as admin...")
    root_exec()
