from utils import ColorUtil as logUtil

__script_version__ = "1.0.0"
__script_name__ = "Arno日常工具集"

__article_temp_version__ = "1.0.0"
__article_temp_name__ = "HB模板替换工具"

__drawable_version__ = "1.0.3"
__drawable_name__ = "资源替换工具"

__fast_merge_version__ = "1.0.0"
__fast_merge_name__ = "快速合并工具"


def print_script_message_start(name, version):
    logUtil.logv("Welcome %s version;%s" % (__script_name__, __script_version__))
    logUtil.logv(">>>>>>>%s执行开始 version: %s>>>>>>>" % (version, name))


def print_script_message_end(name, version):
    logUtil.logv("<<<<<<<%s执行完毕 version: %s<<<<<<<" % (version, name))
