# -*- coding: utf-8 -*-

from lxml import etree
from . import httprequest


class Parser:

    source = 'base'
    imagecut = 1
    uncensored = False
    # update
    proxies = None
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
    expr_uncensored = ''

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
        if core.proxies:
            self.proxies = core.proxies

    def queryNumberUrl(self, number):
        """ 根据番号查询详细信息url
        
        备份查询页面,预览图可能需要
        """
        url = httprequest.get(number)
        return url

    def getHtml(self, url):
        """ 访问网页
        """
        return httprequest.get(url, cookies=self.cookies, proxies=self.proxies, verify=self.verify)

    def getHtmlTree(self, url):
        """ 访问网页,返回`etree`
        """
        resp = httprequest.get(url, cookies=self.cookies, proxies=self.proxies, verify=self.verify)
        ret = etree.fromstring(resp, etree.HTMLParser())
        return ret

    def dictformat(self, htmltree):
        dic = {
            'number': self.getNum(htmltree),
            'title': self.getTitle(htmltree),
            'studio': self.getStudio(htmltree),
            'year': self.getYear(htmltree),
            'outline': self.getOutline(htmltree),
            'runtime': self.getRuntime(htmltree),
            'director': self.getDirector(htmltree),
            'actor': self.getActors(htmltree),
            'release': self.getRelease(htmltree),
            'cover': self.getCover(htmltree),
            'cover_small': self.getSmallCover(htmltree),
            'extrafanart': self.getExtrafanart(htmltree),
            'imagecut': self.imagecut,
            'tag': self.getTags(htmltree),
            'label': self.getLabel(htmltree),
            'actor_photo': self.getActorPhoto(htmltree),
            'website': self.detailurl,
            'source': self.source,
            'series': self.getSeries(htmltree),
            'uncensored': self.getUncensored(htmltree)
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

    def getActors(self, htmltree):
        return self.getAll(htmltree, self.expr_actor)

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
        return self.getAll(htmltree, self.expr_actorphoto)

    def getUncensored(self, htmlree):
        if self.expr_uncensored:
            u = self.getAll(htmlree, self.expr_uncensored)
            return bool(u)
        else:
            return self.uncensored

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
        if expr == '':
            return ''
        result = tree.xpath(expr)
        try:
            return result
        except:
            return ''
