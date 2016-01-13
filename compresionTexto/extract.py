#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import shutil
import sys
import os
import commands
from time import time

ratio_10=0
tiempo_10=0
ratio_100=0
tiempo_100=0
ratio_1000=0
tiempo_1000=0
ratio_10000=0
tiempo_10000=0
ratio_100000=0
tiempo_100000=0
file=open('bzip2.txt')
for line in file:
	line=line.split(' ')
	if((line[0])[:-10]=='10'):
                ratio_10=ratio_10+float(line[3])/5
                tiempo_10=tiempo_10+float(line[4])/5
	if((line[0])[:-10]=='100'):
		ratio_100=ratio_100+float(line[3])/5
		tiempo_100=tiempo_100+float(line[4])/5
        if((line[0])[:-10]=='1000'):
                ratio_1000=ratio_1000+float(line[3])/5
                tiempo_1000=tiempo_1000+float(line[4])/5
        if((line[0])[:-10]=='10000'):
                ratio_10000=ratio_10000+float(line[3])/5
                tiempo_10000=tiempo_10000+float(line[4])/5
        if((line[0])[:-10]=='100000'):
                ratio_100000=ratio_100000+float(line[3])/5
                tiempo_100000=tiempo_100000+float(line[4])/5
file.close()
print('bzip2 10 '+ str(ratio_10) + ' '+ str(tiempo_10))
print('bzip2 100 '+ str(ratio_100) + ' '+ str(tiempo_100))
print('bzip2 1000 '+ str(ratio_1000) + ' '+ str(tiempo_1000))
print('bzip2 10000 '+ str(ratio_10000) + ' '+ str(tiempo_10000))
print('bzip2 100000 '+ str(ratio_100000) + ' '+ str(tiempo_100000))

ratio_10=0
tiempo_10=0
ratio_100=0
tiempo_100=0
ratio_1000=0
tiempo_1000=0
ratio_10000=0
tiempo_10000=0
ratio_100000=0
tiempo_100000=0
file=open('brotli.txt')
for line in file:
        line=line.split(' ')
        if((line[0])[:-10]=='10'):
                ratio_10=ratio_10+float(line[3])/5
                tiempo_10=tiempo_10+float(line[4])/5
	if((line[0])[:-10]=='100'):
                ratio_100=ratio_100+float(line[3])/5
                tiempo_100=tiempo_100+float(line[4])/5
        if((line[0])[:-10]=='1000'):
                ratio_1000=ratio_1000+float(line[3])/5
                tiempo_1000=tiempo_1000+float(line[4])/5
        if((line[0])[:-10]=='10000'):
                ratio_10000=ratio_10000+float(line[3])/5
                tiempo_10000=tiempo_10000+float(line[4])/5
        if((line[0])[:-10]=='100000'):
                ratio_100000=ratio_100000+float(line[3])/5
                tiempo_100000=tiempo_100000+float(line[4])/5
file.close()
print('bro 10 '+ str(ratio_10) + ' '+ str(tiempo_10))
print('bro 100 '+ str(ratio_100) + ' '+ str(tiempo_100))
print('bro 1000 '+ str(ratio_1000) + ' '+ str(tiempo_1000))
print('bro 10000 '+ str(ratio_10000) + ' '+ str(tiempo_10000))
print('bro 100000 '+ str(ratio_100000) + ' '+ str(tiempo_100000))

ratio_10=0
tiempo_10=0
ratio_100=0
tiempo_100=0
ratio_1000=0
tiempo_1000=0
ratio_10000=0
tiempo_10000=0
ratio_100000=0
tiempo_100000=0
file=open('LZMA.txt')
for line in file:
        line=line.split(' ')
        if((line[0])[:-9]=='10'):
                ratio_10=ratio_10+float(line[3])/5
                tiempo_10=tiempo_10+float(line[4])/5
	if((line[0])[:-9]=='100'):
                ratio_100=ratio_100+float(line[3])/5
                tiempo_100=tiempo_100+float(line[4])/5
        if((line[0])[:-9]=='1000'):
                ratio_1000=ratio_1000+float(line[3])/5
                tiempo_1000=tiempo_1000+float(line[4])/5
        if((line[0])[:-9]=='10000'):
                ratio_10000=ratio_10000+float(line[3])/5
                tiempo_10000=tiempo_10000+float(line[4])/5
        if((line[0])[:-9]=='100000'):
                ratio_100000=ratio_100000+float(line[3])/5
                tiempo_100000=tiempo_100000+float(line[4])/5
file.close()
print('LZMA 10 '+ str(ratio_10) + ' '+ str(tiempo_10))
print('LZMA 100 '+ str(ratio_100) + ' '+ str(tiempo_100))
print('LZMA 1000 '+ str(ratio_1000) + ' '+ str(tiempo_1000))
print('LZMA 10000 '+ str(ratio_10000) + ' '+ str(tiempo_10000))
print('LZMA 100000 '+ str(ratio_100000) + ' '+ str(tiempo_100000))

