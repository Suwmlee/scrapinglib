# -*- coding: utf-8 -*-

# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler
logging.getLogger(__name__).addHandler(NullHandler())

from .api import search, getSupportedSources
