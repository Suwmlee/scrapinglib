# -*- coding: utf-8 -*-


from urllib.parse import quote, urljoin
from .parser import Parser


class Tmdb(Parser):
    """
    两种实现,带apikey与不带key
    apikey
    """
    source = 'tmdb'

    expr_title = '//head/meta[@property="og:title"]/@content'
    expr_release = '//div/span[@class="release"]/text()'
    expr_cover = '//head/meta[@property="og:image"]/@content'
    expr_outline = '//head/meta[@property="og:description"]/@content'

    def extraInit(self):
        imagecut = 0
        apikey = None

    def queryNumberUrl(self, number: str):
        """ 区分 ID 与 名称
        """
        if number.isdigit():
            id  = number
            detailurl = "https://www.themoviedb.org/movie/" + id + "?language=zh-CN"
        else:
            queryUrl = "https://www.themoviedb.org/search?query=" + quote(number, encoding="utf8") + "&language=zh-CN"
            queryTree = self.getHtmlTree(queryUrl)
            cardsexpr = '//div[@class="card v4 tight"]/div/div[2]/div/div/div/a'
            cardselement = self.getTreeAll(queryTree, cardsexpr)
            # 获取所有结果列表，最小到a标签，h2为标题，href为url
            # cardselement[0].xpath('@href') / cardselement[0].xpath('h2/text()')
            if len(cardselement):
                firstUrl = self.getTreeElement(cardselement[0], '@href')
                detailurl = urljoin("https://www.themoviedb.org", firstUrl)
            else:
                raise Exception("TMDB: Can't find detail page URL")
        return detailurl


    def getCover(self, htmltree):
        return "https://www.themoviedb.org" + self.getTreeElement(htmltree, self.expr_cover)

