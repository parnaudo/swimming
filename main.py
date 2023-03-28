from bs4 import BeautifulSoup
import requests
# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

def time_greater_than_4(time):
    print(time[:1])
    if time.endswith("pm") and int(time[:1]) > 4:
        return True
    else:
        return False


today = '2023-03-28'
url = "https://app.jackrabbitclass.com/jr3.0/Openings/OpeningsJS?OrgID=531495&Loc=SF&showcols=Cat1&hidecols=tuition,description,session,StartDate,EndDate,ages,gender,class&sort=days,StartTime&closed=full&style=color:blue"
print(f"Fetching data from {url} for {today}.")
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
table_rows = soup.table.find_all('tr')
print(f"Fetched {len(table_rows) - 1} rows.")
l = []
cols = [a.string for a in soup.table.tr.find_all('th')]
print(cols)
for tr in table_rows:
    # print(tr)
    th = tr.find_all('th')
    # print(th)
    td = tr.find_all('td')
    # print(td)
    # print("NEWLINE")
    header = [tr.text.strip() for tr in th]
    if header[0] == 'Level 1 (ages 3-5)':
        print("header: ",header[0])
        row = [tr.text.strip() for tr in td]
        print("row: ",row[1])
        start_time = row[1].split("-")
        after_4 = time_greater_than_4(start_time[0])
        print(start_time)
        if after_4 == True:
            print("BINGOOOOOOOO")
            print(after_4)
            twilio_body=f"Petite Baleen spot is OPEN at {':'.join(row)}"
            # <a href='https://www.swimlpb.com/locations/san-francisco'>click here</a>
            print(twilio_body)
            phone_numbers = ['+15712127641','+18583426154']
            message = client.messages \
                .create(
                    body=twilio_body,
                    from_='+18885221227',
                    to=phone_numbers
                )

# print(message)
    # # print(row)

    # print("header: ",header[0])
    # # if(header)
    # row = [tr.text.strip() for tr in td]
    # print("row: ",row)
#     l.append(row)
# df = pd.DataFrame(l, columns=cols)
# print(f'Pre-process df size: {df.shape}')
