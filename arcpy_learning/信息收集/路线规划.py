from urllib import parse
from urllib.request import urlopen
import csv
import json
import pandas as pd


def get_road(origins, destinations, tactics="0", coord_type="wgs84", ret_coordtype="gcj02"):
    print("查询")
    your_ak = 'cmZLqIXPG9ZxF5M6ifYlYRoCXaLbjFA2'
    queryStr = '/directionlite/v1/driving?origin={}&destination={}&tactics={}&coord_type={}&ret_coordtype={}&ak={}'.format(
        origins, destinations, tactics, coord_type, ret_coordtype, your_ak)
    url = parse.quote("http://api.map.baidu.com" + queryStr, safe="/:=&?#+!$,;'@()*[]")
    response = urlopen(url).read().decode('utf-8')
    responseJson = json.loads(response)
    if responseJson.get('status') == 0:
        distance = responseJson.get('result')['routes'][0]['distance']
        duration = responseJson.get('result')['routes'][0]['duration']
        return distance, duration
    else:
        return "——", "——"


if __name__ == '__main__':
    open_file = r'C:\Users\Administrator\Desktop\geoinfo.csv'
    write_file = 'cost_Matrix.csv'
    with open(open_file, 'r', encoding='utf-8') as location_file:
        location_data = csv.reader(location_file)
        locations = []
        for i in location_data:
            locations.append(i[0])
        location_file.close()
    with open(write_file, 'a+', encoding='utf-8') as f:
        text = ""
        for i in locations:
            text = text + i + ","
        f.write(text + "\n", )
        f.close()
    with open(open_file, 'r', encoding='utf-8') as file:
        data = csv.reader(file)
        locations_list = []
        for i in data:
            locations_list.append(i)
        del locations_list[0]
        num = 1
        for i in locations_list:
            cost_list = [i[0]]
            for j in locations_list:
                duration = get_road(origins=i[2] + "," + i[1], destinations=j[2] + "," + j[1])[1]
                cost_list.append(duration)
                print(num)
                num += 1
            data = pd.DataFrame(data=[cost_list])
            data.to_csv(write_file, mode='a', index=False, header=False)
        file.close()

    print('路线查找结束')
