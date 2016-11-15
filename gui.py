from Tkinter import *
import os
import string
import tkFont
from pinyin.hmm import viterbi as vb
import pinyincut
from TrieTree import TrieTree
from PIL import Image

alphabets='abcdefghijklmnopqrstuvwxyz'

#number = ['0', '1', '2'. '3', '4', '5', '6', '7', '8', '9']
candidate = []
PAGE_SIZE = 5
page_index = 0
current_page_size = 0
cursor_location = 0

long_sentences = TrieTree()
long_sentences.read_file('dict.txt')


def pagedown():
    global  candidate, page_index, PAGE_SIZE, current_page_size,cursor_location
     
    total = len(candidate)
     
    if page_index * PAGE_SIZE + current_page_size < total:
        page_index = page_index + 1
        current_page_size = min(total - page_index * PAGE_SIZE, PAGE_SIZE)

    result = []
    for i in range(1, current_page_size + 1):
        result.append(str(i) + "." + candidate[page_index*PAGE_SIZE + i - 1][0])
    
    return '\n'.join(result)
    
def pageup():
    global  candidate, page_index, PAGE_SIZE, current_page_size,cursor_location
     
    total = len(candidate)
     
    if page_index > 0:
        page_index = page_index - 1
        current_page_size = PAGE_SIZE
    result = []
    for i in range(1, current_page_size + 1):
        result.append(str(i) + "." + candidate[page_index*PAGE_SIZE + i - 1][0])
    return '\n'.join(result)

def clikpageup():
    global E1, T1
    result = pageup()
    E1.update()
    T1.delete(1.0,END)
    T1.insert(END,result)
def clikpagedown():
    global E1, T1
    result = pagedown()
    E1.update()
    T1.delete(1.0,END)
    T1.insert(END,result)

def lookup_long_sentences(word):
    #global long_sentences
    
    word = word.lower()
    word = word.replace(' ', '')
    longsent = long_sentences.search(word)
    cand = []
    for sent in longsent:
        cand.append((sent[1], sent[2], sent[0]))#word prob and pinyin and freq is bigger than any prob
    return cand



def lookup_result(word):
    
    global  candidate, page_index, PAGE_SIZE, current_page_size, cursor_location
    word = word.lower()
        
    
    
    pinyin_sequen_list = pinyincut.cut(word)
    path_num = len(pinyin_sequen_list)
    #path_v_map = {}
    
    candidate = lookup_long_sentences(word)
    for pinyin_sequen in pinyin_sequen_list:
        if len(pinyin_sequen):
            V, index = vb.viterbi(pinyin_sequen)
            for charac_zh, prob in V.items():
                candidate.append((charac_zh, prob, pinyin_sequen[0:index]))
            #path_v_map=dict(path_v_map, **V)
    
    candiset = set()
    index = 0
    while index < len(candidate):        
        tup = candidate[index]
        if tup[0] in candiset:
            candidate.remove(tup)
            continue
        else:
            candiset.add(tup[0])
        index = index + 1
    #i is used to indicate id
    candidate = sorted(candidate, key=lambda d: d[1], reverse=True)
    #remove congfu de
    
    
    page_index = 0
    current_page_size = min(PAGE_SIZE, len(candidate))
    result = []
    for i in range(1, current_page_size + 1):
        result.append(str(i) + "." + candidate[page_index*PAGE_SIZE + i - 1][0])
    return '\n'.join(result)
    #for path, pro in sorted(path_v_map.items(), key=lambda d: d[1], reverse=True):
    #    result.append(path)
    

