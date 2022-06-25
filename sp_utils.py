# -*- coding: UTF-8 -*-

import copy
import os
import errno


def sp_create_file_if_not_exit(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

def sp_month_map():
    """
    月份对编号的映射: Jan -> 1 ...
    """
    month_to_num = {}
    month_to_num['Jan'] = 1
    month_to_num['Feb'] = 2
    month_to_num['Mar'] = 3
    month_to_num['Apr'] = 4
    month_to_num['May'] = 5
    month_to_num['Jun'] = 6
    month_to_num['Jul'] = 7
    month_to_num['Aug'] = 8
    month_to_num['Sep'] = 9
    month_to_num['Oct'] = 10
    month_to_num['Nov'] = 11
    month_to_num['Dec'] = 12

    return month_to_num;

def sp_convert_UTC_to_timestamp(UTC_time):
    ts = "";
    #UTCG format: 7 Jul 2020 19:00:00.000
    temp = UTC_time.split();

    return ts;

# reference: https://www.cnblogs.com/wt7018/p/11610286.html
# 遍历文件夹下的所有文件
def sp_walkFile(file):
    # root 表示当前正在访问的文件夹路径
    # dirs 表示该文件夹下的子目录名list
    # files 表示该文件夹下的文件list
    for root, dirs, files in os.walk(file):
        filename_list = [];
        # 遍历当前文件夹下的所有文件,并将csv文件放到filename_list之中并返回。
        for f in files:
            # 组合文件夹路径和文件名形成文件的全路径名
            file_name = os.path.join(root, f);
            print(file_name)
            if(file_name.endswith(".csv")):
                filename_list.append(file_name);

        #for d in dirs:
        #    print(os.path.join(root, d))
        return filename_list