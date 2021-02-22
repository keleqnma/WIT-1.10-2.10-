#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import print_function
import codecs
import sys
import time
import datetime
import os
from datetime import timedelta, datetime


def read_chinese_file(filepath):
    f = open(filepath, 'r')
    lines = [line.strip() for line in f]
    for index, ch in enumerate(lines):
        lines[index] = str(ch).decode('utf-8')
    f.close()
    return lines


check_in_list = read_chinese_file('Check-inlist.txt')

checked_names = sys.stdin.readlines()
for index, ch in enumerate(checked_names):
    checked_names[index] = str(ch).decode('utf-8')

uncheck_list = []
for name in check_in_list:
    # 移除开头
    extract_name = name
    for index, ch in enumerate(name):
        if ch == " ":
            extract_name = name[index+1:]
            break

    # 移除末尾空格
    while len(extract_name) > 1 and extract_name[-1] == " ":
        extract_name = extract_name[:-2]

    found = False
    for checked_name in checked_names:
        if extract_name in checked_name:
            found = True
            break
    if found == False:
        uncheck_list.append(extract_name)

notification = "滴滴滴打卡提示！现在是北京时间："
output = "，请以下未完成打卡的姑娘尽量完成打卡哦"
print("\n\n"+notification.decode('utf-8')+time.strftime(
    "%Y-%m-%d %H:%M:%S", time.localtime())+output.decode('utf-8'))

for uncheck_name in uncheck_list:
    print('@'+uncheck_name)

# 写入当天打卡记录，判断时间是否早于当天下午四点，如果早于，则是前一天的打卡
end_check_time = datetime.strptime(
    str(datetime.now().date())+'16:00', '%Y-%m-%d%H:%M')

time_now = datetime.now()

if time_now < end_check_time:
    check_day = (datetime.today() + timedelta(-1)).strftime('%Y-%m-%d')
else:
    check_day = time_now.strftime('%Y-%m-%d')

check_log_f = open('log/'+check_day + ' checked.txt', 'w')
for checked_name in checked_names:
    check_log_f.write(checked_name.encode('utf-8'))
check_log_f.close()

uncheck_log_f = open('log/'+check_day + ' unchecked.txt', 'w')
for uncheck_name in uncheck_list:
    uncheck_log_f.write(uncheck_name.encode('utf-8'))
    uncheck_log_f.write('\n')
uncheck_log_f.close()

# 输出未打卡历史记录
uncheck_dict = {}
path = os.getcwd()+'/log'
files = os.listdir(path)
for file in files:
    if 'unchecked' in file:
        names = read_chinese_file(path + '/' + file)
        for name in names:
            if name in uncheck_dict:
                uncheck_dict[name] = uncheck_dict[name] + 1
            else:
                uncheck_dict[name] = 1

# 按未打卡次数排序
uncheck_thre = 7
sorted_pairs = sorted(uncheck_dict.items(), key=lambda kv: kv[1])
print('\n'+"多次未打卡名单".decode('utf-8'))
for pair in sorted_pairs:
    if pair[1] >= uncheck_thre:
        print(pair[0], end=' ')
        print(pair[1], end='')
        print("次".decode('utf-8'))
