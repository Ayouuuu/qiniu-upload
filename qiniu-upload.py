import qiniu
import os
from qiniu import put_file
import imghdr
import hashlib
import time

# 七牛云密钥
ak = ""
sk = ""
# 存储桶名
bucket_name = ""
q = qiniu.Auth(ak, sk)
# 自定义七牛云存储路径名
upload_name = "img/"
# search_path = path = os.getcwd() + os.sep + "img" + os.sep
search_path = path = os.getcwd() + os.sep

def get_file_md5(file):
    with open(file, 'rb') as fp:
        data = fp.read()
        return hashlib.md5(data).hexdigest()

    
policy = {
    "insertOnly": 0
}


def upload_file(key, path):
    token = q.upload_token(bucket_name,key,3600,policy=policy)
    ret, info = put_file(token, key, path, version="v2")
    if ret is not None:
        print("上传成功: " + path)
        return 1
    print("上传失败: " + path)
    return 0


def imgLog():
    createFile("logs.log", list_files)
    print('已上传'+str(len(list_files))+'个文件')


def insertMd5():
    createFile("md5.txt", list_md5)


def createFile(name, list):
    file = open(os.getcwd() + os.sep + name, 'a', encoding='utf-8')
    for fileName in list:
        file.write(fileName + '\n')
    file.close()


def containMd5(md5):
    if list_md5.__contains__(md5):
        return True
    return False


def loadMd5():
    path = os.getcwd() + os.sep + "logs.log"
    if not os.path.exists(path):
        os.mknod("logs.log")
    file = open(path, 'r')
    if file is None:
        return
    lines = file.readlines()
    for line in lines:
        md5 = line.replace("\n", "").split(",")[0]
        if not containMd5(md5):
            list_md5.append(md5)


list_md5 = []
list_files = []

if __name__ == '__main__':
    loadMd5()
    path = search_path
    arr = os.listdir(path)
    try:
        for f in arr:
            if os.path.isfile(path+f):
                if imghdr.what(path + f) is not None:
                    md5 = get_file_md5(path + f)
                    if not containMd5(md5):
                        if upload_file(upload_name+f,path+f):
                            localTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                            list_files.append(md5 + "," + path + f + "," + localTime)
                            list_md5.append(md5)
                    else:
                        print("忽略文件: " + path+f)
    except Exception as e:
        print(e)
    imgLog()
