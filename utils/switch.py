import os

import yaml


class Switch:
    rootPath = os.path.dirname(os.path.abspath(__file__))
    configPath = os.path.join(rootPath, "switch.yaml")
    switch = yaml.safe_load(open(configPath))

    def is_proxy_on(self):
        res = self.switch["proxy"]
        if res == "ON":
            return True
        elif res == "OFF":
            return False


if __name__ == '__main__':
    a = Switch()
    print(a.is_proxy_on())
