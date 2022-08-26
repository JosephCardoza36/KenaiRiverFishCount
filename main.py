import requests
import smtplib
from datetime import datetime, timedelta
import csv


today = datetime.today()
yesterday = today - timedelta(days=1)
yesterday_day = (yesterday.day)

MY_EMAIL = MY_EMAIL
MY_PASSWORD = SECRET
URL = "http://www.adfg.alaska.gov/sf/FishCounts/index.cfm?ADFG=main.displayResults&COUNTLOCATIONID=40&SpeciesID=420"

response = requests.get('https://www.adfg.alaska.gov/sf/FishCounts/index.cfm?ADFG=export.JSON&countLocationID=40&year=2022,2021,2020,2019,2018&speciesID=420')
fish_data = (response.json())



with open("fish_data.csv", "w") as file:
    writer = csv.writer(file)
    header = ["Index","Dates", "Fish Count"]
    writer.writerow(header)


    for n in range(len(fish_data["DATA"])):
        year = fish_data["DATA"][n][1].split(" ")[2]
        month = fish_data["DATA"][n][1].split(" ")[0]
        day = fish_data["DATA"][n][1].split(" ")[1]
        if year == "2022":
            fish_count = int(fish_data["DATA"][n][2])
            dates = (fish_data["DATA"][n][1]).split("00:00:00")
            writer.writerow([n, fish_count, dates[0].strip()])




        if int(fish_count) > 9000 and int(day) == int(yesterday_day):
            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                result = connection.login(user=MY_EMAIL, password=MY_PASSWORD)
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=MY_EMAIL,
                    msg=f"Subject: GO FISHING\n\nKenai Fish Count: {fish_count} | Date: {month} {day}\n\n{URL}")




