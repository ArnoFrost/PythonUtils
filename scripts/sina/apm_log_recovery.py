#!/usr/bin/python
# -*- coding:utf-8 -*-
# 日志回捞 did -> ldid
import os
import sys
import time
from urllib import parse
from clickhouse_driver import Client

__curr_dir = os.path.dirname(os.path.abspath(__file__))


def read_file_lines(path):
    lines = None
    try:
        with open(path, 'r') as f:
            lines = f.read().splitlines(False)
    except Exception as e:
        print(e)
    return lines


if __name__ == '__main__':
    """
    click house 设备查询脚本
    """
    args = sys.argv[1:]
    args_size = len(args)

    _date_str = '2022-07-12'
    _did_file = None
    if args_size > 0:
        _date_str = args[0]
    if args_size > 1:
        _did_file = args[1]
    if _did_file == None:
        _did_file = __curr_dir + '/' + 'did_file'
    print('_date_str', _date_str)
    print('_did_file', _did_file)
    if not _date_str:
        print('请输入过滤的日期')
        exit()
    if not os.path.exists(_did_file):
        print('did文件不存在:' + _did_file)
        exit()

    did_list = read_file_lines(_did_file)
    if not did_list or len(did_list) <= 0:
        print('did文件内容为空')
        exit()
    else:
        print('读取did数量：' + str(len(did_list)))
    ldld_list = []

    client = Client(host='ck3x.mars.grid.sina.com.cn', port=9000, database='apm',
                    user='apm', password='lwGxOWXm')
    # like_arg = 'https://newsapi.sina.cn%'
    like_arg = '%&lDid=%'
    start_time = int(time.time())
    ldid_list_str = ''
    for did in did_list:
        sql = "select _request_url from apm_msg_all where date >= '" + _date_str + "' and _device_id = '" + did + "' and _request_url like '" + like_arg + "' limit 1;"
        request_url = ''
        lDid = ''
        try:
            query_results = client.execute(sql)

            if len(query_results) != 0:
                request_url = str(query_results[0][0])
            print(request_url)
            if request_url:
                # 在python3当中有自带的库urllib.parse，python2当中是w3lib.url，使用方法跟urllib.parse类似，这里不做演示
                # aaaa = urlparse.urlparse(aaa)  # 查看ParseResult对象
                # print aaaa
                params = parse.parse_qs(request_url)
                lDid = params.get('lDid')[0]
                ldid_list_str += lDid + ','
        except Exception as e:
            print("execute Exception:" + str(e))
        ldld_list.append(lDid)

    end_time = int(time.time()) - start_time
    print('耗时:' + str(end_time))

    if len(ldid_list_str) > 0:
        print('did分别对应的ldid:')
        print(ldld_list)
        print('')
        print('ldid列表字符串:')
        print(ldid_list_str[:-1])
        did_dir = os.path.dirname(os.path.abspath(_did_file))
        ldid_output_file = did_dir + '/' + os.path.basename(_did_file) + '_ldid'
        print("写文件到本地: " + ldid_output_file)
        with open(ldid_output_file, 'w') as file:
            for ldid in ldld_list:
                file.write(ldid + "\n")
    else:
        print('找不到ldid')
