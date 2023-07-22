import json
import requests
from requests.structures import CaseInsensitiveDict

def address_to_coord(address: str,api_key: str, cityinfo: bool=False) -> list[float]:
    """
        此function透過Geogapify Geocode API將地址轉換為經緯度座標
        
        Args:
            address (str): 欲轉換的地址
            api_key (str): API的key
            cityinfo (bool): 顯示該地址位於的縣市英文名稱(概略)

        Returns:
            lat, lot (float, float): 地址轉換過後的經緯度座標
    """

    url = "https://api.geoapify.com/v1/geocode/search?text=" + address + "&apiKey=" + api_key
# https://api.geoapify.com/v1/geocode/search?text=松山機場&apiKey=f0305e991db040688c28b59ac6d9fbd5
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    resp = requests.get(url, headers=headers).json()
    coord = resp["features"][0]["geometry"]["coordinates"]
    
    if cityinfo == True:
        city = resp["features"][0]["properties"]["city"]
        return city

    return coord


def distance_calc(coord1: list[float], coord2: list[float], mode: str, api_key: str) :
    """
        計算起始點與目的地的路線距離並依交通方式計算通行時間

        Args:
            coord1, coord2: list[float] 起始,目的地的經緯度座標
            mode: str {driving|bicycling|walking|transit} 交通方式
            api_key: str API的key
        
        Returns:
            distance, duration (int, float): 計算過後的交通距離及花費時間(單位：公里,秒)

    """

    url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + str(coord1[1]) + "%2C" + str(coord1[0]) + "&destinations=" + str(coord2[1]) + "%2C" + str(coord2[0]) + "&mode=" + mode +"&key=" + api_key
    payload = {}
    headers = {}
    
    resp = requests.get(url, headers=headers, data=payload).json()
    # print(resp["rows"][0]["elements"][0])
    # print(resp)
    distance = float(resp["rows"][0]["elements"][0]["distance"]["value"])*0.001 #m->km
    duration = float(resp["rows"][0]["elements"][0]["duration"]["value"])
    
    return distance, duration

def taxi_calc(distance: float, city: str) -> int:
    """
        利用行車距離及出發地所在縣市估算計程車車資
        *未於下方列出的縣市為查無資料，並以平均值估算之

        Args:
            distance (float): 行車距離(單位：公里)
            city (str): 出發地所在縣市(英文名稱)
        
        Returns:
            int: 估算的車資
    
    """
    if city == "Keelong" or city == "New Taipei" or city == "Taipei":
        return (85 + ((distance*1000-1250)/200)*5)
    elif city == "Taoyuan City" or city == "Taoyuan":
        return (90 + ((distance*1000-1250)/200)*5)
    elif city == "Hsinchu":
        return (100 + ((distance*1000-1250)/200)*5)
    elif city == "Taichung":
        return (85 + ((distance*1000-1500)/200)*5)
    elif city == "Taibao City" or city == "CHiayi":
        return (100 + ((distance*1000-1250)/220)*5)
    elif city == "Tainan":
        return (85 + ((distance*1000-1250)/200)*5)
    elif city == "Kaoshiung":
        return (85 + ((distance*1000-1250)/200)*5)
    elif city == "Maioli City" or city == "Maioli":
        return (100 + ((distance*1000-1250)/200)*5)
    elif city == "Douliu City" or city == "Douliu" or city == "Yunlin":
        return (100 + ((distance*1000-1250)/220)*5)
    elif city == "Zhanghua City" or city == "Zhanghua":
        return (100 + ((distance*1000-1500)/250)*5)
    else:
        return (90 + ((distance*1000-1250)/200)*5)


x = address_to_coord("桃園市大園區航站南路9號","f0305e991db040688c28b59ac6d9fbd5")
y = address_to_coord("台北市松山區敦化北路340之9號1樓","f0305e991db040688c28b59ac6d9fbd5")
dis, dur = distance_calc(x,y ,"driving", "AIzaSyB8jGb3zHAnT_47p-c-5avxJ4KieHEs7-c")
fare = taxi_calc(dis, address_to_coord("桃園市大園區航站南路9號","f0305e991db040688c28b59ac6d9fbd5",True))
print(fare)