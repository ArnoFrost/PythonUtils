# 自动放置模板脚本
# !/usr/bin/env python
import os
import re
import shutil
import zipfile
from sys import argv

import wget


def traverse_dir(current_dir, deep=0):
    """
    current_dir: 绝对路径: "./"  或当前路径: 'D:/picture'
    """
    dir_list = os.listdir(current_dir)
    # traverse folder first.
    path_list, file_list = [], []
    for dir in dir_list:
        path = os.path.join(current_dir, dir)
        if os.path.isdir(path):
            path_list.append(dir)
        else:
            file_list.append(dir)
    dir_list = path_list + file_list

    # traverse all dir.
    for dir in dir_list:
        path = os.path.join(current_dir, dir)
        if os.path.isdir(path):
            # do something to this directory
            print("\t" * deep, dir)
            traverse_dir(path, deep + 1)
        if os.path.isfile(path):
            # do something to this file
            print("\t" * deep, "|--", dir)


def zip_file(file_path, dst_path):
    z_file = zipfile.ZipFile(file_path, "r")
    # ZipFile.namelist(): 获取ZIP文档内所有文件的名称列表
    for fileM in z_file.namelist():
        z_file.extract(fileM, dst_path)
    z_file.close()


# script, from_file, to_file = argv
script, download_url = argv
# download_url = "http://mjs.sinaimg.cn//wap/project/snal_v2/7.3.63/index/index.php"
# version_number = re.match("\d.\d.\d{2}", download_url)
pattern = re.compile(r'\d.\d.\d{2}')
version_number = pattern.findall(download_url)[0]
print("地址是 %s ,版本号是 %s" % (download_url, version_number))
# 模板根目录
rebase_branch_name = "devTrunk"
tempRoot = "/Users/xuxin14/Desktop/Temp"
# 替换根目录
projectRoot = "/Users/xuxin14/Desktop/SinaProjects/SinaNews的副本"
# 定义常量
from_file = tempRoot + "/" + version_number + "/index"
to_file = projectRoot + "/SinaNews/src/main/assets/article_v2"
php_name = tempRoot + "/" + version_number + "/index.php"
zip_name = tempRoot + "/" + version_number + "/index.zip"
# 拷贝目录

# 1. 下载文件准备目录
print("下载文件路径 %s" % php_name)
print("模板目录是 " + tempRoot + ", 工程目录是 " + projectRoot + '\n')
os.mkdir(tempRoot + "/" + version_number)
wget.download(download_url, out=php_name)
# 2.解压缩
# 2.1 修改文件名

os.rename(php_name, zip_name)
# 2.2 解压文件
zip_file(zip_name, from_file)
# 3.复制文件
print("执行拷贝=============>\n")
# 3.1 整理文件 移除多余文件
need_remove_file_path1 = from_file + '/' + version_number
need_remove_file_path2 = from_file + "/version.json"
# traverse_dir(from_file, 1)
os.remove(need_remove_file_path1)
print("移除文件=============>" + version_number + '\n')
os.remove(need_remove_file_path2)
print("移除文件=============> version.json \n")
# traverse_dir(from_file, 1)

# 3.2 复制文件
print("递归拷贝从 %s 到 %s" % (from_file, to_file) + '\n')
shutil.copytree(from_file, to_file, dirs_exist_ok=True)
print("<=============拷贝结束\n")

# 4.git commit
# 4.1 进入到指定目录
os.chdir(projectRoot)
print("进入目录 当前 :")
os.system('pwd')
# 4.2 转换分支更新最新
os.system('git fetch')
os.system('git checkout features/xuxin14/article_temp_upgrade')
os.system('git rebase %s' % rebase_branch_name)
# 初步不添加危险操作
# os.system('git push -f')
# 4.3 执行提交
os.system('git add .')
os.system('git commit -m \"Feature: 升级正文Hb 模板 %s\"' % version_number)
print("提交完毕")
