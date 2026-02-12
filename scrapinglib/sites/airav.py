# -*- coding: utf-8 -*-

import json
import re
from lxml import etree
from ..base_scraper import BaseScraper
from .javbus import Javbus

class Airav(BaseScraper):
    source = 'airav'
    content_type = 'adult'
    priority = 40

    expr_title = '/html/head/title/text()'
    expr_number = '//li[contains(text(),"番號：")]/span/text()'
    expr_studio = '//li[contains(text(),"廠商：")]/a/text()'
    expr_release = '//div[@class="video-item"]/div[contains(@class,"me-4")]/text()'
    expr_outline = "string(//div[@class='video-info']/p[@class='my-3'])"
    expr_actor = '//li[contains(text(),"女優：")]/a/text()'
    expr_cover = '//meta[@property="og:image"]/@content'
    expr_tags = '//li[contains(text(),"標籤：")]/a/text()'
    expr_series = '//li[contains(text(),"系列：")]/a/text()'
    expr_extrafanart = '//div[@class="mobileImgThumbnail"]/a/@href'

    def extraInit(self):
        # for javbus
        self.specifiedSource = None
        self.addtion_Javbus = False

    def search(self, number: str):
        self.number = number.upper()
        if self.specifiedUrl:
            self.detailurl = self.specifiedUrl
        else:
            self.detailurl = self.queryNumberUrl(self.number)
        if self.addtion_Javbus:
            engine = Javbus()
            javbusinfo = engine.scrape(self.number, self)
            if javbusinfo == 404:
                self.javbus = {"title": ""}
            else:
                self.javbus = json.loads(javbusinfo)
        self.htmlcode = self.getHtml(self.detailurl)
        htmltree = etree.fromstring(self.htmlcode, etree.HTMLParser())
        result = self.dictformat(htmltree)
        return result

    def queryNumberUrl(self, number: str):
        queryUrl =  "https://airav.io/search_result?kw=" + number
        queryTree = self.getHtmlTree(queryUrl)
        results = self.getTreeAll(queryTree, '//div[contains(@class,"row row-cols-2 row-cols-lg-4 g-2 mt-0")]/div/div')
        for i in results:
            title = self.getTreeElement(i, '//div[contains(@class,"oneVideo-body")]/h5/text()')
            detailurl = self.getTreeElement(i, '//div[contains(@class,"oneVideo-top")]/a/@href')
            if title.upper().startswith(number):
                return "https://airav.io" + detailurl
        return None

    def getNum(self, htmltree):
        if self.addtion_Javbus:
            result = self.javbus.get('number')
            if isinstance(result, str) and len(result):
                return result
        number = self.getTreeElement(htmltree, self.expr_number)
        if number:
            return number.strip()
        title = super().getNum(htmltree)
        match = re.search(r'^([A-Z]+-\d+)', title)
        if match:
            return match.group(1)
        return ''

    def getTitle(self, htmltree):
        title = super().getTitle(htmltree)
        match = re.search(r'^[A-Z]+-\d+\s+(.*?)\s+-\s+airav\.io$', title)
        if match:
            return match.group(1).strip()
        title = re.sub(r'^[A-Z]+-\d+\s+', '', title)
        title = re.sub(r'\s+-\s+airav\.io$', '', title)
        return title.strip()

    def getStudio(self, htmltree):
        if self.addtion_Javbus:
            result = self.javbus.get('studio')
            if isinstance(result, str) and len(result):
                return result
        return super().getStudio(htmltree)

    def getRelease(self, htmltree):
        if self.addtion_Javbus:
            result = self.javbus.get('release')
            if isinstance(result, str) and len(result):
                return result
        try:
            return re.search(r'\d{4}-\d{2}-\d{2}', str(super().getRelease(htmltree))).group()
        except:
            return ''

    def getYear(self, htmltree):
        if self.addtion_Javbus:
            result = self.javbus.get('year')
            if isinstance(result, str) and len(result):
                return result
        release = self.getRelease(htmltree)
        return str(re.findall('\d{4}', release)).strip(" ['']")

    def getOutline(self, htmltree):
        return self.getTreeAll(htmltree, self.expr_outline).replace('\n','').strip()

    def getRuntime(self, htmltree):
        if self.addtion_Javbus:
            result = self.javbus.get('runtime')
            if isinstance(result, str) and len(result):
                return result
        return ''

    def getDirector(self, htmltree):
        if self.addtion_Javbus:
            result = self.javbus.get('director')
            if isinstance(result, str) and len(result):
                return result
        return ''

    def getActors(self, htmltree):
        a = super().getActors(htmltree)
        b = [ i.strip() for i in a if len(i)]
        if len(b):
            return b
        if self.addtion_Javbus:
            result = self.javbus.get('actor')
            if isinstance(result, list) and len(result):
                return result
        return []

    def getCover(self, htmltree):
        if self.addtion_Javbus:
            result = self.javbus.get('cover')
            if isinstance(result, str) and len(result):
                return result
        return super().getCover(htmltree)

    def getSeries(self, htmltree):
        series = self.getTreeElement(htmltree, self.expr_series)
        if series and len(series.strip()):
            return series.strip()
        if self.addtion_Javbus:
            result = self.javbus.get('series')
            if isinstance(result, str) and len(result):
                return result
        return ''
