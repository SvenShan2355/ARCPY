from urllib import parse
from urllib.request import urlopen
import csv
import json
import re
import pandas as pd
import math


def get_urt(name, address):
    # 输入你的秘钥，获取地址http://lbsyun.baidu.com/apiconsole/key/create
    your_ak = 'qUUo9UEFVG4EgQ23PkpOdruI2VEjzMCm'
    queryStr = '/geocoding/v3/?address={}&output=json&ak={}&callback=showLocation'.format(name, your_ak)
    # 由于URL里面含有中文，所以需要用parse.quote进行处理，然后返回最终可调用的url
    url = parse.quote("http://api.map.baidu.com" + queryStr, safe="/:=&?#+!$,;'@()*[]")
    response = urlopen(url).read().decode('utf-8')
    reshape_response = re.findall("\((.*?)\)", response)[0]
    print(reshape_response)
    # 将返回的数据转化成json格式
    responseJson = json.loads(reshape_response)
    # 获取经纬度
    if responseJson.get('status') == 0:
        lon = responseJson.get('result')['location']['lng']
        lat = responseJson.get('result')['location']['lat']
        # status = responseJson.get('status')
        # 获取误差范围
        confidence = responseJson.get('result')['confidence']
        # 获取地区等级
        level = responseJson.get('result')['confidence']
        # 转坐标
        lon1, lat1 = getWgs84xy(float(lon), float(lat))

        data = pd.DataFrame(data=[[name, address, lon1, lat1, confidence, level]],
                            columns=['地名', '地址', '经度', '纬度', '误差（米）', '地区等级'])

        data.to_csv('goeinfo.csv', mode='a', index=False, header=False)
        return data
    else:
        data = pd.DataFrame(data=[[name, address, "none", "none", "none", "none"]],
                            columns=['地名', '地址', '经度', '纬度', '误差（米）', '地区等级'])

        data.to_csv('goeinfo.csv', mode='a', index=False, header=False)
        return data

x_pi = float(3.14159265358979324 * 3000.0 / 180.0)
# //pai
pi = float(3.1415926535897932384626)
# //离心率
ee = float(0.00669342162296594323)
# //长半轴
a = float(6378245.0)


def bd09togcj02(bd_lon, bd_lat):
    x = (bd_lon - 0.0065)
    y = (bd_lat - 0.006)
    z = (math.sqrt(x * x + y * y)) - (0.00002 * math.sin(y * x_pi))
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
    gg_lng = z * math.cos(theta)
    gg_lat = z * math.sin(theta)

    return gg_lng, gg_lat


def gcj02tobd09(lng, lat):
    z = math.sqrt(lng * lng + lat * lat) + 0.00002 * math.sin(lat * x_pi)
    theta = math.atan2(lat, lng) + 0.000003 * math.cos(lng * x_pi)
    bd_lng = z * math.cos(theta) + 0.0065
    bd_lat = z * math.sin(theta) + 0.006
    return bd_lng, bd_lat


def gcj02towgs84(lng, lat):
    dlat = transformlat(lng - 105.0, lat - 35.0)
    dlng = transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [lng * 2 - mglng, lat * 2 - mglat]


def transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * math.sqrt(abs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 * math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 * math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 * math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret


def transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * math.sqrt(abs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 * math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 * math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 * math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret


def getWgs84xy(x, y):
    doubles_gcj = bd09togcj02(x, y)
    doubles_wgs84 = gcj02towgs84(doubles_gcj[0], doubles_gcj[1])
    return doubles_wgs84


def rowreturn(row):
    x = getWgs84xy(row['lng'], row['lat'])
    return x[0]


def rowreturny(row):
    x = getWgs84xy(row['lng'], row['lat'])
    return x[1]


if __name__ == '__main__':
    # 加载地区名，这里放在tuple里，也可以从csv等文件读取
    with open('goeinfo.csv', 'a+', encoding='utf-8') as f:
        f.write("地名,地址,经度,纬度,误差（米）,地区等级\n", )
        f.close()
    with open(r'C:\Users\Administrator\Desktop\yiliao2.csv', 'r', encoding='utf-8') as file:
        data = csv.reader(file)
        for i in data:
            get_urt(i[0], i[2])

    print('地区加载完成，已生成结果')
