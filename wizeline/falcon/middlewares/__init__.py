# flake8: noqa
__version__ = '1.0.0'

from wizeline.falcon.middlewares.secret import APISecretMiddleware, require_secret
from wizeline.falcon.middlewares.json import JSONMiddleware
