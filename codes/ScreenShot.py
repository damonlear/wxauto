from selenium import webdriver
import time
import os.path
from selenium.webdriver.chrome.options import Options

qstheory_url = "http://www.qstheory.cn/"
people_url = "http://paper.people.com.cn/rmrb"
weibo_url_people = "https://m.weibo.cn/u/2803301701?uid=2803301701&t=0&luicode=10000011&lfid=100103type%3D1%26q%3D%E4%BA%BA%E6%B0%91%E6%97%A5%E6%8A%A5"
weibo_url_news = "https://m.weibo.cn/u/2656274875?uid=2656274875&luicode=10000011&lfid=100103type%3D1%26q%3D%E6%96%B0%E9%97%BB%E8%81%94%E6%92%AD"

DOWNLOAD_PATH = 'output/shot.png'
CHROME_DRIVER = r"input/chromedriver_win32/chromedriver.exe"

def webshot(url, filepath, isFullScreen = True):
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
    except Exception as e:
        print(filepath, e)


def getScreenshot(url=people_url, filepath=DOWNLOAD_PATH):
    t = time.time()
    # 两个参数，前面url，后面保存地址
    webshot(url, filepath, False)
    print("操作结束，耗时：{:.2f}秒".format(float(time.time() - t)))
    return DOWNLOAD_PATH

# 截图测试代码
if __name__ == '__main__':
    print("__main__")
    t = time.time()
    # 两个参数，前面url，后面保存地址
    webshot(people_url, DOWNLOAD_PATH, False)
    print("操作结束，耗时：{:.2f}秒".format(float(time.time() - t)))
