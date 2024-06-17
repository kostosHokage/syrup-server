from twikit import Client
import json
import time
from datetime import datetime
import httpx
import os

accounts = [
    {
        'USERNAME': 'analaurafuhr',
        'EMAIL': 'crieroui@tenermail.com',
        'PASSWORD': 'h1jolg6c5lmj',
        'proxy': 'http://d6j8mS7EPtIciNYTFWk0:RNW78Fm5@185.162.130.85:10000'
    },
    {
        'USERNAME': 'sachnila',
        'EMAIL': 'akcbuqpm@fmailler.com',
        'PASSWORD': 'lo1578j91po9',
        'proxy': 'http://d6j8mS7EPtIciNYTFWk0:RNW78Fm5@185.162.130.85:10001'
    },
    {
        'USERNAME': 'zilionaritf',
        'EMAIL': 'abnyvrms@tenermail.com',
        'PASSWORD': 'ifichd8iijgp',
        'proxy': 'http://d6j8mS7EPtIciNYTFWk0:RNW78Fm5@185.162.130.85:10002'
    },
    {
        'USERNAME': 'CruzDcruz2x',
        'EMAIL': 'pyqjyjqz@fmailler.com',
        'PASSWORD': 'fl9bdeghn65f',
        'proxy': 'http://d6j8mS7EPtIciNYTFWk0:RNW78Fm5@185.162.130.85:10003'
    },
    {
        'USERNAME': 'zakie2xhjj',
        'EMAIL': 'briaaclc@tenermail.com',
        'PASSWORD': 'adnhmcagd2h5',
        'proxy': 'http://d6j8mS7EPtIciNYTFWk0:RNW78Fm5@185.162.130.85:10004'
    },
]

def authorize_client(account):
    client = Client('en-US', proxy=account['proxy'])
    client.login(
        auth_info_1=account['USERNAME'],
        auth_info_2=account['EMAIL'],
        password=account['PASSWORD']
    )
    return client

# Используем httpx для выполнения HTTP-запроса
def get_usernames():
    url = 'https://1a3f4278e6da.vps.myjino.ru/api/usernames'
    response = httpx.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Не удалось получить usernames с сервера")

usernames = get_usernames()

# Загружаем инициалы пользователей из accounts.json
user_initials = {}
accounts_file_path = 'accounts.json'
if os.path.exists(accounts_file_path):
    accounts_data = json.load(open(accounts_file_path, 'r'))
    for account in accounts_data:
        for username in account['usernames']:
            user_initials[username] = account['userInitial']

current_account_index = 0
client = authorize_client(accounts[current_account_index])
all_user_data = []
request_count = 0
request_limit = 95
reset_time = 15 * 60

for USER_SCREEN_NAME in usernames:
    while True:
        try:
            if request_count >= request_limit:
                print("Достигнут лимит запросов, переключение на другой аккаунт...")
                current_account_index = (current_account_index + 1) % len(accounts)
                client = authorize_client(accounts[current_account_index])
                request_count = 0

            user = client.get_user_by_screen_name(USER_SCREEN_NAME)
            request_count += 1

            user_data = {
                'screen_name': USER_SCREEN_NAME,
                'id': user.id,
                'name': user.name,
                'followers': user.followers_count,
                'following_count': user.following_count,
                'verified': user.verified,
                'created_at': user.created_at,
                'location': user.location,
                'userInitial': user_initials.get(USER_SCREEN_NAME, '')
            }

            all_user_data.append(user_data)
            time.sleep(1)
            break
        except Exception as e:
            print(f"Ошибка получения данных для {USER_SCREEN_NAME}: {e}")

            if '429' in str(e):
                print("Достигнут лимит запросов, переключение на другой аккаунт...")
                current_account_index = (current_account_index + 1) % len(accounts)
                client = authorize_client(accounts[current_account_index])
                request_count = 0
            else:
                user_data = {
                    'screen_name': USER_SCREEN_NAME,
                    'id': '-',
                    'name': '-',
                    'followers': '-',
                    'following_count': '-',
                    'verified': '-',
                    'created_at': '-',
                    'location': '-',
                    'userInitial': user_initials.get(USER_SCREEN_NAME, '')
                }

                all_user_data.append(user_data)
                break

output_path = 'all_user_data.json'
with open(output_path, 'w') as json_file:
    json.dump(all_user_data, json_file, indent=4)

current_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
log_json_path = 'log.json'
date_update = {'dateUpdate': current_time_str}
with open(log_json_path, 'w') as json_log_file:
    json.dump(date_update, json_log_file, indent=4)

print("Данные были записаны в файл all_user_data.json")
print(f"Время последнего запуска записано в файл log.json")
