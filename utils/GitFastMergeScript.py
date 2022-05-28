# 快速merge上一个分支脚本
# !/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from sys import argv


# execute command, and return the output
def execCmd(cmd):
    r = os.popen(cmd)
    text = r.read()
    r.close()
    return text


# write "data" to file-filename
def writeFile(filename, data):
    f = open(filename, "w")
    f.write(data)
    f.close()


script, project_path, need_merge_branch = argv

# p_root = '/Users/xuxin14/Desktop/SinaProjects/'
# normal_name = "SinaNews"
# vice_name = "SinaNews的副本"
# project_root = ''

# # 判断路径
# print(type(isVice))
#
# if isVice:
#     project_root = p_root + vice_name
# else:
#     project_root = p_root + normal_name

# 进入目录
os.chdir(project_path)
print("进入目录 当前 :")
os.system('pwd')

# 拿到当前分支名
cur_branch_name = execCmd('git cur')
print("获取分支名: %s" % cur_branch_name)

# 切换分支
os.system('git checkout %s' % need_merge_branch)
os.system('git cur')
os.system('git mergeno %s' % cur_branch_name)
