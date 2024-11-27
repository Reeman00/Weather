import urllib.request
import urllib.parse
import json
from django.shortcuts import render

def index(request):
    """
    Handle GET and POST requests for the weather app.
    If the method is POST, fetch weather data from the OpenWeatherMap API
    for the city provided by the user.
    """
    data = {}  # Initialize an empty dictionary to hold weather data or errors

    if request.method == 'POST':
        # Retrieve the city name from the form submission
        city = request.POST.get('city', '').strip()

        # Validate that the city name is not empty
        if not city:
            data['error'] = "City name cannot be empty. Please enter a valid city."
        else:
            try:
                # Encode the city name for safe use in the URL
                city_encoded = urllib.parse.quote(city)
                
                # Construct the API URL with the encoded city name and your API key
                api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city_encoded}&units=metric&appid=dc4e8b7be14b3b54feafb6e2577503f0'

                # Fetch data from the OpenWeatherMap API
                source = urllib.request.urlopen(api_url).read()

                # Load the JSON response into a Python dictionary
                list_of_data = json.loads(source)

                # Check if the API returned an error code (e.g., city not found)
                if list_of_data.get('cod') != 200:
                    data['error'] = list_of_data.get('message', 'City not found. Please check your input.')
                else:
                    # Extract weather data and populate the `data` dictionary
                    data = {
                        "city": city,
                        "country_code": str(list_of_data['sys']['country']),
                        "coordinate": f"{list_of_data['coord']['lon']}, {list_of_data['coord']['lat']}",
                        "temp": f"{list_of_data['main']['temp']} °C",
                        "pressure": str(list_of_data['main']['pressure']),
                        "humidity": str(list_of_data['main']['humidity']),
                        "main": str(list_of_data['weather'][0]['main']),
                        "description": str(list_of_data['weather'][0]['description']),
                        "icon": list_of_data['weather'][0]['icon'],
                    }
            except urllib.error.URLError as e:
                # Handle network-related errors
                data['error'] = "Unable to connect to the weather service. Please check your network connection."
                print(f"Network error: {e}")
            except json.JSONDecodeError as e:
                # Handle errors decoding the JSON response
                data['error'] = "Error processing the weather data. Please try again later."
                print(f"JSON error: {e}")
            except Exception as e:
                # Catch-all for any unexpected errors
                data['error'] = "An unexpected error occurred. Please try again later."
                print(f"Unexpected error: {e}")

    # Render the `index.html` template with the weather data or errors
    return render(request, "main/index.html", {"data": data})
