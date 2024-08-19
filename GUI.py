from tkinter import *
from tkinter import ttk
from tkinter import Tk, Label, messagebox
from random import randint

from weatherApp import *


#? function that gets new weather data from the API using user input
def buttonGetWeather():
    location = tBox.get()
    result = updateLocationStr(location)
    if result != None:
        # print(result["name"])
        showWeather(result)
        return result
    else:
        show_invalid_location_popup()


#? Function to show a popup when the user enters an invalid location
def show_invalid_location_popup():
    try:
        pop = Tk()
        pop.title("Invalid Location")
        pop.geometry("300x100")
        pop.resizable(width=False, height=False)
        pop.iconbitmap("saveFiles/img/favicon.ico")
        pop.configure(bg="red")
        label = Label(pop, text="Invalid Location, Please try again!", font=("Calibri", 15))
        label.pack()
        pop.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


#? Function to get previously weather data from the API that has been saved to a file
def buttonGetOldWeather():
    loc = tBox.get()
    if loc == "":
        #! insert a popup that will tell the user that the location is invalid
        show_invalid_location_popup()
    result = weatherDataArray(loadFromArray(loc))
    
    
    if result != None:
        #TODO: Add a function that will display the weather data in THE MAIN WINDOW OF THE APP
        showWeather(result.result[result.position])
        #* If there is more than one result, then we will add a button that will allow the user to see the next weather data and the previous weather data
        fillWeatherbox(result)
            
            
            
    else:
        show_invalid_location_popup()

#? function that sets the weather to the next one in the array
# def setWeatherNext( result: weatherDataArray):
#     if result != None:
#         showWeather(result.next())
    
#? Function to generate random x and y coordinates for the background image, MAKES THE APP LOOK MORE INTERESTING    
def wpRandomX() -> int:
    return randint( -368, 0)

def wpRandomY() -> int:
    return randint( -575,0)
#? Function to display the date of the weather data that was retrieved
def showDate(result):
    dateEntry.config(state="normal", font=("Calibri", 15), bg="white", fg="black")
    dateEntry.delete(0, END)
    dateEntry.insert(0, result['date'])
    dateEntry.config(state="readonly")
    return result['date']

#? Function to display the time of the weather data that was retrieved
def showTime(result):
    timeEntry.config(state="normal", font=("Calibri", 15), bg="white", fg="black")
    timeEntry.delete(0, END)
    timeEntry.insert(0, result['time'])
    timeEntry.config(state="readonly")
    return result['time']

#? Function to display the description of the weather data that was retrieved
def showDesc(result):
    descEntry.config(state="normal", font=("Calibri", 15), bg="white", fg="black")
    descEntry.delete(0, END)
    descEntry.insert(0, getDesc(result))
    descEntry.config(state="readonly")
    return getDesc(result)

#? Function to display the temperature of the weather data that was retrieved
def showTemp(result):
    tempEntry.config(state="normal", font=("Calibri", 15), bg="white", fg="black")
    tempEntry.delete(0, END)
    tempEntry.insert(0, f"{round(result['main']['temp'])}°C")
    tempEntry.config(state="readonly")
    return getTemp(result)

#? Function to display the high temperature of the weather data that was retrieved
def showHigh(result):
    highEntry.config(state="normal", font=("Calibri", 15), bg="white", fg="black")
    highEntry.delete(0, END)
    
    highEntry.insert(0, f"{round(result['main']['temp_max'])}°C")
    highEntry.config(state="readonly")
    return getHigh(result)

#? Function to display the low temperature of the weather data that was retrieved
def showLow(result):
    lowEntry.config(state="normal", font=("Calibri", 15), bg="white", fg="black")
    lowEntry.delete(0, END)
    
    lowEntry.insert(0, f"{round(result['main']['temp_min'])}°C")
    lowEntry.config(state="readonly")
    return getLow(result)

