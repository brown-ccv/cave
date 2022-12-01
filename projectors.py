import typer
from pathlib import Path
from threading import Thread
from enum import Enum
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

class Projector(int, Enum):
    LEFT_BOTTOM = 21
    LEFT_TOP = 22
    FRONT_BOTTOM = 23
    FRONT_TOP = 24
    RIGHT_BOTTOM = 25
    RIGHT_TOP = 26
    FLOOR = 27
    
class State(str, Enum):
    ON = "on"
    OFF = "off"

# Globals
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()

# Power on the projector 
def power_on(projector, driver):
    try: 
        button = driver.find_element(By.NAME, "PowerOn")
    except: 
        print("ERROR POWERING ON PROJECTOR:", projector.name)    
    else:
        button.click()
        print("POWERED ON:", projector.name)
 
# Power off the projector       
def power_off(projector, driver):   
    try:
        button = driver.find_element(By.NAME, "PowerOff")
    except:
        print("ERROR POWERING OFF PROJECTOR:", projector.name)    
    else:
        button.click()
        print("POWERED OFF:", projector.name)
    return driver.close()


def change_projector(projector: Projector, state: State):
    IP = "http://192.168.1." + str(projector.value)

    # Set options
    options.add_argument("headless")
    driver = webdriver.Chrome(service=service, options=options)

    # Launch Chrome
    print("ACCESSING PROJECTOR:", projector.name)
    try:
        driver.get(IP)
    except WebDriverException:
        print("CONNECTION ERROR ON:", projector.name, " ", IP)
        return driver.close()

    # Ignore lamp warning and switch to status controls page
    driver.switch_to.alert.accept()
    driver.switch_to.frame("mainFrame")
    driver.get(IP + "/status.html")

    # Power on projector
    if(state == State.ON):
        power_on(projector, driver)
    elif (state == State.OFF):
        power_off(projector, driver)

    return driver.close()
    
def main(
    state: State = typer.Argument(..., help="Whether to turn the projectors on or off")
    # TODO: Add typer.option to specify specific projectors to turn on/offs
):
    """
    Power on or off the CAVE projectors
    """
    
    threads = []
    for projector in Projector:
        t = Thread(target=change_projector, args=(projector, state))
        threads.append(t)
        t.start()
    
    for t in threads: t.join()
    print("\nDONE. YOU MAY CLOSE THIS WINDOW")

if __name__ == "__main__":
    typer.run(main)