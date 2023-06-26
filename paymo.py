import calendar
import datetime
import time
import requests

api_key = 'REPLACE_WITH_API_KEY'
headers = {'Accept': 'application/json'}
auth = (api_key, 'random_text_here')
params = {'where': 'active=true'}


user_response = requests.get('https://app.paymoapp.com/api/users', headers=headers, auth=auth, params=params)

ignore_list = ['Admin', 'Ops Team', 'Admin Team', 'External Freelance'] # replace with custom ignore list depending on requirements

names = []
ids = []
output = []

if user_response.status_code == 200:
    for user in user_response.json()['users']:
        if user['name'] in ignore_list or 'REPLACE_WITH_EMAIL_AFTER_@' not in user['email']:
            continue
        names.append(user['name'])

        temp_id = {'name': user['name'], 'id': user['id']}
        ids.append(temp_id)

        for project in user['assigned_projects']:
            worked = {'name': user['name'], 'projects': project}
            output.append(worked)

else:
    print(f"API access failed with status code {user_response.status_code}")

# Get current month
now = datetime.datetime.now()
start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%dT%H:%M:%SZ')
last_day = calendar.monthrange(now.year, now.month)[1]
end_date = now.replace(day=last_day, hour=23, minute=59, second=59, microsecond=0).strftime('%Y-%m-%dT%H:%M:%SZ')

time_interval = f"{start_date},{end_date}"

for user in ids:
    params = {'where': f'user_id={user["id"]} and time_interval in ("{start_date}","{end_date}")'}
    time_entries_response = requests.get('https://app.paymoapp.com/api/entries', headers=headers, auth=auth, params=params)

    if time_entries_response.status_code == 200:
        total = 0
        time_entries = time_entries_response.json()['entries']
        
        for entry in time_entries:
            total += entry['duration']

    total_minutes = total // 60
    total_hours = total_minutes // 60
    remaining_minutes = total_minutes % 60
    print (f"{user['name']}: {total_hours} hours, {remaining_minutes} minutes")

    time.sleep(3)

else: 
    print(f"API access failed with status code {time_entries_response.status_code}")