# -*- coding: utf-8 -*-

import re
import json
import logging
import importlib

from .parser import Parser
from .httprequest import HTTP_CLIENT_AUTO, HTTP_CLIENT_REQUESTS, HTTP_CLIENT_CURL_CFFI


def search(number, sources: str = None, http_client: str = HTTP_CLIENT_AUTO, **kwargs):
    """ 根据`番号/电影`名搜索信息

    :param number: number/name  depends on type
    :param sources: sources string with `,` Eg: `avsox,javbus`
    :param http_client: HTTP 客户端类型 ('requests', 'curl_cffi', 'auto')
    :param type: `adult`, `general`
    """
    sc = Scraping()
    return sc.search(number, sources, http_client=http_client, **kwargs)


def getSupportedSources(tag='adult'):
    """
    :param tag: `adult`, `general`
    """
    sc = Scraping()
    if tag == 'adult':
        return ','.join(sc.adult_full_sources)
    else:
        return ','.join(sc.general_full_sources)


class Scraping:
    """
    """
    adult_full_sources = ['javlibrary', 'javdb', 'javbus', 'airav', 'fanza', 'xcity', 'jav321',
                          'mgstage', 'fc2', 'avsox', 'dlsite', 'carib', 'madouclub', 'madouqu',
                          'getchu', 'gcolle', 'javday'
                          ]

    general_full_sources = ['tmdb', 'imdb']
    proxies = None
    verify = None
    specifiedSource = None
    specifiedUrl = None

    dbcookies = None
    dbsite = None
    # 使用storyline方法进一步获取故事情节
    morestoryline = False
    # HTTP 客户端类型：'requests'（默认）, 'curl_cffi'（绕过 Cloudflare）, 'auto'
    http_client = HTTP_CLIENT_AUTO

    def search(self, number, sources=None, proxies=None, verify=None, type='adult',
               specifiedSource=None, specifiedUrl=None,
               dbcookies=None, dbsite=None, morestoryline=False, 
               http_client: str = HTTP_CLIENT_AUTO
               ):
        self.proxies = proxies
        self.verify = verify
        self.specifiedSource = specifiedSource
        self.specifiedUrl = specifiedUrl
        self.dbcookies = dbcookies
        self.dbsite = dbsite
        self.morestoryline = morestoryline
        self.http_client = http_client
        
        if type == 'adult':
            return self.searchAdult(number, sources)
        else:
            return self.searchGeneral(number, sources)

    def searchGeneral(self, name, sources):
        """ 查询电影电视剧
        imdb,tmdb
        """
        if self.specifiedSource:
            sources = [self.specifiedSource]
        else:
            sources = self.checkGeneralSources(sources, name)
        json_data = {}
        for source in sources:
            try:
                logging.debug(f'[+]select {source}')
                try:
                    module = importlib.import_module('.' + source, 'scrapinglib')
                    parser_type = getattr(module, source.capitalize())
                    parser: Parser = parser_type()
                    data = parser.scrape(name, self)
                    if data == 404:
                        continue
                    json_data = json.loads(data)
                except Exception as e:
                    logging.debug(e)
                # if any service return a valid return, break
                if self.get_data_state(json_data):
                    logging.debug(f"[+]Find movie [{name}] metadata on website '{source}'")
                    break
            except:
                continue

        # Return if data not found in all sources
        if not json_data:
            logging.debug(f'[-]Movie Number [{name}] not found!')
            return None

        return json_data

    def searchAdult(self, number, sources):
        if self.specifiedSource:
            sources = [self.specifiedSource]
        else:
            sources = self.checkAdultSources(sources, number)
        json_data = {}
        for source in sources:
            try:
                logging.debug(f'[+]select {source}')
                try:
                    module = importlib.import_module('.' + source, 'scrapinglib')
                    parser_type = getattr(module, source.capitalize())
                    parser: Parser = parser_type()
                    data = parser.scrape(number, self)
                    if data == 404:
                        continue
                    json_data = json.loads(data)
                    # clean json_data
                    json_data = self.clean_title_tags(json_data)
                except Exception as e:
                    logging.debug(e)
                # if any service return a valid return, break
                if self.get_data_state(json_data):
                    logging.debug(f"[+]Find movie [{number}] metadata on website '{source}'")
                    break
            except:
                continue

        # Return if data not found in all sources
        if not json_data:
            logging.debug(f'[-]Movie Number [{number}] not found!')
            return None

        return json_data

    def checkGeneralSources(self, c_sources, name):
        if not c_sources:
            sources = self.general_full_sources
        else:
            sources = c_sources.split(',')

        # check sources in func_mapping
        todel = []
        for s in sources:
            if not s in self.general_full_sources:
                logging.debug('[!] Source Not Exist : ' + s)
                todel.append(s)
        for d in todel:
            logging.debug('[!] Remove Source : ' + s)
            sources.remove(d)
        return sources

    def checkAdultSources(self, c_sources, file_number):
        if not c_sources:
            sources = self.adult_full_sources
        else:
            sources = c_sources.split(',')

        def insert(sources, source):
            if source in sources:
                sources.insert(0, sources.pop(sources.index(source)))
            return sources

        if len(sources) <= len(self.adult_full_sources):
            # if the input file name matches certain rules,
            # move some web service to the beginning of the list
            lo_file_number = file_number.lower()
            if "carib" in sources and (re.search(r"^\d{6}-\d{3}", file_number)
            ):
                sources = insert(sources, "carib")
            elif "item" in file_number or "GETCHU" in file_number.upper():
                sources = insert(sources, "getchu")
            elif "rj" in lo_file_number or "vj" in lo_file_number or re.search(r"[\u3040-\u309F\u30A0-\u30FF]+",
                                                                               file_number):
                sources = insert(sources, "getchu")
                sources = insert(sources, "dlsite")
            elif "fc2" in lo_file_number:
                if "fc2" in sources:
                    sources = insert(sources, "fc2")
            elif "mgstage" in sources and \
                    (re.search(r"\d+\D+", file_number) or "siro" in lo_file_number):
                sources = insert(sources, "mgstage")
            elif "gcolle" in sources and (re.search("\d{6}", file_number)):
                sources = insert(sources, "gcolle")
            elif "madouclub" in sources and (re.search(r"^[a-z0-9]{3,}-[0-9]{1,}$", lo_file_number)):
                sources = insert(sources, "madouclub")

            elif re.search(r"^\d{5,}", file_number) or "heyzo" in lo_file_number:
                if "avsox" in sources:
                    sources = insert(sources, "avsox")
            elif re.search(r"^[a-z0-9]{3,}$", lo_file_number):
                if "xcity" in sources:
                    sources = insert(sources, "xcity")
                if "madouclub" in sources:
                    sources = insert(sources, "madouclub")

        # check sources in func_mapping
        todel = []
        for s in sources:
            if not s in self.adult_full_sources:
                logging.debug('[!] Source Not Exist : ' + s)
                todel.append(s)
        for d in todel:
            logging.debug('[!] Remove Source : ' + s)
            sources.remove(d)
        return sources

    def clean_title_tags(self, data: dict) -> dict:
        """清理标题中的标签词缀等"""
        if "title" in data and data["title"]:
            patterns = [
                r'【[^】]*限定[^】]*】',
                r'【[^】]*DMM[^】]*】',
                r'【[^】]*FANZA[^】]*】',
                r'【[^】]*独占[^】]*】',
                r'【[^】]*配信[^】]*】',
                r'【[^】]*デジタル[^】]*】',
                r'【[^】]*独家[^】]*】',
                r'\[[^\]]*限定[^\]]*\]',
                r'\[[^\]]*DMM[^\]]*\]',
                r'\[[^\]]*FANZA[^\]]*\]',
            ]

            title = data["title"]
            for pattern in patterns:
                title = re.sub(pattern, '', title)

            title = re.sub(r'\s+', ' ', title).strip()
            data["title"] = title

        resolution_patterns = [
            r'^\d+[pP]$',
            r'^\d+[kK]$',
            r'^[Hh][Dd]$',
            r'^[Ss][Dd]$',
        ]

        # 清理 tag 字段
        if "tag" in data and isinstance(data["tag"], list):
            cleaned_tags = []
            for tag in data["tag"]:
                if tag and isinstance(tag, str):
                    should_keep = True
                    for pattern in resolution_patterns:
                        if re.match(pattern, tag.strip()):
                            should_keep = False
                            break
                    if should_keep:
                        cleaned_tags.append(tag)
            data["tag"] = cleaned_tags

        # 清理 label 字段
        if "label" in data and data["label"] and isinstance(data["label"], str):
            label = data["label"].strip()
            for pattern in resolution_patterns:
                if re.match(pattern, label):
                    data["label"] = ''
                    break

        return data

    def get_data_state(self, data: dict) -> bool:  # 元数据获取失败检测
        if "title" not in data or "number" not in data:
            return False
        if data["title"] is None or data["title"] == "" or data["title"] == "null":
            return False
        if data["number"] is None or data["number"] == "" or data["number"] == "null":
            return False
        return True
