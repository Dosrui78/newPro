import time
import requests
import execjs
import urllib3
from retrying import retry
from faker import Faker
from loguru import logger

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
__all__ = ['Requests', 'Result']

__result__code = {
    200: "成功",
    417: "请求超时",
    600: "请求异常",
    400: "请求出现语法错误",
    401: "没有访问权限",
    403: "服务器拒绝执行该请求",
    404: "指定的页面不存在",
    405: "请求方法对指定的资源不适用",
    406: "客户端无法接受相应数据",
    408: "等待请求时服务器超时",
    409: "请求与当前资源的状态冲突，导致请求无法完成",
    410: "请求的资源已不存在，并且没有转接地址",
    500: "服务器尝试执行请求时遇到了意外情况",
    501: "服务器不具备执行该请求所需的功能",
    502: "网关或代理服务器从上游服务器收到的响应无效",
    503: "服务器暂时无法处理该请求",
    504: "在等待上游服务器响应时，网关或代理服务器超时",
    505: "服务器不支持请求中所用的 HTTP 版本",
    1: "无法解析服务器的 DNS 地址",
    2: "连接失败",
    -7: "操作超时",
    -100: "服务器意外关闭了连接",
    -101: "连接已重置",
    -102: "服务器拒绝了连接",
    -104: "无法连接到服务器",
    -105: "无法解析服务器的 DNS 地址",
    -109: "无法访问该服务器",
    -138: "无法访问网络",
    -130: "代理服务器连接失败",
    -106: "互联网连接已中断",
    -401: "从缓存中读取数据时出现错误",
    -400: "缓存中未找到请求的条目",
    -331: "网络 IO 已暂停",
    -6: "无法找到该文件或目录",
    -310: "重定向过多",
    -324: "服务器已断开连接，且未发送任何数据",
    -346: "收到了来自服务器的重复标头",
    -349: "收到了来自服务器的重复标头",
    -350: "收到了来自服务器的重复标头",
    -118: "连接超时"
}


def Result(code, msg=None):
    return code, msg or __result__code.get(code, '')

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
        kwargs.setdefault('proxies', {'http': None, 'https': None})
        try:
            res = self.session.get(url, **kwargs)
            # print(retrying.Attempt(2))
            res.encoding = res.apparent_encoding
            if res.status_code == 200:
                self.log(f"get请求成功，请求地址：{url}")
                return res
            else:
                start_time = time.time()
                res = self.session.post(url, **kwargs)
                self.log(f"get请求地址：{url}， 状态码：{res.status_code}， 直接get请求时间：{time.time() - start_time}")
                return res
        except Exception as e:
            self.log(f"get请求失败，请求地址：{url}")
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
        kwargs.setdefault('proxies', {'http': None, 'https': None})
        try:
            res = self.session.post(url, **kwargs)
            res.encoding = res.apparent_encoding
            if res.status_code == 200:
                self.log(f"post请求成功，请求地址：{url}")
                return res
            else:
                start_time = time.time()
                res = self.session.post(url, **kwargs)
                self.log(f"post请求地址：{url}， 状态码：{res.status_code}， 直接post请求时间：{time.time() - start_time}")
                return res
        except Exception as e:
            self.log(f"post请求失败，请求地址：{url}")
            raise e

# Test = Requests()
# Test.get_request('https://www.baidu.com/')