#? Function to display the wind speed and direction of the weather data that was retrieved
def showWind(result):
    windEntry.config(state="normal", font=("Calibri", 15), bg="white", fg="black")
    windEntry.delete(0, END)
    
    windEntry.insert(0, f"{result['wind']['speed']}m/s {result['wind']['deg']}°")
    windEntry.config(state="readonly")

#? Function to display the location of the weather data that was retrieved
def showLocation(result):
    locationEntry.config(state="normal"  ,  font=("Calibri", 15), bg="white", fg="black")
    locationEntry.delete(0, END)
    
    locationEntry.insert(0, f"{result['name']}, {result['sys']['country']}")
    locationEntry.config(state="readonly")
    return f"{result['name']}, {result['sys']['country']}"

#? Function to display the weather data that was retrieved from the API
def showWeather(result):
    showLocation(result)
    showDate(result)
    showTime(result)
    showDesc(result)
    showTemp(result)
    showHigh(result)
    showLow(result)
    showWind(result)

def fillWeatherbox(result):
    weatherLBox.delete(0, END)
    for i in range(len(result.result)):
        text = f"{result.result[i]['name']}, {result.result[i]['sys']['country']}, {result.result[i]['date']}, {result.result[i]['time']}"
        weatherLBox.insert(i, text)

def getOldWeatherList():
    inputPlace = weatherLBox.get(weatherLBox.curselection())
    location = inputPlace.split(",")[0]
    time = inputPlace.split(",")[3]
    date = inputPlace.split(",")[2]
    d = date.removeprefix(" ")
    t = time.removeprefix(" ")
    resultList = loadFromArray(location)
    for i in range(len(resultList)):
        if resultList[i]['date'] == d and resultList[i]['time'] == t:
            showWeather(resultList[i])
            return resultList[i]


#? Setting up the window of the app and it's dimensions and title
root = Tk()
root.title("Weather App")
root.geometry("368x764")
root.resizable(width=False, height=False)
root.iconbitmap("saveFiles/img/favicon.ico")
#? Setting the background of the app to be a cloudy sky
bg = PhotoImage(file = "saveFiles/img/file.png")
wallP = Label( root, image = bg)
wallP.place(x =wpRandomX(), y =wpRandomY())
#? Setting up the header of the app
header = Label(root, text="Please enter the name of the City: ", font=("Calibri", 15))
header.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
header.configure(bg="gold", fg="black")

#? Setting up the text box for the user to input the city name
tBox = Entry(root, width=35 , borderwidth=5, font=("Calibri", 15), bg="white", fg="black")
tBox.grid(row=1, column=0, columnspan=4, padx=5, pady=5)

#? Setting up the different types of Search Buttons 
# * Button to get the weather data from the API
b1 = ttk.Button(root, text="Search New Weather", command=buttonGetWeather)
b1.grid(row=2, column=0, columnspan=1, padx=1, pady=1)
b1.configure(style="TButton")

# * Button to get the weather data from the saved file
b2 = ttk.Button(root, text="Search Old Weather", command=buttonGetOldWeather)
b2.grid(row=2, column=2, columnspan=1, padx=1, pady=1, ipadx=10)
b2.configure(style="TButton")
#? Labels to show the data that was retrieved from the API in the GUI
#* Label to show the location of the weather data
locationLabel = Label(root, text="Location: ", font=("Calibri", 15))
locationLabel.grid(row=5, column=0, columnspan=1, padx=1, pady=1)
locationLabel.configure(bg="gold", fg="black")
#* entry to put the weather data in 
locationEntry = Entry(root, width=15, borderwidth=5, font=("Calibri", 15), bg="white", fg="black", state="readonly")
locationEntry.grid(row=5, column=2, columnspan=1, padx=1, pady=1)




# * Label to show the date of the weather data
dateLabel = Label(root, text="Date: ", font=("Calibri", 15))
dateLabel.grid(row=6, column=0, columnspan=1, padx=1, pady=1)
dateLabel.configure(bg="gold", fg="black")

#* Entry to put the weather data in
dateEntry = Entry(root, width=15, borderwidth=5, font=("Calibri", 15), bg="white", fg="black", state="readonly")
dateEntry.grid(row=6, column=2, columnspan=1, padx=1, pady=1)

