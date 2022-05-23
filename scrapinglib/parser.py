# -*- coding: utf-8 -*-

import json
from lxml import etree, html
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
    expr_studio2 = ''
    expr_year = ''
    expr_runtime = ''
    expr_runtime2 = ''
    expr_release = ''
    expr_outline = ''
    expr_director = ''
    expr_actor = ''
    expr_tags = ''
    expr_label = ''
    expr_label2 = ''
    expr_series = ''
    expr_series2 = ''
    expr_cover = ''
    expr_smallcover = ''
    expr_extrafanart = ''
    expr_trailer = ''
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
        resp = httprequest.get(url, cookies=self.cookies, proxies=self.proxies, verify=self.verify)
        if '<title>404 Page Not Found' in resp or '<title>未找到页面' in resp or '<title>お探しの商品が見つかりません' in resp:
            return 404
        return resp

    def getHtmlTree(self, url):
        """ 访问网页,返回`etree`
        """
        resp = httprequest.get(url, cookies=self.cookies, proxies=self.proxies, verify=self.verify)
        ret = etree.fromstring(resp, etree.HTMLParser())
        return ret

    def dictformat(self, htmltree):
        try:
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
                'trailer': self.getTrailer(htmltree),
                'imagecut': self.imagecut,
                'tag': self.getTags(htmltree),
                'label': self.getLabel(htmltree),
                'actor_photo': self.getActorPhoto(htmltree),
                'website': self.detailurl,
                'source': self.source,
                'series': self.getSeries(htmltree),
                'uncensored': self.getUncensored(htmltree)
            }
        except Exception as e:
            print(e)
            dic = {"title": ""}
        js = json.dumps(dic, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':'), )
        return js

    def getNum(self, htmltree):
        """ 增加 strip 过滤
        """
        return self.getTreeIndex(htmltree, self.expr_number)

    def getTitle(self, htmltree):
        return self.getTreeIndex(htmltree, self.expr_title)

    def getStudio(self, htmltree):
        try:
            return self.getTreeIndex(htmltree, self.expr_studio).strip(" ['']")
        except:
            pass
        try:
            ret = self.getTreeIndex(htmltree, self.expr_studio2).strip(" ['']")
        except:
            ret = ''
        return ret

    def getYear(self, htmltree):
        return self.getTreeIndex(htmltree, self.expr_year).strip()

    def getRuntime(self, htmltree):
        try:
            return self.getTreeIndex(htmltree, self.expr_runtime).strip(" ['']")
        except:
            pass
        try:
            ret = self.getTreeIndex(htmltree, self.expr_runtime2).strip(" ['']")
        except:
            ret = ''
        return ret

    def getRelease(self, htmltree):
        return self.getTreeIndex(htmltree, self.expr_release).strip()

    def getOutline(self, htmltree):
        return self.getTreeIndex(htmltree, self.expr_outline)

    def getDirector(self, htmltree):
        return self.getTreeIndex(htmltree, self.expr_director)

    def getActors(self, htmltree):
        return self.getAll(htmltree, self.expr_actor)

    def getTags(self, htmltree):
        return self.getTreeIndex(htmltree, self.expr_tags)

    def getLabel(self, htmltree):
        try:
            return self.getTreeIndex(htmltree, self.expr_label).strip(" ['']")
        except:
            pass
        try:
            ret = self.getTreeIndex(htmltree, self.expr_label2).strip(" ['']")
        except:
            ret = ''
        return ret

    def getSeries(self, htmltree):
        try:
            return self.getTreeIndex(htmltree, self.expr_series).strip(" ['']")
        except:
            pass
        try:
            ret = self.getTreeIndex(htmltree, self.expr_series2).strip(" ['']")
        except:
            ret = ''
        return ret

    def getCover(self, htmltree):
        """ 增加开头检测 https
        """
        return self.getTreeIndex(htmltree, self.expr_cover)

    def getSmallCover(self, htmltree):
        return self.getTreeIndex(htmltree, self.expr_smallcover)

    def getExtrafanart(self, htmltree):
        return self.getTreeIndex(htmltree, self.expr_extrafanart)

    def getTrailer(self, htmltree):
        return self.getTreeIndex(htmltree, self.expr_extrafanart)

    def getActorPhoto(self, htmltree):
        return self.getAll(htmltree, self.expr_actorphoto)

    def getUncensored(self, htmlree):
        if self.expr_uncensored:
            u = self.getAll(htmlree, self.expr_uncensored)
            return bool(u)
        else:
            return self.uncensored

    def getTreeIndex(self, tree: html.HtmlElement, expr, index = 0):
        """ 根据表达式从`xmltree`中获取匹配值,默认 index 为 0
        """
        if expr == '':
            return ''
        result = tree.xpath(expr)
        try:
            return result[index]
        except:
            return ''

    def getAll(self, tree: html.HtmlElement, expr):
        """ 根据表达式从`xmltree`中获取全部匹配值
        """
        if expr == '':
            return ''
        result = tree.xpath(expr)
        try:
            return result
        except:
            return ''
