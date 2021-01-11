#!/usr/bin/python
# -*- coding: UTF-8 -*-
import codecs
import sys
import time

f = open('Check-inlist.txt', 'r')
check_in_list = [line.strip() for line in f]
for index, ch in enumerate(check_in_list):
    check_in_list[index] = str(ch).decode('utf-8')
f.close()

checked_names = sys.stdin.readlines()
for index, ch in enumerate(checked_names):
    checked_names[index] = str(ch).decode('utf-8')
uncheck_list = []

notification = "滴滴滴打卡提示！现在是北京时间："
output = "，请以下未完成打卡的姑娘尽量完成打卡哦"
print ("\n\n"+notification.decode('utf-8')+time.strftime(
    "%Y-%m-%d %H:%M:%S", time.localtime())+output.decode('utf-8'))

for name in check_in_list:
    # 移除开头
    extract_name = name
    for index, ch in enumerate(name):
        if ch == "@":
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
        uncheck_list.append(name)

for uncheck_name in uncheck_list:
    print(uncheck_name)
