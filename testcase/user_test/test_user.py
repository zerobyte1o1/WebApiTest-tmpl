import pytest
import allure
from apis.user.user import User


@allure.epic("针对业务场景的测试")
@allure.feature("场景：用户注册-用户登录-查看用户")
class TestUser:
    user = User()

    @allure.story("用例-用户登出接口")
    @allure.title("请求登出接口")
    @allure.description("该用例检查用户登出操作")
    @allure.issue("", name="点击，跳转到对应BUG的链接地址")
    @allure.testcase("", name="点击，跳转到对应用例的链接地址")
    @allure.step("步骤1==>登出")
    @pytest.mark.p0
    def test_logout(self):
        res = self.user.logout_api()
        assert res.status_code == 200
        assert res.json()["code"] == "00000"
