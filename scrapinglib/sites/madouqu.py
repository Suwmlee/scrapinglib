# -*- coding: utf-8 -*-

import re
from lxml import etree
from urllib.parse import urlparse, unquote
from ..base_scraper import BaseScraper


class Madouqu(BaseScraper):
    source = 'madouqu'
    content_type = 'adult'
    priority = 80

    expr_title = "//h1[@class='entry-title']/text()"
    expr_studio = '//span[@class="meta-category"]//i[@class="dot"]/following-sibling::text()'
    expr_tags = '/html/head/meta[@name="description"]/@content'
    expr_cover = '//meta[@property="og:image"]/@content'
    expr_actor = '//p[contains(., "麻豆女郎")]/text()'

    def extraInit(self):
        self.imagecut = 4
        self.uncensored = True
        self.allow_number_change = True

    def search(self, number):
        if self.specifiedUrl:
            self.detailurl = self.specifiedUrl
        else:
            self.detailurl = f"https://madouqu.com/video/{number}/"
        
        self.htmlcode = self.getHtml(self.detailurl)
        if self.htmlcode == 404:
            return 404
        htmltree = etree.fromstring(self.htmlcode, etree.HTMLParser())

        result = self.dictformat(htmltree)
        return result

    def getNum(self, htmltree):
        try:
            # Extract from URL
            filename = unquote(urlparse(self.detailurl).path)
            # Remove trailing slash and video/ prefix
            result = filename.replace('/video/', '').replace('/', '').strip()
            return result
        except:
            return ''

    def getTitle(self, htmltree):
        # Get title from h1.entry-title element
        return self.getTreeElement(htmltree, self.expr_title).strip()

    def getStudio(self, htmltree):
        # Get studio from the text inside meta-category span
        try:
            studio_text = self.getTreeElement(htmltree, self.expr_studio)
            if studio_text:
                return studio_text.strip()
            # Fallback to category link text if needed
            category_text = self.getTreeElement(htmltree, '//span[@class="meta-category"]//a/text()')
            if category_text:
                return category_text.strip()
        except:
            pass
        return "麻豆传媒"

    def getActors(self, htmltree) -> list:
        try:
            actor_text = self.getTreeElement(htmltree, self.expr_actor)
            if '：' in actor_text:
                actor = actor_text.split('：')[1].strip()
                return [actor]
        except:
            pass
        return []

    def getCover(self, htmltree):
        try:
            url = self.getTreeElement(htmltree, self.expr_cover)
            return url.strip()
        except:
            return ''

    def getTags(self, htmltree):
        studio = self.getStudio(htmltree)
        tags = super().getTags(htmltree)
        # Extract tags from meta description and filter out studio
        return [tag for tag in tags if studio not in tag and '麻豆' not in tag] 