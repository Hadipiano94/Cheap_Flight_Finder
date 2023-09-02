import requests

# on_going = True
# while on_going:
first_name = input("Hello to Flight-Finder!\nWhat is your First Name?\n").capitalize()
last_name = input("\nWhat is your Last Name?\n").capitalize()
hometown_IATA = input("\nWhat is your hometown's IATA code? -it's a 3 letter uppercase code-\n").upper()
email1 = input("\nPlease write down your E-mail too.\n")
email2 = input("\nfor the confirmation, please write down your E-mail one more time.\n")
while email1 != email2:
    email2 = input("\nYou wrote it differently the 2nd time!\nCan you write it down one more time?\n-if you wrote it wrong at the first place, please refresh the link and start over-\n")
email = email1
# adding new user to trips/users
USERS_ENDPOINT = "https://api.sheety.co/your_url"
USER_PARAMS = {
    "user": {
        "firstName": first_name,
        "lastName": last_name,
        "homeTown": hometown_IATA,
        "email": email,
    }
}
HEADER = {
    "Content-Type": "application/json",
}
try:
    add_user_response = requests.post(url=USERS_ENDPOINT, json=USER_PARAMS, headers=HEADER)
    add_user_response.raise_for_status()
    print("\nEmail successfully added.")
except requests.exceptions.HTTPError:
    print("Unsuccessful!")
    # print(add_user_response.json()["errors"][0]["detail"])

# user_answer = input("Want to add another User? Y/N\n")
# if user_answer.lower() in ["y", "yes", "ye"]:
#     pass
# else:
#     on_going = False
