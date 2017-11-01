#coding=utf-8
import jieba.analyse
import re
import jieba.posseg as pseg

sentenceNum = 2
sourceFile = open("source_text/IT/2.txt",'rb')
# for line in sourceFile:
#     sourceDocument += line
stopWordPath = "stopWord"
stopWordFile = open(stopWordPath, "rb")
jieba.analyse.set_stop_words(stopWordPath)

def ReduceRedundancy(sentenceList):
    resultSentenceList = sentenceList
    return resultSentenceList


# 设置分句的标志符号；可以根据实际需要进行修改
cutlist = "。！？".decode('utf-8')

# 检查某字符是否分句标志符号的函数；如果是，返回True，否则返回False
def FindToken(cutlist, char):
    if char in cutlist:
        return True
    else:
        return False

# 进行分句的核心函数
def Cut(cutlist, lines):  # 参数1：引用分句标志符；参数2：被分句的文本，为一行中文字符
    l = []  # 句子列表，用于存储单个分句成功后的整句内容，为函数的返回值
    line = []  # 临时列表，用于存储捕获到分句标志符之前的每个字符，一旦发现分句符号后，就会将其内容全部赋给l，然后就会被清空

    for i in lines:  # 对函数参数2中的每一字符逐个进行检查 （本函数中，如果将if和else对换一下位置，会更好懂）
        if FindToken(cutlist, i):  # 如果当前字符是分句符号
            line.append(i)  # 将此字符放入临时列表中
            l.append(''.join(line))  # 并把当前临时列表的内容加入到句子列表中
            line = []  # 将符号列表清空，以便下次分句使用
        else:  # 如果当前字符不是分句符号，则将该字符直接放入临时列表中
            line.append(i)
    return l

def extractive_summarization(inputFile):
    #step1 surface liguistic
    #将句子放进一个list里，以结束标点来分界。
    # separator = "。|！|？"
    # sourceSentenceList = re.split(separator, sourceDocument)
    sourceSentenceList = []
    sourceDocument = ""
    #以下为调用上述函数实现从文本文件中读取内容并进行分句。
    for lines in sourceFile:
        l = Cut(list(cutlist),list(lines.decode('utf-8')))
        for line in l:
           if line.strip()!="":
                li = line.strip().split()
                for sentence in li:
                    sourceDocument += sentence
                    sourceSentenceList.append(sentence)
    # for sen in sourceSentenceList:
    #     print sen

    #step2 redundancy detection
    #TE tool
    withoutRedundancySentenceList = ReduceRedundancy(sourceSentenceList)

    #step3 topic identification
    keyWordList = jieba.analyse.extract_tags(sourceDocument, topK=10, withWeight=False, allowPOS=())
    print "KeyWords: "
    for index, item in enumerate(keyWordList):
        print str(index + 1) + ": " + item

    #step4 relevance detection
    #code quantity principle(CQP)
    #一个句子中，含有包含主题词的短语越长，它的重要性越大，得分越高
    sortedSentenceMap = {}
    for sen in withoutRedundancySentenceList:
        mark  = 0
        seg_list = jieba.cut(sen)
        poss_list = pseg.cut(sen)
        for i in range(0, len(keyWordList)):
            for word in poss_list:
                if word.flag == "t" or word.flag == "tg":
                    mark += 1
            if keyWordList[i] in seg_list:
                mark += len(keyWordList) - i
        sortedSentenceMap.__setitem__(sen, mark)
    sortedSentenceMap = sorted(sortedSentenceMap.items(), key=lambda sortedSentenceMap:sortedSentenceMap[1], reverse=True)

    #step5 summary generation
    resultList = []
    for sen in withoutRedundancySentenceList:
        cnt = 0
        for key, value in sortedSentenceMap:
            if cnt >= sentenceNum:
                break
            if sen == key:
                resultList.append(sen.replace('\n', '').replace(' ', ''))
                break
            cnt += 1
    extractive_summary = ""
    for sen in resultList:
        extractive_summary += sen
    return extractive_summary

extractive_summary = extractive_summarization(sourceFile)
def similarityCalculate(sen1, sen2):
    return 0
def abstractive_summarization(extractive_summary):
    abstractive_summary = ""
    separator = "。"
    extractSentList = re.split(separator, extractive_summary)
    #1 building word graph
    word_list = []
    first_word_list = []
    for sen in extractSentList:
        word_list_local = list(jieba.cut(sen.encode("utf-8").replace("，","").replace("。", "")))
        first_word_list.append(word_list_local[0])
        word_list.extend(word_list_local)
    for word in word_list:
        print word
    for first_word in first_word_list:
        print first_word


    #2 filtering incorrect path

    correctPathList = []
    #3 making combination
    result_list = []
    for extractSent in extractSentList:
        for correctPathSent in correctPathList:
            if similarityCalculate(extractSent, correctPathSent) > 0.5:
                result_list.append(correctPathSent)
            else:
                result_list.append(extractSent)
    for sen in result_list:
        abstractive_summary += sen
    return abstractive_summary
print abstractive_summarization(extractive_summary)
