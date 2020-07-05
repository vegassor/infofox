import sys
import getpass
import random
import string
import requests
import csv
from datetime import datetime


class AuthError(Exception):
    def __str__(self):
        return 'Bad login or password'

class ArgvError(Exception):
    def __str__(self):
        return 'Bad parameters passed'


def get_token(username, password, host='coolstorybob.pythonanywhere.com'):
    r_login = requests.post(f'http://{host}/auth/token/login', {'username': username, 'password': password})
    
    if r_login.status_code == 200:
        return r_login.json().get('auth_token')

def is_superuser(token, host='coolstorybob.pythonanywhere.com'):
    r = requests.get(f'http://{host}/auth/is_superuser/', headers={"Authorization": "Token "+token})
    return r.json().get('is_superuser')

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
        username = 'one'
        password = 'passphrase'
        amount = 10
        if len(sys.argv) == 1:
            username = input('Username: ')
            password = getpass.getpass(prompt='Password: ')
            amount = int(input('Amount of bracelets you want to create: '))
        elif len(sys.argv) == 2:          
            if sys.argv[1] != '-s':
                raise ArgvError
            resp = input('Amount of bracelets you want to create (10 is default): ')
            if resp != '':
                amount = int(resp)
        else:
            raise ArgvError
        try:
            host = 'coolstorybob.pythonanywhere.com'
            token = get_token(username, password, host)
            
            if not token or not is_superuser(token, host):
                raise AuthError
                
            # b = generate_bracelets(token, 10, host)
            b = generate_bracelets_on_server(token, amount, host)
            filename = f'Партия браслетов от {datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.csv'
            
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f, delimiter=';')
                for bracelet in b:
                    print(bracelet[0])
                    url = f'http://coolstorybob.herokuapp.com/bracelet?id={bracelet[0]}'
                    writer.writerow([bracelet[0], bracelet[1], url])
        except AuthError as e:
            print(e)
    except (ArgvError, ValueError):
        print('Bad parameters passed')