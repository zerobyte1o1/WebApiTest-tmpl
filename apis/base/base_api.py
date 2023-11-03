import os
import ssl
import urllib.request as ur
import yaml
import urllib3
from utils.env import Env
from utils.mock import Mock
from utils.switch import Switch
from faker import Faker


class BaseApi:
    get_env = Env()
    url = get_env.get_env()
    account = get_env.get_account()
    password = get_env.get_pwd()
    env_name = get_env.get_env_name()
    env_debug=get_env.get_debug()
    faker = Faker(locale='zh_CN')
    mock=Mock()

    def __init__(self, proxy_=None):
        """

        @rtype: object
        """

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        switch = Switch()
        is_switch_on = switch.is_proxy_on()
        if is_switch_on is True:
            # 走代理时，全局取消证书验证，避免报错
            ssl._create_default_https_context = ssl._create_unverified_context
            proxy_ = "127.0.0.1:8080"
        else:
            pass
        if proxy_:
            proxy = {
                "http": 'http://' + proxy_,
                "https": 'http://' + proxy_
            }
        else:
            proxy = None
        proxy_support = ur.ProxyHandler(proxy)
        # build a new opener that adds authentication and caching FTP handlers
        opener = ur.build_opener(proxy_support, ur.CacheFTPHandler)
        # install it
        ur.install_opener(opener)

    def get_variables(self, module_name: str, variables_name: str):
        """
        :param module_name:
        :param variables_name: for instance: variables_name="create_product_project_temp"
        :return: json
        """
        if self.env_debug is True:
            root_path = os.path.abspath(os.path.join(os.getcwd(),"../../"))
        else:
            root_path = os.path.abspath(os.path.join(os.getcwd()))
        # pytest执行需要删除../../
        path = os.path.join(root_path, "case_data/variables_.yaml")
        variables = yaml.safe_load(open(path))
        res = variables[module_name][variables_name]
        return res

    def modify_variables(self, target_json, args: list = None):
        """
        CAUTION: 多级dict用:隔开即可;列表层级用>隔开即可

        :param target_json: 目标Json, 配合method get_variables使用
        :param args: 列表形式的参数, 记录目标参数和修改后的效果。for instance:
            args=[("addr>0:area", "jojo"), ("code", "jojo")]
        :return: Json after modified
        """
        json_temp = target_json
        if args is not None:
            for (target, change_to) in args:
                if ":" in target:
                    keys = target.split(":")
                    self.deep_target(json_temp, keys, change_to)
                else:
                    json_temp[target] = change_to

        return json_temp

    def deep_target(self, json_temp, keys, change_to, digit=0, num=0, list_digit=None):
        """
        多层级dict递归赋值
        :param list_digit:列表层数
        :param json_temp:目标Json, 配合method get_variables使用
        :param keys:多级dict的key值拆分的list
        :param change_to:赋值value
        :param digit:当次层级计数
        :param num:总层级数
        """
        if digit == 0:
            num = len(keys)
        key = keys[digit]
        if list_digit is None:
            if ">" in key:
                list_digit = int(key.split(">")[1])
                key = key.split(">")[0]
                self.deep_target(json_temp[key], keys, change_to, digit, num, list_digit)
            else:
                digit += 1
                if digit == num:
                    json_temp[key] = change_to
                else:
                    self.deep_target(json_temp[key], keys, change_to, digit, num)
        else:
            digit += 1
            self.deep_target(json_temp[list_digit], keys, change_to, digit, num, None)


if __name__ == '__main__':
    b = BaseApi()
    t = b.get_variables(module_name="function_script", variables_name="create_role")
    res1 = b.modify_variables(target_json=t, args=[("a?", "jojo5"), ("code", "jojo5")])
    print(res1)
