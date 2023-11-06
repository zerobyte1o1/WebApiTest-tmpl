import os
import requests
from utils.logger import logger
import yaml
from utils.env import Env
from utils.mock import Mock
from faker import Faker
import json as complexjson

class BaseApi:
    get_env = Env()
    url = get_env.get_env()
    account = get_env.get_account()
    password = get_env.get_pwd()
    env_name = get_env.get_env_name()
    env_debug = get_env.get_debug()
    faker = Faker(locale='zh_CN')
    mock = Mock()

    def __init__(self,api_root_url):
        self.api_root_url = api_root_url
        self.session = requests.session()

    def get(self, url, **kwargs):
        return self.request(url, "GET", **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self.request(url, "POST", data, json, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self.request(url, "PUT", data, **kwargs)

    def delete(self, url, **kwargs):
        return self.request(url, "DELETE", **kwargs)

    def patch(self, url, data=None, **kwargs):
        return self.request(url, "PATCH", data, **kwargs)

    def request(self, url, method, data=None, json=None, **kwargs):
        url = self.api_root_url + url
        headers = dict(**kwargs).get("headers")
        params = dict(**kwargs).get("params")
        files = dict(**kwargs).get("params")
        cookies = dict(**kwargs).get("params")
        self.request_log(url, method, data, json, params, headers, files, cookies)
        if method == "GET":
            return self.session.get(url, **kwargs)
        if method == "POST":
            return requests.post(url, data, json, **kwargs)
        if method == "PUT":
            if json:
                # PUT 和 PATCH 中没有提供直接使用json参数的方法，因此需要用data来传入
                data = complexjson.dumps(json)
            return self.session.put(url, data, **kwargs)
        if method == "DELETE":
            return self.session.delete(url, **kwargs)
        if method == "PATCH":
            if json:
                data = complexjson.dumps(json)
            return self.session.patch(url, data, **kwargs)

    def request_log(self, url, method, data=None, json=None, params=None, headers=None, files=None, cookies=None,
                    **kwargs):
        logger.info("接口请求地址 ==>> {}".format(url))
        logger.info("接口请求方式 ==>> {}".format(method))
        # Python3中，json在做dumps操作时，会将中文转换成unicode编码，因此设置 ensure_ascii=False
        logger.info("接口请求头 ==>> {}".format(complexjson.dumps(headers, indent=4, ensure_ascii=False)))
        logger.info("接口请求 params 参数 ==>> {}".format(complexjson.dumps(params, indent=4, ensure_ascii=False)))
        logger.info("接口请求体 data 参数 ==>> {}".format(complexjson.dumps(data, indent=4, ensure_ascii=False)))
        logger.info("接口请求体 json 参数 ==>> {}".format(complexjson.dumps(json, indent=4, ensure_ascii=False)))
        logger.info("接口上传附件 files 参数 ==>> {}".format(files))
        logger.info("接口 cookies 参数 ==>> {}".format(complexjson.dumps(cookies, indent=4, ensure_ascii=False)))

    def get_variables(self, module_name: str, variables_name: str):
        """
        :param module_name:
        :param variables_name: for instance: variables_name="create_product_project_temp"
        :return: json
        """
        if self.env_debug is True:
            root_path = os.path.abspath(os.path.join(os.getcwd(), "../../"))
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


def get(func):
    def wrapper(*args, **kwargs):
        print(args)
        return func

    return wrapper


if __name__ == '__main__':
    pass
