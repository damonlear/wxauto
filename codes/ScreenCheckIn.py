from selenium import webdriver
import time
import os.path
from selenium.webdriver.chrome.options import Options

import random

from selenium.webdriver.common.by import By

checkIn_url = "https://edu2.yixiaoneng.com/f/tMtIEp/s/8R00JD?q%5B0%5D%5Bfield_1%5D={}&q%5B0%5D%5Bfield_2_associated_field_3%5D=nAlJ&embedded="

DOWNLOAD_CHECKIN_PATH = 'output/checkin.png'
CHROME_DRIVER = r"input/chromedriver_win32/chromedriver.exe"


def getlocalStrTime(formate='%Y-%m-%d'):
    print("获取今天日期")
    times = time.time()
    local_time = time.localtime(times)
    local_strftime = time.strftime(formate, local_time)
    print("今天日期：{}".format(local_strftime))
    return local_strftime


def getUrl():
    date = getlocalStrTime()
    return checkIn_url.format(date)

def webshot(url, filepath, isFullScreen=True):
    print(url)
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
    cookies = {"name": "rs_token_8R00JD", "value": "00311"}
    try:
        ## 先请求再add保证时同一个浏览器cookies
        driver.get(link)
        driver.add_cookie(cookies)
        driver.get(link)
        ## 这里不延时可能会导致  Message: no such element: Unable to locate element: {"method":"css selector","selector":"[id="main-container"]"}
        print("等待加载10秒防止Message: no such element")
        time.sleep(10)
        driver.refresh()
        if(isFullScreen):
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
        if(webshot(getUrl(), DOWNLOAD_CHECKIN_PATH, False)):
            break
    print("操作结束，耗时：{:.2f}秒".format(float(time.time() - t)))
    return DOWNLOAD_CHECKIN_PATH


# 截图测试代码
if __name__ == '__main__':
    print("__main__")
    t = time.time()
    # 两个参数，前面url，后面保存地址
    while(True):
        if(webshot(getUrl(), DOWNLOAD_ONE_PATH, False)):
            break
    print("操作结束，耗时：{:.2f}秒".format(float(time.time() - t)))
