#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 快速merge上一个分支脚本
import os
import subprocess
import sys

sys.path.append('/Users/xuxin14/GeekProject/ArnoGeek/ArnoToolKit/scripts/')
import utils.colorful_log as log_util

# region 定义描述日志
__name__ = "git快速合并替换工具"
__version__ = "1.0.1"
log_util.log_start(__name__, __version__)
# endregion
# region zsh示例
'''
# 定义一个函数来运行Python脚本，并传递所有必要的参数
run_fast_merge_script() {
    python /Users/xuxin14/GeekProject/ArnoGeek/ArnoToolKit/scripts/geek/git_fast_merge_script.py "$@"
}

# 为上面的函数定义别名
alias fastmerge='run_fast_merge_script $(pwd)'
alias fmo='run_fast_merge_script /Users/xuxin14/Desktop/SinaProjects/SinaNews'
'''


# endregion

# 执行命令
def exec_cmd(cmd):
    """执行给定的shell命令并返回输出"""
    try:
        return subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        log_util.e('Error executing command: {}'.format(e))
        sys.exit(1)


# region 准备工作
def git_fast_merge_script(project_path, need_merge_branch):
    log_util.log_start(__name__, __version__)
    log_util.v(f"快速合并脚本 需要合并分支 {need_merge_branch}")

    # 进入目录
    os.chdir(project_path)

    log_util.i("进入目录 当前 :")
    print(exec_cmd('pwd'))

    # 更新仓库
    log_util.i("更新仓库")
    log_util.i(exec_cmd('git fetch'))

    # 拿到当前分支名
    cur_branch_name = exec_cmd('git symbolic-ref --short HEAD')
    log_util.i(f"获取分支名: {cur_branch_name}")

    # 切换分支
    log_util.i(exec_cmd(f'git checkout {need_merge_branch}'))
    log_util.i(exec_cmd('git symbolic-ref --short HEAD'))

    # 禁用fast-forward
    log_util.i(exec_cmd(f'git merge --no-ff {cur_branch_name}'))

    log_util.log_end(__name__, __version__)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {} PROJECT_PATH NEED_MERGE_BRANCH'.format(sys.argv[0]))
        sys.exit(1)

    project_path = sys.argv[1]
    need_merge_branch = sys.argv[2]

    git_fast_merge_script(project_path, need_merge_branch)
