# -*- coding: utf-8 -*-

import mechanicalsoup
import requests
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from curl_cffi import requests as curl_requests

G_USER_AGENT = r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
G_DEFAULT_TIMEOUT = 10
G_DEFAULT_RETRY = 3


def get(url: str, cookies=None, ua: str = None, extra_headers=None, return_type: str = None, encoding: str = None,
        retry: int = G_DEFAULT_RETRY, timeout: int = G_DEFAULT_TIMEOUT, proxies=None, verify=None):
    """
    网页请求核心函数

    是否使用代理应由上层处理
    """
    errors = ""
    headers = {"User-Agent": ua or G_USER_AGENT}
    if extra_headers != None:
        headers.update(extra_headers)
    for i in range(retry):
        try:
            result = requests.get(url, headers=headers, timeout=timeout, proxies=proxies,
                                  verify=verify, cookies=cookies)
            if return_type == "object":
                return result
            elif return_type == "content":
                return result.content
            else:
                result.encoding = encoding or result.apparent_encoding
                return result.text
        except Exception as e:
            logging.debug(f"[-]Connect: {url} retry {i + 1}/{retry}")
            errors = str(e)
    if "getaddrinfo failed" in errors:
        logging.debug("[-]Connect Failed! Please Check your proxy config")
        logging.debug("[-]" + errors)
    else:
        logging.debug("[-]" + errors)
        logging.debug('[-]Connect Failed! Please check your Proxy or Network!')
    raise Exception('Connect Failed')


def post(url: str, data: dict = None, files=None, cookies=None, ua: str = None, return_type: str = None, encoding: str = None,
         retry: int = G_DEFAULT_RETRY, timeout: int = G_DEFAULT_TIMEOUT, proxies=None, verify=None):
    """
    是否使用代理应由上层处理
    """
    errors = ""
    headers = {"User-Agent": ua or G_USER_AGENT}

    for i in range(retry):
        try:
            result = requests.post(url, data=data, files=files, headers=headers, timeout=timeout, proxies=proxies,
                                   verify=verify, cookies=cookies)
            if return_type == "object":
                return result
            elif return_type == "content":
                return result.content
            else:
                result.encoding = encoding or result.apparent_encoding
                return result
        except Exception as e:
            logging.debug(f"[-]Connect: {url} retry {i + 1}/{retry}")
            errors = str(e)
    if "getaddrinfo failed" in errors:
        logging.debug("[-]Connect Failed! Please Check your proxy config")
        logging.debug("[-]" + errors)
    else:
        logging.debug("[-]" + errors)
        logging.debug('[-]Connect Failed! Please check your Proxy or Network!')
    raise Exception('Connect Failed')


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = G_DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


def request_session(cookies=None, ua: str = None, retry: int = G_DEFAULT_RETRY, timeout: int = G_DEFAULT_TIMEOUT, proxies=None, verify=None, use_curl_cffi=False):
    """
    创建 HTTP session
    
    Args:
        use_curl_cffi: 是否使用 curl_cffi 绕过 Cloudflare（用于 javdb）
    """
    if use_curl_cffi:
        # 使用 curl_cffi 模拟真实 Chrome 浏览器
        session = curl_requests.Session(impersonate="chrome120")
        
        session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
        })
        
        if isinstance(cookies, dict) and len(cookies):
            session.cookies.update(cookies)
        if proxies:
            if 'https' in proxies:
                session.proxies = {'https': proxies['https'], 'http': proxies.get('http', proxies['https'])}
            elif 'http' in proxies:
                session.proxies = {'http': proxies['http'], 'https': proxies.get('https', proxies['http'])}
        session.verify = False if verify is False else True
        
        return session
    
    # 普通 requests session
    session = requests.Session()
    session.headers = {"User-Agent": ua or G_USER_AGENT}
    
    retries = Retry(total=retry, connect=retry, backoff_factor=1,
                    status_forcelist=[429, 500, 502, 503, 504])
    session.mount("https://", TimeoutHTTPAdapter(max_retries=retries, timeout=timeout))
    session.mount("http://", TimeoutHTTPAdapter(max_retries=retries, timeout=timeout))
    
    if isinstance(cookies, dict) and len(cookies):
        requests.utils.add_dict_to_cookiejar(session.cookies, cookies)
    if verify is not None:
        session.verify = verify
    if proxies:
        session.proxies = proxies
    
    return session


# storyline xcity only
def get_html_by_form(url, form_select: str = None, fields: dict = None, cookies: dict = None, ua: str = None,
                     return_type: str = None, encoding: str = None,
                     retry: int = G_DEFAULT_RETRY, timeout: int = G_DEFAULT_TIMEOUT, proxies=None, verify=None):
    session = requests.Session()
    if isinstance(cookies, dict) and len(cookies):
        requests.utils.add_dict_to_cookiejar(session.cookies, cookies)
    retries = Retry(total=retry, connect=retry, backoff_factor=1,
                    status_forcelist=[429, 500, 502, 503, 504])
    session.mount("https://", TimeoutHTTPAdapter(max_retries=retries, timeout=timeout))
    session.mount("http://", TimeoutHTTPAdapter(max_retries=retries, timeout=timeout))
    if verify:
        session.verify = verify
    if proxies:
        session.proxies = proxies
    try:
        browser = mechanicalsoup.StatefulBrowser(user_agent=ua or G_USER_AGENT, session=session)
        result = browser.open(url)
        if not result.ok:
            return None
        form = browser.select_form() if form_select is None else browser.select_form(form_select)
        if isinstance(fields, dict):
            for k, v in fields.items():
                browser[k] = v
        response = browser.submit_selected()

        if return_type == "object":
            return response
        elif return_type == "content":
            return response.content
        elif return_type == "browser":
            return response, browser
        else:
            result.encoding = encoding or "utf-8"
            return response.text
    except requests.exceptions.ProxyError:
        logging.debug("[-]get_html_by_form() Proxy error! Please check your Proxy")
    except Exception as e:
        logging.debug(f'[-]get_html_by_form() Failed! {e}')
    return None


# storyline javdb only
def get_html_by_scraper(url: str = None, cookies: dict = None, ua: str = None, return_type: str = None,
                        encoding: str = None, retry: int = G_DEFAULT_RETRY, proxies=None, timeout: int = G_DEFAULT_TIMEOUT, verify=None):
    session = curl_requests.Session(impersonate="chrome120")
    
    if isinstance(cookies, dict) and len(cookies):
        session.cookies.update(cookies)
    if proxies:
        if 'https' in proxies:
            session.proxies = {'https': proxies['https'], 'http': proxies.get('http', proxies['https'])}
        elif 'http' in proxies:
            session.proxies = {'http': proxies['http'], 'https': proxies.get('https', proxies['http'])}
    session.verify = False if verify is False else True
    
    try:
        if isinstance(url, str) and len(url):
            result = session.get(str(url), timeout=timeout)
        else:
            return session
        if result.status_code != 200:
            return None
        if return_type == "object":
            return result
        elif return_type == "content":
            return result.content
        elif return_type == "scraper":
            return result, session
        else:
            return result.text
    except Exception as e:
        logging.debug(f"[-]get_html_by_scraper() failed. {e}")
    return None
