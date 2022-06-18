# 自动放置模板脚本
# !/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import shutil
import zipfile
from sys import argv

import wget

# region zsh示例
''' 
FastReplaceDrawable(){
   # drawable_name = "arno_test.png"
   # 替换根目录
   project_root=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
   drawable_name=$1
   drawable_root="/Users/xuxin14/Desktop/DrawableMerge"
   python /Users/xuxin14/PycharmProjects/pythonProject/utils/FastReplaceDrawableScript.py $drawable_name $project_root $drawable_root
}
alias frd=FastReplaceDrawable

eg:

> $[project_root]/ fad [drawable_name]
'''

# endregion

script, drawable_name, project_root, drawable_root = argv
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
from_file = drawable_root
to_file = project_root + "/SinaNews/src/main/res"

# region xhdpi 尺寸定义
from_file_2x = drawable_root + "/" + folder_2x
to_file_2x = to_file + "/" + folder_2x
from_file_2x_night = drawable_root + "/" + folder_2x
to_file_2x_night = to_file + "/" + folder_2x
# endregion

# endregion

# region 1. 重命名文件
file = os.listdir(from_file_2x)[0]
os.rename(file, drawable_name)

file = os.listdir(from_file_2x_night)[0]
os.rename(file, drawable_name)
# endregion

# region 2. 强制替换
shutil.copyfile(from_file_2x, to_file_2x)
shutil.copyfile(from_file_2x_night, to_file_2x_night)
# endregion


print("复制完毕")
