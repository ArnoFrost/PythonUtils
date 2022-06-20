# 自动放置模板脚本
# !/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import shutil
from sys import argv

# region zsh示例
''' 
FastReplaceDrawable(){
   # drawable_name = "arno_test.png"
   # 替换根目录
   project_root=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
   drawable_name=$1
   drawable_root="/Users/xuxin14/Desktop/DrawableMerge"
   python /Users/xuxin14/PycharmProjects/pythonProject/utils/FastReplaceDrawableScript.py $drawable_name $drawable_root $project_root 
}
alias frd=FastReplaceDrawable

eg:

> $[project_root]/ fad [drawable_name]
'''

# endregion
version_name = "1.01"
print("\033[32m>>>>>>>Drawable资源替换脚本 %s>>>>>>>\033[0m" % version_name)


class DrawableFolder:
    src_file = ""
    dst_file = ""
    # 1 xhdpi 2 xxhdpi 3 night-xhdpi 4 night-xxhdpi
    type = 1

    def __init__(self, src_file, dst_file, type):
        self.src_file = src_file
        self.dst_file = dst_file
        self.type = type


script, drawable_name, drawable_root, project_root = argv
print("替换的图标是 %s " % drawable_name)
print("当前路径是 %s " % project_root)
print("替换路径是 %s " % drawable_root)
# region 常量定义

drawable_dict = {
    1: "drawable-xhdpi",
    2: "drawable-xxhdpi",
    3: "drawable-night-xhdpi",
    4: "drawable-night-xxhdpi",
}


def get_type_string(drawable_type):
    """
    将drawable映射为字符串
    :param drawable_type:
    :return:
    """
    return drawable_dict.get(drawable_type, "Invalid DrawableType")
# 定义常量
folder_2x = "drawable-xhdpi"
folder_2x_night = 'drawable-night-xhdpi'
folder_3x = "drawable-xxhdpi"
folder_3x_night = "drawable-night-xxhdpi"

# 目录定义
src_file_root = drawable_root
dst_file_root = project_root + "/SinaNews/src/main/res"

# region xhdpi 尺寸定义
src_file_2x = drawable_root + "/" + folder_2x
dst_file_2x = dst_file_root + "/" + folder_2x
src_file_2x_night = drawable_root + "/" + folder_2x_night
dst_file_2x_night = dst_file_root + "/" + folder_2x_night

src_file_3x = drawable_root + "/" + folder_3x
dst_file_3x = dst_file_root + "/" + folder_3x
src_file_3x_night = drawable_root + "/" + folder_3x_night
dst_file_3x_night = dst_file_root + "/" + folder_3x_night
# endregion


drawableList = list[DrawableFolder]()
drawableList.append(DrawableFolder(src_file_2x, dst_file_2x, 1))
drawableList.append(DrawableFolder(src_file_2x_night, dst_file_2x_night, 3))
drawableList.append(DrawableFolder(src_file_3x, dst_file_3x, 2))
drawableList.append(DrawableFolder(src_file_3x_night, dst_file_3x_night, 4))


# endregion
def search(listdir, suffix):
    for filename in listdir:
        if filename.endswith(suffix):
            # print("找到原文件名 %s" % filename)
            return filename
        else:
            continue
    return


def search_first_image_file(path):
    return search(path, ".png")


for i, folder in enumerate(drawableList):
    # region 1. 重命名文件
    try:
        file = search_first_image_file(os.listdir(folder.src_file))
        original_name = folder.src_file + "/" + file
        need_file_name = folder.src_file + "/" + drawable_name
        dst_file_name = folder.dst_file + "/" + drawable_name
        # print("路径打印 %s " % original_name)
        # print("路径打印目的地 %s " % need_file_name)
        os.rename(original_name, need_file_name)
        print("找到文件 %s " % file)
    except Exception as e:
        print("\033[33m%s 未找到对应文件 忽略\033[0m" % get_type_string(folder.type))
        continue
    # endregion
    # region 2. 强制替换
    else:
        try:
            print("执行替换 %s" % dst_file_name)
            shutil.copyfile(need_file_name, dst_file_name)
        except Exception as e:
            print("\033[31m拷贝失败 %s\033[0m" % e)
            continue
        else:
            print("\033[32m替换图标素材完毕\033[0m")
            # 替换后自动重命名
            os.rename(need_file_name, need_file_name + ".old")
    # endregion
print("\033[32m<<<<<<<Drawable资源替换脚本 执行结束 %s<<<<<<<\033[0m" % version_name)