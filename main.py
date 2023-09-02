import requests
import smtplib
from datetime import datetime, timedelta


def make_msg(flight_list):

    subject = "Deal Flights waiting for YOU!"
    message_text = "List of Cheap Flights:\n\n\n"
    for fly in flight_list:
        message_text += f"-{fly['from_city']}-{fly['from_airport']} to {fly['to_city']}-{fly['to_airport']} on {fly['date']} at {fly['time']}. flight No.{fly['flight_number']}, {fly['available_seats']} seats available. €{fly['price']}\n\n"
    msg_text = f"Subject:{subject}\n\n{message_text}"
    return msg_text


my_gmail = "your email"
gmail_connection = "smtp.gmail.com"
app_password = "your app pass"

TODAY = datetime.now().date()
DATE_TO = TODAY + timedelta(days=30)
date_from = TODAY.strftime("%d/%m/%Y")
date_to = DATE_TO.strftime("%d/%m/%Y")

"""Getting Users List"""

USERS_ENDPOINT = "https://api.sheety.co/your_url"
users_response = requests.get(url=USERS_ENDPOINT)
# print(users_response.json()["users"])
users = [{"name": user["firstName"].capitalize(),
          "hometown_IATA": user["homeTown"].upper(),
          "email": user["email"],
          # "time": int(user["preferredTime"]),
          } for user in users_response.json()["users"]]
# print(users)

"""Searching for their Trips"""

for user in users:

    TRIPS_ENDPOINT = "https://api.sheety.co/your_url"
    trips_response = requests.get(url=TRIPS_ENDPOINT)
    destinations_text = ""
    for city in trips_response.json()["cities"]:
        destinations_text += f"{city['iataCode']},"
    destinations_text = destinations_text.strip(",")
    # print(destinations_text)

    # destinations_text = "PAR,NYC,IST"

    # trips = [{"from": user["hometown_IATA"],
    #           "to": city["iataCode"],
    #           "price_limit": city["lowestPrice"],
    #           "currency": city["currency"],
    #           } for city in trips_response.json()["cities"]]
    # print(trips)

    # trips = [{'from': 'IZM', 'to': 'PAR', 'price_limit': 1000, 'currency': 'EUR'}, {'from': 'IZM', 'to': 'NYC', 'price_limit': 10000, 'currency': 'USD'}, {'from': 'IZM', 'to': 'IST', 'price_limit': 500, 'currency': 'TRY'}]

    KIWI_ENDPOINT = "https://api.tequila.kiwi.com/v2/search"
    TEQUILA_ID = "your tequila id"
    TEQUILA_KEY = "your key"

    # for city in trips:

    KIWI_PARAMS = {
        "fly_from": user["hometown_IATA"],
        "fly_to": destinations_text,
        "date_from": date_from,
        "date_to": date_to,
        # "price_to": city["price_limit"],
        "flight_type": "oneway",
        "one_for_city": 1,
        "max_stopovers": 0,
        "sort": "price",
    }
    HEADERS = {
        "apikey": TEQUILA_KEY,
        "accept": "application/json",
    }

    kiwi_response = requests.get(url=KIWI_ENDPOINT, params=KIWI_PARAMS, headers=HEADERS)
    flights = kiwi_response.json()["data"]
    flights_list = []
    for flight in flights:
        flights_list.append({
            "price": flight["price"],
            "from_airport": flight["flyFrom"],
            "to_airport": flight["flyTo"],
            "from_city": flight["cityFrom"],
            "to_city": flight["cityTo"],
            "date": flight["route"][0]["local_departure"].split(sep="T")[0],
            "time": flight["route"][0]["local_departure"].split(sep="T")[1].split(".")[0],
            "flight_number": flight["route"][0]["flight_no"],
            "available_seats": flight["availability"]["seats"],
        }
        )

    msg = make_msg(flights_list).encode("utf-8")
    # print(msg)
    with smtplib.SMTP(gmail_connection) as connection:
        connection.starttls()
        connection.login(user=my_gmail, password=app_password)
        connection.sendmail(from_addr=my_gmail, to_addrs=user["email"], msg=msg)
        # print("Email sent!")
