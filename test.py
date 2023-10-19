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
            return self.list[number]
        else:
            return None


class Weathertests(unittest.TestCase):

    def test_search_han(self):
        search = WeatherLocSearch.search("Hannover")
        file = json.load(open("Hannover.json"))
        self.assertEqual(len(search.list), len(file))
        for i in search.list:
            thiszipcode = i.get("zipcode")
            if not thiszipcode in str(file):
                return False
        return True

    def test_search_ber(self):
        search = WeatherLocSearch.search("Berlin")
        file = json.load(open("Berlin.json"))
        self.assertEqual(len(search.list), len(file))
        for i in search.list:
            thiszipcode = i.get("zipcode")
            if not thiszipcode in str(file):
                return False
        return True

    def test_get_list(self):
        weatherlist = WeatherLocList(json.load(open("Hannover.json")))
        list = weatherlist.get_list()
        self.assertEqual(weatherlist.get_list(), json.load(open("Hannover.json")))

    def test_choose_list_zero(self):
        weatherlist = WeatherLocList(json.load(open("Berlin.json")))
        loc = weatherlist.choose(0)
        s = '{"name": "Berlin", "zipcode": "12439", "latitude": 52.517778, "longitude": 13.405556, "region1": "Berlin", "region2": "Berlin"}'
        self.assertEqual(loc, json.loads(s))

    def test_choose_list_minus(self):
        weatherlist = WeatherLocList(json.load(open("Berlin.json")))
        loc = weatherlist.choose(-5)
        self.assertEqual(loc, None)

    def test_choose_list_to_big(self):
        weatherlist = WeatherLocList(json.load(open("Berlin.json")))
        loc = weatherlist.choose(50)
        self.assertEqual(loc, None)


def main():
    print(json.load(open("Hannover.json")))
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
