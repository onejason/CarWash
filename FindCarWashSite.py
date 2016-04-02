#coding:utf-8
from bs4 import BeautifulSoup
import requests
import time
import datetime
import re

# 查询建行洗车点Excel,并在baidu地图上显示


# 建行洗车点网站
url = "http://store.ccb.com/sc/branch/business/20110831_1314781953.html"

wb_data=requests.get(url)
wb_data.encoding='utf8'
text = wb_data.text

print text
#excel下载地址例子:http://store.ccb.com/sc/share/tese/20110831_1314781953/20160328141351012913.xls

#searchObj = re.search(r'marketValue = \'(\d+\.\d+)\';', text)
