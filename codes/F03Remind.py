# 微信
# 请求
import requests
from bs4 import BeautifulSoup
import numpy
# 定时任务
import schedule
import time
import os
import random

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
def getlocalStrTime(formate=date_format_default):
    print("获取今天日期")
    times = time.time()
    local_time = time.localtime(times)
    local_strftime = time.strftime(formate, local_time)
    print("今天日期：{}".format(local_strftime))
    return local_strftime


####################################### 网络请求 #######################################
# 获取日期对应的请求地址的链接
def getQueryUrl(date=getlocalStrTime()):
    return query_3_url.format(date)


# 获取已打卡的人员名单的名字
def requestQiandao(url):
    print("请求链接{}".format(url))
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
    print("系统签到合计{}人：{}".format(len(array), array))
    return array


####################################### 微信请求 #######################################
# 获取对话框函数
def go2TargeChat(user="共赴热爱F4 2.0"):
    wx.Search(user)
    print("搜索" + user)


# 发送单行消息函数
def sendSingleMessage(message="亲爱的喜党"):
    wx.SendMsg(message)
    print("----单行发送----\r\n" + message)


# 发送多行消息函数
def sendMuteMessage(message="亲爱的喜党"):
    WxUtils.SetClipboard(message)
    wx.SendClipboard()
    print("----复制发送 多行发送----\r\n" + message)


# 提醒没打卡
def sendNoCheckInWarming(isSendWechat=True):
    # 获取未打开的人员名单
    # TODO 不知道为什么python函数直接带函数时，作为参数的函数没有被调用
    date = getlocalStrTime()
    url = getQueryUrl(date)
    clockInArrays = requestQiandao(url)
    ndarray = numpy.array(clockInArrays)
    notCheckIn = []
    for name in allArray.keys():
        if len(ndarray) > 0 and (ndarray == name).any():
            print("\t{}已签到".format(name))
        else:
            notCheckIn.append("{} @{} ".format(name, allArray[name]))
            print("WARMING！！！ {}未签到".format(name))

    if isSendWechat:
        if len(notCheckIn) >= 0:
            sendMuteMessage(
                "共赴热爱，感恩一路有你！\r\n忘记打卡的小伙伴记得打卡哦 : {}".format(','.join(str(i) for i in notCheckIn)))
        else:
            sendMuteMessage(
                "共赴热爱，感恩一路有你！全因有你同行\r\n今天{}位喜党都完成了打卡".format(len(allArray)))



# 发送提醒今天打卡链接
def sendCheckInTip():
    path = "./input/打卡链接"
    if os.path.isfile(path):
        f = open("./input/打卡链接", 'r', encoding='utf-8')
        lines = f.read()
        f.close()
        print(lines)
        sendMuteMessage("今天是{}，没有记录就没有发生\r\n\r\n{}".format(getlocalStrTime(), lines))
    else:
        print("{}文件不存在".format(path))

# 发送点赞文本
def sendWorkingTip(message="点赞"):
    sendMuteMessage(message)


# 发送分享期待文本
def sendShareYourFinish():
    arrays = [
        "每天进步一点点，拥抱幸福是必然。", "每天进步一点点，成长足迹看得见。",
        "每天进步一点点，波折烦恼都不见。", "每天进步一点点，前进不止一小点。",
        "每天进步一点点，努力就会到终点。", "每天进步一点点，理想终会被实现。",
        "每天进步一点点，目标距离缩小点。", "每天进步一点点，成功就会在眼前。",
        "每天进步一点点，生活幸福比蜜甜。", "每天进步一点点，一切都会圆满点。"
    ]
    sendMuteMessage(
        "天青色等烟雨，而我在等你。\r\n{}\r\n{}\r\n期待您今天的分享@所有人".format(random.choice(arrays), getOneWord()))


# 获取金句一句
def getOneWord():
    rq = requests.get("https://v1.hitokoto.cn/")
    return rq.json()["hitokoto"]


####################################### 长新闻截图 #######################################
def request_download():
    rq = requests.get("http://bjb.yunwj.top/php/tp/lj.php/")
    IMAGE_URL = rq.json()["tp1"]
    print(IMAGE_URL)
    r = requests.get(IMAGE_URL)
    os.makedirs('./output/', exist_ok=True)
    with open('./output/allNews.png', 'wb') as f:
        f.write(r.content)
    print("下载完成")
    wx.SendFiles('./output/allNews.png')