ratio_10=0
tiempo_100=0
ratio_100=0
tiempo_100=0
ratio_1000=0
tiempo_1000=0
ratio_10000=0
tiempo_10000=0
ratio_100000=0
tiempo_100000=0
file=open('zopfli.txt')
for line in file:
        line=line.split(' ')
        if((line[0])[:-9]=='10'):
                ratio_10=ratio_10+float(line[3])/5
                tiempo_10=tiempo_10+float(line[4])/5
	if((line[0])[:-9]=='100'):
                ratio_100=ratio_100+float(line[3])/5
                tiempo_100=tiempo_100+float(line[4])/5
        if((line[0])[:-9]=='1000'):
                ratio_1000=ratio_1000+float(line[3])/5
                tiempo_1000=tiempo_1000+float(line[4])/5
        if((line[0])[:-9]=='10000'):
                ratio_10000=ratio_10000+float(line[3])/5
                tiempo_10000=tiempo_10000+float(line[4])/5
        if((line[0])[:-9]=='100000'):
                ratio_100000=ratio_100000+float(line[3])/5
                tiempo_100000=tiempo_100000+float(line[4])/5
file.close()
print('Zopfli 10 '+ str(ratio_10) + ' '+ str(tiempo_10))
print('Zopfli 100 '+ str(ratio_100) + ' '+ str(tiempo_100))
print('Zopfli 1000 '+ str(ratio_1000) + ' '+ str(tiempo_1000))
print('Zopfli 10000 '+ str(ratio_10000) + ' '+ str(tiempo_10000))
print('Zopfli 100000 '+ str(ratio_100000) + ' '+ str(tiempo_100000))

ratio_10=0
tiempo_10=0
ratio_100=0
tiempo_100=0
ratio_1000=0
tiempo_1000=0
ratio_10000=0
tiempo_10000=0
ratio_100000=0
tiempo_100000=0
file=open('gzip.txt')
for line in file:
        line=line.split(' ')
        if((line[0])[:-10]=='10'):
                ratio_10=ratio_10+float(line[3])/5
                tiempo_10=tiempo_10+float(line[4])/5
        if((line[0])[:-10]=='100'):
                ratio_100=ratio_100+float(line[3])/5
                tiempo_100=tiempo_100+float(line[4])/5
        if((line[0])[:-10]=='1000'):
                ratio_1000=ratio_1000+float(line[3])/5
                tiempo_1000=tiempo_1000+float(line[4])/5
        if((line[0])[:-10]=='10000'):
                ratio_10000=ratio_10000+float(line[3])/5
                tiempo_10000=tiempo_10000+float(line[4])/5
        if((line[0])[:-10]=='100000'):
                ratio_100000=ratio_100000+float(line[3])/5
                tiempo_100000=tiempo_100000+float(line[4])/5
file.close()
print('gzip 10 '+ str(ratio_10) + ' '+ str(tiempo_10))
print('gzip 100 '+ str(ratio_100) + ' '+ str(tiempo_100))
print('gzip 1000 '+ str(ratio_1000) + ' '+ str(tiempo_1000))
print('gzip 10000 '+ str(ratio_10000) + ' '+ str(tiempo_10000))
print('gzip 100000 '+ str(ratio_100000) + ' '+ str(tiempo_100000))



ratio_10=0
tiempo_10=0
ratio_100=0
tiempo_100=0
ratio_1000=0
tiempo_1000=0
ratio_10000=0
tiempo_10000=0
ratio_100000=0
tiempo_100000=0
file=open('lzhma.txt')
for line in file:
        line=line.split(' ')
        if((line[0])[:-12]=='10'):
                ratio_10=ratio_10+float(line[3])/5
                tiempo_10=tiempo_10+float(line[4])/5
        if((line[0])[:-12]=='100'):
                ratio_100=ratio_100+float(line[3])/5
                tiempo_100=tiempo_100+float(line[4])/5
        if((line[0])[:-12]=='1000'):
                ratio_1000=ratio_1000+float(line[3])/5
                tiempo_1000=tiempo_1000+float(line[4])/5
        if((line[0])[:-12]=='10000'):
                ratio_10000=ratio_10000+float(line[3])/5
                tiempo_10000=tiempo_10000+float(line[4])/5
        if((line[0])[:-12]=='100000'):
                ratio_100000=ratio_100000+float(line[3])/5
                tiempo_100000=tiempo_100000+float(line[4])/5
file.close()
print('lzhma 10 '+ str(ratio_10) + ' '+ str(tiempo_10))
print('lzhma 100 '+ str(ratio_100) + ' '+ str(tiempo_100))
print('lzhma 1000 '+ str(ratio_1000) + ' '+ str(tiempo_1000))
print('lzhma 10000 '+ str(ratio_10000) + ' '+ str(tiempo_10000))
print('lzhma 100000 '+ str(ratio_100000) + ' '+ str(tiempo_100000))

