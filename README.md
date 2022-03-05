# qiniu-upload
本脚本可以一键上传目录中的图片文件到七牛云,建议使用`Python3`运行,且需要安装 `qiniu`扩展
```shell
pip install qiniu
```
# 特性
- 根据MD5忽略重复上传
- 自定义七牛云存储路径
- 覆盖已存在的文件
# 配置文件
```python
#密钥
ak = ""
sk = ""
# 存储桶名
bucket_name = ""
q = qiniu.Auth(ak, sk)
# 七牛云路径名
upload_name = ""
# search_path = path = os.getcwd() + os.sep + "img" + os.sep
search_path = path = os.getcwd() + os.sep
```
# 使用方法
填写好 `密钥`、`存储桶名`、`七牛云路径`,将该`py`文件放置图片目录
```shell
# 上传运行路径内的所有文件 
python3 qiniu-upload.py
python3 qiniu-upload.py -d <指定目录>
python3 qiniu-upload.py -f <指定文件路径>
# 忽略MD5验证
python3 qiniu-upload.py -d <指定目录> -i true
# 忽略MD5验证，且只上传 php,js 文件
python3 qiniu-upload.py -d <指定目录> -i true -t php,js
```
|参数|说明|默认|
|:---|:---:|:---:|
|-f <文件路径>|指定单文件上传|None
|-d <目录路径>|指定文件夹上传|None
|-i true|忽略MD5验证|进行验证
|-t <文件后缀>|-t php,js,css|全部上传

