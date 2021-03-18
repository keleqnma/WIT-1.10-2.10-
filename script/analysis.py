#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 输出未打卡历史记录
import os
import jieba
import re
import collections


def read_chinese_file(filepath):
    f = open(filepath, 'r')
    lines = [line.strip() for line in f]
    f.close()
    return lines


def get_stat_dict(keyword):
    stat_dict = {}
    path = os.getcwd()+'/log'
    files = os.listdir(path)
    for file in files:
        if keyword in file:
            names = read_chinese_file(path + '/' + file)
            for name in names:
                if name in stat_dict:
                    stat_dict[name] = stat_dict[name] + 1
                else:
                    stat_dict[name] = 1
    sorted_pairs = sorted(
        stat_dict.items(), key=lambda kv: kv[1], reverse=True)
    print("第二期未打卡名单排行:")
    for pair in sorted_pairs:
        print(pair[0], end=' ')
        print(pair[1], end='')
        print("次")


def get_word_freq():
    path = os.getcwd()+'/log'
    files = os.listdir(path)
    string_data = ""
    for file in files:
        if ' checked' in file:
            lines = read_chinese_file(path + '/' + file)
            for index, line in enumerate(lines):
                if len(line) == 0:
                    lines = lines[index + 1:]
                    break
            for index, line in enumerate(lines):
                if line == None:
                    continue
                lines[index] = cut_line(line)
                line = lines[index]
                lines[index] = cut_line(line)
                if lines[index] != None:
                    string_data += lines[index]
    seg_list_exact = jieba.cut(string_data, cut_all=False, HMM=True)
    stopwords = read_chinese_file('cn_stopwords.txt')
    object_list = []
    for word in seg_list_exact:  # 循环读出每个分词
        if word not in stopwords:
            object_list.append(word)  # 分词追加到列表
    # 词频统计
    word_counts = collections.Counter(object_list)       # 对分词做词频统计
    word_counts_top = word_counts.most_common(100)
    for key, time in word_counts_top:
        print(key, ":", time, "次")


def cut_line(line):
    for index, ch in enumerate(line):
        if ch == ' ':
            line = line[index + 1:]
            return line
    return line


get_stat_dict('unchecked')
get_word_freq()
