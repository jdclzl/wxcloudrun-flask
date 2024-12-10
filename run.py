# 创建应用实例
import sys

from flask import request, Flask
from wxcloudrun import app
from aip import AipImageClassify

""" 你的 APPID AK SK """
APP_ID = "56511544"
API_KEY = "P7VEk6Dz8k9yPtYcp7cjKkJh"
SECRET_KEY = "AprgPOOkEhQDfCUVMnwWpnWydZa6ZRYj"
client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)
""" 如果有可选参数 """
options = {}
options["baike_num"] = 5

app = Flask(__name__)

""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

@app.route("/detect", methods=["POST"])
def detect():
    if request.content_type.startswith('application/json'):            
        img = request.json.get('img')
        res = client.plantDetect(img, options)
        return res
    return {}


# 启动Flask Web服务
if __name__ == '__main__':
    app.run("0.0.0.0", "80")
