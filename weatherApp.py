import requests
import json
from datetime import datetime
import time
from os import path
# description = result.json()['weather'][0]['description']

# temperature = round(result.json()['main']['temp'])
# feelsLike = round(result.json()['main']['feels_like'])
# high = round(result.json()['main']['temp_max'])
# low = round(result.json()['main']['temp_min'])

#? function to get the time so we can seperate the JSON files by the hour and date
def getTime():
    t = time.localtime()
    current_time = time.strftime("%H:%M", t)
    return current_time


def getResultJson():
    # * Gets the api key from the apiKey.txt file
    apiKey = open("apiKey.txt", "r").read()
    while True:
        #* Asks the user for the city name that they want the weather for, will keep looping until the user enters a valid city name
        location = input("Enter the city name: ")
        #* Uses the requests library to access the openweathermap api and get the weather data for the city that the user entered
        result = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid={apiKey}")
        if result.json()['cod'] == '404':
            print("Invalid location!")
            continue
        print (f"the city of {result.json()['name']} is valid")
        #* Returns the JSON data that was retrieved from the openweathermap api
        #* It also saves the time and date of the weather so that we may access it at a later time
        
        newResult = result.json()
        
        # saveLocationAndTime(newResult['name'], str(time))
        saveToArray(newResult)
        # saveDataArray(newResult)
        return newResult

#updates the location of the user

def getDesc(result):
    return result['weather'][0]['description']

def getTemp(result):
    return f"{round(result['main']['temp'])}°C"

def getHigh(result):
    return f"{round(result['main']['temp_max'])}°C"

def getLow(result):
    return f"{round(result['main']['temp_min'])}°C"


def updateLocationStr(loc):
        # * Gets the api key from the apiKey.txt file
    apiKey = open("apiKey.txt", "r").read()
    if loc == "":
        return None
    while True:
        #* Asks the user for the city name that they want the weather for, will keep looping until the user enters a valid city name
        location = loc
        #* Uses the requests library to access the openweathermap api and get the weather data for the city that the user entered
        result = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid={apiKey}")
        if result.json()['cod'] == '404':
            print("Invalid location!")
            return None
        print(f"Location being set to: {result.json()['name']}")
        #* Returns the JSON data that was retrieved from the openweathermap api and saves to be used later
        time = getTime()
        d = datetime.now().date()
        date = str(d)
        newResult = result.json()
        newResult.update({"date": date, "time": str(time)})
        
        saveToArray(newResult)
        return newResult
    
def getWind(result):
    windSpeed = result['wind']['speed']
    windDeg = result['wind']['deg']
    return f"{windSpeed} m/s, {windDeg}°"





# ?This program should save all the JSON info to a file so that we can access it later
#? it should also organize the data in a way that is easy to access and read from and so that 
#? we can access it later and save multiple locations and their weather data from different dates

# needs to save the data to a file only if the data isn't already there
def saveData(result):
    d = datetime.now().date()
    date = str(d)
    path = fr"saveFiles\{result['name']}WeatherData{date}.json"
    with open(path, "w") as file:
        json.dump(result, file)
        
def loadData(location, date):
    path = fr"saveFiles\{location}WeatherData{date}.json"
    with open(path, "r") as file:
        data = json.load(file)
        return data

def saveDataArray(result):
    listObj = []
    d = datetime.now().date()
    date = str(d)
    p = fr"saveFiles\{result['name']}WeatherData{date}.json"
    if path.isfile(p):
        with open(p) as fp:
            listObj = json.load(fp)
            listObj.append(result)
        listObj.append(result)
        with open(p, "w") as fp:
            json.dump(listObj, fp)
    else:
        listObj.append(result)
        with open(p, "w") as fp:
            json.dump(listObj, fp)
            
            
def saveToArray(result):
    listObj = [] 
    p = fr"saveFiles\{result['name']}WeatherData.json"
    saveLocation(result['name'])
    if path.isfile(p):
        with open(p) as fp:
            listObj = json.load(fp)
            listObj.append(result)
        listObj.append(result)
        print(result)
        with open(p, "w") as fp:
            json.dump(listObj, fp)
    else:
        listObj.append(result)
        with open(p, "w") as fp:
            json.dump(listObj, fp)
    # saveLocation(newResult['name'])
            
def loadFromArray(location):
    path = fr"saveFiles\{location}WeatherData.json"
    with open(path, "r") as file:
        data = json.load(file)
        return data
            

def findWeatherHour(resultList, time):
    for result in resultList:
        if result["time"] == time:
            return result
    

def saveLocation(location):
    d = str(datetime.now())
    with open(r"saveFiles\locations.txt", "a") as file:
        file.write(f"{location}, {str(d)}, {getTime()} \n")
        
def saveLocationAndTime(location, time):
    with open(r"saveFiles\locations.txt", "a") as file:
        file.write(f"{location}, {time} \n")
        
def loadLocations():
    with open(r"saveFiles\locations.txt", "r") as file:
        locations = file.readlines()
        return locations
    
def showCountry(result):
    return result['sys']['country']

def showCity(result):
    return result['name']   

#* This class is used to store the weather data that is retrieved from the openweathermap api
#* It is used to store the data in a way that is easy to access and read from
#* It also allows us to store multiple weather data from different dates and times
#? It was made because it was difficult to access the data from the JSON file that was saved and keep the order of the current weather data
class weatherDataArray:
    def __init__(self, result):
        self.result = result
        self.position = 0
        self.length = len(result)
    
    def setPos(self, pos):
        self.position = pos
        return self.result[pos]
        
    def next(self):
        if self.position < self.length:
            self.position += 1
            return self.result[self.position]
        else:
            return self.result[self.position]
    def prev(self):
        if self.position > 0:
            self.position -= 1
            return self.result[self.position]
        else:
            return self.result[self.position]
    