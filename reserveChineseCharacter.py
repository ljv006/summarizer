# -*- coding: utf-8 -*-
"""
输入文件格式需要是gb2312
"""
import checkLegal

def reserveChinese(line):
    strBuffer = line.decode('utf-8', 'ignore')
    str = ""
    for oneWord in strBuffer:
        if checkLegal.is_chinese(oneWord):
            str += oneWord
    str = str.encode('utf-8')
    return str