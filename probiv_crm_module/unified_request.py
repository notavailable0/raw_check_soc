import requests
import json

proxyDict = {
    "http": '',
    "https": '',
}

def create_proxy_dict():
    with open('proxies.txt', 'r') as p:
        proxy = p.readlines()
        print(proxy)
        proxyDict['http'] = proxy[0].strip('\n')
        proxyDict['https'] = proxy[1].strip('\n')

def send_request(g, url, headers, **kwargs):
    if 'cookies' in kwargs.keys(): cookies = kwargs['cookies']
    else: cookies = None
    proxies = proxyDict

    result = None
    while result is None:
        try:
            if g == 'get':
                if (cookies):
                    r = requests.get(url, headers=headers, proxies=proxies, cookies=cookies)
                    return r.text
                else:
                    r = requests.get(url, headers=headers, proxies=proxies)
                    print(url)
                    print(headers)
                    print(proxies)
                    return r.text

            elif g == 'post':
                data = kwargs['data']
                if (cookies):
                    r = requests.post(url, headers=headers, proxies=proxies, data=data, cookies=cookies)
                    return r.text
                else:
                    r = requests.post(url, headers=headers, data=data, proxies=proxies)
                    return r.text

        except Exception as e:
            print(e)