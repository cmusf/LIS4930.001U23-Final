import requests
import argparse
import prettytable

# Parse arguments
parser = argparse.ArgumentParser(description='Weather forecast')

# Allow the user to choose a location to forecast
parser.add_argument('-l', '--location', type=str, default='', help='Location to forecast')

args = parser.parse_args()


location = ''
isLatLong = False

if args.location != '':
    location = args.location
else:
    # Get the user's location
    url = 'http://ipinfo.io/json'
    response = requests.get(url)
    data = response.json()

    # Check if we have loc, if not use data['city']
    if 'loc' in data:
        location = data['loc']
        isLatLong = True
    else:
        location = data['city']

    # Print the location
    print("I've detected your location as being near: " + location)

class Weather:
    # Create a weather class for each weather value
    def __init__(self, time, weather, temp, humidity):
        self.time = time
        self.weather = weather
        self.temp = temp
        self.humidity = humidity

    def __str__(self):
        return self.time + ' ' + self.weather + ' ' + self.temp + ' ' + self.humidity
    
def getWeatherAt(loc, isLatLong):
    # Get the weather data
    if isLatLong:
        lat, long = location.split(',')
        url = f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={long}&mode=json&appid=41b66b0cf23f1f570ecd4ff4ad171c10&units=imperial'
    else:
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={location}&mode=json&appid=41b66b0cf23f1f570ecd4ff4ad171c10&units=imperial'
    response = requests.get(url)
    data = response.json()


    # Create a list of weather objects
    weatherList = []
    for item in data['list']:
        weatherList.append(Weather(item['dt_txt'], item['weather'][0]['description'], str(item['main']['temp']) + '°F', item['main']['humidity']))

    # Format the data into a table
    table = prettytable.PrettyTable(['Time', 'Weather', 'Temperature', 'Humidity'])

    for item in weatherList:
        table.add_row([item.time, item.weather, item.temp, item.humidity])

    print(table)

    # Write to weather_report.txt
    with open('weather_report.txt', 'w') as file:
        file.write(str(table))
        file.close()


getWeatherAt(location, isLatLong)
