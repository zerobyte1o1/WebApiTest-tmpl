import os

import yaml


class Env:
    rootPath = os.path.dirname(os.path.abspath(__file__))
    configPath = os.path.join(rootPath, "env.yaml")
    env = yaml.safe_load(open(configPath))
    url = "env"

    def get_env(self):
        url_new = self.url.replace("env", self.env["env"][self.env["default"]]["name"])
        return url_new

    def get_account(self):
        account = self.env["env"][self.env["default"]]["account"]
        return account

    def get_pwd(self):
        pwd = self.env["env"][self.env["default"]]["password"]
        return pwd

    def get_env_name(self):
        return self.env["default"]

    def get_debug(self):
        return self.env["debug"]




if __name__ == "__main__":
    ge = Env()
    res = ge.get_debug()
    print(res)
