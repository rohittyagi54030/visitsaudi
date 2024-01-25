import os

os.system("pip3 install -r requirements.txt")
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time

try:
    os.system("pip3 install PyVirtualDisplay==1.3.2")
except:
    pass
from pyvirtualdisplay import Display
from sys import platform
import os
import datetime
import random
import telegram_send_msg as tg
import requests


def chrome_proxy(country: str, city: str, provider: str) -> dict:
    if provider == "OL":
        num = random.randint(0, 10000000000)
        padded_num = str(num).rjust(10, '0')
        if city != "":
            wire_options = {
                "proxy": {
                    "http": f"http://customer-rajat-cc-{country.lower()}-city-{city.lower()}-sessid-{padded_num}-sesstime-10:Rohit#1212##@pr.oxylabs.io:7777",
                    "https": f"http://customer-rajat-cc-{country.lower()}-city-{city.lower()}-sessid-{padded_num}-sesstime-10:Rohit#1212##@pr.oxylabs.io:7777",
                }
            }
        else:
            wire_options = {
                "proxy": {
                    "http": f"http://customer-rajat-cc-{country.lower()}-sessid-{padded_num}-sesstime-10:Rohit#1212##@pr.oxylabs.io:7777",
                    "https": f"http://customer-rajat-cc-{country.lower()}-sessid-{padded_num}-sesstime-10:Rohit#1212##@pr.oxylabs.io:7777",
                }
            }
    elif provider == "BD":
        num = random.randint(0, 1000000)
        padded_num = str(num).rjust(6, '0')
        if city != "":
            wire_options = {
                "proxy": {
                    "http": f"http://brd-customer-hl_17599b6f-zone-residential-country-{country.lower()}-city-{city.lower()}-session-{padded_num}:h7hij5ok48ky@brd.superproxy.io:22225",
                    "https": f"http://brd-customer-hl_17599b6f-zone-residential-country-{country.lower()}-city-{city.lower()}-session-{padded_num}:h7hij5ok48ky@brd.superproxy.io:22225",
                }
            }
        else:
            wire_options = {
                "proxy": {
                    "http": f"http://brd-customer-hl_17599b6f-zone-residential-country-{country.lower()}-session-{padded_num}:h7hij5ok48ky@brd.superproxy.io:22225",
                    "https": f"http://brd-customer-hl_17599b6f-zone-residential-country-{country.lower()}-session-{padded_num}:h7hij5ok48ky@brd.superproxy.io:22225",
                }
            }
    else:
        wire_options = {
            "proxy": {
                "http": f"http://madanrajat:pKQ85G0bWjPcgtqX_country-{country.title()}@proxy.packetstream.io:31112",
                "https": f"http://madanrajat:pKQ85G0bWjPcgtqX_country-{country.title()}@proxy.packetstream.io:31112",
            }
        }
    return wire_options


def get_country(country_code, city):
    location = None
    location_file = 'City_list.csv'
    with open(location_file, "r", encoding="utf-8") as file:
        csv_file = csv.reader(file)
        for row in csv_file:
            if str(city) in str(row[0]):
                if row[0].split(";")[0].lower() == country_code.lower():
                    location = row[0]
                    break
    return location


runBatFile = "no"
autocontrol = 'yes'
refresh = 'no'
telegram_ss = 'yes'
ss_delay = 0

proxy = "yes"
api_url = "https://masteradmins.superadscience.com"

user_name = "rajat"
provider = "PS"  # choices=["OL", "BD", "PS"]
repeated_ips = "Fresh IP"  # choices=["Repeated IP", "Fresh IP"]
country = "Egypt" # full name of country must be provided in case of PS
city = ""  # leave blank if not required
database = "psriyadh"

resp = requests.post(api_url + '/save-database/', params={"db": database.lower()})
if resp.status_code != 200:
    print("Network Error! Try Again!")
    exit()

db_id = resp.json()["id"]

if city != "":
    print("True")
    city_details = get_country(country, city.lower())
    if city_details:
        country = city_details.split(";")[0]
        country = country
        city = city

ip_address = requests.get('https://api.ipify.org').text

runs = 100
run = 0

