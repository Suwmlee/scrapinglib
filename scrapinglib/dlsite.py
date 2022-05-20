# -*- coding: utf-8 -*-

import re
from lxml import etree
from .parser import Parser


class Dlsite(Parser):
    source = 'dlsite'
    imagecut = 0

    expr_title = '/html/head/title/text()'
    expr_actor = '//th[contains(text(),"声优")]/../td/a/text()'
    expr_studio = '//th[contains(text(),"系列名")]/../td/span[1]/a/text()'
    expr_studio2 = '//th[contains(text(),"社团名")]/../td/span[1]/a/text()'
    expr_outline = '//*[@class="work_parts_area"]/p/text()'
    expr_series = '//th[contains(text(),"系列名")]/../td/span[1]/a/text()'
    expr_series2 = '//th[contains(text(),"社团名")]/../td/span[1]/a/text()'
    expr_director = '//th[contains(text(),"剧情")]/../td/a/text()'
    expr_release = '//th[contains(text(),"贩卖日")]/../td/a/text()'
    expr_cover = '//*[@id="work_left"]/div/div/div[2]/div/div[1]/div[1]/ul/li[1]/picture/source/@srcset'
    expr_tags = '//th[contains(text(),"分类")]/../td/div/a/text()'
    expr_label = '//th[contains(text(),"系列名")]/../td/span[1]/a/text()'
    expr_label2 = '//th[contains(text(),"社团名")]/../td/span[1]/a/text()'

    def search(self, number, core: None):
        self.number = number.upper()
        self.updateCore(core)

        self.detailurl = 'https://www.dlsite.com/maniax/work/=/product_id/' + number + '.html/?locale=zh_CN'
        self.cookies = {'locale': 'zh-cn'}

        htmltree = self.getHtmlTree(self.detailurl)
        result = self.dictformat(htmltree)
        return result

    def getNum(self, htmltree):
        return self.number

    def getTitle(self, htmltree):
        result = super().getTitle(htmltree)
        result = result[:result.rfind(' | DLsite')]
        result = result[:result.rfind(' [')]
        return result

    def getOutline(self, htmltree):
        total = []
        result = self.getAll(htmltree, self.expr_outline)
        for i in result:
            total.append(i.strip('\r\n'))
        return str(total).strip(" ['']").replace("', '', '",r'\n').replace("', '",r'\n').strip(", '', '")

    def getRelease(self, htmltree):
        return super().getRelease(htmltree).replace('年','-').replace('月','-').replace('日','')

    def getCover(self, htmltree):
        return 'https:' + super().getCover(htmltree).replace('.webp', '.jpg')

    def getTags(self, htmltree):
        return self.getAll(htmltree, self.expr_tags)

    def getYear(self, htmltree):
        try:
            release = self.getRelease(htmltree)
            result = str(re.search('\d{4}', release).group())
            return result
        except:
            return release
