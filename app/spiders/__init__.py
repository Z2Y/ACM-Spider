import settings
from bs4 import BeautifulSoup
from tornado import gen, httpclient
from tornado.queues import Queue
from app.logger import logger
from app.exceptions import LoadPageException

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.3; WOW64)AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/51.0.2704.103 Safari/537.36'


# 数据缓存池
DataPool = Queue(maxsize=settings.DATA_POOL_SIZE)


class DataType:
    Submit = 0
    Code = 1


class HttpMethod:
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'


class Spider:
    TAG = '[BASE]'

    def __init__(self):
        pass

    def __repr__(self):
        return '<{}Spider>'.format(self.TAG)

    @staticmethod
    def fetch(url, callback=None, raise_error=True, **kwargs):
        http_client = httpclient.AsyncHTTPClient()
        return http_client.fetch(url, callback=callback, raise_error=raise_error,
                                 user_agent=USER_AGENT, **kwargs)

    @staticmethod
    def get_bs4(markup, parser):
        return BeautifulSoup(markup, parser)

    @staticmethod
    def get_lxml_bs4(markup):
        return BeautifulSoup(markup, 'lxml')

    @staticmethod
    @gen.coroutine
    def load_page(url, headers=None):
        response = None
        try:
            response = yield Spider.fetch(url, headers=headers)
        except httpclient.HTTPError as ex:
            logger.error('加载 {} 失败: {}'.format(url, ex))
            raise LoadPageException('加载 {} 失败: {}'.format(url, ex))
        finally:
            return response

    @staticmethod
    @gen.coroutine
    def put_queue(item_list):
        for item in item_list:
            if 'account' in item:
                yield DataPool.put(item)

    @gen.coroutine
    def run(self):
        raise Exception('Not Implemented!')


