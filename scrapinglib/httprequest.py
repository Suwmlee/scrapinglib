# -*- coding: utf-8 -*-

import requests

G_USER_AGENT = r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.133 Safari/537.36'


def get(url: str, cookies: dict = None, ua: str = None, return_type: str = None, encoding: str = None, retry: int = 3, proxies=None, timeout: int = None, verify=None):
    """
    网页请求核心函数
    
    是否使用代理应由上层处理
    """
    errors = ""
    headers = {"User-Agent": ua or G_USER_AGENT}  # noqa

    for i in range(retry):
        try:
            result = requests.get(url, headers=headers, timeout=timeout, proxies=proxies,
                                  verify=verify,
                                  cookies=cookies)
            if return_type == "object":
                return result
            elif return_type == "content":
                return result.content
            else:
                result.encoding = encoding or result.apparent_encoding
                return result.text
        except Exception as e:
            print("[-]Connect retry {}/{}".format(i + 1, retry))
            errors = str(e)
    if "getaddrinfo failed" in errors:
        print("[-]Connect Failed! Please Check your proxy config")
        print("[-]" + errors)
    else:
        print("[-]" + errors)
        print('[-]Connect Failed! Please check your Proxy or Network!')
    raise Exception('Connect Failed')
