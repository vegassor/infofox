import random
import string
import requests
import csv
from datetime import datetime


class AuthError(Exception):
    def __str__(self):
        return 'Bad login or password'


def get_token(username, password, host='coolstorybob.pythonanywhere.com'):
    r_login = requests.post(f'http://{host}/auth/token/login', {'username': username, 'password': password})
    
    if r_login.status_code == 200:
        return r_login.json().get('auth_token')


def generate_bracelets(token, amount=1, host='coolstorybob.pythonanywhere.com'):
    create_url = f'http://{host}/api/userpage/bracelet/add/'  
    saved_codes = []
    headers = {'Authorization': f'Token {token}'}
    
    print(f'Requests to {create_url}')
    print('{: ^4}|{: ^8}|{: ^15}'.format('№','id', 'unique_code'))
    print('{:-^27}'.format(''))
    
    for i in range(1, amount+1):
        generated_code = ''.join(
            random.SystemRandom().choice(string.ascii_lowercase + string.digits) 
            for _ in range(8)
        )
        body = {'unique_code': generated_code}
        r = requests.post(create_url, body, headers=headers)
        
        if r.status_code == 201:
            b_id = r.json().get('bracelet_id')
            print('{: ^4}|{: ^8}|{: ^15}'.format(i, b_id, generated_code))
            saved_codes.append((b_id, generated_code))
    
    return saved_codes


def generate_bracelets_on_server(token, amount=1, host='coolstorybob.pythonanywhere.com'):
    create_url = f'http://{host}/api/userpage/bracelet/add/many/'  
    headers = {'Authorization': f'Token {token}'}
    body = {'amount': amount}
    saved_codes = []
    r = requests.post(create_url, body, headers=headers)
    
    if r.status_code == 201:
        bracelets = r.json().get('bracelets')
        for b in bracelets:
            saved_codes.append((b.get('bracelet_id'), b.get('unique_code')))
        return saved_codes

    
    
if __name__ == '__main__':
    try:
        token = get_token('one', 'pasphrase', 'localhost:8000')
        if not token:
            raise AuthError
        # b = generate_bracelets(token, 10, 'localhost:8000')
        b = generate_bracelets_on_server(token, 5, 'localhost:8000')
        
        filename = f'Партия браслетов от {datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv'
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            for bracelet in b:
                url = f'http://coolstorybob.herokuapp.com/bracelet/{bracelet[0]}'
                writer.writerow([bracelet[0], bracelet[1], url])
    except AuthError as e:
        print(e)