def on_press(event):
    global E1,T1, T2, candidate, PAGE_SIZE, page_index, current_page_size, cursor_location
    #number key
    
    #翻页
    print event.keycode
  
    word = E1.get().encode('utf-8')
    word = word.lower()
    
    if event.keycode == 40 or event.keycode == 187:#down_key or +/=_key
        if event.keycode == 187:
             E1.delete(cursor_location, cursor_location + 1)
        result = pagedown()
    elif event.keycode == 38 or event.keycode == 189:#up_key or _-_key
        if event.keycode == 189:
             E1.delete(cursor_location, cursor_location + 1)
        result = pageup()
        
    #chose
    elif event.keycode in range(48, 58):
        E1.delete(cursor_location, cursor_location + 1)
        word = E1.get().encode('utf-8')
        word = word.lower()
        if (event.keycode - 48) in range(1, current_page_size+ 1):
            T2.insert(END, candidate[page_index * PAGE_SIZE +(event.keycode - 49)][0])  
             #zhao到最后一个拼音的位置
            choesen_list = candidate[page_index * PAGE_SIZE +(event.keycode - 49)][2]
            
            last_pinyin_index = 0
            for pin in choesen_list:
                last_pinyin_index = word.find(pin, last_pinyin_index)
            delete_index = min(last_pinyin_index + len(choesen_list[-1]), cursor_location)
            print 'lastpinyin index', last_pinyin_index
            print 'delte_last', choesen_list[-1]
            print 'delte_index', delete_index
            E1.delete(0, delete_index)
            word = E1.get().encode('utf-8')
            cursor_location =  cursor_location - delete_index
            tolook = word[0:cursor_location]
            result = lookup_result(tolook)
        else:#ignore other number ke
            text = []
            for i in range(1, current_page_size + 1):
                text.append(str(i) + "." + candidate[page_index*PAGE_SIZE + i - 1][0])
            result = '\n'.join(text)
    elif event.keycode in range(96, 106):
        E1.delete(cursor_location, cursor_location + 1)
        word = E1.get().encode('utf-8')
        word = word.lower()
        if (event.keycode - 96) in range(1, current_page_size+ 1):
            T2.insert(END, candidate[page_index * PAGE_SIZE +(event.keycode - 97)][0])  
             #zhao到最后一个拼音的位置
            choesen_list = candidate[page_index * PAGE_SIZE +(event.keycode - 97)][2]
            last_pinyin_index = 0
            for pin in choesen_list:
                last_pinyin_index = word.find(pin, last_pinyin_index)
            delete_index = min(last_pinyin_index + len(choesen_list[-1]), cursor_location)
            print 'lastpinyin index', last_pinyin_index
            print 'delte_last', choesen_list[-1]
            print 'delte_index', delete_index
            E1.delete(0, delete_index)
            word = E1.get().encode('utf-8')
            cursor_location =  cursor_location - delete_index
            tolook = word[0:cursor_location]
            result = lookup_result(tolook)
        else:#ignore other number key
           
            text = []
            for i in range(1, current_page_size + 1):
                text.append(str(i) + "." + candidate[page_index*PAGE_SIZE + i - 1][0])
            result = '\n'.join(text)
    elif event.keycode == 13:#enter
        if len(candidate):
            T2.insert(END, candidate[page_index * PAGE_SIZE][0])  
             #zhao到最后一个拼音的位置
            choesen_list = candidate[page_index * PAGE_SIZE][2]
            last_pinyin_index = 0
            for pin in choesen_list:
                last_pinyin_index = word.find(pin, last_pinyin_index)
            delete_index = min(last_pinyin_index + len(choesen_list[-1]), cursor_location)
            print 'lastpinyin index', last_pinyin_index
            print 'delte_last', choesen_list[-1]
            print 'delte_index', delete_index
            E1.delete(0, delete_index)
            word = E1.get().encode('utf-8')
            cursor_location =  cursor_location - delete_index
        tolook = word[0:cursor_location]
        result = lookup_result(tolook)
    elif event.keycode in range(65, 91) or event.keycode == 8 or event.keycode == 46 or event.keycode == 32:#a-Z or backspace or delete or space
        if event.keycode == 8:
            cursor_location = max(0, cursor_location - 1)
        elif event.keycode != 46:#delete cursor dont move
            cursor_location = min(len(word), cursor_location + 1)
        tolook = word[0:cursor_location]
        result = lookup_result(tolook)
    elif event.keycode == 37 or event.keycode == 39:#left or right
        cursor_location = cursor_location + event.keycode -38
        if cursor_location < 0:
            cursor_location = 0
        elif cursor_location > len(word):
            cursor_location = len(word)
        tolook = word[0:cursor_location]
        result = lookup_result(tolook)
    else:#default
        text = []
        for i in range(1, current_page_size + 1):
            text.append(str(i) + "." + candidate[page_index*PAGE_SIZE + i - 1][0])
        result = '\n'.join(text)
   #igonore other key
    
   
    #E1.insert(0, word)
    #E1.icursor(location)
    E1.update()
    
    T1.delete(1.0,END)
    T1.insert(END,result)
   
        

def on_alt_d(event):
    global E1
    E1.focus_set()
    E1.select_range(0, END)

def on_esc(event):
    global E1
    E1.delete(0, END)

root = Tk()
root.title("SkyInput——We are little fairies")
root.resizable(0,0)
root.iconbitmap('skyinput.ico')


frame1 = Frame(root,width=480,height=50)
frame1.pack_propagate(0)
frame1.pack()


frame2 = Frame(root,width=480,height=180)
frame2.pack_propagate(0)
frame2.pack()

frame3 = Frame(root,width=480,height=300)
frame3.pack_propagate(0)
frame3.pack()

frameB = Frame(frame2,width=50,height=180)
frameB.pack_propagate(0)
frameB.pack(side=RIGHT,expand=True)
frameT1 = Frame(frame2,width=430,height=180)
frameT1.pack_propagate(0)
frameT1.pack(side=LEFT,expand=True)


L1 = Label(frame1, text="SkyInput", fg = 'Chocolate', font=tkFont.Font(size=16,weight='bold'))
L1.pack(side=LEFT)

E1 = Entry(frame1,width=400,font=tkFont.Font(size=20,weight='bold'))
E1.pack(side=RIGHT,expand=True)
E1.focus_set()
T1 = Text(frameT1,height=480,wrap='word',fg = 'Chocolate',font=tkFont.Font(size=25,weight='bold'))
T1.pack(expand=True)
T2 = Text(frame3,height=480,wrap='word',font=tkFont.Font(size=20))
T2.pack(expand=True)

frameBup = Frame(frameB,width=50,height=90)
frameBup.pack_propagate(0)
frameBup.pack(side=TOP,expand=True)
frameBdown = Frame(frameB,width=50,height=90)
frameBdown.pack_propagate(0)
frameBdown.pack(side=BOTTOM,expand=True)

photoup=PhotoImage(file='up.gif')

photodown=PhotoImage(file='down.gif')
Bup = Button(frameBup, image = photoup, command = clikpageup)
Bup.pack()
Bdown = Button(frameBdown, image= photodown, command = clikpagedown)
Bdown.pack()

E1.bind("<KeyRelease>",on_press)
root.bind("<Alt-d>",on_alt_d)
root.bind("<Escape>",on_esc)


if __name__ == "__main__":
    root.mainloop()
