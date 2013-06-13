from urllib import quote_plus
from urlparse import urljoin

import requests


METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']


class Method(object):

    def __init__(self, method, url, auth):
        self.method = getattr(requests, method.lower())
        self.url = url
        self.auth = auth

    def __call__(self, **kwargs):
        return self.method(
            self.url,
            auth=self.auth,
            headers={
                'Accept': 'application/json',
            },
            data=kwargs,
        )


class EndPoint(object):

    def __init__(self, api, url):
        self.api = api
        self.url = url

    def __getitem__(self, item):
        url = self.url + '/' if not self.url.endswith('/') else self.url
        return EndPoint(
            self.api,
            urljoin(url, quote_plus(unicode(item))),
        )

    def __getattr__(self, attr):
        if attr in METHODS:
            return Method(
                method=attr,
                url=self.url,
                auth=self.api.auth,
            )
        return self[attr]


class Api(EndPoint):

    def __init__(self, base_url, auth=None):
        super(Api, self).__init__(self, base_url)
        self.auth = auth

    def __call__(self, url):
        self.url = url
        return self
