from apis.base.get_token import GetToken

class User(GetToken):
    def logout_api(self):
        return self.get("account/logout")


if __name__ == '__main__':
    res=User().logout_api()
    print(res.text)