import sys

import requests
from retrying import retry
from faker import Faker
from loguru import logger
from requests.exceptions import ConnectionError

__all__ = ['Requests']


class Requests(object):
    def __init__(self):
        self.session = requests.Session()
        self.headers = {'User-Agent': Faker().user_agent()}
        logger.add('./log.log', format="{time:YYYY-MM-DD HH:mm:ss} {level} {message}", level="DEBUG")
        self.log = logger

    @retry(stop_max_attempt_number=3, wait_fixed=2000, retry_on_result=lambda x: x is None)
    def get_request(self, url, **kwargs):
        """
        发送get请求
        :param url: 请求地址
        """
        kwargs.setdefault('timeout', 10)
        kwargs.setdefault('verify', False)
        kwargs.setdefault('headers', self.headers)
        kwargs.setdefault('allow_redirects', False)
        for retryCount in range(1, 6):
            try:
                res = self.session.get(url, **kwargs)
                if res.status_code == 200:
                    res.encoding = 'utf-8'
                    self.log.info(f"第{retryCount}次请求成功，请求地址：{url}")
                    return res
                else:

                    self.log.info(f"第{retryCount}次请求失败，请求地址：{url}")
                    continue
            except Exception as e:
                # self.log.error(f"第{retryCount}次请求失败，请求地址：{url}")
                raise e

    @retry(stop_max_attempt_number=3, wait_fixed=2000, retry_on_result=lambda x: x is None)
    def post_request(self, url, **kwargs):
        """
        发送get请求
        :param url: 请求地址
        """
        kwargs.setdefault('timeout', 10)
        kwargs.setdefault('verify', False)
        kwargs.setdefault('headers', self.headers)
        kwargs.setdefault('allow_redirects', False)
        for retryCount in range(1, 6):
            try:
                res = self.session.post(url, **kwargs)
                if res.status_code == 200:
                    res.encoding = 'utf-8'
                    self.log.info(f"第{retryCount}次请求成功，请求地址：{url}")
                    return res
                else:
                    self.log.info(f"第{retryCount}次请求失败，请求地址：{url}")
                    continue
            except Exception as e:
                # self.log.error(f"第{retryCount}次请求失败，请求地址：{url}")
                raise ConnectionError
