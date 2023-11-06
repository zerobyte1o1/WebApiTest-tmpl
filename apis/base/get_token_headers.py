from apis.base.base_api import BaseApi
from apis.base.login import Login


class GetTokenHeader(BaseApi):
    def __init__(self, api_root_url, **kwargs):
        super(GetTokenHeader, self).__init__(api_root_url, **kwargs)
        self.get_token()

    def get_token(self):
        Login(BaseApi.url).login_api()


if __name__ == '__main__':
    pass