if proxy == 'yes':
    from seleniumwire import webdriver

    if repeated_ips == "Fresh IP":
        while True:
            proxies = chrome_proxy(country, city, provider)
            driver = webdriver.Chrome(
                ChromeDriverManager().install(), seleniumwire_options=proxies
            )
            driver.get("https://api.ipify.org")
            ip = driver.find_element(By.TAG_NAME, 'pre').text
            resp = requests.post(api_url + '/check-ip/',
                                 params={"ip": ip, "db": db_id, "user": user_name})
            json_data = resp.json()
            if json_data["status"] == "success":
                print(f"Serial:- {json_data['serial']}")
                driver.close()
                break
            else:
                driver.close()
    else:
        proxies = chrome_proxy(country, city, provider)
        driver = webdriver.Chrome(
            ChromeDriverManager().install(), seleniumwire_options=proxies
        )
        driver.get("https://api.ipify.org")
        ip = driver.find_element(By.TAG_NAME, 'pre').text
        resp = requests.post(api_url + '/check-ip/', params={"ip": ip, "db": db_id, "user": user_name})
        driver.close()



else:
    from selenium import webdriver

options = webdriver.ChromeOptions()
uas = []
import csv

device = 2

if device == 1:
    csv_file = "./UserAgentMobile.csv"
    device_name = "Mobile"
elif device == 2:
    csv_file = "./DesktopUserAgent.csv"
    device_name = "Desktop"
else:
    print("Try Again!")
    time.sleep(10)
    exit()

with open(csv_file, "r") as csvfile:
    reader_variable = csv.reader(csvfile, delimiter=",")
    for row in reader_variable:
        uas.append(row)
ua = random.choice(uas)
print('ua', ua)
options.add_argument(f"user-agent={ua[0]}")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
# options.add_experimental_option("detach", True)
if device == 1:
    mobile_emulation = {
        "deviceMetrics": {"width": 375, "height": 812, "pixelRatio": 3.0},
        "userAgent": ua[0]
    }
    options.add_experimental_option("mobileEmulation", mobile_emulation)
# Autocontrol
if (autocontrol == 'yes'):
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--window-size=1420,1080")
    display = Display(visible=0, size=(1420, 1080))
    display.start()

url = "https://superadme.com/tracker/click.php?key=cqs0hwquwt1hubqoovls"
while True:
    try:
        s_time = datetime.datetime.now()
        if run < runs:
            print(f"Running for {device_name}:- ", run)
            if proxy == 'yes':
                driver = webdriver.Chrome(ChromeDriverManager().install(), options=options,
                                          seleniumwire_options=proxies)
            else:
                driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            move = ActionChains(driver)
            driver.maximize_window()
            driver.get(url)

            # time.sleep(5)
            # if run == 0 and telegram_ss == 'yes':
            #     driver.get_screenshot_as_file("screenshot.png")
            #     time.sleep(2)
            #     time.sleep(ss_delay)
            #     tg.telegram_bot_sendimage('screenshot.png', 2, '', 'ip_address::' + ip_address + "updated",
            #                               'ip_address::' + ip_address + "updated", '')

            try:
                element = driver.find_element(By.CLASS_NAME, "c27-teaser-with-cards")
                print("Scrolling to element")
                driver.execute_script('window.scrollTo(0, 1450);')
                time.sleep(10)
                driver.execute_script('document.getElementsByClassName("slide-cta_HJ0x2")[0].click();')
                driver.get_screenshot_as_file("screenshot.png")
                time.sleep(2)
                time.sleep(ss_delay)
                tg.telegram_bot_sendimage('screenshot.png', 2, '', 'ip_address::' + ip_address + "updated",
                                          'ip_address::' + ip_address + "updated", '')
                run += 1
            except:
                pass

            time.sleep(15)
            # RunBat
            if (runBatFile == "yes"):
                if (platform == 'linux'):
                    activeNetworks = os.popen('nmcli con show --active').read()
                    splitedActiveNetworks = activeNetworks.split('\n')
                    b = splitedActiveNetworks[1][:splitedActiveNetworks[1].find('-')]
                    c = b.split(' ')
                    d = " "
                    c = c[:-1]
                    e = d.join(c)
                    e = e.strip()

                    os.popen("nmcli con down '" + e + "'").read()
                    print("connection disconnected")
                    time.sleep(10)
                    os.popen("nmcli con up '" + e + "'").read()
                    print("connection established")
                    time.sleep(50)
                else:
                    # driver.switch_to.window(driver.window_handles[1])
                    driver.execute_script('javascript:document.title="run_bat1"')
                    time.sleep(7)
                    print("Chaning to hello world")
                    driver.execute_script('javascript:document.title="hello_world"')
                    time.sleep(33)
            driver.quit()
    except:
        try:
            driver.quit()
        except:
            pass



