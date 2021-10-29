from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import random
import pandas as pd
import threading
import requests
import os
from queue import Queue
from selenium import webdriver
import time
from selenium import webdriver
import undetected_chromedriver.v2 as uc
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import get_log, invite

# acc_file = open('accounts.txt','r')
accounts = [i for i in range(0, 4)]    # 4 windows


def main(account):
    global accounts
    # os.system('/Applications/Brave\ Browser.app/Contents/MacOS/Brave\ Browser --remote-debugging-port=9222 --user-data-dir=“/Users/vedant/Library/Application Support/BraveSoftware/Brave-Browser/Default”')

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    DRIVER_BIN = os.path.join(PROJECT_ROOT, "./chromedriver")
    caps = DesiredCapabilities().CHROME
    # caps['goog:loggingPrefs'] = {'performance': 'ALL'}
    options = Options()
    options.binary_location = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
    # options.add_argument("user-data-dir=/Users/vedant/Library/Application Support/BraveSoftware/Brave-Browser/Profile 4")

    options.add_experimental_option("debuggerAddress", "127.0.0.1:9221")
    # caps["pageLoadStrategy"] = "eager"

    driver = webdriver.Chrome(desired_capabilities=caps, executable_path=DRIVER_BIN, options=options)
    s_id = driver.session_id

    time.sleep(random.randint(200, 300) / 110)

    wait = WebDriverWait(driver, 15)

    windows = driver.window_handles
    file_1 = open('invite', 'r')
    data = file_1.readlines()

    # for window in windows:
    #     if window in done:
    #         continue

    done = []
    for j in range(account, account + 3):   # 3 is because I will open 3 tabs manually in each window

        if windows[j] in done:
            continue
        try:
            driver.switch_to.window(windows[j])
            time.sleep(1)

            if s_id != driver.session_id:
                print('not in ...')
                continue

            print("window sid: " + str(driver.session_id))

            time.sleep(random.randint(100, 300) / 100)
            for i in data:
                i = i.replace('\n', '').strip().split(' - ', 1)
                verify = i[1].strip()
                i = i[0].strip()
                driver.get(i)
                time.sleep(random.randint(500, 600) / 109)
                # server = i.rsplit('/', 1)[1]
                # headers = get_log.create_headers(driver, i, server)
                # print(headers)
                # # breakpoint()
                # time.sleep(random.randint(500, 700) / 108)
                # invite.inv(server, headers)
                invite = wait.until(EC.presence_of_element_located((By.CLASS_NAME,
                                                                    'marginTop40-i-78cZ.button-3k0cO7.button-38aScr.lookFilled-1Gx00P.colorBrand-3pXr91.sizeLarge-1vSeWK.fullWidth-1orjjo.grow-q77ONN')))
                invite.click()
                time.sleep(random.randint(500, 700) / 109)

                driver.get(verify)
                id_ = verify.rsplit('/', 1)[1]
                # print(driver.page_source)
                message_id = 'message-reactions-' + str(verify.rsplit('/', 1)[1])
                time.sleep(random.randint(300, 600) / 108)

                container = wait.until(EC.presence_of_element_located((By.ID, message_id)))
                # print(container)
                try:
                    complete = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME,
                                                                                              'button-1YxJv4.button-38aScr.lookFilled-1Gx00P.colorBrand-3pXr91.sizeSmall-2cSMqn.grow-q77ONN')))
                    complete.click()
                    time.sleep(random.randint(200, 300) / 108)
                    check_box = wait.until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'inputDefault-3JxKJ2.input-3ITkQf')))
                    driver.execute_script("arguments[0].scrollIntoView();", check_box)
                    check_box.click()
                    time.sleep(random.randint(400, 500) / 108)
                    submit = wait.until(EC.presence_of_element_located((By.CLASS_NAME,
                                                                        'submitButton-YEItfy.button-38aScr.lookFilled-1Gx00P.colorGreen-29iAKY.sizeMedium-1AC_Sl.grow-q77ONN')))
                    submit.click()
                    time.sleep(random.randint(400, 500) / 108)
                except:
                    print('No Terms and conditions')
                    pass
                reaction = container.find_element(By.CLASS_NAME, 'reactionInner-15NvIl')
                time.sleep(random.randint(200, 400) / 101)
                driver.execute_script("arguments[0].scrollIntoView();", container)
                time.sleep(random.randint(200, 400) / 108)
                reaction.click()
                time.sleep(random.randint(300, 600) / 108)

            driver.get('https://discord.com/guild-discovery')
            # windows.pop(windows.index(window))
            # done.append(window)
            time.sleep(random.randint(500, 700) / 108)
        except Exception as e:
            print(e)
            pass
            done.append(windows[j])


def threader():
    while True:
        # gets an worker from the queue
        worker = q.get()

        # Run the example job with the avail worker in queue (thread)
        main(worker)

        # completed with the job
        q.task_done()


# Create the queue and threader
q = Queue()

# how many threads are we going to allow for
for x in range(len(accounts)):
    t = threading.Thread(target=threader)

    # classifying as a daemon, so they will die when the main dies
    t.daemon = True

    # begins, must come after daemon definition
    t.start()

start = time.time()

# 100 jobs assigned.
for worker in range(len(accounts)):
    q.put(accounts[worker])

# wait until the thread terminates.
q.join()
