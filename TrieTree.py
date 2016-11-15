class TrieTree(object):
    wordlist = []
    def __init__(self):
        self.wordlist = []
        self.treedict = {}

    def add(self, word, contains):
        treedict = self.treedict
        tree = self
        for i in range(len(word)):
            char = word[i]
            if char in treedict.keys():
                tree = treedict[char]
            else:
                treedict[char] = TrieTree()
                tree = treedict[char]
            treedict = tree.treedict
            if i == len(word) - 1:
                tree.wordlist.append(contains)


    def search(self, word):
        tree = self
        treedict = self.treedict
        for char in word:
            if char in treedict:
                tree = treedict[char]
                treedict = tree.treedict
            else:
                return []

 
        return tree.wordlist
     
    
    def read_file(self, filename):
        with file('dict.txt ','rb') as longsentences:
            for line in longsentences:
                #line = line.encode('utf-8')
                line = line.decode('utf-8')
                line = line.replace('\n', '')
                line = line.replace('\r', '')
                line = line.replace('?', '1')
                phases = line.split('\t')
                if len(phases) != 3:
                    continue
                rawpinyin = phases[0]
                word = phases[1]
                freq = phases[2]
                pinyin = rawpinyin.replace(' ', '')
                pinyin_list = rawpinyin.split(' ')
                self.add(pinyin, (pinyin_list, word, int(freq)))
                
if __name__ == '__main__':
    a = TrieTree()
    a.read_file('')
    print a.search('zhongguogongchandang')
                
                