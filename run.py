# 创建应用实例
from flask import request, Flask
from wxcloudrun import app
import base64
from aip import AipImageClassify

import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

def query(content):
    # 请求地址
    url = 'https://baike.baidu.com/item/' + urllib.parse.quote(content)
    # 请求头部
    headers = { 
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36' 
    }
    # 利用请求地址和请求头部构造请求对象
    req = urllib.request.Request(url=url, headers=headers, method='GET')
    # 发送请求，获得响应
    response = urllib.request.urlopen(req)
    # 读取响应，获得文本
    text = response.read().decode('utf-8')
    baike_info = {
        "description": "",
        "image_url": ""
    }
    soup = BeautifulSoup(text, 'html.parser')
    meta_tag = soup.find('meta', attrs={'name': 'description'})
    baike_info['description'] = meta_tag['content']
    meta_tag = soup.find('meta', attrs={'name': 'image'})
    baike_info['image_url'] = meta_tag['content']
    return baike_info

""" 你的 APPID AK SK """
APP_ID = "56511544"
API_KEY = "P7VEk6Dz8k9yPtYcp7cjKkJh"
SECRET_KEY = "AprgPOOkEhQDfCUVMnwWpnWydZa6ZRYj"
client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)
""" 如果有可选参数 """
options = {}
options["baike_num"] = 5

app = Flask(__name__)

@app.route("/detect", methods=["POST"])
def detect():
    if request.content_type.startswith('application/json'):            
        img = request.json.get('img')
        decoded_data = base64.b64decode(img)
        res = client.plantDetect(decoded_data, options)
        if 'description' not in res['result'][0]['baike_info']:
            res['result'][0]['baike_info'] = query(res['result'][0]['name'])
        return res
    return {}


# 启动Flask Web服务
if __name__ == '__main__':
    app.run("0.0.0.0", "80")
