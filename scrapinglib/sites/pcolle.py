# -*- coding: utf-8 -*-

import re
from ..base_scraper import BaseScraper


class Pcolle(BaseScraper):
    source = 'pcolle'
    content_type = 'adult'
    priority = 80

    expr_title = '//th[contains(text(),"商品名")]/../td/text()'
    expr_studio = '//th[contains(text(),"販売会員")]/../td/a/text()'
    expr_label = '//th[contains(text(),"販売会員")]/../td/a/text()'
    expr_release = '//th[contains(text(),"販売開始日")]/../td/text()'
    expr_tags = '//section[contains(@class,"item_tags")]//a[not(@rel)]/text()'
    expr_uservotes = '//th[contains(text(),"合計評価数")]/../td/text()'
    expr_cover = '//a[@rel="lightbox[images]" and not(contains(@href,"sub_"))]/@href'
    expr_extrafanart = '//a[@rel="lightbox[images]" and contains(@href,"sub_")]/@href'

    def extraInit(self):
        self.imagecut = 0

    def search(self, number: str):
        self.number = re.sub(r'(?i)^PCOLLE-', '', number)
        if self.specifiedUrl:
            self.detailurl = self.specifiedUrl
        else:
            self.detailurl = 'https://www.pcolle.com/product/detail/?product_id=' + self.number
        htmltree = self.getHtmlTree(self.detailurl)
        result = self.dictformat(htmltree)
        return result

    def getNum(self, htmltree):
        num = self.getTreeElement(htmltree, '//th[contains(text(),"商品ID")]/../td/text()')
        return 'PCOLLE-' + num

    def getRelease(self, htmltree):
        release = super().getRelease(htmltree)
        m = re.search(r'(\d{4})年(\d{2})月(\d{2})日', release)
        if m:
            return f'{m.group(1)}-{m.group(2)}-{m.group(3)}'
        return release

    def getOutline(self, htmltree):
        texts = self.getTreeAll(htmltree, '//section[contains(@class,"item_description")]//text()')
        lines = [t.strip() for t in texts if t.strip() and t.strip() != '商品説明']
        return '\n'.join(lines)