####################################### 人民网截图 #######################################
def sendScreenshotNews():
    from ScreenShot import getScreenshot
    wx.SendFiles(getScreenshot())


def sendScreenshotOne():
    from ScreenWufazhuce import getScreenshot
    wx.SendFiles(getScreenshot())

####################################### 每周的提醒的函数 #######################################

def getWechatAtGroupMember():
    tmplist = ["@所有人 "]
    for key, value in allArray.items():
        tmplist.append("{} @{} ".format(key, value))
    return "，".join(tmplist).strip('，')

def sendSaturdayWriteMeetingRecordRemind():
    # print("没有记录，就没有发生\r\n今天({})周六，喜党们记得写明天的会议记录哦\r\n{}".format(getlocalStrTime(), getWechatAtGroupMember()))
    sendMuteMessage("没有记录，就没有发生\r\n今天({})周六，喜党们记得写明天的会议记录哦\r\n明天早会哦，记得写会议记录\r\n{}".format(getlocalStrTime(), getWechatAtGroupMember()))

def sendSundayJoinMeetingRemind():
    path = "./input/腾讯会议"
    if os.path.isfile(path):
        f = open(path, 'r', encoding='utf-8')
        lines = f.read()
        f.close()
        print(lines)
        sendMuteMessage("{}\r\n{}".format(lines, getWechatAtGroupMember()))
    else:
        print("{}文件不存在".format(path))

def init():
    folder = "./input/"
    if not os.path.exists(folder):  # 判断是否存在文件夹如果不存在则创建为文件夹
        print("{}文件不存在，创建文件夹".format(folder))
        os.makedirs(folder)
    folder = "./output/"
    if not os.path.exists(folder):  # 判断是否存在文件夹如果不存在则创建为文件夹
        print("{}文件不存在，创建文件夹".format(folder))
        os.makedirs(folder)

    # 用来判断微信启动时，微信是否正常 但后续并没有再判断了
    while (True):
        try:
            # 校验selenium依赖是否正常运行
            from ScreenWufazhuce import getScreenshot
            getScreenshot()
        except Exception as e:
            print(e)
            print("Chrome浏览器驱动异常")
            time.sleep(1)
            continue

####################################### 主程序 #######################################
'''
超凡04组打卡提醒主程序
仅支持微信win客户端
必须先打开微信win客户端，建议用一台空闲服务器登录一个微信
当前名单被写死，因此仅支持本组内使用
当前所有参数均被写死，因此仅内部使用
'''
if __name__ == '__main__':
    init()
    while (True):
        try:
            ## 加tab避免卡顿导致的搜索失败
            wx.SearchBox.SendKeys('{Tab}')
            wx.SearchBox.SendKeys('{Tab}')
            go2TargeChat("文件传输助手")
            wx.SearchBox.SendKeys('{Tab}')
            wx.SearchBox.SendKeys('{Tab}')
            go2TargeChat("文件传输助手")
            break
        except Exception as e:
            print(e)
            print("微信客户端未打开，请打开Windows微信客户端口到前台")
            time.sleep(1)
            continue

    ####################################### 每天的日常提醒 #######################################
    schedule.every().day.at("07:15").do(sendCheckInTip)
    schedule.every().day.at("07:16").do(sendScreenshotNews)

    ## 提醒未打卡 定时任务设置
    schedule.every().day.at("08:29").do(request_download)
    schedule.every().day.at("08:30").do(sendNoCheckInWarming)

    ## 提醒践行 定时任务设置
    schedule.every().day.at("19:59:55").do(sendScreenshotOne)
    schedule.every().day.at("20:00").do(sendShareYourFinish)

    ####################################### 每周的提醒 #######################################
    ## 提醒周6写会议纪要
    schedule.every().saturday.at("18:00").do(sendSaturdayWriteMeetingRecordRemind)
    ## 提醒周6把会议通知提醒发出来
    schedule.every().saturday.at("19:30").do(sendSundayJoinMeetingRemind)

    ## 提醒周天开会
    schedule.every().sunday.at("06:20").do(sendSundayJoinMeetingRemind)

    ## 定时任务触发器运行，固定API
    while True:
        schedule.run_pending()
