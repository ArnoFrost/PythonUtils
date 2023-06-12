# 快速merge上一个分支脚本
# !/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import utils.colorful_log as log_util
from sys import argv

# region 定义描述日志
__name__ = "git快速合并替换工具"
__version__ = "1.0.1"
log_util.log_start(__name__, __version__)
# endregion
# region zsh示例
'''
fastMerge(){
   need_merge_branch=$1
   project_path=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
   # echo "当前工作目录 :$project_path "
   python /Users/xuxin14/PycharmProjects/ArnoToolKit/scripts/git_fast_merge_script.py $project_path $need_merge_branch
}
alias fastmerge=fastMerge

#快速merge 原版
fastMegeO(){
   python /Users/xuxin14/PycharmProjects/ArnoToolKit/scripts/git_fast_merge_script.py /Users/xuxin14/Desktop/SinaProjects/SinaNews $1
}
alias fmo=fastMegeO

#快速merge 副本
fastMergeC(){
   python /Users/xuxin14/PycharmProjects/ArnoToolKit/scripts/git_fast_merge_script.py /Users/xuxin14/Desktop/SinaProjects/SinaNews的副本 $1
}
alias fmc=fastMergeC
'''


# endregion
# execute command, and return the output
def exec_cmd(cmd):
    r = os.popen(cmd)
    text = r.read()
    r.close()
    return text


script, project_path, need_merge_branch = argv
# region 准备工作
log_util.v("快速合并脚本 需要合并分支 %s " % need_merge_branch)
# 进入目录
os.chdir(project_path)
log_util.i("进入目录 当前 :")
os.system('pwd')
# 更新仓库
log_util.i("更新仓库")
os.system('git fetch')
# endregion

# region 操作流程
# 拿到当前分支名
cur_branch_name = exec_cmd('git symbolic-ref --short HEAD')
log_util.i("获取分支名: %s" % cur_branch_name)

# 切换分支
os.system('git checkout %s' % need_merge_branch)
os.system('git symbolic-ref --short HEAD')
# 禁用fast-forward
os.system('git merge --no-ff %s' % cur_branch_name)
# endregion

log_util.log_end(__name__, __version__)
