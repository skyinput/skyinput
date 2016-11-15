import os
import string
import copy

dict_path = 'syllable.bdt'
all_pinyin = set()
max_pinyin_len = 6
with open(dict_path, 'r', ) as f:
    for line in f:
        all_pinyin.add(line.strip())

shengmu = ['b', 'p', 'm', 'f', 'd', 't', 'n', 'l', 'g', 'k', 'h', 'zh', 'ch', 'sh', 'z', 'c', 's', 'y', 'w']
jqx = ['j', 'q', 'x', 'r']
yunmu = ['a', 'o', 'e', 'i', 'u', 'v', 'ai', 'ei', 'ui', 'ao', 'ou', 'iu', 'ie', 've', 'er', 'an', 'en', 'in', 'un', 'vn', 'ang', 'eng', 'ing', 'ong']
def cut(sequen):
    if not len(sequen):
        return [[]]
    sequen = sequen.lower()
    sub_sequen = sequen.split()
    path_list = [[]]
    for subs in sub_sequen:
        temp_path_list = []
        lenght = len(subs)
        for j in xrange(min(max_pinyin_len, lenght + 1)):
            if subs[0:j] in all_pinyin:            
                if j==lenght:#the last word
                    temp_path_list.append([subs[0:j]])
                else:
                    after = cut(subs[j:lenght])
                    if len(after):
                        now = []
                        now.append(subs[0:j])
                        for after_list in after:
                            v = copy.copy(now)  
                            v.extend(after_list)
                            temp_path_list.append(v)
        temp_new = []
        for path in path_list:    
            for sub_list in temp_path_list:   
                v = copy.copy(path)
                v.extend(sub_list)
                temp_new.append(v)
        path_list = temp_new
        
    global shengmu, yunmu,jqx
    
    if not len(path_list) or not len(path_list[0]):#error
        last = sequen[-1]
        lasttwo = sequen[len(sequen) - 2: len(sequen)]
        if last in shengmu or lasttwo in shengmu:
            sequen = sequen + 'a'
        elif last in jqx:
            sequen = sequen + 'i'
        else:
            return path_list
        path_list = cut(sequen)
            
        
    return path_list
    
    
#for test
if __name__ == '__main__':
    a = cut('g')
    for x in a:
        print x[0:1]
    print a