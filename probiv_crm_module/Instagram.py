import hashlib
import hmac
import json
import random
import urllib
import urllib.parse
import sys
import time
import requests
import inspect

import uuid as uuid
from bs4 import BeautifulSoup

from strg_res import headers_ig, ua_l
from unified_request import send_request
from loglog import logging

# Todo osint
# todo overwrite strg_res
# ToDo1 sort the exceptions stuff


class Instagram():
    # init
    def __init__(self, data):
        self.API_URL = 'https://i.instagram.com/api/v1/'
        self.USERS_LOOKUP_URL = self.API_URL + 'users/lookup/'
        self.SIG_KEY_VERSION = '4'
        self.IG_SIG_KEY = 'e6358aeede676184b9fe702b30f4fd35e71744605e39d2181a34cede076b3c33'

        #todo fetch credentials from data
        self.accounts_to_check = []
        self.current_sessionid = None

        #todo delete to normal
        #r = self.check_ig(data['phone'])
        r = True

        if r == None:
            logging(f'{inspect.currentframe().f_code.co_name} : something went wrong FUCK THIS SHOULD NOT BE HERE FUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCK : {name};{email};{phone}')
            return

        if r == True:
            sess = '46012304898%3Ai9RU23yn9HjWFb%3A21'
            name = 'Artjom Kozlov'
            email = 'asdfasdfasdfasdfa95@gmail.com'
            phone = ''

            self.dumpor('Artjom Kozlov')
            for i in range(10):
                data = self.osint_ig(sess, name, email, phone)


            if data['data'] == None:
                return {'ig':True, 'data':'error'}

            if data['ig'] == True:
                return {
                'ig':True,
                'username':data['data']['user']['username'],
                'all_data':data['data']}

        elif r == False:
            return {'ig':False}

        elif r == None:
            logging(f'{inspect.currentframe().f_code.co_name} : something went wrong FUCK THIS SHOULD NOT BE HERE FUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCK : {name};{email};{phone}')
            return {'ig': 'error'}


    def osint_ig(self, sessionId, name, email, phone):

        self.current_sessionid = sessionId
        print(self.accounts_to_check)
        if self.accounts_to_check == None:
            return logging(f'{inspect.currentframe().f_code.co_name} : no acc to check return none : {name};{email};{phone}')
        else:

            for account in self.accounts_to_check:
                print(account)
                infos = self.getInfo(account[1:])
                print(json.dumps(infos, indent=4, sort_keys=True))

                if infos["user"] == None:
                    print(infos["error"])
                    logging(f'{inspect.currentframe().f_code.co_name} : {infos["error"]} : {name};{email};{phone}')

                else:
                    other_infos = self.advanced_lookup(account[1:])
                    print(json.dumps(other_infos, indent=4, sort_keys=True))


                    if other_infos['user'] == None:
                        logging(f'{inspect.currentframe().f_code.co_name} : no other_infos : {name};{email};{phone}')

                    elif 'obfuscated_email' in other_infos['user'].keys():
                        if other_infos['user']['obfuscated_email'].split('@')[0][0] + other_infos['user']['obfuscated_email'].split('@')[0][-1] == email.split('@')[0][0]+email.split('@')[0][-1]:
                            return {"ig": True, 'data': other_infos}

                    elif other_infos["error"] == "rate limit":
                        logging(f'{inspect.currentframe().f_code.co_name} : rate limit : {name};{email};{phone}')

                    elif 'obfuscated_phone' in other_infos['user'].keys():
                        if other_infos['user']['obfuscated_phone'][-1]+other_infos['user']['obfuscated_phone'][-2] == phone[-1]+phone[-2]:
                            return {"ig": True, 'data': other_infos}

                    elif other_infos['user']['status'] == "fail":
                        logging(f'{inspect.currentframe().f_code.co_name} : other infos fail  : {name};{email};{phone}')
                        return {"ig": True, 'data': None}

        return {"ig": False, 'data': None}

    def advanced_lookup(self, username):

        def generate_signature(data):
            return 'ig_sig_key_version=' + self.SIG_KEY_VERSION + '&signed_body=' + hmac.new(self.IG_SIG_KEY.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest() + '.' + urllib.parse.quote_plus(data)

        def generate_data(phone_number_raw):
            data = {'login_attempt_count': '0',
                    'directly_sign_in': 'true',
                    'source': 'default',
                    'q': phone_number_raw,
                    'ig_sig_key_version': self.SIG_KEY_VERSION
                    }
            return data

        data = generate_signature(json.dumps(generate_data(username)))
        headers = {
            "Accept-Language": "en-US",
            "User-Agent": "Instagram 101.0.0.15.120",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept-Encoding": "gzip, deflate",
            "X-FB-HTTP-Engine": "Liger",
            "Connection": "close"}
        try:
            r = send_request('post', self.USERS_LOOKUP_URL, headers, data=data)
            print(r)
            return({"user": json.loads(r), "error": None})
        except Exception as e:
            print(e)
            return({"user": None, "error": "rate limit"})


    def check_ig(self, phone_number):
            current_session = self.setup_session()
            data = self.generate_data(phone_number)

            response = current_session.post(self.USERS_LOOKUP_URL, data=self.generate_signature(json.dumps(data)))
            print(response.text)
            if response.ok:
                return True
            elif response.status_code == 404:
                return False
            else:
                return None

    # generating uuid
    def generate_uuid(type):
        gen_uuid = str(uuid.uuid4())
        return gen_uuid if type else gen_uuid.replace('-', '')


    def generate_device_id():
        return str(uuid.uuid4()).replace('-', '')[:16]


    def generate_signature(self, data):
        return 'ig_sig_key_version=' + self.SIG_KEY_VERSION + '&signed_body=' + hmac.new(self.IG_SIG_KEY.encode('utf-8'),
                                                                                    data.encode('utf-8'),
                                                                                    hashlib.sha256).hexdigest() + '.' \
               + urllib.parse.quote_plus(data)


    def generate_headers(self):
        # This is very basic headers and is literally copy pasted from burp.
        hdrs = dict(headers_ig)['User-Agent'] = self.generate_user_agent()
        return hdrs


    def generate_user_agent(self):

        return random.choice(ua_l)

    def setup_session(self):
        if self.session == None:


            return self.session

        else:
            return self.session

    def generate_data(self, phone_number_raw):
            data = {'phone_id': self.generate_uuid(True),
                    'guid': self.generate_uuid(True),
                    'device_id': self.generate_device_id(),
                    'login_attempt_count': '0',
                    'directly_sign_in': 'true',
                    'source': 'default',
                    'q': phone_number_raw,
                    'ig_sig_key_version': self.SIG_KEY_VERSION
                    }
            return data

    def dumpor(self, name):
        url = "https://dumpor.com/search?query="
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        req = url + name.replace(" ", "+")

        try:
            accounts = []
            r = send_request('get', req, headers)

            #response = requests.get(req, headers=headers, proxies=proxyDict)
            #print(response.text)

            soup = BeautifulSoup(r, 'html.parser')
            accounts = soup.findAll('a', {"class": "profile-name-link"})
            for account in accounts:
                self.accounts_to_check.append(account.text)
            return({"user": self.accounts_to_check, "error": None})
        except Exception as e:
            print(e)
            return({"user": None, "error": "rate limit"})

    def getInfo(self, username):
        userId = self.getUserId(username)
        if userId["error"] != None:
            return({"user": None, "error": "User not found or rate limit"})

        else:
            cookies = {'sessionid': self.current_sessionid}
            headers = {'User-Agent': 'Instagram 64.0.0.14.96', }
            url = 'https://i.instagram.com/api/v1/users/' +userId["id"]+'/info/'
            r = send_request('get', url, headers, cookies=cookies)
            # r = requests.get(url, headers=headers, cookies=cookies, proxies=proxyDict)
            info = json.loads(r)
            print(info)
            infoUser = info["user"]
            infoUser["userID"] = userId["id"]
            return({"user": infoUser, "error": None})

    def getUserId(self, username):
        cookies = {'sessionid': self.current_sessionid}
        headers = {'User-Agent': 'Instagram 64.0.0.14.96', }
        url = 'https://www.instagram.com/{}/?__a=1'.format(username)
        r = send_request('get', url, headers, cookies=cookies)
##        r = requests.get('https://www.instagram.com/{}/?__a=1'.format(username),
##                headers=headers, cookies=cookies, proxies=proxyDict)

        try:
            info = json.loads(r)
            print(info)
            id = info["logging_page_id"].strip("profilePage_")
            return({"id": id, "error": None})
        except Exception as e:
            print(e)
            return({"id": None, "error": "User not found or rate limit"})

Instagram(data = 'asdf')