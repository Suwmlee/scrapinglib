
from http.cookies import SimpleCookie
import sys
import json
import logging
sys.path.insert(0,'../scrapinglib')
from scrapinglib import getSupportedSources
from scrapinglib import search as orignal_search

def load_cookies(rawcookie):
    cookie = SimpleCookie()
    cookie.load(rawcookie)
    cookies = {}
    for key, morsel in cookie.items():
        cookies[key] = morsel.value
    return cookies


proxydict = {
    "http": "socks5h://127.0.0.1:1080",
    "https": "socks5h://127.0.0.1:1080"
}


def search(number, source=None, **kwargs):
    """ test
    """
    logging.basicConfig(level=logging.DEBUG)
    data = orignal_search(number, source, **kwargs)
    beaty = json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':'))
    return beaty

# NOTE: 浏览器内鼠标选取复制,不是右键`copy value`
# javdb仅VIP才能浏览fc2等页面，因此使用cookies刮削fc2的方式不可行了
# cookies_copy = "theme=auto; locale=zh; _ym_d=1645511085; _ym_uid=1645511085939221453; over18=1; list_mode=h; _ym_isad=1; hide_app_banner=1"
# cookies = load_cookies(cookies_copy)


sources = getSupportedSources()
print(f"supported sources: {sources}")

# print(search('012717_472', 'avsox', proxies=proxydict))
# print(search('FC2-PPV-2848294', 'avsox', proxies=proxydict))
# print(search('012717_472', specifiedSource='avsox', specifiedUrl='https://avsox.click/cn/movie/32628c999f07a942', proxies=proxydict))

# print(search('STAR-438', 'javbus', proxies=proxydict))
# print(search('ABP-960', 'javbus', proxies=proxydict, morestoryline=True))
# print(search('MMNT-010', 'javbus', proxies=proxydict))
# print(search('ipx-292', 'javbus', proxies=proxydict))
# print(search('CEMD-011', 'javbus', proxies=proxydict))
# print(search('CJOD-278', 'javbus', proxies=proxydict))
# print(search('BrazzersExxtra.21.02.01', 'javbus', proxies=proxydict))
# print(search('100221_001', 'javbus', proxies=proxydict))
# print(search('AVSW-061', 'javbus', proxies=proxydict))
# print(search('AVSW-061', specifiedSource='javbus', specifiedUrl='https://www.buscdn.fun/AVSW-061', proxies=proxydict))

# print(search('RCTD-288', 'xcity', proxies=proxydict))
# print(search('VNDS-2624', 'xcity', proxies=proxydict))
# print(search('ABP-988', 'xcity', proxies=proxydict))
# print(search('ABW-179', specifiedSource='xcity', specifiedUrl='https://xcity.jp/avod/detail/?id=169480', proxies=proxydict))

# print(search('SIRO-4149', 'mgstage', proxies=proxydict))
# print(search('ABW-246', 'mgstage', proxies=proxydict))
# print(search('390JNT-044', 'mgstage', proxies=proxydict))
# print(search('SIRO-4149', specifiedSource='mgstage', specifiedUrl='https://www.mgstage.com/product/product_detail/SIRO-4149/', proxies=proxydict))

# print(search('MD0129', 'madou', proxies=proxydict))
# print(search('TM0002', 'madou', proxies=proxydict))
# print(search('MD0222', 'madou', proxies=proxydict))
# print(search('MD0140-2', 'madou', proxies=proxydict))
# print(search('MAD039', 'madou', proxies=proxydict))
# print(search('JDMY027', 'madou', proxies=proxydict))
# print(search('MAD039', specifiedSource='madou', specifiedUrl='https://madou.club/mad039-%e6%9c%ba%e7%81%b5%e5%8f%af%e7%88%b1%e5%b0%8f%e5%8f%ab%e8%8a%b1-%e5%bc%ba%e8%af%b1%e5%83%a7%e4%ba%ba%e8%bf%ab%e7%8a%af%e8%89%b2%e6%88%92.html', proxies=proxydict))

# print(search('FC2-2903008', 'fc2', proxies=proxydict))
# print(search('FC2-2182382', 'fc2', proxies=proxydict))
# print(search('FC2-607854', 'fc2', proxies=proxydict))
# print(search('FC2-2787433', 'fc2', proxies=proxydict))
# print(search('FC2-2787433', specifiedSource='fc2', specifiedUrl='https://adult.contents.fc2.com/article/2787433/', proxies=proxydict))

# print(search('VJ013178', 'dlsite', proxies=proxydict))
# print(search('RJ329607', 'dlsite', proxies=proxydict))
# print(search('RJ167911', 'dlsite', proxies=proxydict))  # 打折标签 50% OFF
# print(search('牝教師4～穢された教壇～ 「生意気ドジっ娘女教師・美結～高飛車ハメ堕ち2濁金」', 'dlsite', proxies=proxydict))
# print(search('RJ329607', specifiedSource='dlsite', specifiedUrl='https://www.dlsite.com/maniax/work/=/product_id/RJ329607.html/?locale=zh_CN', proxies=proxydict))

# print(search('jul-404', 'jav321', proxies=proxydict))
# print(search('jul-401', 'jav321', proxies=proxydict))
# print(search('sivr-160', 'jav321', proxies=proxydict))
# print(search('sivr-160', specifiedSource='jav321', specifiedUrl='https://www.jav321.com/video/sivr00160', proxies=proxydict))

