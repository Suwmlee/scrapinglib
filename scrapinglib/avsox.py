# -*- coding: utf-8 -*-

import re
from .parser import Parser


class Avsox(Parser):
    
    source = 'avsox'
    imagecut = 3

    expr_number = '//span[contains(text(),"识别码:")]/../span[2]/text()'
    expr_title = '/html/body/div[2]/h3/text()'
    expr_year = '//span[contains(text(),"发行时间:")]/../text()'
    expr_studio = '//p[contains(text(),"制作商: ")]/following-sibling::p[1]/a/text()'
    expr_release = '//span[contains(text(),"发行时间:")]/../text()'
    expr_cover = '/html/body/div[2]/div[1]/div[1]/a/img/@src'
    expr_smallcover = '//*[@id="waterfall"]/div/a/div[1]/img/@src'
    expr_tags = '/html/head/meta[@name="keywords"]/@content'
    expr_label = '//p[contains(text(),"系列:")]/following-sibling::p[1]/a/text()'
    expr_series = '//span[contains(text(),"系列:")]/../span[2]/text()'

    def queryNumberUrl(self, number):
        qurySiteTree = self.getHtmlTree('https://tellme.pw/avsox')
        site = self.getFirst(qurySiteTree, '//div[@class="container"]/div/a/@href')
        self.searchtree = self.getHtmlTree(site + '/cn/search/' + number)
        result1 = self.getFirst(self.searchtree, '//*[@id="waterfall"]/div/a/@href')
        if result1 == '' or result1 == 'null' or result1 == 'None':
            self.searchtree = self.getHtmlTree(site + '/cn/search/' + number.replace('-', '_'))
            result1 = self.getFirst(self.searchtree, '//*[@id="waterfall"]/div/a/@href')
            if result1 == '' or result1 == 'null' or result1 == 'None':
                self.searchtree = self.getHtmlTree(site + '/cn/search/' + number.replace('_', ''))
                result1 = self.getFirst(self.searchtree, '//*[@id="waterfall"]/div/a/@href')
        return "https:" + result1

    def getNum(self, htmltree):
        new_number = self.getFirst(htmltree, self.expr_number)
        if new_number.upper() != self.number.upper():
            raise ValueError('number not found')
        self.number = new_number
        return new_number

    def getTitle(self, htmltree):
        t = super().getTitle(htmltree).replace('/','').strip(self.number)
        return str(t)

    def getStudio(self, htmltree):
        return super().getStudio(htmltree).replace("', '",' ')

    def getSmallCover(self, htmltree):
        s = self.getFirst(self.searchtree, self.expr_smallcover)
        return s

    def getTags(self, htmltree):
        tags = super().getTags(htmltree).split(',')
        return [i.strip() for i in tags[2:]]  if len(tags) > 2 else []

    def getYear(self, htmltree):
        return re.findall('\d{4}', super().getYear(htmltree))[0]
