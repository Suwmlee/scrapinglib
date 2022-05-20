# -*- coding: utf-8 -*-

import re
from lxml import etree
from bs4 import BeautifulSoup
from .parser import Parser


class Mgstage(Parser):
    source = 'mgstage'

    expr_number = '//th[contains(text(),"品番：")]/../td/a/text()'
    expr_title = '//*[@id="center_column"]/div[1]/h1/text()'
    expr_studio = '//th[contains(text(),"メーカー：")]/../td/a/text()'
    expr_outline = '//p/text()'
    expr_runtime = '//th[contains(text(),"収録時間：")]/../td/a/text()'
    expr_director = '//th[contains(text(),"シリーズ")]/../td/a/text()'
    expr_actor = '//th[contains(text(),"出演：")]/../td/a/text()'
    expr_release = '//th[contains(text(),"配信開始日：")]/../td/a/text()'
    expr_cover = '//*[@id="EnlargeImage"]/@href'
    expr_label = '//th[contains(text(),"シリーズ：")]/../td/a/text()'
    expr_tags = '//th[contains(text(),"ジャンル：")]/../td/a/text()'
    expr_tags2 = '//th[contains(text(),"ジャンル：")]/../td/text()'
    expr_year = '//th[contains(text(),"配信開始日：")]/../td/a/text()'
    expr_series = '//th[contains(text(),"シリーズ")]/../td/a/text()'

    def search(self, number, core: None):
        self.number = number.upper()
        self.updateCore(core)

        self.cookies = {'adc':'1'}
        self.detailurl = 'https://www.mgstage.com/product/product_detail/'+str(self.number)+'/'
        self.htmlcode = self.getHtml(self.detailurl)

        soup = BeautifulSoup(self.htmlcode, 'lxml')
        self.detailpage = str(soup.find(attrs={'class': 'detail_data'})).replace('\n                                        ','').replace('                                ','').replace('\n                            ','').replace('\n                        ','')
        b2 = str(soup.find(attrs={'id': 'introduction'})).replace('\n                                        ','').replace('                                ','').replace('\n                            ','').replace('\n                        ','')
        self.htmlcodetree = etree.HTML(self.htmlcode)
        self.detailtree = etree.HTML(self.detailpage)
        self.introtree = etree.HTML(b2)

        result = self.dictformat(self.detailtree)
        return result

    def getTitle(self, htmltree):
        return super().getTitle(self.htmlcodetree).replace('/', ',').replace("\\n",'').replace('        ', '').strip()

    def getOutline(self, htmltree):
        return super().getOutline(self.introtree).strip(" ['']").replace(u'\\n', '').replace("', '', '", '')

    def getRuntime(self, htmltree):
        return super().getRuntime(htmltree).rstrip('mi')

    def getRelease(self, htmltree):
        return super().getRelease(htmltree).replace('/','-')

    def getCover(self, htmltree):
        return super().getCover(self.htmlcodetree)

    def getTags(self, htmltree):
        html = etree.fromstring(self.detailpage, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
        result1 = str(self.getAll(html, self.expr_tags)).strip(" ['']").strip('\\n    ').strip('\\n')
        result2 = str(self.getAll(html, self.expr_tags2)).strip(" ['']").strip('\\n    ').strip('\\n')
        result = str(result1 + result2).strip('+').replace("', '\\n",",").replace("', '","").replace('"','').replace(',,','').split(',')
        return result

    def getExtrafanart(self, htmltree):
        html_pather = re.compile(r'<dd>\s*?<ul>[\s\S]*?</ul>\s*?</dd>')
        html = html_pather.search(self.htmlcode)
        if html:
            html = html.group()
            extrafanart_pather = re.compile(r'<a class=\"sample_image\" href=\"(.*?)\"')
            extrafanart_imgs = extrafanart_pather.findall(html)
            if extrafanart_imgs:
                return extrafanart_imgs
        return ''

    def getYear(self, htmltree):
        y = super().getYear(htmltree)
        return str(re.findall('\d{4}', y)).strip(" ['']"),


    def getTreeIndex(self, tree, expr, index=0):
        if expr == '':
            return ''
        if tree == self.detailtree:
            result1 = str(tree.xpath(expr)).strip(" ['']").strip('\\n    ').strip('\\n').strip(" ['']").replace(u'\\n', '').replace("', '', '", '')
            result2 = str(tree.xpath(expr.replace('td/a/','td/'))).strip(" ['']").strip('\\n    ').strip('\\n')
            return str(result1 + result2).strip('+').replace("', '",'').replace('"','')
        else:
            result = tree.xpath(expr)
            try:
                return result[index]
            except:
                return ''
