from selenium import webdriver
import time
import os.path
from selenium.webdriver.chrome.options import Options

import random

from selenium.webdriver.common.by import By

wufazhuce_url = "http://wufazhuce.com/one/"

DOWNLOAD_ONE_PATH = 'output/one.png'
CHROME_DRIVER = r"input/chromedriver_win32/chromedriver.exe"


def getrate_random(len4=4):
    listr = []
    for _ in range(len4):
        yan = random.randint(0, 9)
        listr.append(yan)
    return ''.join(str(i) for i in listr)


def getUrl():
    return wufazhuce_url + getrate_random()


def webshot(url, filepath, isFullScreen=True):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    chromedriver = CHROME_DRIVER
    driver = webdriver.Chrome(options=options, executable_path=chromedriver)
    driver.implicitly_wait(10)
    driver.maximize_window()
    # 返回网页的高度的js代码
    link = url
    try:
        driver.get(link)
        if (isFullScreen):
            for _ in range(10):
                driver.execute_script(
                    'document.documentElement.scrollTop = document.documentElement.scrollHeight'
                )
                print('driver.execute_script')
                time.sleep(1)
        else:
            # 返回网页的高度的js代码
            js_height = "return document.body.clientHeight"
            height = driver.execute_script(js_height)
            k = 1
            KS = 500
            while True:
                if k * KS < height:
                    js_move = "window.scrollTo(0,{})".format(k * KS)
                    print(js_move)
                    driver.execute_script(js_move)
                    time.sleep(0.5)
                    height = driver.execute_script(js_height)
                    k += 1
                else:
                    break

        scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
        scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
        driver.set_window_size(scroll_width, scroll_height)
        driver.get_screenshot_as_file(filepath)
        print("Process {} get one pic !!!".format(os.getpid()))
        time.sleep(0.1)

        ## 网页抓包的
        if driver.find_element("id", "main-container").text.find("404 Not Found") >= 0:
            print("错误" + url)
            return False
        else:
            print("正常")
            return True
    except Exception as e:
        print(filepath, e)
        return False

def getScreenshot():
    t = time.time()
    # 两个参数，前面url，后面保存地址
    while(True):
        if(webshot(getUrl(), DOWNLOAD_ONE_PATH, False)):
            break
    print("操作结束，耗时：{:.2f}秒".format(float(time.time() - t)))
    return DOWNLOAD_ONE_PATH


# 截图测试代码
if __name__ == '__main__':
    print("__main__")
    t = time.time()
    # 两个参数，前面url，后面保存地址
    while(True):
        if(webshot(getUrl(), DOWNLOAD_ONE_PATH, False)):
            break
    print("操作结束，耗时：{:.2f}秒".format(float(time.time() - t)))
