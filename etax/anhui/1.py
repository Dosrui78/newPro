# 安徽税局登录
from utils import *
import ddddocr
import types

PATH = 'https://etax.anhui.chinatax.gov.cn'


# 滑块验证码
class Login(Requests):
    def __init__(self) -> None:
        super().__init__()

    def get_uuid(self) -> str:
        # 获取uuid，以供获取滑块验证码图片用
        data = {
            "type": "2",
            "width": "355",
            "height": "200",
            "referer": PATH + "/cas/login",
        }
        res = self.post_request(PATH + "/cas/captcha/conf", data=data)
        if res.status_code == 200:
            d = res.json()
            uuid = d.get("data").get("uuid")
            return uuid

    def get_sources(self) -> tuple:
        """获取验证码图片"""
        uuid = self.get_uuid()
        data = {
            "width": "355",
            "height": "200",
            "type": "2",
            "uuid": uuid,
            "referer": PATH + "/cas/login",
        }
        res = self.post_request(PATH + '/cas/captcha/sources', data=data)
        if res.status_code == 200:
            d = res.json().get("data")
            bg_uri = d.get("bg")
            ft_uri = d.get("ft")
            token = d.get("token")
            return bg_uri, ft_uri, token

    def get_img_content(self, bg, ft) -> tuple:
        res1 = self.get_request(bg)
        res2 = self.get_request(ft)
        return res1.content, res2.content

    def get_distance(self, bg_content, ft_content) -> float:
        """
        :param bg_url: 背景图地址
        :param slice_url: 滑块图地址
        :return: distance
        :rtype: Integer
        """
        slide = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
        result = slide.slide_match(ft_content, bg_content, simple_target=True)
        return result['target'][0]

    def get_check(self, bg_uri, ft_uri, token):
        """检验验证是否通过"""
        data = {
            "data": "f8qqkKD1uQDzs+y34hrudiswBeCG1PAAhsgUxpVVO+PnIxGevUvMvekYqpsJMmTqf9CcEEpSrcgHFC5SriMkiDZSTHwUtcefVWVJZE2v+GIUy1zPuS9ZHxmeXbQY8pkI",
            "uuid": "736b5cf60bce42a7a49e64a33874dbe3",
            "ekey": "XN6QJw1ANtwbuBWVudlvxK0vHEwg05LdyvTXqSbdKQzvCtHyijtAJDfogVbJddP6vUQTJNW/cYoW9Ej9hi1/kw==",
            "iv": "61a128a8bbb1fca8",
            "type": "2",
            "width": "355",
            "height": "200",
            "time": "1664295203451",
            "referer": "https://etax.anhui.chinatax.gov.cn/cas/login"
        }
        res1, res2 = self.get_img_content(bg_uri, ft_uri)
        distance = self.get_distance(res1, res2)
        return distance


login = Login()
bg_uri, ft_uri, token = login.get_sources()
print(login.get_check(bg_uri, ft_uri, token))
