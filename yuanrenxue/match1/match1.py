from utils import *


class M1(Requests):
    def __init__(self):
        super().__init__()
        self.uri = 'https://match.yuanrenxue.com/api/match/1'

    def main(self):
        self.headers.update({
            "Accept-encoding": "gzip, deflate, br",
            "Referer": "https://match.yuanrenxue.com/match/1",
            'User-Agent': 'yuanrenxue.project',
        })

        sum = 0
        count = 0
        for i in range(1, 6):
            param_data = self.execJS('match1.js', 'M1', i)
            res = self.get_request(self.uri, params=param_data, headers=self.headers)
            if res.status_code == 200:
                data = res.json().get('data')
                count += len(data)
                for dat in data:
                    sum += dat.get('value')
        self.log("5页机票总和：{}，平均值：{}".format(sum, int(sum/count)))



MM = M1()
MM.main()
