# -*- coding: utf-8 -*-

from lxml import etree
from . import httprequest


class Parser:

    source = 'base'

    imagecut = 1
    # update
    proxy = None
    cookies = None
    verify = None

    number = ''
    detailurl = ''
    # xpath expr
    expr_number = ''
    expr_title = ''
    expr_studio = ''
    expr_year = ''
    expr_runtime = ''
    expr_release = ''
    expr_outline = ''
    expr_director = ''
    expr_actor = ''
    expr_tags = ''
    expr_label = ''
    expr_series = ''
    expr_cover = ''
    expr_smallcover = ''
    expr_extrafanart = ''
    expr_actorphoto = ''

    def __init__(self) -> None:
        pass

    def search(self, number, core: None):
        """ 搜索番号
        """
        self.number = number
        self.updateCore(core)

        self.detailurl = self.queryNumberUrl(number)
        htmltree = self.getHtmlTree(self.detailurl)
        result = self.dictformat(htmltree)
        return result

    def updateCore(self, core):
        """ 从`core`内更新参数
        
        针对需要传递的参数: cookies, proxy等
        子类继承后修改
        """
        pass

    def queryNumberUrl(self, number):
        """ 根据番号查询详细信息url
        
        备份查询页面,预览图可能需要
        """
        url = httprequest.get(number)
        return url

    def getHtmlTree(self, url):
        """ 访问网页,返回`etree`
        """
        resp = httprequest.get(url, cookies=self.cookies, proxies=self.proxy, verify=self.verify)
        ret = etree.fromstring(resp, etree.HTMLParser())
        return ret

    def dictformat(dic, htmltree):
        dic = {
            'number': dic.getNum(htmltree),
            'title': dic.getTitle(htmltree),
            'studio': dic.getStudio(htmltree),
            'year': dic.getYear(htmltree),
            'outline': dic.getOutline(htmltree),
            'runtime': dic.getRuntime(htmltree),
            'director': dic.getDirector(htmltree),
            'actor': dic.getActor(htmltree),
            'release': dic.getRelease(htmltree),
            'cover': dic.getCover(htmltree),
            'cover_small': dic.getSmallCover(htmltree),
            'extrafanart': dic.getExtrafanart(htmltree),
            'imagecut': dic.imagecut,
            'tag': dic.getTags(htmltree),
            'label': dic.getLabel(htmltree),
            'actor_photo': dic.getActorPhoto(htmltree),
            'website': dic.detailurl,
            'source': dic.source,
            'series': dic.getSeries(htmltree)
        }
        return dic

    def getNum(self, htmltree):
        return self.getFirst(htmltree, self.expr_number)

    def getTitle(self, htmltree):
        return self.getFirst(htmltree, self.expr_title)

    def getStudio(self, htmltree):
        return self.getFirst(htmltree, self.expr_studio)

    def getYear(self, htmltree):
        return self.getFirst(htmltree, self.expr_year)

    def getRuntime(self, htmltree):
        return self.getFirst(htmltree, self.expr_runtime)

    def getRelease(self, htmltree):
        return self.getFirst(htmltree, self.expr_release)

    def getOutline(self, htmltree):
        return self.getFirst(htmltree, self.expr_outline)

    def getDirector(self, htmltree):
        return self.getFirst(htmltree, self.expr_director)

    def getActor(self, htmltree):
        return self.getFirst(htmltree, self.expr_actor)

    def getTags(self, htmltree):
        return self.getFirst(htmltree, self.expr_tags)

    def getLabel(self, htmltree):
        return self.getFirst(htmltree, self.expr_label)

    def getSeries(self, htmltree):
        return self.getFirst(htmltree, self.expr_series)

    def getCover(self, htmltree):
        return self.getFirst(htmltree, self.expr_cover)

    def getSmallCover(self, htmltree):
        return self.getFirst(htmltree, self.expr_smallcover)

    def getExtrafanart(self, htmltree):
        return self.getFirst(htmltree, self.expr_extrafanart)

    def getActorPhoto(self, htmltree):
        return self.getFirst(htmltree, self.expr_actorphoto)

    def getFirst(self, tree, expr):
        """ 根据表达式从`xmltree`中获取第一个匹配值
        """
        if expr == '':
            return ''
        result = tree.xpath(expr)
        try:
            return result[0]
        except:
            return ''

    def getAll(self, tree, expr):
        """ 根据表达式从`xmltree`中获取全部匹配值
        """
        result = tree.xpath(expr)
        try:
            return result
        except:
            return ''
