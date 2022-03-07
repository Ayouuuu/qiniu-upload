#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import qiniu
import os
import json

ak = "iOxql1MY4B4Y4vlJu6-McAO13NwHeZAXkb1G87is"
sk = "NcLotWrCuSlDQmQBSNBYtZonXKLpj2hStEeMJn5R"
bucket_name = "aypu10031"
q = qiniu.Auth(ak, sk)
bucket_manager = qiniu.BucketManager(q)
url = 'https://img.ayou10031.cn/'

list_files = []
prefix = "img/"


def listFiles():
    list = bucket_manager.list(bucket_name, prefix=prefix)
    marker = list[0]['marker']
    arr = list[0]['items']
    addFile(arr)
    if not marker == "":
        listFilesMark(marker)


def addFile(arr):
    for file in arr:
        list_files.append(url + file['key'])


def listFilesMark(mark):
    list = bucket_manager.list(bucket_name, prefix=prefix, marker=mark)
    arr = list[0]['items']
    addFile(arr)
    if not list[1]:
        listFilesMark(list[0]['marker'])

def saveLog():
    createFile("jsonLog.log",list_files)

def createFile(name, list):
    file = open(os.getcwd() + os.sep + name, 'w', encoding='utf-8')
    for fileName in list:
        file.write(fileName + '\n')
    file.close()

if __name__ == '__main__':
    listFiles()
    print("已成功保存 "+str(len(list_files))+"个文件")
    saveLog()
