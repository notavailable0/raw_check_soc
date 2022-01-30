import sys
import time
import json
import httpx
import hmac
import hashlib
import urllib
import requests
from httpx import get
from bs4 import BeautifulSoup


def main(sessionid, name, email, phone, timeout):

    sessionsId = sessionid
    name =  name
    email =  email
    phone =  phone
    timeout =  timeout

    session = requests.Session()

    proxies = {
               'http': 'http://hoomma:25rL9TWh92koW6lU@proxy.packetstream.io:31112',
               'https': 'http://hoomma:25rL9TWh92koW6lU@proxy.packetstream.io:31112',
            }

    session.proxies = proxies

    accounts = dumpor(name)

    if accounts["user"] == None:
        print(accounts["error"])
    else:
        for account in accounts["user"]:
            name_f, email_f, phone_f = 0, 0, 0
            infos = getInfo(account[1:], sessionsId)
##            print(json.dumps(infos, indent=4, sort_keys=True))

            if infos["user"] == None:
                print(infos["error"])

            else:
                other_infos = advanced_lookup(account[1:])
                print(json.dumps(other_infos, indent=4, sort_keys=True))
                print(other_infos.keys())

                if 'obfuscated_email' in other_infos['user'].keys():

                    if other_infos['user']['obfuscated_email'].split('@')[0][0] + other_infos['user']['obfuscated_email'].split('@')[0][-1] == email.split('@')[0][0]+email.split('@')[0][-1]:
                        return {"ig": True, 'data': other_infos}
                    if other_infos["error"] == "rate limit":
                        return print("Rate limit please wait a few minutes before you try again")

                elif 'obfuscated_phone' in other_infos['user'].keys():
                    print('nmber:')
                    print(other_infos['user']['obfuscated_phone'])
                    print(other_infos['user']['obfuscated_phone'][-1]+other_infos['user']['obfuscated_phone'][-2])

                elif other_infos['user']['status'] == 'fail':
                    print('account has been detected, adding to sleep list for 1h')


##                    if other_infos['user']['obfuscated_email'][-1:-2]


            ## need to create exceptions etc.


def getUserId(username, sessionsId):
    cookies = {'sessionid': sessionsId}
    headers = {'User-Agent': 'Instagram 64.0.0.14.96', }
    r = get('https://www.instagram.com/{}/?__a=1'.format(username),
            headers=headers, cookies=cookies)
    try:
        info = json.loads(r.text)
        id = info["logging_page_id"].strip("profilePage_")
        return({"id": id, "error": None})
    except:
        return({"id": None, "error": "User not found or rate limit"})


def getInfo(username, sessionId):
    userId = getUserId(username, sessionId)
    if userId["error"] != None:
        return({"user": None, "error": "User not found or rate limit"})
    else:
        cookies = {'sessionid': sessionId}
        headers = {'User-Agent': 'Instagram 64.0.0.14.96', }
        response = get('https://i.instagram.com/api/v1/users/' +
                       userId["id"]+'/info/', headers=headers, cookies=cookies)
        info = json.loads(response.text)
        infoUser = info["user"]
        infoUser["userID"] = userId["id"]
        return({"user": infoUser, "error": None})


