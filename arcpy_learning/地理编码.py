from urllib import parse
from urllib.request import urlopen
import csv
import json
import re
import pandas as pd


def get_urt(name, address):
    # 输入你的秘钥，获取地址http://lbsyun.baidu.com/apiconsole/key/create
    your_ak = 'qUUo9UEFVG4EgQ23PkpOdruI2VEjzMCm'
    queryStr = '/geocoding/v3/?address={}&output=json&ak={}&callback=showLocation'.format(address, your_ak)
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
        data = pd.DataFrame(data=[[name, address, lon, lat, confidence, level]],
                            columns=['地名', '地址', '经度', '纬度', '误差（米）', '地区等级'])

        data.to_csv('goeinfo.csv', mode='a', index=False, header=False)
        return data
    else:
        data = pd.DataFrame(data=[[name, address, "none", "none", "none", "none"]],
                            columns=['地名', '地址', '经度', '纬度', '误差（米）', '地区等级'])

        data.to_csv('goeinfo.csv', mode='a', index=False, header=False)
        return data


if __name__ == '__main__':
    # 加载地区名，这里放在tuple里，也可以从csv等文件读取
    # with open('goeinfo.csv', 'a+', encoding='utf-8') as f:
    #     f.write("地名,地址,经度,纬度,误差（米）,地区等级\n", )
    #     f.close()
    with open(r'C:\Users\Administrator\Desktop\wenhua.csv', 'r', encoding='utf-8') as file:
        data = csv.reader(file, )
        for i in data:
            get_urt(i[0], i[1])

    print('地区加载完成，已生成结果')
