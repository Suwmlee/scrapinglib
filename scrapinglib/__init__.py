# -*- coding: utf-8 -*-

# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler
logging.getLogger(__name__).addHandler(NullHandler())

from .scraper import search, getSupportedSources
from .httprequest import HTTP_CLIENT_AUTO, HTTP_CLIENT_REQUESTS, HTTP_CLIENT_CURL_CFFI

# 对外暴露 HTTP 客户端类型常量
__all__ = [
    'search',
    'getSupportedSources',
    'HTTP_CLIENT_AUTO',
    'HTTP_CLIENT_REQUESTS',
    'HTTP_CLIENT_CURL_CFFI',
]
