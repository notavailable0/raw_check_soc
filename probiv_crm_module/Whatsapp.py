import requests
import json

## https://webservice.checkwa.com/ works with its api
## credentials for the site
## qlsx32@mail.ru:Ruttur123

def check_wa(p):
    username = 'theowll'
    apikey = '43fd05-f190cc-0bfed7-26745e-b58da9'
    action = 'check'

    if '+' in p['phone']:
        p['phone'] = str(p['phone'].lstrip('+'))

    cod = p['ccode']
    num = str(p['phone']).lstrip(str(cod))
    print(cod)
    print(num)


    r = requests.get("https://webservice.checkwa.com/", params={"user": username, "apikey": apikey, "action": action,"num": num,"cod": cod})
    print(r.text)
    response = json.loads(r.text)

    if response["code"] == "001":

        return {p['id'] : {'wa': True}}

    elif response["code"] == "002":

        return {p['id'] : {'wa': False}}

    else:
        return {p['id'] : {'wa': False}}

