# -*- coding: utf-8 -*-

from .avsox import Avsox

def search(number):
    sc = Scraping()
    return sc.search(number)


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

    funMap = {
            'avsox': Avsox().search,
        }

    dbcookies = 'db cookie'

    def search(self, number):

        
        sources = ['avsox']

        ret = ''
        for souce in sources:
            js = self.funMap[souce](number, self)
            print(js)
    
        return ret
