from time import sleep
import unittest
import requests
import json


class WeatherLocSearch:
    def search(search_loc):
        url = f"https://www.agrar.basf.de/api/geodata/getByAddress?address={search_loc}&countries=DE&maxresults=25&languages=DE&autocomplete=false"
        loc_list = requests.get(url).json()
        return WeatherLocList(loc_list)


class WeatherLocList:
    list = {}

    def __init__(self, list):
        self.list = list

    def get_list(self):
        return self.list

    def choose(self, number):
        if number in range(len(self.list)):
            return WeatherLoc(self.list[number])
        else:
            return None
class WeatherLoc:

    def __init__(self, loc):
        self.loc = loc

    def get_loc(self):
        return self.loc

    def get_weather(self):
        lat = self.loc.get("latitude")
        long = self.loc.get("longitude")
        url = f"https://www.agrar.basf.de/api/weather/weatherDetails?latitude={lat}&longitude={long}"
        req = requests.get(url).json()
        return Weather(req)

class Weather:

    def __init__(self, weather):
        self.weather = weather

    def get_json(self):
        return self.weather

    def cur_weather_obj(self):
        wnow = self.weather.get("days1h")[0].get("1h")[0]
        time = wnow.get("time")
        temp = wnow.get("tair")
        hum = wnow.get("relhum")
        wind = wnow.get("wsms")
        clouds = wnow.get("cloud")
        obj = {
            'time': time,
            'temp': temp,
            'hum': hum,
            'wind': wind,
            'clouds': clouds
        }
        return obj

class Weathertests(unittest.TestCase):

    def test_search_han(self):
        search = WeatherLocSearch.search("Hannover")
        file = json.load(open("testdata/Hannover.json"))
        self.assertEqual(len(search.list), len(file))
        for i in search.list:
            thiszipcode = i.get("zipcode")
            if not thiszipcode in str(file):
                return False
        return True

    def test_search_ber(self):
        search = WeatherLocSearch.search("Berlin")
        file = json.load(open("testdata/Berlin.json"))
        self.assertEqual(len(search.list), len(file))
        for i in search.list:
            thiszipcode = i.get("zipcode")
            if not thiszipcode in str(file):
                return False
        return True

    def test_get_list(self):
        weatherlist = WeatherLocList(json.load(open("testdata/Hannover.json")))
        list = weatherlist.get_list()
        self.assertEqual(weatherlist.get_list(), json.load(open("testdata/Hannover.json")))

    def test_choose_list_zero(self):
        weatherlist = WeatherLocList(json.load(open("testdata/Berlin.json")))
        loc = weatherlist.choose(0)
        s = '{"name": "Berlin", "zipcode": "12439", "latitude": 52.517778, "longitude": 13.405556, "region1": "Berlin", "region2": "Berlin"}'
        self.assertEqual(loc.get_loc(), json.loads(s))

    def test_choose_list_minus(self):
        weatherlist = WeatherLocList(json.load(open("testdata/Berlin.json")))
        loc = weatherlist.choose(-5)
        self.assertEqual(loc, None)

    def test_choose_list_to_big(self):
        weatherlist = WeatherLocList(json.load(open("testdata/Berlin.json")))
        loc = weatherlist.choose(50)
        self.assertEqual(loc, None)

    def test_weatherloc_in(self):
        location = WeatherLoc(json.loads('{"name":"Berlin","zipcode":"12439","latitude":52.517778,"longitude":13.405556,"region1":"Berlin","region2":"Berlin"}'))
        self.assertEqual(location.loc, json.loads('{"name":"Berlin","zipcode":"12439","latitude":52.517778,"longitude":13.405556,"region1":"Berlin","region2":"Berlin"}'))

    def test_weatherloc_in2(self):
        list = WeatherLocList(json.load(open("testdata/Berlin.json")))
        location = list.choose(0)
        self.assertEqual(location.get_loc(), json.loads('{"name":"Berlin","zipcode":"12439","latitude":52.517778,"longitude":13.405556,"region1":"Berlin","region2":"Berlin"}'))

    def test_weatherloc_getweather(self):
        location = WeatherLoc(json.loads('{"name":"Berlin","zipcode":"12439","latitude":52.517778,"longitude":13.405556,"region1":"Berlin","region2":"Berlin"}'))
        weather = location.get_weather().get_json()
        self.assertTrue(weather.get("units"))
        self.assertTrue(weather.get("day1h"))
        self.assertTrue(weather.get("lastUpdated"))
        self.assertTrue(weather.get("days"))
        self.assertTrue(weather.get("days1h"))

    def test_weather_in(self):
        weather = Weather(json.load(open("testdata/weather.json")))
        self.assertEqual(weather.get_json(), json.load(open("testdata/weather.json")))

    def test_weather_cur_json(self):
        weather = Weather(json.load(open("testdata/weather.json")))
        self.assertEqual(weather.cur_weather_obj(), json.loads('{"time": "11:00", "temp": 7, "hum": 93, "wind": 7, "clouds": 100}'))


def main():
    print(json.load(open("testdata/Hannover.json")))
    print("-------------------------")
    WeatherLocSearch("Hannover")

    print("input location")
    # search_loc = input()
    search_loc = "Hannover"
    url = f"https://www.agrar.basf.de/api/geodata/getByAddress?address={search_loc}&countries=DE&maxresults=25&languages=DE&autocomplete=false"
    website = requests.get(url)
    loc_list = website.json()
    # print(loc_list)
    print("chose city: ")
    sleep(1)
    for i in range(len(loc_list)):
        element = loc_list[i]
        region = element.get("region1")
        name = element.get("name")
        zipcode = element.get("zipcode")
        output = f"{i}. {region} {name} {zipcode}"
        print(output)
    loc_num = int(input())
    if loc_num >= 0 and loc_num <= len(loc_list):
        loc = loc_list[loc_num]
    else:
        print("wrong number")
# main()

weather = Weather(json.load(open("testdata/weather.json")))
weather.cur_weather_obj()