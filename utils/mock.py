import os
import string
import random
import time


class Mock:
    def mock_data(self, data_name: str):
        ran_str = '_' + ''.join(random.sample(string.ascii_letters + string.digits, 6))
        res = data_name + ran_str
        return res

    # 毫秒级时间戳
    def current_time(self):
        t = time.time()
        return int(round(t * 1000))

    def attachment_path(self, attachment_name: str):
        root_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
        path = os.path.join(root_path, "utils/attachment/" + attachment_name)
        return path


if __name__ == "__main__":
    mock = Mock()
    print(mock.mock_data("test"))
    # print(mock.attachment_path("s"))
