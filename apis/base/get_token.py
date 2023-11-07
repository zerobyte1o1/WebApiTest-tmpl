from apis.base.base_api import BaseApi
from apis.base.login import Login


class GetToken(BaseApi):

    def __init__(self, api_root_url=BaseApi.url, **kwargs):
        super(GetToken, self).__init__(api_root_url, **kwargs)
        self.get_token()

    def get_token(self):
        """
        添加token
        :return:
        """
        res=Login(BaseApi.url).login_api()
        token=res.json()["data"]["tokenValue"]
        header_token={
            "Authorization":"Bearer "+token
        }
        self.session.headers.update(header_token)

if __name__ == '__main__':
    pass