# print(search("pred00251", 'fanza', proxies=proxydict))
# print(search("MIAA-391", 'fanza', proxies=proxydict))
# print(search("OBA-326", 'fanza', proxies=proxydict))
# print(search("POW-044", 'fanza', proxies=proxydict))
# print(search("POW023", 'fanza', proxies=proxydict))
# print(search('POW023', specifiedSource='fanza', specifiedUrl='https://www.dmm.co.jp/digital/videoc/-/detail/=/cid=pow023', proxies=proxydict))

# print(search('ADV-R0624', 'airav', proxies=proxydict))  # javbus页面返回404, airav有数据
# print(search('ADN-188', 'airav', proxies=proxydict))    # 一人
# print(search('CJOD-278', 'airav', proxies=proxydict))   # 多人 javbus演员名称采用日语假名，airav采用日文汉字
# print(search('SPRD-1005', 'airav', proxies=proxydict))  # 剧照
# print(search('SPRD-1005', specifiedSource='airav', specifiedUrl='https://cn.airav.wiki/video/SPRD-1005', proxies=proxydict))

# print(search("070116-197", 'carib', proxies=proxydict)) # actor have photo
# print(search("041721-001", 'carib', proxies=proxydict))
# print(search("080520-001", 'carib', proxies=proxydict))
# print(search('080520-001', specifiedSource='carib', specifiedUrl='https://www.caribbeancom.com/moviepages/080520-001/index.html', proxies=proxydict))

# print(search('91CM-121', 'mv91', proxies=proxydict))
# print(search('91CM-122', 'mv91', proxies=proxydict))
# print(search('91CM-143', 'mv91', proxies=proxydict))
# print(search('91MS-006', 'mv91', proxies=proxydict))
# print(search('91MS-006', specifiedSource='mv91', specifiedUrl='https://www.91mv.org/index/detail?id=108J9W', proxies=proxydict))

# print(search('GCOLLE-840724', 'gcolle', proxies=proxydict))
# print(search('840724', 'gcolle', proxies=proxydict))
# print(search('840386', 'gcolle', proxies=proxydict))
# print(search('838671', 'gcolle', proxies=proxydict))
# print(search('814179', 'gcolle', proxies=proxydict))
# print(search('834255', 'gcolle', proxies=proxydict))
# print(search('834255', specifiedSource='gcolle', specifiedUrl='https://gcolle.net/product_info.php/products_id/834255', proxies=proxydict))

# print(search('AGAV-042', 'javdb', proxies=proxydict, dbsite='javdb40'))
# print(search('BANK-022', 'javdb', proxies=proxydict))
# print(search('070116-197', 'javdb', proxies=proxydict))
# print(search('093021_539', 'javdb', proxies=proxydict))  # 没有剧照 片商pacopacomama
# print(search('4030-2405', 'javdb', proxies=proxydict))   # 番号不全
# print(search('heydouga-4030-2405', 'javdb', proxies=proxydict))
# print(search('SIRO-4042', 'javdb', proxies=proxydict))
# print(search('FC2-2278260', 'javdb', proxies=proxydict, dbcookies=cookies))
# print(search('FC2-735670', 'javdb', proxies=proxydict))
# print(search('FC2-1174949', 'javdb', proxies=proxydict)) # not found
# print(search('MVSD-439', 'javdb', proxies=proxydict))
# print(search('EHM0001', 'javdb', proxies=proxydict)) # not found
# print(search('FC2-2314275', 'javdb', proxies=proxydict))
# print(search('EBOD-646', 'javdb', proxies=proxydict))
# print(search('LOVE-262', 'javdb', proxies=proxydict))
# print(search('ABP-890', 'javdb', proxies=proxydict))
# print(search('blacked.14.12.08', 'javdb', proxies=proxydict))
# print(search('EBOD-646', specifiedSource='javdb', specifiedUrl='https://javdb.com/v/DY484', proxies=proxydict))

# print(search('item4039214', 'getchu', proxies=proxydict))       # GETCHU-4039214 https://dl.getchu.com/i/item4039214
# print(search('GETCHU-4039214', 'getchu', proxies=proxydict))
# print(search('お兄ちゃん、朝までずっとギュッてして！ 女未すみ編', 'getchu', proxies=proxydict)) # GETCHU-1139198 http://www.getchu.com/soft.phtml?id=1139198
# print(search('GETCHU-1139198', 'getchu', proxies=proxydict))
# print(search('GETCHU-1139198', specifiedSource='getchu', specifiedUrl='http://www.getchu.com/soft.phtml?id=1139198', proxies=proxydict))

# print(search('IPX-292', 'javlibrary', proxies=proxydict))
# print(search('STAR-438', 'javlibrary', proxies=proxydict, morestoryline=True))
# print(search('SNIS-003', 'javlibrary', proxies=proxydict, morestoryline=True))
# print(search('n1403', 'javlibrary', proxies=proxydict))   # not found
# print(search('SSNI-468', 'javlibrary', proxies=proxydict))
# print(search('SSNI-468', specifiedSource='javlibrary', specifiedUrl='https://www.javlibrary.com/cn/?v=javli7zkyu', proxies=proxydict))

# print(search('EBOD-646', proxies=proxydict))

# print(search('14534', 'tmdb', type='general'))
# print(search('526896', 'tmdb', type='general'))
# print(search('the dark knight', 'tmdb', type='general'))
# print(search('14534', specifiedSource='tmdb', specifiedUrl='https://www.themoviedb.org/movie/14534?language=zh-CN', type='general'))

# print(search('tt0468569', 'imdb', type='general'))
# print(search('tt0108002', 'imdb', type='general'))
# print(search('tt0108002', specifiedSource='imdb', specifiedUrl='https://www.imdb.com/title/tt0108002', type='general'))
