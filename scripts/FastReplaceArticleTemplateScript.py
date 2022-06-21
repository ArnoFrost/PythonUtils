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
import ColorfulLog as logUtil
# region 定义描述日志
__name__ = "Hb模板替换工具"
__version__ = "1.0.1"
logUtil.log_start(__name__, __version__)
# endregion
''' 
updateHb(){
   # download_url = "http://mjs.sinaimg.cn//wap/project/snal_v2/7.3.63/index/index.php"
   # 替换根目录
   project_root=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
   download_url=$1
   rebase_branch_name="devTrunk"
   temp_root="/Users/xuxin14/Desktop/Temp"
   python /Users/xuxin14/PycharmProjects/pythonProject/scripts/FastReplaceArticleTemplateScript.py $download_url $rebase_branch_name $project_root $temp_root
}
alias updatehb=updateHb

eg:
> $[project_root]/ updatehb [download_url]
'''


# endregion
# execute command, and return the output
def execCmd(cmd):
    r = os.popen(cmd)
    text = r.read()
    r.close()
    return text


def zip_file(file_path, dst_path):
    z_file = zipfile.ZipFile(file_path, "r")
    # ZipFile.namelist(): 获取ZIP文档内所有文件的名称列表
    for fileM in z_file.namelist():
        z_file.extract(fileM, dst_path)
    z_file.close()


script, download_url, rebase_branch_name, project_root, temp_root = argv
# version_number = re.match("\d.\d.\d{2}", download_url)
pattern = re.compile(r'\d\.\d\.\d+')
version_number = pattern.findall(download_url)[0]
logUtil.logv("地址是 %s ,版本号是 %s" % (download_url, version_number))
# region 常量定义
# 模板根目录
# rebase_branch_name = "devTrunk"
# temp_root = "/Users/xuxin14/Desktop/Temp"
# 替换根目录
# project_root = "/Users/xuxin14/Desktop/SinaProjects/SinaNews的副本"
# 定义常量
src_file = temp_root + "/" + version_number + "/index"
dst_file = project_root + "/SinaNews/src/main/assets/article_v2"
php_name = temp_root + "/" + version_number + "/index.php"
zip_name = temp_root + "/" + version_number + "/index.zip"
# endregion

# region 1.下载文件准备目录
# 拷贝目录
logUtil.logd("下载文件路径 %s" % php_name)
logUtil.logd("模板目录是 " + temp_root + ", 工程目录是 " + project_root + '\n')
try:
    os.mkdir(temp_root + "/" + version_number)
    wget.download(download_url, out=php_name)
except Exception as e:
    logUtil.loge("步骤1 执行发生问题 终止 %s " % e)
# endregion
else:
    try:
        # region 2.解压缩
        # 2.1 修改文件名

        os.rename(php_name, zip_name)
        # 2.2 解压文件
        zip_file(zip_name, src_file)
        # endregion
    except Exception as e:
        logUtil.loge("步骤2 执行发生问题 终止 %s " % e)
    else:
        try:
            # region 3.复制文件
            logUtil.logi("\n执行拷贝=============>\n")
            # 3.1 整理文件 移除多余文件
            need_remove_file_path1 = src_file + '/' + version_number
            need_remove_file_path2 = src_file + "/version.json"
            # traverse_dir(src_file, 1)
            os.remove(need_remove_file_path1)
            logUtil.logi("移除文件=============>" + version_number + '\n')
            os.remove(need_remove_file_path2)
            logUtil.logi("移除文件=============> version.json \n")
            # traverse_dir(src_file, 1)

            # 3.2 复制文件
            logUtil.logi("递归拷贝从 %s 到 %s" % (src_file, dst_file) + '\n')
            shutil.copytree(src_file, dst_file, dirs_exist_ok=True)
            logUtil.logd("<=============拷贝结束\n")
        except Exception as e:
            logUtil.loge("步骤3 执行发生问题 终止 %s " % e)
        else:
            try:
                # region 4.git commit
                # 4.1 进入到指定目录
                os.chdir(project_root)
                logUtil.logi("进入目录 当前 :")
                os.system('pwd')
                # 4.2 转换分支更新最新
                os.system('git fetch origin %s:%s' % (rebase_branch_name, rebase_branch_name))
                # cur_branch_name = execCmd('git symbolic-ref --short HEAD')
                # logUtil.print_log_i("获取分支名: %s" % cur_branch_name)
                # os.system('git checkout features/xuxin14/article_temp_upgrade')
                os.system('git rebase %s' % rebase_branch_name)
                # 初步不添加危险操作
                # os.system('git push -f')
                # 4.3 执行提交
                os.system('git add .')
                os.system('git commit -m \"Feature: 升级正文Hb 模板 %s\"' % version_number)
                logUtil.logv("提交完毕")
                # endregion
            except Exception as e:
                logUtil.loge("步骤3 执行发生问题 终止 %s " % e)
            else:
                logUtil.log_end(__name__, __version__)
    # endregion
