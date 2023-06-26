import time
import requests
import json

api_key = 'REPLACE_WITH_API_KEY'
headers = {'Accept': 'application/json'}
auth = (api_key, 'random_text_here')
params = {'where': 'active=true'}

response = requests.get('https://app.paymoapp.com/api/users', headers=headers, auth=auth, params=params)

ignore_list = ['Admin', 'Ops Team', 'Admin Team', 'External Freelance'] # replace with custom ignore list depending on requirements
output = []

if response.status_code == 200:
    start_time = time.time()
    users = response.json()['users']
    for user in users:
        if user['name'] in ignore_list or 'REPLACE_WITH_EMAIL_AFTER_@' not in user['email']:
            continue
        output.append(user['name'])
        if 'REPLACE_WITH_USER_EMAIL' in user['email']:
            print(json.dumps(user, indent=4))
        for project in user['assigned_projects']:
            project_response = requests.get(f'https://app.paymoapp.com/api/projects/{project}', headers=headers, auth=auth, params=params)
            if project_response.status_code == 200:
                projects = project_response.json()['projects']
                for project in projects:
                    print(project['name'])
            else:
                print(f"API access failed with status code {project_response.status_code}")
        
            time.sleep(3)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")