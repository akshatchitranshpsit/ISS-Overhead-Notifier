import requests
from datetime import datetime
import time

MY_LAT = float(input('Enter your latitude:'))
MY_LONG =float(input("Enter your longitude:"))


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Check if both lat and long are within +/- 5 degrees
    if (iss_latitude - 5 <= MY_LAT <= iss_latitude + 5) and \
            (iss_longitude - 5 <= MY_LONG <= iss_longitude + 5):
        return True
    return False


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()

    # Parse UTC times
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()

    # Simple UTC hour comparison (Note: For precise local time, use pytz or dateutil)
    if time_now.hour >= sunset or time_now.hour < sunrise:
        return True
    return False


# Main Loop
while True:
    if is_iss_overhead() and is_night():
        print("ISS Is Overhead - Look Up!")
        # Add email sending code here
    else:
        print("ISS Is Not Overhead")

    time.sleep(60)