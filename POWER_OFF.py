from threading import Thread
from enum import Enum
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

# Globals
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
class Projector(Enum):
    LEFT_BOTTOM = 21
    LEFT_TOP = 22
    FRONT_BOTTOM = 23
    FRONT_TOP = 24
    RIGHT_BOTTOM = 25
    RIGHT_TOP = 26
    FLOOR = 27

def powerOff(projector):
    IP = "http://192.168.1." + str(projector.value)

    # Set options
    options.add_argument("headless")
    driver = webdriver.Chrome(service=service, options=options)

    # Launch Chrome
    print("ACCESSING PROJECTOR:", projector.name)
    try: driver.get(IP)
    except WebDriverException:
        print("CONNECTION ERROR:", projector.name, " ", IP)
        return driver.close()

    # Ignore lamp warning and switch to status controls page
    driver.switch_to.alert.accept()
    driver.switch_to.frame("mainFrame")
    driver.get(IP + "/status.html")

    # Power on projector
    try: button = driver.find_element(By.NAME, "PowerOff")
    except: print("ERROR POWERING ON PROJECTOR:", projector.name)    
    else:
        button.click()
        print("POWERED OFF:", projector.name)
    return driver.close()

if __name__ == '__main__':
    threads = []
    for projector in Projector:
        t = Thread(target=powerOff, args=(projector,))
        threads.append(t)
        t.start()
    
    for t in threads: t.join()
    print("\nDONE. YOU MAY CLOSE THIS WINDOW")
    