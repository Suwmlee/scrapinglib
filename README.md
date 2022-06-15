# scrapinglib


## 使用:

```python
from scrapinglib import search

# 搜刮`TMDB`编号`14534`的电影信息
data = search('14534', 'tmdb', type='general')

# 使用代理
proxydict = {
    "http": "socks5h://127.0.0.1:1080",
    "https": "socks5h://127.0.0.1:1080"
}
data = search('14534', 'tmdb', type='general', proxies=proxydict)

```
