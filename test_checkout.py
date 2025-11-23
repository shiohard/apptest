import requests, multiprocessing, time
import pytest
from checkout_service import app
def run_server():
    # 启动 Flask 服务
    app.run(port=5000)
def test_checkout_total():
    # 1. 在独立进程中启动服务
    p = multiprocessing.Process(target=run_server)
    p.daemon = True
    p.start()
    time.sleep(2)
    try:
        # 2. 准备测试数据 (3个单价为20的商品)
        data = {"items": [{"price": 20, "quantity": 3}]}

        # 3. 发送 POST 请求
        # 注意：如果有网络代理软件，有时 127.0.0.1 会报错，也可以尝试用 localhost
        res = requests.post("http://127.0.0.1:5000/checkout", json=data)

        # 4. 断言验证
        assert res.status_code == 200
        assert res.json()["total"] == 60

    finally:
        # 5. 无论测试成功失败，都要关闭服务进程
        p.terminate()
        p.join()  # 确保进程完全退出