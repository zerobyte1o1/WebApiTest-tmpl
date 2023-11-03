from apis.base.base_api import BaseApi
import requests

class GetTokenHeader(BaseApi):
    def __init__(self, **kwargs):
        """
        如果传回账号密码，则更新账号header
        :param kwargs:
        """
        super().__init__()
        if kwargs:
            self.headers = self.get_headers(account=kwargs["account"],
                                            password=kwargs["password"]
                                           )
        else:
            self.headers = self.get_headers()

    def get_token(self, account=BaseApi.account, password=BaseApi.password):
        headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
        print(account)
        url="https://api.shifang.co/account/login/doLogin"
        data={"loginCode":account,
              "loginType":"CYPHER",
              "password":password,
              "random":1698907864626}
        res=requests.post(url,data=data,headers=headers)
        print(res.json())
        token = "Bearer " + res.token
        return token

    def get_headers(self, account=BaseApi.account, password=BaseApi.password):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        headers.setdefault("authorization", self.get_token(account, password))
        return headers


if __name__ == '__main__':
    a = GetTokenHeader()
    res = a.get_token()
    print(res)
