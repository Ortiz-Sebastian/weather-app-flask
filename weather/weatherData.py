import requests
from pprint import pprint
import time
import string
import json


ApiKey = '61f43d359364a0addd43a1679089c2bd'

class Weather():
    def getdata(self, city,units):
        url = "https://api.openweathermap.org/data/2.5/weather?appid=" + ApiKey+"&q="+ city+"&units="+ units
        info = requests.get(url).json()
        info['main']['temp'] = round(info['main']['temp'])
        info['main']['feels_like'] = round(info['main']['feels_like'])
        info['main']['temp_max'] = round(info['main']['temp_max'])
        info['main']['temp_min'] = round(info['main']['temp_min'])

        return info

    def getTime(self, dt, fullTime):
        if fullTime:
            timetupp = time.localtime(dt)
            tdTime = time.strftime("%a, %d %b %Y %H:%M:%S",timetupp)
        else:
            timetupp = time.localtime(dt)
            tdTime = time.strftime("%a, %d",timetupp)
        return tdTime

    def getweeklydata(self, lon, lat,units):
            url = "https://api.openweathermap.org/data/3.0/onecall?appid=" + ApiKey+"&lat="+ str(lat) +"&lon="+ str(lon)+"&exclude=minutely&units="+ units
            weeklyData = []
            info = requests.get(url).json()
            pprint(info)
            for day in info["daily"][1:]:
                date = self.getTime(day["dt"], False)
                maxTemp = round(day["temp"]["max"])
                minTemp = round(day["temp"]["min"])
                weatherName = day["weather"][0]["main"]
                weatherDes = day["summary"]
                icon = day["weather"][0]["icon"]
                url = self.getImageUrl(icon)
                dict = {"date": date, "max": maxTemp, "min": minTemp, "name": weatherName, "description": weatherDes,"imageName": icon, "url": url}
                weeklyData.append(dict)
            return weeklyData
    def getImageUrl(self, id):
            url = "https://openweathermap.org/img/wn/"+id+"@2x.png"
            return url

