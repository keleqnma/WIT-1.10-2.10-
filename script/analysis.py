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


def get_stat_dict(keyword, words):
    stat_dict = {}
    len_dict = {}
    path = os.getcwd()+'/script/log'
    files = os.listdir(path)
    for file in files:
        if keyword in file:
            lines = read_chinese_file(path + '/' + file)
            for line in lines:
                key = ""
                content_len = 0
                if keyword == 'unchecked':
                    key = line
                elif '. ' in line:
                    key, content_len = get_name_content_len(line)
                if len(key) <= 1:
                    continue
                if key in stat_dict:
                    stat_dict[key] = stat_dict[key] + 1
                else:
                    stat_dict[key] = 1
                if keyword != 'unchecked':
                    if key in len_dict:
                        len_dict[key] = len_dict[key] + content_len
                    else:
                        len_dict[key] = content_len
    print_dict(stat_dict, words, "次")
    if keyword != 'unchecked':
        avg_len_dict = {}
        print_dict(len_dict, "总打卡字数", "字")
        for key in stat_dict:
            # print(key, len_dict[key], stat_dict[key])
            avg_len_dict[key] = len_dict[key] / stat_dict[key]
        print_dict(avg_len_dict, "均打卡字数", "字")


def print_dict(stat_dict, words, quantifer):
    print("第二期"+words+"名单前五名:")
    sorted_pairs = sorted(
        stat_dict.items(), key=lambda kv: kv[1], reverse=True)
    top_three = sorted_pairs[:5]
    for pair in top_three:
        print(pair[0], end=' ')
        print(pair[1], end='')
        print(quantifer)
    print("")


def get_name_content_len(line):
    name = ""
    name_begin_idx = 0
    content_length = 0
    for index, ch in enumerate(line):
        if ch == " ":
            if name_begin_idx == 0:
                name_begin_idx = index + 1
            else:
                name = line[name_begin_idx:index]
                content_length = len(line) - index
                break
    return name, content_length


def get_word_freq():
    path = os.getcwd()+'/script/log'
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
    path = os.getcwd()+'/script'
    stopwords = read_chinese_file(path+'/cn_stopwords.txt')
    object_list = []
    for word in seg_list_exact:  # 循环读出每个分词
        if word not in stopwords:
            object_list.append(word)  # 分词追加到列表
    # 词频统计
    word_counts = collections.Counter(object_list)
    word_counts_top = word_counts.most_common(100)
    for key, time in word_counts_top:
        if ' ' not in key and len(key) > 0:
            print(key, ":", time, "次")


def cut_line(line):
    for index, ch in enumerate(line):
        if ch == ' ':
            line = line[index + 1:]
            return line
    return line


get_stat_dict('unchecked', '未打卡')
get_stat_dict(' checked', '打卡')
get_word_freq()
