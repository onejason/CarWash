#coding:utf-8
from bs4 import BeautifulSoup
import requests
import time
import datetime
import re
import xlrd
import os

#####################################
# 查询建行洗车点Excel,并在baidu地图上显示
#####################################

xls_file_name = 'ccb_car_wash_sites.xls'
html_file_name = 'baidu_map_for_sites.html'

##########################
### 从建行洗车点网站下载Excel
##########################
url = "http://store.ccb.com/sc/branch/business/20110831_1314781953.html"
wb_data=requests.get(url)
soup = BeautifulSoup(wb_data.text, 'lxml')

# 找到 class=link_blue 的 a 标签
# a = soup.find("a", class_="link_blue")
# 另外一种方法: 找到包含"商户名单"的 a 标签
tag = soup.find("a", text=re.compile(u"商户名单"))

url = tag.get('href')
# print url
download_url = 'http://store.ccb.com'+ url
print '下载地址为: ' + download_url

# excel下载地址例子:http://store.ccb.com/sc/share/tese/20110831_1314781953/20160328141351012913.xls

print "downloading with requests"
r = requests.get(download_url)

with open(xls_file_name, "wb") as xml_file:
     xml_file.write(r.content)
xml_file.close
print "downloading done"

################
# 读取Excel的内容
################

print "reading xls"
data = xlrd.open_workbook(xls_file_name)
table = data.sheet_by_index(1)
nrows = table.nrows
ncols = table.ncols
flag = 0
addresses = []
# 循环行列表数据
for i in range(nrows):
    district = table.row_values(i)[1]
    if district:
        if ((district == u'高新区') | (district == u'天府新区') | (district == u'武侯区') | (district == u'锦江区')) :
            #print table.row_values(i)[3]
            addresses.append(table.row_values(i)[3])
            flag = 1
        else:
            flag = 0
    else:
        if flag == 1:
            #print table.row_values(i)[3]
            addresses.append(table.row_values(i)[3])

###############
# 生成百度地图脚本
###############
print "generating html"
html_code2 = ''
for str in addresses:
    html_code2 += '        \"' + str + '\",\n'

html_code1 = u'''<!DOCTYPE html>
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf8" />
	<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
	<title>批量地址</title>
	<style type="text/css">
		body, html{width: 100%;height: 100%;margin:0;font-family:"微软雅黑";}
		#l-map{height:800px;width:100%;}
		#r-result{width:100%; font-size:14px;line-height:20px;}
	</style>
	<script type="text/javascript" src="http://api.map.baidu.com/api?v=2.0&ak=您的密钥"></script>
</head>
<body>
	<div id="l-map"></div>
	<div id="r-result">
		<input type="button" value="批量地址解析" onclick="bdGEO()" />
		<div id="result"></div>
	</div>
</body>
</html>
<script type="text/javascript">
	// 百度地图API功能
	var map = new BMap.Map("l-map");
	map.centerAndZoom(new BMap.Point(104.072179,30.539082), 13);
	map.enableScrollWheelZoom(true);
	var index = 0;
	var myGeo = new BMap.Geocoder();
	var adds = [
'''

html_code3 = u'''    ];
	function bdGEO(){
		var add = adds[index];
		geocodeSearch(add);
		index++;
	}
	function geocodeSearch(add){
		if(index < adds.length){
			setTimeout(window.bdGEO,400);
		}
		myGeo.getPoint(add, function(point){
			if (point) {
				document.getElementById("result").innerHTML +=  index + "、" + add + ":" + point.lng + "," + point.lat + "</br>";
				var address = new BMap.Point(point.lng, point.lat);
				addMarker(address,new BMap.Label(index+":"+add,{offset:new BMap.Size(20,-10)}));
			}
		}, "成都市");
	}
	// 编写自定义函数,创建标注
	function addMarker(point,label){
		var marker = new BMap.Marker(point);
		map.addOverlay(marker);
		marker.setLabel(label);encode('utf8')
	}
</script>'''

all_string = html_code1 + html_code2 + html_code3
htlm_file = file(html_file_name, 'w+')
htlm_file.write(all_string.encode('utf-8'))
htlm_file.close

# 删除xls文件
print 'deleting downloaded xls file'
if os.path.exists(xls_file_name):
    os.remove(xls_file_name)

print u'DONE, 请打开:'+html_file_name
print u'百度地图开放平台->批量地址解析demo: http://developer.baidu.com/map/jsdemo.htm#i7_3'