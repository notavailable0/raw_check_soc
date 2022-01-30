from telethon import TelegramClient, sync
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.types import InputPhoneContact

import os.path

def check_tg(phone_numbers, api_id, api_hash):
    try:
        with TelegramClient('detect.session', api_id, api_hash) as client:
                input_contact_list = []
                for phone_number in phone_numbers:
                    phone_dict = dict(phone_number)
                    phone_number = phone_number['phone']
                    input_contact_list.append(
                        InputPhoneContact(client_id=0, phone=phone_number,
                                          first_name=phone_number,
                                          last_name=phone_number))
                client(ImportContactsRequest(input_contact_list))
                for phone_number in phone_numbers:
                    try:
                        contact = client.get_input_entity(phone_number['phone'])
                        # If the user's id is not 0 then the user has an account in Telegram
                        if contact.user_id > 0:
                            return {phone_dict['id'] : {'tg': True}}
                        else:
                            return {phone_dict['id'] : {'tg': False}}

                    except ValueError as e:

                        # TODO Use an error logger
                        if "Cannot find any entity corresponding to" in str(e):
                            return {phone_dict['id'] : {'tg': False}}
                        else:

                            print(e)
                            return {phone_dict['id'] : {'tg': "fuck"}}
    except Exception as e:
        print(e)