#* Label to show the time of the weather data
timeLabel = Label(root, text="Your Local Time: ", font=("Calibri", 15))
timeLabel.grid(row=7, column=0, columnspan=1, padx=1, pady=1)
timeLabel.configure(bg="gold", fg="black")

#* Entry to put the time the weather data was collected in
timeEntry = Entry(root, width=15, borderwidth=5, font=("Calibri", 15), bg="white", fg="black", state="readonly")
timeEntry.grid(row=7, column=2, columnspan=1, padx=1, pady=1)

#* Label to show the description of the weather data
descLabel = Label(root, text="Description: ", font=("Calibri", 15))
descLabel.grid(row=8, column=0, columnspan=1, padx=1, pady=1)
descLabel.configure(bg="gold", fg="black")

#* Entry to show the description of the weather data
descEntry = Entry(root, width=15, borderwidth=5, font=("Calibri", 15), bg="white", fg="black", state="readonly")
descEntry.grid(row=8, column=2, columnspan=1, padx=1, pady=1)

#* Label to show the temperature of the weather data
tempLabel = Label(root, text="Temperature: ", font=("Calibri", 15))
tempLabel.grid(row=9, column=0, columnspan=1, padx=1, pady=1)
tempLabel.configure(bg="gold", fg="black")

#* Entry to show the temperature of the weather data
tempEntry = Entry(root, width=15, borderwidth=5, font=("Calibri", 15), bg="white", fg="black", state="readonly")
tempEntry.grid(row=9, column=2, columnspan=1, padx=1, pady=1)


#* Label to show the high temperature of the weather data
highLabel = Label(root, text="Temp High: ", font=("Calibri", 15))
highLabel.grid(row=10, column=0, columnspan=1, padx=1, pady=1)
highLabel.configure(bg="gold", fg="black")
#* Entry to show the high temperature of the weather data
highEntry = Entry(root, width=15, borderwidth=5, font=("Calibri", 15), bg="white", fg="black", state="readonly")
highEntry.grid(row=10, column=2, columnspan=1, padx=1, pady=1)


#* Label to show the low temperature of the weather data
lowLabel = Label(root, text="Low: ", font=("Calibri", 15))
lowLabel.grid(row=11, column=0, columnspan=1, padx=1, pady=1)
lowLabel.configure(bg="gold", fg="black")

#* Entry to show the low temperature of the weather data
lowEntry = Entry(root, width=15, borderwidth=5, font=("Calibri", 15), bg="white", fg="black", state="readonly")
lowEntry.grid(row=11, column=2, columnspan=1, padx=1, pady=1)


#* Label to show the WIND speed and direction of the weather data
windLabel = Label(root, text="Wind: ", font=("Calibri", 15))
windLabel.grid(row=12, column=0, columnspan=1, padx=1, pady=1)
windLabel.configure(bg="gold", fg="black")



#* Entry to show the wind speed and direction of the weather data
windEntry = Entry(root, width=15, borderwidth=5, font=("Calibri", 15), bg="white", fg="black", state="readonly")
windEntry.grid(row=12, column=2, columnspan=1, padx=1, pady=1)

#* Listbox to show the previously searched weather data and the button to get the info

lButton = ttk.Button(root, text="Select from List", command=getOldWeatherList)
lButton.grid(row=13, column=0, columnspan=1, padx=1, pady=1)
lButton.configure(style="TButton")

weatherLBox = Listbox(root, width=30, height=8, borderwidth=5, font=("Calibri", 15), bg="white", fg="black")
weatherLBox.grid(row=14, column=0, columnspan=3, padx=1, pady=1)






root.mainloop()

# We need to make this in a gridd view so that we may have a more
# defined setup of the weather attributes and we can have a potential for a more complex GUI
# We can also add a button that will allow the user to change the location of the weather data
# we should also show the option to access previouslu searched locations
# and weather information from a previous time. 