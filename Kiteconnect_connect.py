
from selenium import webdriver
from kiteconnect import KiteConnect
import os
import time
from pyotp import TOTP
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager



cwd=os.getcwd()

def autologin():
    token_path = "Kiteconnect.txt"
    # print(cwd+"/"+token_path)
    key_Secret=  open(os.path.join(cwd,token_path),'r').read().split()
    kite = KiteConnect(api_key=key_Secret[0])

    options=webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)

    driver.get(kite.login_url())
    driver.implicitly_wait(10)
    username=driver.find_element(By.XPATH,'//*[@id="userid"]')
    password=driver.find_element(By.XPATH,'//*[@id="password"]')
   
    username.send_keys(key_Secret[2])
    password.send_keys(key_Secret[3])
    driver.find_element(By.XPATH,'//*[@id="container"]/div/div/div/form/div[4]/button').click()

    totp_token=TOTP(key_Secret[4])
    token=totp_token.now()
    
    totp =driver.find_element(By.CSS_SELECTOR,'#container > div.content > div > div > form > div.su-input-group.su-static-label.su-has-icon.twofa-value.digits > input[type=text]')
    totp.send_keys(token)
    
    driver.find_element(By.XPATH,'//*[@id="container"]/div/div/div[2]/form/div[3]/button').click()
    time.sleep(10)
    print(driver.current_url)
    request_token = driver.current_url.split('request_token=')[1][:32]
    print(request_token)
    with open(os.path.join(cwd,'request_token.txt'),'w') as the_file:
        the_file.write(request_token)
    driver.quit()

autologin()

request_token = open(os.path.join(cwd,"request_token.txt"),'r').read()
key_secret= open(os.path.join(cwd,'Kiteconnect.txt'),'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
data=kite.generate_session(request_token,api_secret=key_secret[1])
with open(os.path.join(cwd,'access_token.txt'),'w') as file:
    file.write(data['access_token'])
