## FACEBOOK TO RUN U NEED INSTALL THIS GO MODULE
## https://github.com/yasserjanah/FacebookChecker

## ya ebu alibabu

import os

def check_fb(num):
    try:
        res = os.popen(f'C:\\Users\\akozl\\go\\bin\\FacebookChecker.exe -id {num}').read()
        if 'ERROR' in str(res):
            print(res)
            return False
        else:
            print(res)
            return True

    except Exception as e: print(e)

#print(check_fb('1234'))