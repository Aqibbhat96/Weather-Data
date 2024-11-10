#First we import the necessary Packages that we will use i.e. Requests (to get the data from URL) and pandas (to get our data in a data frame format)
import requests
import pandas as pd

#Initialize an empty list to store our data.
data_list = []

# Set the starting datetime for the loop.
start_datetime = pd.to_datetime("2023-01-29 00:00:00")

#Start the first for loop that iterates 52 times (as there are 52 weeks in a year).
for i in range(52):
    #To Calculate the timestamp for an API request.
    x = i * 168 * 3600 + 1675238400
    #API Request to OpenWeatherMap and convert that in JSON format.

    url = f"https://history.openweathermap.org/data/2.5/history/city?lat=19.03793&lon=-98.20346&type=hour&units=metric&start={x}&end=1706774399&appid=7f35c9662b80d4241b38417dd01d19e7"
    response = requests.get(url)
    data = response.json()
    
    #Now 2nd loop is to loop through the entries of the API response.
    for entry in data['list']:
           #Now we extract and format the data in a dictionary form.
           entry_data = {     
                "DT": entry['dt'],
                #Here we convert timestamp to datetime then adjust timezone, and add 1 hour. Then we format it as a string with timezone information.
                "Datetime": (pd.to_datetime(entry['dt'], unit='s', origin='unix', utc=True).tz_convert('America/Mexico_City') + pd.to_timedelta(1, unit='h')).strftime("%Y-%m-%d %H:%M:%S %z") + " UTC",
                #To extract the month from the datetime column.
                "Month": pd.to_datetime(entry['dt'], unit='s', origin='unix', utc=True).tz_convert('America/Mexico_City').month,
                #To extract the year from the datetime column.
                "Year": pd.to_datetime(entry['dt'], unit='s', origin='unix', utc=True).tz_convert('America/Mexico_City').year,
                "Timezone": '-21600',
                "City_Name": "Puebla",
                "Latitude": '19.03793',
                "Longitude": '-98.20346',
                "Temp": entry['main']['temp'],
                "Feels_like": entry['main']['feels_like'],
                "Temp_Min": entry['main']['temp_min'],
                "Temp_Max": entry['main']['temp_max'],
                "Pressure": entry['main']['pressure'],
                "Humidity": entry['main']['humidity'],
                "Wind_Speed": entry['wind']['speed'],
                "Wind_Deg": entry['wind']['deg'],
                "Wind_Gust": entry['wind']['speed'],
                "Clouds_all": entry['clouds']['all'],
                "Weather_Id": entry['weather'][0]['id'],
                "Weaather_main": entry['weather'][0]['main'],
                "Weather_Description": entry['weather'][0]['description'],
                "Weather_icon": entry['weather'][0]['icon']
                    }
          
           # Append the entry data to the list initialized earlier.
           data_list.append(entry_data)
           
#To Create a DataFrame from the list of data
entry_data_df = pd.DataFrame(data_list)

#to convert the months from numerical form to alphabetical.
for i in range(12):
    months_replace = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]
    entry_data_df['Month'] = entry_data_df['Month'].replace(i+1, months_replace[i])
    

#To export the DataFrame into a CSV file.
entry_data_df.to_csv(r"C:\Users\Lenovo\Desktop\Assignments of DANA\Assignment 3\Puebla_Weather_2023.csv", index=False)

