import requests
import json
import datetime
import pytz
import random
import re
from tzwhere import tzwhere

def week(i):
        switcher={
                0:'Monday',
                1:'Tuesday',
                2:'Wednesday',
                3:'Thursday',
                4:'Friday',
                5:'Saturday',
                6:'Sunday'
             }  
        return switcher.get(i,"Invalid day of week")

url = "https://community-open-weather-map.p.rapidapi.com/weather"
quoteUrl = "https://type.fit/api/quotes?fbclid=IwAR3mcNvaX_LPuwVd4lm2LTT_DmBsqQInx4OOEBHz4TTD5xC6ZesDZKnCLEM"
namedayUrl = "https://imienniczek.pl"
regex = r'imieniny\-[a-z]*[a-z]\"'
city = input("Enter city to check: ")

querystring = {"q":city,"lat":"0","lon":"0","callback":"","id":"2172797","lang":"null","units":"metric","mode":""}

headers = {
    'x-rapidapi-key': "f80a0e5c29mshd8925035f46f352p11b6adjsn611e07aea267",
    'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
    }

response = json.loads(requests.request("GET", url, headers=headers, params=querystring).text)
quoteResponse = json.loads((requests.request("GET", quoteUrl)).text)
namedayResponse = (requests.request("GET", namedayUrl).text).split("Już wiesz")[0]

tz = tzwhere.tzwhere()

timeZone = pytz.timezone(tz.tzNameAt(response['coord']['lat'], response['coord']['lon']))

basicTime = datetime.datetime.now(timeZone)

number =random.randint(0, len(quoteResponse)) 

names = re.findall(regex, namedayResponse) 
for i in range(0, len(names)):
    names[i] = names[i].split('-')[1]
    names[i] = names[i].split('"')[0]

print("\nCity: " + city, "\nCurrent Time:", week(basicTime.weekday()), basicTime, "\nWeather:", response['weather'][0]['description'], "\nTemp:", response['main']['temp'], " [C], Feels like temp:", response['main']['feels_like'], " [C]", "\nPressure:", response['main']['pressure'], "[hPa]")

print("\nNames of the day: ",  end='')
for i in names:
    print(i.capitalize(), " ", end='')

print("\nQuote of the day:", quoteResponse[number]['text'], "\nAuthor:", quoteResponse[number]['author'])
