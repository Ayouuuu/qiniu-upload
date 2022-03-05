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
# 运行
python3 qiniu-upload.py
```