def advanced_lookup(username):
    USERS_LOOKUP_URL = 'https://i.instagram.com/api/v1/users/lookup/'
    SIG_KEY_VERSION = '4'
    IG_SIG_KEY = 'e6358aeede676184b9fe702b30f4fd35e71744605e39d2181a34cede076b3c33'

    def generate_signature(data):
        return 'ig_sig_key_version=' + SIG_KEY_VERSION + '&signed_body=' + hmac.new(IG_SIG_KEY.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest() + '.' + urllib.parse.quote_plus(data)

    def generate_data(phone_number_raw):
        data = {'login_attempt_count': '0',
                'directly_sign_in': 'true',
                'source': 'default',
                'q': phone_number_raw,
                'ig_sig_key_version': SIG_KEY_VERSION
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
        r = httpx.post(USERS_LOOKUP_URL, headers=headers, data=data)
        rep = r.json()
        return({"user": rep, "error": None})
    except:
        return({"user": None, "error": "rate limit"})


def dumpor(name):
    url = "https://dumpor.com/search?query="
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    req = url + name.replace(" ", "+")

    try:
        account_list = []
        response = requests.get(req, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        accounts = soup.findAll('a', {"class": "profile-name-link"})
        for account in accounts:
            account_list.append(account.text)
        return({"user": account_list, "error": None})
    except:
        return({"user": None, "error": "rate limit"})

sess = '46012304898%3Ai9RU23yn9HjWFb%3A21'
name = 'Artjom Kozlov'
email = 'akozlov295@gmail.com'
phone = ''
timeout = 1

main(sess, name, email, phone, timeout)
#46012304898%3Ai9RU23yn9HjWFb%3A21
#{'user': {'pk': 7814832798, 'username': 'artjomkozlov', 'full_name': 'Artjom Kozlov', 'is_private': False, 'profile_pic_url': 'https://instagram.fmuc4-1.fna.fbcdn.net/v/t51.2885-19/s150x150/31976442_231961224233274_6749939919147237376_n.jpg?_nc_ht=instagram.fmuc4-1.fna.fbcdn.net&_nc_cat=106&_nc_ohc=FNcKCAF-UtEAX9tHKg2&edm=AEF8tYYBAAAA&ccb=7-4&oh=00_AT_jLDv5ENNAPgsqWLLNBPc8ig14eVkUK_mqYxP-_BijZA&oe=61F1BB14&_nc_sid=a9513d', 'profile_pic_id': '1784722491769841196_7814832798', 'is_verified': False, 'follow_friction_type': 0, 'has_anonymous_profile_picture': False, 'media_count': 0, 'follower_count': 107, 'following_count': 381, 'following_tag_count': 0, 'biography': '', 'external_url': '', 'show_fb_link_on_profile': False, 'primary_profile_link_type': 0, 'total_igtv_videos': 0, 'has_videos': False, 'total_ar_effects': 0, 'usertags_count': 14, 'is_favorite': False, 'is_favorite_for_stories': False, 'is_favorite_for_highlights': False, 'is_interest_account': False, 'hd_profile_pic_versions': [{'width': 320, 'height': 320, 'url': 'https://instagram.fmuc4-1.fna.fbcdn.net/v/t51.2885-19/s320x320/31976442_231961224233274_6749939919147237376_n.jpg?_nc_ht=instagram.fmuc4-1.fna.fbcdn.net&_nc_cat=106&_nc_ohc=FNcKCAF-UtEAX9tHKg2&edm=AEF8tYYBAAAA&ccb=7-4&oh=00_AT9ftdon20cYAtnZFAL7xpilkKEPzQKCkTUdbAZkipOamw&oe=61F2CF64&_nc_sid=a9513d'}, {'width': 640, 'height': 640, 'url': 'https://instagram.fmuc4-1.fna.fbcdn.net/v/t51.2885-19/s640x640/31976442_231961224233274_6749939919147237376_n.jpg?_nc_ht=instagram.fmuc4-1.fna.fbcdn.net&_nc_cat=106&_nc_ohc=FNcKCAF-UtEAX9tHKg2&edm=AEF8tYYBAAAA&ccb=7-4&oh=00_AT9D9lf5-GuZPWfzxRkuBaMsmo-grMK2hXllokZI4g78MQ&oe=61F198CD&_nc_sid=a9513d'}], 'hd_profile_pic_url_info': {'url': 'https://instagram.fmuc4-1.fna.fbcdn.net/v/t51.2885-19/31976442_231961224233274_6749939919147237376_n.jpg?_nc_ht=instagram.fmuc4-1.fna.fbcdn.net&_nc_cat=106&_nc_ohc=FNcKCAF-UtEAX9tHKg2&edm=AEF8tYYBAAAA&ccb=7-4&oh=00_AT_3tSYrngSlbzEb4a5GNNeQ9z1MJno1QNIc1en5aLomMw&oe=61F12AEA&_nc_sid=a9513d', 'width': 720, 'height': 720}, 'mutual_followers_count': 0, 'has_highlight_reels': True, 'has_guides': False, 'can_be_reported_as_fraud': False, 'is_business': False, 'professional_conversion_suggested_account_type': 2, 'account_type': 1, 'is_call_to_action_enabled': None, 'interop_messaging_user_fbid': 101325384602408, 'pronouns': [], 'include_direct_blacklist_status': True, 'is_potential_business': False, 'show_post_insights_entry_point': True, 'request_contact_enabled': False, 'is_bestie': False, 'has_unseen_besties_media': False, 'show_account_transparency_details': False, 'auto_expand_chaining': False, 'highlight_reshare_disabled': False, 'is_memorialized': False, 'open_external_url_with_in_app_browser': True, 'userID': '7814832798'}, 'error': None}
#{'user': {'multiple_users_found': False, 'email_sent': False, 'sms_sent': False, 'lookup_source': 'username', 'corrected_input': 'artjomkozlov', 'obfuscated_email': 'a*******5@gmail.com', 'user': {'pk': 7814832798, 'username': 'artjomkozlov', 'full_name': 'Artjom Kozlov', 'is_private': False, 'profile_pic_url': 'https://instagram.fmuc4-1.fna.fbcdn.net/v/t51.2885-19/s150x150/31976442_231961224233274_6749939919147237376_n.jpg?_nc_ht=instagram.fmuc4-1.fna.fbcdn.net&_nc_cat=106&_nc_ohc=FNcKCAF-UtEAX9tHKg2&edm=AGygydIBAAAA&ccb=7-4&oh=00_AT-MHLUWQ7RxtJEZR3f0zbQAqOZG10py5Te4OD5EduZQmQ&oe=61F1BB14&_nc_sid=41f71f', 'profile_pic_id': '1784722491769841196_7814832798', 'is_verified': False, 'follow_friction_type': -1, 'has_anonymous_profile_picture': False, 'has_highlight_reels': False}, 'has_valid_phone': False, 'can_email_reset': True, 'can_sms_reset': False, 'can_wa_reset': False, 'user_id': 7814832798, 'email': 'artjomkozlov', 'phone_number': None, 'fb_login_option': True, 'status': 'ok'}, 'error': None}
