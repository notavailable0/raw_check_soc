from Instagram import check_ig
from Telegram import check_tg
from Whatsapp import check_wa
from facebook import check_fb
from logo_ansii import lgp
from unified_request import create_proxy_dict

import requests
import json

from multiprocessing import Pool

## get numbers for check
## check for all available services
## send back

## resp => list with phone dicts


# TODO rewrite code to normal form
# TODO create a bd or list with sleeping accounts
# TODO create a queue with ready accounts
# TODO check for limits of the networks etc.
# TODO finish exceptions ig osint
# TODO ok
# TODO vk
# TODO fb search by immage??? check this method
# todo3 привести жизнь в порядок.

# time spent: 15h

'''
привет бодь, тут какойто факап случился, вот ты и наверное зашел, чекни пжста перед тем как ебаться с кодом:

    сервис с вацапами оплачен?
    на телеге нет бана?
    чекни руками, можно с дедика сделать запрос на сайт социалкИ?
    го работает стабильно?

    больше подсказать не могу, сори что тратится твоё время...
'''


def main(i):
    output = []
    output1 = {"id" : i['id'], "tg":"", "wa" : "", "ig": "", "fb":""}

    # initiate checker class, if some result for the network => send it in json back


    try:
        # add tg multiakk usage
        tg_check = check_tg([i], "16245835", "3d0cb690c3f6e74236dfd88a2923a9ff")
        output1['tg'] = tg_check[i['id']]['tg']
        #print(output1)
    except Exception as e:
        print(e)
        output1['tg'] = "error"

    try:
        #print(int(i['ccode']))
        wa_check = check_wa(i)
        output1['wa'] = wa_check[i['id']]['wa']

    except Exception as e:
        print(e)

    output1['ig'] = check_ig(i['phone'])['ig']

    output1['fb'] = check_fb("+"+str(i['phone']))

    output.append(dict(output1))

    for i in output:
        print(i)
        # igName
        nid = i['id']
        data = dict({
            "tg": i['tg'],
            "fb": i['fb'],
            "wa": i['wa'],
            "ig": i['ig']
        })
        print(json.dumps(data))
        headers = {"Content-type": "application/json", "Accept" : "application/json", "user-agent" : 'Mozilla/5.0 (X11; Ubuntu; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2820.59 Safari/537.36'}
        r = requests.put(f'http://2187997.hb443171.web.hosting-test.net/mg-validate/{nid}', data = json.dumps(data), headers = headers)
        print(r.text)



def pool_handler(workd):
    p = Pool(10)
    p.map(main, workd)

if __name__ == '__main__':
    lgp()
    create_proxy_dict()
    for i in range(10):
        nl = []
        headers = {"Content-type": "application/json", "Accept" : "application/json", "user-agent" : ''}
        r = requests.get('http://2187997.hb443171.web.hosting-test.net/mg-validate', headers=headers)
        r = json.loads(r.text)
        print(r)

        for i in r:
            nl.append({"id" : i['id'], 'ccode':i['phone_code'], 'ncphone':i['phone_no_code'], 'phone':i['phone']})

        pool_handler(nl)
