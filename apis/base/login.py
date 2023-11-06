import json

from base_api import BaseApi
from utils.encrypt import encrpt


class Login(BaseApi):
    def __init__(self, api_root_url, **kwargs):
        super(Login, self).__init__(api_root_url, **kwargs)

    def cipher_api(self):
        """
        请求公钥接口
        :return:
        """
        res = self.get('account/login/cipher')
        return res

    def login_api(self):
        """
        登录接口
        :return:
        """
        cipher_res = json.loads(self.cipher_api().text)
        headers = {'accept': 'application/json, text/plain, */*', 'Content-Type': 'application/json'}
        key = cipher_res['data']['publicKeyStr']
        password = encrpt(BaseApi.password, key)
        data = {"loginCode": BaseApi.account,
                "loginType": "CYPHER",
                "passwd": password,
                "random": cipher_res['data']['random']}
        return self.post('account/login/doLogin', json=data, headers=headers)


if __name__ == '__main__':
    res = Login('https://api.shifang.co/').login_api()
    print(res.text)
