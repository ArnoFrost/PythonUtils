# 自动放置模板脚本
# !/usr/bin/env python
import os
import shutil
from sys import argv
import zipfile


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


def zip(file_path, dst_path):
    zFile = zipfile.ZipFile(file_path, "r")
    # ZipFile.namelist(): 获取ZIP文档内所有文件的名称列表
    for fileM in zFile.namelist():
        zFile.extract(fileM, dst_path)
    zFile.close()


# script, from_file, to_file = argv
script, version_number = argv
# 模板根目录
tempRoot = "/Users/xuxin14/Desktop/Temp"
# 替换根目录
projectRoot = "/Users/xuxin14/Desktop/SinaProjects/SinaNews的副本"
print("执行拷贝=============>\n")
print("模板目录是 " + tempRoot + ", 工程目录是 " + projectRoot + '\n')

# 拷贝目录
from_file = tempRoot + "/" + version_number + "/index"
to_file = projectRoot + "/SinaNews/src/main/assets/article_v2"

# 1.解压缩
# 1.1 修改文件名
php_name = tempRoot + "/" + version_number + "/index.php"
zip_name = tempRoot + "/" + version_number + "/index.zip"
os.rename(php_name, zip_name)
# 1.2 解压文件
zip(zip_name, from_file)
# 2.复制文件
# 2.1 整理文件 移除多余文件
need_remove_file_path1 = from_file + '/' + version_number
need_remove_file_path2 = from_file + "/version.json"
traverse_dir(from_file, 1)
os.remove(need_remove_file_path1)
print("移除文件=============>" + version_number + '\n')
os.remove(need_remove_file_path2)
print("移除文件=============> version.json \n")
traverse_dir(from_file, 1)

# 2.2 复制文件
print("递归拷贝从 %s 到 %s" % (from_file, to_file) + '\n')
shutil.copytree(from_file, to_file, dirs_exist_ok=True)
print("<=============拷贝结束\n")

# 3.git commit
# 3.1 进入到指定目录
os.chdir(projectRoot)
print("进入目录 当前 :")
os.system('pwd')
# 3.2 commit
os.system('git add .')
os.system('git commit -m \"Feature: 升级正文Hb 模板 %s\"' % version_number)
print("提交完毕")
