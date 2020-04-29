import os
import re
from datetime import datetime
from tkinter import *
from tkinter.filedialog import askdirectory

# pyinstaller -F -w tellog2csv.py

file_rule=os.getcwd()+'\\tellog2csv.cfg'
file_directory = ''
file_result = ''
rule_def=[[0,5],[7,12],[14,19],[21,25],[28,32],[42,46],[54,55],[58,76],[76,77],[79,80],[82,102]]
rule=rule_def.copy()

def get_rule():
    global rule
    if os.path.exists(file_rule):
        rule=[]
        with open(file_rule) as file_in:
            for line in file_in:
                rule.append(line.split())

def clear_str(str_in):
    get_rule()
    global rule
    str_out=''
    for i in rule:
        str_out += str_in[int(i[0]):int(i[1])]+';'
    return str_out

def pars_tellog(tellog_src, file_name):
    s=len(tellog_src)
    i=0
    tellog_tbl=[]
    if s>0:
        while i<s:
            if (tellog_src[i].find('/')==2 and i<s-1):
                tellog_tbl.append(clear_str(tellog_src[i]+tellog_src[i+1]) + file_name + '\n')
            i+=1
    return tellog_tbl

def main_p():
    global file_result
    file_result= os.getcwd() + '\\result_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.csv'
    for file_src in os.listdir(file_directory):
        lines=[]
        with open(file_directory + '\\' + file_src) as file_in:
            lines += file_in.readlines()
        with open(file_result, "a") as file_out:
            file_out.write(''.join(pars_tellog(lines, file_src)))

def clicked1():
    global file_directory
    file_directory = askdirectory()
    lbl1.configure(text=file_directory)

def clicked2():
    global file_directory
    if file_directory == '':
        lbl2.configure(text='Каталог не задан')
    else:
        main_p()
        lbl2.configure(text='Файл сформирован: '+ file_result)

def clicked3():
    global file_rule
    global rule_def
    with open(file_rule, "w") as file_ru:
        for i in rule:
                file_ru.write(str(i[0])+' '+str(i[1])+'\n')
    lbl3.configure(text='Файл настроек создан: '+ file_rule)

window = Tk()
window.geometry('400x250')
window.title("tellog2csv")
btn1 = Button(window, text="Выбрать каталог с Логами", command=clicked1)
btn1.grid(column=0, row=0)
lbl1 = Label(window, text="Каталог не выбран")
lbl1.grid(column=0, row=1)
btn2 = Button(window, text="Конвертация", command=clicked2)
btn2.grid(column=0, row=2)
lbl2 = Label(window, text="")
lbl2.grid(column=0, row=3)
btn3 = Button(window, text="Сбросить настройки", command=clicked3)
btn3.grid(column=0, row=4)
if os.path.exists(file_rule)==FALSE:
    lbl3 = Label(window, text="Используются стандартные настройки")
else:
    lbl3 = Label(window, text="Используются настройки: "+file_rule)
lbl3.grid(column=0, row=5)

window.mainloop()
get_rule()