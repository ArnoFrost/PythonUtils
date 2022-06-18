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


class DrawableFolder:
    src_file = ""
    dst_file = ""

    def __init__(self, src_file, dst_file):
        self.src_file = src_file
        self.dst_file = dst_file


script, drawable_name, drawable_root, project_root = argv
print("替换的图标是 %s " % drawable_name)
print("当前路径是 %s " % project_root)
print("替换路径是 %s " % drawable_root)
# region 常量定义
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
drawableList.append(DrawableFolder(src_file_2x, dst_file_2x))
drawableList.append(DrawableFolder(src_file_2x_night, dst_file_2x_night))
drawableList.append(DrawableFolder(src_file_3x, dst_file_3x))
drawableList.append(DrawableFolder(src_file_3x_night, dst_file_3x_night))

# endregion


for i, folder in enumerate(drawableList):
    # region 1. 重命名文件
    try:
        file = os.listdir(folder.src_file)[0]
        print("找到文件 %s " % file)
        original_name = folder.src_file + "/" + file
        need_file_name = folder.src_file + "/" + drawable_name
        dst_file_name = folder.dst_file + "/" + drawable_name
        # print("路径打印 %s " % original_name)
        # print("路径打印目的地 %s " % need_file_name)
        os.rename(original_name, need_file_name)
    except FileNotFoundError:
        print("未找到文件相应目录文件 %s ,忽略" % folder.src_file)
        continue
    except Exception as e:
        print("未找到文件 %s" % e)
        continue
    # endregion
    # region 2. 强制替换
    else:
        try:
            print("执行替换 %s" % dst_file_name)
            shutil.copyfile(need_file_name, dst_file_name)
        except Exception as e:
            print("拷贝失败 %s" % e)
            continue
        else:
            print("替换图标素材完毕")

    # endregion
