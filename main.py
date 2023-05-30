from bs4 import BeautifulSoup
import requests
# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
import datetime  
now = datetime.datetime.now()  

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
#account_sid = 'MG07a5b06e7cd9a774b5e6bbfe6a2eaf6c'
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

def time_greater_than_4(time):
    print(time[:1])
    if time.endswith("pm") and int(time[:1]) > 4:
        return True
    else:
        return False

# class_level = 'Level 5 (ages 6-10)'
class_level = 'Level 1 (ages 3-5)'
today = '2023-03-28'
url = "https://app.jackrabbitclass.com/jr3.0/Openings/OpeningsJS?OrgID=531495&Loc=SF&showcols=Cat1&hidecols=tuition,description,session,StartDate,EndDate,ages,gender,class&sort=days,StartTime&closed=full&style=color:blue"
print(f"Fetching data from {url} for {now}.")
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
table_rows = soup.table.find_all('tr')
print(f"Fetched {len(table_rows) - 1} rows.")
l = []
cols = [a.string for a in soup.table.tr.find_all('th')]
print(cols)
for tr in table_rows:
    th = tr.find_all('th')
    td = tr.find_all('td')
    header = [tr.text.strip() for tr in th]
    if header[0] == class_level:
        print("header: ",header[0])
        row = [tr.text.strip() for tr in td]
        print("row: ",row)
        class_day = row[0]
        start_time = row[1].split("-")
        after_4 = time_greater_than_4(start_time[0])
        print("Petite Baleen class starts at: ",start_time[0])
        weekdays = ['Mon','Tue','Wed','Thu','Fri']
        weekend = ['Sat','Sun']
        if after_4 == True and class_day in weekdays:
            print("BINGOOOOOOOO")
            print(after_4)
            twilio_body=f"Petite Baleen spot is OPEN on {row[0]} at {row[1]}"
            print(twilio_body)
            phone_numbers = ['']
            message = client.messages \
                .create(
                    body=twilio_body,
                    messaging_service_sid='MG07a5b06e7cd9a774b5e6bbfe6a2eaf6c',
                    # from_='+18885221227',
                    to=phone_numbers
                )
        elif class_day in weekend:
            print("Weekend Class WOOT")
            twilio_body=f"Petite Baleen spot is OPEN on {row[0]} at {row[1]}"
            print(twilio_body)
            phone_numbers = []
            message = client.messages \
                .create(
                    body=twilio_body,
                    messaging_service_sid='MG07a5b06e7cd9a774b5e6bbfe6a2eaf6c',
                    to=phone_numbers
                )
        else:
            print("everything is too early 😭")
