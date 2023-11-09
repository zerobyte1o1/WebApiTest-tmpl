from utils.encrypt import encrpt


class UserData:
    def login_data(self):
        """
        login在base里完善了不用单独写data，此为展示
        :return:
        """
        # 读取variables文件对应的接口请求架构
        variables_temp = self.get_variables(module_name="log", variables_name="role_list_filter")
        # 补全架构确实的数据
        args = [("passwd", ), ("login", ), ("random", )]
        variables = self.modify_variables(target_json=variables_temp, args=args)
        return variables