# -*- coding: utf-8 -*-

import re
import json
from scrapinglib.javbus import Javbus
from .avsox import Avsox


def search(number, souces=None, proxies=None):
    sc = Scraping()
    return sc.search(number, souces, proxies)


class Scraping():
    """

    只需要获得内容,不经修改

    如果需要翻译等,再针对此方法封装一层
    不做 naming rule 处理,放到封装层,保持内部简介

    可以指定刮削库,可查询当前支持的刮削库
    可查询演员多个艺名

    参数:
        number
        cookies
        proxy
        sources
        multi threading

        [x] translate
        [x] naming rule
        [x] convert: actress name/tags

    """

    full_sources = ['avsox', 'javbus']
    func_mapping = {
        'avsox': Avsox().search,
        'javbus': Javbus().search
    }

    proxies = None

    def search(self, number, sources=None, proxies = None):
        self.proxies = proxies

        sources = self.checkSources(sources, number)
        json_data = {}
        for source in sources:
            try:
                print('[+]select', source)
                try:
                    json_data = json.loads(self.func_mapping[source](number, self))
                except:
                    json_data = self.func_mapping[source](number, self)
                # if any service return a valid return, break
                if self.get_data_state(json_data):
                    print(f"[+]Find movie [{number}] metadata on website '{source}'")
                    break
            except:
                break

        # Return if data not found in all sources
        if not json_data:
            print('[-]Movie Number not found!')
            return None

        return json_data


    def checkSources(self, c_sources, file_number):
        if not c_sources:
            c_sources = self.full_sources

        sources = c_sources.split(',')
        def insert(sources,source):
            if source in sources:
                sources.insert(0, sources.pop(sources.index(source)))
            return sources

        if len(sources) <= len(self.func_mapping):
            # if the input file name matches certain rules,
            # move some web service to the beginning of the list
            lo_file_number = file_number.lower()
            if "carib" in sources and (re.match(r"^\d{6}-\d{3}", file_number)
            ):
                sources = insert(sources,"carib")
            elif "item" in file_number:
                sources = insert(sources,"getchu")
            elif re.match(r"^\d{5,}", file_number) or "heyzo" in lo_file_number:
                if "avsox" in sources:
                    sources = insert(sources,"avsox")
            elif "mgstage" in sources and \
                    (re.match(r"\d+\D+", file_number) or "siro" in lo_file_number):
                sources = insert(sources,"mgstage")
            elif "fc2" in lo_file_number:
                if "fc2" in sources:
                    sources = insert(sources,"fc2")
            elif "gcolle" in sources and (re.search("\d{6}", file_number)):
                sources = insert(sources,"gcolle")
            elif "dlsite" in sources and (
                    "rj" in lo_file_number or "vj" in lo_file_number
            ):
                sources = insert(sources,"dlsite")
            elif re.match(r"^[a-z0-9]{3,}$", lo_file_number):
                if "xcity" in sources:
                    sources = insert(sources,"xcity")
                if "madou" in sources:
                    sources = insert(sources,"madou")
            elif "madou" in sources and (
                    re.match(r"^[a-z0-9]{3,}-[0-9]{1,}$", lo_file_number)
            ):
                sources = insert(sources,"madou")

        # check sources in func_mapping
        todel = []
        for s in sources:
            if not s in self.func_mapping:
                print('[!] Source Not Exist : ' + s)
                todel.append(s)
        for d in todel:
            print('[!] Remove Source : ' + s)
            sources.remove(d)
        return sources

    def get_data_state(self, data: dict) -> bool:  # 元数据获取失败检测
        if "title" not in data or "number" not in data:
            return False
        if data["title"] is None or data["title"] == "" or data["title"] == "null":
            return False
        if data["number"] is None or data["number"] == "" or data["number"] == "null":
            return False
        return True