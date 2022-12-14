# 微信
# 请求
import requests
from bs4 import BeautifulSoup
import numpy
# 定时任务
import schedule
import time

from wxauto import WeChat, WxUtils


# 日期格式化的格式
date_format_default = '%Y-%m-%d'
# 获取当前微信客户端
wx = WeChat()
# 易效能系统查询我们组的链接 不同组不一样 生成规则未知 还需要cookeis作为密码，看头文件知道的
query_3_url = "https://edu2.yixiaoneng.com/f/tMtIEp/s/8R00JD?q%5B0%5D%5Bfield_1%5D={}&q%5B0%5D%5Bfield_2_associated_field_3%5D=nAlJ&embedded="
# 发送对象
WHO_USER = "共赴热爱F4 2.0"
# 组员名单列表 = {"真实名字":"群名"}
allArray = {
    "蔡雪金": "F01蔡雪金",
    "赵雨涵": "Aurora💫",
    "林华玉": "林",
    "赵超": "超凡304赵超",
    "唐子涵": "甲亢speed.",
    "周秀娟": "周秀娟",
    "李岳珉": "李岳珉",
    "李晓娟": "超凡308李晓娟",
#    "肖娟": "",
    "丘凤梅": "F10丘凤梅",
    "耿洁": "超凡03-11耿洁",
    "张碧芬": "超凡312张碧芬",
    "单文科": "单文科",
}

####################################### 公共类 #######################################

# 获取今天的日期对应的请求地址的链接
def getlocalStrTime(formate = date_format_default):
    times = time.time()
    local_time = time.localtime(times)
    local_strftime = time.strftime(formate, local_time)
    print("今天日期：{}".format(local_strftime))
    return local_strftime

####################################### 网络请求 #######################################
# 获取日期对应的请求地址的链接
def getQueryUrl(date = getlocalStrTime()):
    return query_3_url.format(date)

# 获取已打卡的人员名单的名字
def requestQiandao(url):
    # 密码311
    cookies = {"rs_token_8R00JD": "00311"}
    page = requests.get(url
                        , cookies=cookies
                        )
    # print(page.text)

    page.encoding = "utf-8"
    # 网页格式化
    soup = BeautifulSoup(page.text, features="html.parser")
    # 学员名字 找td标签属性为name-field的内容
    name_items = soup.find_all("td", class_="name-field")
    # 学员学号
    id_items = soup.find_all("td", class_="cascade-drop-down")
    array = []
    # for company_item in name_items:
    # dd = company_item.text.strip()
    # print(company_item)
    # print(dd)
    # array.append(dd)
    for index in range(len(name_items)):
        n = name_items[index].text.strip()
        i = id_items[index].text.strip()
        print("【name = {}】【index = {}】".format(n, i))
        array.append(n)

    array.sort()
    return array


####################################### 微信请求 #######################################
# 获取对话框
def go2TargeChat(user = "共赴热爱F4 2.0"):
    wx.Search(user)
    print("搜索" + user)

# 发送消息
def sendSingleMessage(message = "亲爱的喜党"):
    wx.SendMsg(message)
    print("单行发送" + message)

def sendMuteMessage(message = "亲爱的喜党"):
    WxUtils.SetClipboard(message)
    wx.SendClipboard()
    print("复制发送" + message)

# 提醒没打卡
def sendNoCheckInWarming():
    # 获取未打开的人员名单
    clockInArrays = requestQiandao(getQueryUrl())
    ndarray = numpy.array(clockInArrays)
    notCheckIn = []
    for name in allArray.keys():
       if((ndarray == name).any()):
           print("{}已签到".format(name))
       else:
           notCheckIn.append("{} @{} ".format(name, allArray[name]))
           print("WARMING！！！ {}未签到".format(name))

    sendMuteMessage("共赴热爱，感恩一路有你！\r\n忘记打卡的小伙伴记得打卡哦 : {}".format(','.join(str(i) for i in notCheckIn)))

# 提醒今天打卡
def sendCheckInTip():
    f = open("./input/打卡链接", 'r', encoding='utf-8')
    lines = f.read()
    f.close()
    print(lines)
    sendMuteMessage("今天是{}，没有记录就没有发生\r\n\r\n{}".format(getlocalStrTime(), lines))

def sendWorkingTip():
    sendMuteMessage("点赞")

def sendShareYourFinish():
    sendMuteMessage("天青色等烟雨，而我在等你。\r\n{}\r\n期待您今天的分享".format(getOneWord()))

# 获取金句一句
def getOneWord():
    rq = requests.get("https://v1.hitokoto.cn/")
    return rq.json()["hitokoto"]

####################################### 人民网截图 #######################################

def sendScreenshotNews():
    from ScreenShot import getScreenshot
    wx.SendFiles(getScreenshot())

def sendScreenshotOne():
    from ScreenWufazhuce import getScreenshot
    wx.SendFiles(getScreenshot())

####################################### 主程序 #######################################
'''
超凡04组打卡提醒主程序
仅支持微信win客户端
必须先打开微信win客户端，建议用一台空闲服务器登录一个微信
当前名单被写死，因此仅支持本组内使用
当前所有参数均被写死，因此仅内部使用
'''
if __name__ == '__main__':
    while(True):
        try:
            from ScreenWufazhuce import getScreenshot
            getScreenshot()
        except Exception as e:
            print(e)
            print("Chrome浏览器驱动异常")
            time.sleep(1)
            continue

        try:
            ## 加tab避免卡顿导致的搜索失败
            wx.SearchBox.SendKeys('{Tab}')
            wx.SearchBox.SendKeys('{Tab}')
            go2TargeChat(WHO_USER)
            wx.SearchBox.SendKeys('{Tab}')
            wx.SearchBox.SendKeys('{Tab}')
            go2TargeChat(WHO_USER)
            break
        except Exception as e:
            print(e)
            print("微信客户端未打开，请打开Windows微信客户端口到前台")
            time.sleep(1)
            continue

    ## 提醒打卡
    schedule.every().day.at("07:30").do(sendCheckInTip)
    schedule.every().day.at("07:31").do(sendScreenshotNews)

    ## 提醒为打卡
    schedule.every().day.at("08:30").do(sendNoCheckInWarming)

    ## 提醒践行
    schedule.every().day.at("19:59:55").do(sendScreenshotOne)
    schedule.every().day.at("20:00").do(sendShareYourFinish)

    while True:
        schedule.run_pending()

