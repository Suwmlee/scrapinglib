# -*- coding: utf-8 -*-

from lxml import etree
from . import httprequest


class Parser:

    source = 'base'

    imagecut = 1
    # update
    proxy = None
    cookies = None
    number = ''
    detailurl = ''
    # xpath
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
        """
        pass

    def queryNumberUrl(self, number):
        """ 根据番号查询详细信息url
        
        备份查询页面,预览图可能需要
        """
        url = httprequest.get(number)
        return url

    def getHtmlTree(self, url):
        resp = httprequest.get(url)
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

    def getFirst(self, tree, expr):
        """ 根据表达式从`etree`中获取第一个值
        """
        if expr == "":
            return ""
        result = tree.xpath(expr)
        try:
            return result[0]
        except:
            return ""

    def getAll(self, tree, expr):
        result = tree.xpath(expr)
        try:
            return result
        except:
            return ""

    def getNum(self, htmltree):
        if self.expr_title == '':
            return ''
        t = self.getFirst(htmltree, self.expr_number)
        return str(t)

    def getTitle(self, htmltree):
        if self.expr_title == '':
            return ''
        t = self.getFirst(htmltree, self.expr_title)
        return str(t)

    def getStudio(self, htmltree):
        if self.expr_studio == '':
            return ''
        t = self.getFirst(htmltree, self.expr_studio)
        return str(t)

    def getYear(self, htmltree):
        if self.expr_year == '':
            return ''
        t = self.getFirst(htmltree, self.expr_year)
        return str(t)

    def getRuntime(self, htmltree):
        if self.expr_runtime == '':
            return ''
        t = self.getFirst(htmltree, self.expr_runtime)
        return str(t)

    def getRelease(self, htmltree):
        if self.expr_release == '':
            return ''
        t = self.getFirst(htmltree, self.expr_release)
        return str(t)

    def getOutline(self, htmltree):
        if self.expr_outline == '':
            return ''
        t = self.getFirst(htmltree, self.expr_outline)
        return str(t)

    def getDirector(self, htmltree):
        if self.expr_director == '':
            return ''
        t = self.getFirst(htmltree, self.expr_director)
        return str(t)

    def getActor(self, htmltree):
        if self.expr_actor == '':
            return ''
        t = self.getFirst(htmltree, self.expr_actor)
        return str(t)

    def getTags(self, htmltree):
        if self.expr_tags == '':
            return ''
        t = self.getFirst(htmltree, self.expr_tags)
        return str(t)

    def getLabel(self, htmltree):
        if self.expr_tags == '':
            return ''
        t = self.getFirst(htmltree, self.expr_label)
        return str(t)

    def getSeries(self, htmltree):
        if self.expr_series == '':
            return ''
        t = self.getFirst(htmltree, self.expr_series)
        return str(t)

    def getCover(self, htmltree):
        if self.expr_series == '':
            return ''
        t = self.getFirst(htmltree, self.expr_cover)
        return str(t)

    def getSmallCover(self, htmltree):
        if self.expr_series == '':
            return ''
        t = self.getFirst(htmltree, self.expr_smallcover)
        return str(t)

    def getExtrafanart(self, htmltree):
        if self.expr_series == '':
            return ''
        t = self.getFirst(htmltree, self.expr_extrafanart)
        return str(t)

    def getActorPhoto(self, htmltree):
        if self.expr_series == '':
            return ''
        t = self.getFirst(htmltree, self.expr_actorphoto)
        return str(t)
