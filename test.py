from time import sleep
import unittest
import requests
import json


class WeatherLocSearch:
    def search(search_loc):
        url = f"https://www.agrar.basf.de/api/geodata/getByAddress?address={search_loc}&countries=DE&maxresults=25&languages=DE&autocomplete=false"
        loc_list = requests.get(url).json()
        if len(loc_list) == 0:
            return None
        else:
            return WeatherLocList(loc_list)


class WeatherLocList:
    list = {}

    def __init__(self, list):
        self.list = list

    def get_obj(self):
        return self.list

    def choose(self, number):
        if number in range(len(self.list)):
            return WeatherLoc(self.list[number])
        else:
            return None
class WeatherLoc:

    def __init__(self, loc):
        self.loc = loc

    def get_obj(self):
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

    def get_obj(self):
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

    def cur_weather_str(self):
        wnow = self.weather.get("days1h")[0].get("1h")[0]
        time = wnow.get("time")
        temp = wnow.get("tair")
        hum = wnow.get("relhum")
        wind = wnow.get("wsms")
        clouds = wnow.get("cloud")
        degree = self.weather.get("units").get("degree")
        percent = self.weather.get("units").get("percent")
        meters = self.weather.get("units").get("m_s")
        s = f"time: {time}, temperature: {temp}{degree}, humidity: {hum}{percent}, wind: {wind}{meters}, clouds: {clouds}{percent}"
        return s

    def cur_weather_sen(self):
        wnow = self.weather.get("days1h")[0].get("1h")[0]
        time = wnow.get("time")
        temp = wnow.get("tair")
        hum = wnow.get("relhum")
        wind = wnow.get("wsms")
        clouds = wnow.get("cloud")
        degree = self.weather.get("units").get("degree")
        percent = self.weather.get("units").get("percent")
        meters = self.weather.get("units").get("m_s")
        s = f"Now it is {time} and the temperature is {temp}{degree} at a humidity of {hum}{percent}. We have {wind}{meters} wind and the clouds have {clouds}{percent}"
        return s


class Weathertests(unittest.TestCase):


    def test_search_none(self):
        search = WeatherLocSearch.search("tlkdsjflakjdfl")
        self.assertIsNone(search)
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
        list = weatherlist.get_obj()
        self.assertEqual(weatherlist.get_obj(), json.load(open("testdata/Hannover.json")))

    def test_choose_list_zero(self):
        weatherlist = WeatherLocList(json.load(open("testdata/Berlin.json")))
        loc = weatherlist.choose(0)
        s = '{"name": "Berlin", "zipcode": "12439", "latitude": 52.517778, "longitude": 13.405556, "region1": "Berlin", "region2": "Berlin"}'
        self.assertEqual(loc.get_obj(), json.loads(s))

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
        self.assertEqual(location.get_obj(), json.loads('{"name":"Berlin","zipcode":"12439","latitude":52.517778,"longitude":13.405556,"region1":"Berlin","region2":"Berlin"}'))

    def test_weatherloc_getweather(self):
        location = WeatherLoc(json.loads('{"name":"Berlin","zipcode":"12439","latitude":52.517778,"longitude":13.405556,"region1":"Berlin","region2":"Berlin"}'))
        weather = location.get_weather().get_obj()
        self.assertTrue(weather.get("units"))
        self.assertTrue(weather.get("day1h"))
        self.assertTrue(weather.get("lastUpdated"))
        self.assertTrue(weather.get("days"))
        self.assertTrue(weather.get("days1h"))

    def test_weather_in(self):
        weather = Weather(json.load(open("testdata/weather.json")))
        self.assertEqual(weather.get_obj(), json.load(open("testdata/weather.json")))

    def test_weather_cur_obj(self):
        weather = Weather(json.load(open("testdata/weather.json")))
        self.assertEqual(weather.cur_weather_obj(), json.loads('{"time": "11:00", "temp": 7, "hum": 93, "wind": 7, "clouds": 100}'))

    def test_weather_cur_str(self):
        weather = Weather(json.load(open("testdata/weather.json")))
        self.assertEqual(weather.cur_weather_str(), "time: 11:00, temperature: 7°C, humidity: 93%, wind: 7m/s, clouds: 100%")

    def test_weather_cur_sen(self):
        weather = Weather(json.load(open("testdata/weather.json")))
        self.assertEqual(weather.cur_weather_sen(), "Now it is 11:00 and the temperature is 7°C at a humidity of 93%. We have 7m/s wind and the clouds have 100%")

if __name__ == '__main__':
    print("input location for search")
    locationlist = WeatherLocSearch.search(input())
    obj = locationlist.get_obj()
    print("choose city")
    sleep(2)
    for i in range(len(obj)):
        name = obj[i].get("name")
        zipcode = obj[i].get("zipcode")
        print(f"{i}. {name} {zipcode}")
    citynumber = int(input())
    if citynumber in range(len(obj)):
        loc = locationlist.choose(citynumber)
        weather = loc.get_weather()
        weatherobj = weather.cur_weather_obj()
        temp = weatherobj.get("temp")
        print(f"temp  = {temp}")
        print(weather.cur_weather_sen())
        print(weather.cur_weather_str())
    else:
        print(f"number out of range choose between 0 and {len(obj)}")