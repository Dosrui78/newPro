import requests
import execjs
import urllib3
from retrying import retry
from faker import Faker
from loguru import logger
from requests.exceptions import ConnectionError
from requests import RequestException

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
__all__ = ['Requests']


class Requests(object):
    def __init__(self):
        self.session = requests.Session()
        self.headers = {'User-Agent': Faker().user_agent()}
        logger.add('./log.log', format="{time:YYYY-MM-DD HH:mm:ss} {level} {message}", level="DEBUG", encoding="utf-8",
                   rotation="10 MB")

    def log(self, text):
        return logger.info(text)

    def execJS(self, filepath, func_name, *args):
        with open(filepath, 'r', encoding='utf8') as f:
            js = f.read()
        ctx = execjs.compile(js)
        if isinstance(args, tuple):
            if len(args) == 1:
                return ctx.call(func_name, args[0])
            if len(args) == 2:
                return ctx.call(func_name, args[0], args[1])
        return ctx.call(func_name)

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
        try:
            res = self.session.get(url, **kwargs)
            if res.status_code == 200:
                res.encoding = 'utf-8'
                self.log(f"请求成功，请求地址：{url}")
                return res
            else:
                self.log(f"请求地址：{url}， 状态码：{res.status_code}")
        except Exception as e:
            self.log(f"请求失败，请求地址：{url}")
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
        try:
            res = self.session.post(url, **kwargs)
            if res.status_code == 200:
                res.encoding = 'utf-8'
                self.log(f"请求成功，请求地址：{url}")
                return res
            else:
                self.log(f"请求地址：{url}， 状态码：{res.status_code}")
        except Exception as e:
            self.log(f"请求失败，请求地址：{url}")
            raise e
