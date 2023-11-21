from bs4 import BeautifulSoup
import requests
# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
import datetime  
import time
import json
import redis
red = redis.Redis(host='localhost', port=6379, decode_responses=True)

with open('clients.json', 'r') as f:
    clients_dict = json.load(f)

now = datetime.datetime.now()  

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
#account_sid = 'MG07a5b06e7cd9a774b5e6bbfe6a2eaf6c'
auth_token = os.environ['TWILIO_AUTH_TOKEN']
messaging_service_sid='MG07a5b06e7cd9a774b5e6bbfe6a2eaf6c'
client = Client(account_sid, auth_token)

def time_greater_than_4(time):
    print(time[:1])
    if time.endswith("pm") and int(time[:1]) >= 4 and int(time[:1]) <= 7:
        return True
    else:
        return False

def convert_str_to_24hr(time):
    time_dt = datetime.datetime.strptime(time, '%I:%M%p')
    return int(time_dt.strftime("%H"))


def send_twilio_sms(row: list, phone_numbers: list, messaging_service_sid: str, name: str):
    twilio_body=f"Hi {name}, Petite Baleen spot is OPEN on {row[0]} at {row[1]}"
    print(twilio_body)
    if bool(phone_numbers) is True:
        for number in phone_numbers:
            # message = client.messages \
            #     .create(
            #         body=twilio_body,
            #         messaging_service_sid=messaging_service_sid,
            #         # from_='+18885221227',
            #         to=number
            #     )
            print(twilio_body)
            time.sleep(1)
    else:
        print("No numbers to text")    

        # if message.error_code is not None:
        # print(message.error_code)
        # print(message.error_message)

 
url = "https://app.jackrabbitclass.com/jr3.0/Openings/OpeningsJS?OrgID=531495&Loc=SF&showcols=Cat1&hidecols=tuition,description,session,StartDate,EndDate,ages,gender,class&sort=days,StartTime&closed=full&style=color:blue"
print(f"Fetching data from {url} for {now}.")
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
table_rows = soup.table.find_all('tr')
print(f"Fetched {len(table_rows) - 1} rows.")
l = []
cols = [a.string for a in soup.table.tr.find_all('th')]
print(cols)
for name, config in clients_dict.items():
    print(name)
    print(config['weekday_start_hour'])
    for tr in table_rows:
        th = tr.find_all('th')
        td = tr.find_all('td')
        header = [tr.text.strip() for tr in th]
        if header[0] in config['class_level']:
            print("header: ",header[0])
            row = [tr.text.strip() for tr in td]
            print("row: ",row)
            class_day = row[0]
            start_time = row[1].split("-")
            hour_24 = convert_str_to_24hr(start_time[0])
            alert_key = f"{class_day}-{hour_24}-{name}"
            
            if red.exists(alert_key) == False and config['weekday_start_hour'] is not None and config['weekday_end_hour'] is not None and class_day in config['weekdays']:
                print(f"Weekday Eval! {config['weekday_start_hour']} <= {hour_24} <= {config['weekday_end_hour']}")
                if (hour_24 >= config['weekday_start_hour'] and hour_24 <= config['weekday_end_hour']) and class_day in config['weekdays']:
                    print("BING0 Weekday class")
                    print(alert_key)
                    red.set(alert_key,1)
                    send_twilio_sms(row, config['phone_numbers'], messaging_service_sid,name)
            elif red.exists(alert_key) == False and config['weekend_start_hour'] is not None and config['weekend_end_hour'] is not None and class_day in config['weekend_days']:
                print(f"EOW Eval! {config['weekend_start_hour']} <= {hour_24} <= {config['weekend_end_hour']}")
                if (hour_24 >= config['weekend_start_hour'] and hour_24 <= config['weekend_end_hour']) and class_day in config['weekend_days']:
                    print("W00T Weekend Class")
                    print(alert_key)
                    red.set(alert_key,1)
                    send_twilio_sms(row, config['phone_numbers'], messaging_service_sid,name)
            else:
                print("none/nada/zilch matches our params")   
