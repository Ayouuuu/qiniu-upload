import click
import qiniu
import os
from qiniu import put_file
import hashlib
import time
import sys

# 七牛云密钥
ak = ""
sk = ""
# 存储桶名
bucket_name = ""
q = qiniu.Auth(ak, sk)
# 自定义七牛云存储路径名
upload_name = ""
search_path = path = os.getcwd() + os.sep


def get_file_md5(file):
    with open(file, 'rb') as fp:
        data = fp.read()
        return hashlib.md5(data).hexdigest()


policy = {
    "insertOnly": 0
}


def upload_file(key, path):
    md5 = get_file_md5(path)
    if containMd5(md5) and not ignoreMd5:
        print('忽略文件: ' + path)
        return
    token = q.upload_token(bucket_name, key, 3600, policy=policy)
    ret, info = put_file(token, key, path, version="v2")
    if ret is not None:
        print("上传成功: " + upload_name + path)
        addLog(md5, path)
        return 1
    print("上传失败: " + path)
    return 0


def addLog(md5, path):
    localTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    list_files.append(md5 + "," + path + "," + localTime)
    list_md5.append(md5)


def createLog():
    createFile("logs.log", list_files)
    print('已上传' + str(len(list_files)) + '个文件')


def insertMd5():
    createFile("md5.txt", list_md5)


def createFile(name, list):
    dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
    file = open(dirname + os.sep + name, 'a', encoding='utf-8')
    for fileName in list:
        file.write(fileName + '\n')
    file.close()


def containMd5(md5):
    if list_md5.__contains__(md5):
        return True
    return False


def loadMd5():
    dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
    path = dirname + os.sep + "logs.log"
    print(path)
    if not os.path.exists(path):
        os.mknod(path)
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


def scanfile(dir):
    for path, d, filelist in os.walk(dir):
        for filename in filelist:
            full_path = os.path.join(path, filename)
            if containType(full_path):
                allfiles.append(full_path)


def containType(path):
    if file_types is None:
        return True
    for ftype in file_types:
        if path.endswith("." + ftype):
            return True
    return False


allfiles = []
ignoreMd5 = False
file_types = None


@click.command()
@click.option('-f', "--file", type=str, default=None, help="单个文件压缩")
@click.option('-d', "--dir", type=str, default=None, help="被压缩的文件夹")
@click.option('-i', "--ignore", type=bool, default=False, help="忽略MD5验证")
@click.option('-p', "--path", type=str, default="", help="七牛云自定义路径")
@click.option('-t', "--type", type=str, default=None, help="指定文件后缀")
def run(file, dir, ignore, path, type):
    global ignoreMd5
    ignoreMd5 = ignore

    global upload_name
    upload_name = path

    if type is not None:
        global file_types
        file_types = type.split(",")
    if file is not None:
        allfiles.append(file)
        pass
    elif dir is not None:
        scanfile(dir)
        pass
    else:
        print("未指定文件夹，自动定位当前运行目录")
        scanfile(search_path)
        pass
    print("开始上传文件：七牛云路径", ("/" if upload_name == "" else upload_name))
    runUpload()
    createLog()


def runUpload():
    for file in allfiles:
        upload_path = (upload_name + file).replace(os.sep + os.sep, os.sep)
        upload_path = upload_path[1:] if upload_path[0] == '/' else upload_path
        if upload_file(upload_path, file):
            continue


if __name__ == '__main__':
    try:
        loadMd5()
        run()
    except SystemExit:
        pass
    except BaseException as e:
        raise e

