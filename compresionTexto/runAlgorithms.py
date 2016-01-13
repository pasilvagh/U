#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs 
import shutil 
import sys 
import os
import commands
from time import time

def list_files(path):
	files = []
    	for name in os.listdir(path):
        	if os.path.isfile(os.path.join(path, name)):
            		files.append(name)
    	return files 

def limpia():
	os.system("rm -rf "+url+"*.bz2")
	os.system("rm -rf "+url+"*.gz")
	os.system("rm -rf "+url+"*.7z")
	os.system("rm -rf "+url+"*.bro")
	os.system("rm -rf "+url+"*.gz2")
	os.system("rm -rf "+url+"*.lzhma")                       

def compress_bzip2(url):
        fichero=open('bzip2.txt','w')
        for file in list_files(url):
		start_time = time()
                status, output = commands.getstatusoutput("bzip2-1.0.6/bzip2 -c "+url+file+" > "+url+file+".bz2")
		elapsed_time = time() - start_time
		sizeOr=os.path.getsize(url+file)
		sizeCom=os.path.getsize(url+file+".bz2")
		ratio=float(float(sizeCom)/float(sizeOr))*100		
		fichero.write(file+'.bz2 '+str(sizeOr)+' '+str(sizeCom)+' '+str(ratio)+' '+str(elapsed_time)+'\n')
	fichero.close()	


def compress_zopfli(url):
        fichero=open('zopfli.txt','w')
	for file in list_files(url):
                start_time = time()
                status, output = commands.getstatusoutput("zopfli/zopfli "+url+file)
                elapsed_time = time() - start_time
                sizeOr=os.path.getsize(url+file)
                sizeCom=os.path.getsize(url+file+".gz")
                ratio=float(float(sizeCom)/float(sizeOr))*100
                fichero.write(file+'.gz '+str(sizeOr)+' '+str(sizeCom)+' '+str(ratio)+' '+str(elapsed_time)+'\n')
        fichero.close()

def compress_LZMA(url):
 	fichero=open('LZMA.txt','w')
        for file in list_files(url):
                start_time = time()
                status, output = commands.getstatusoutput("7za a "+url+file+".7z "+url+file)
                elapsed_time = time() - start_time
                sizeOr=os.path.getsize(url+file)
                sizeCom=os.path.getsize(url+file+".7z")
                ratio=float(float(sizeCom)/float(sizeOr))*100
                fichero.write(file+'.7z '+str(sizeOr)+' '+str(sizeCom)+' '+str(ratio)+' '+str(elapsed_time)+'\n')
        fichero.close()


def compress_brotli(url):
        fichero=open('brotli.txt','w')
        for file in list_files(url):
                start_time = time()
                status, output = commands.getstatusoutput("brotli-master/tools/./bro --input "+url+file+" --output "+url+file+".bro")
                elapsed_time = time() - start_time
                sizeOr=os.path.getsize(url+file)
                sizeCom=os.path.getsize(url+file+".bro")
                ratio=float(float(sizeCom)/float(sizeOr))*100
                fichero.write(file+'.bro '+str(sizeOr)+' '+str(sizeCom)+' '+str(ratio)+' '+str(elapsed_time)+'\n')
        fichero.close()

def compress_gzip(url):
        fichero=open('gzip.txt','w')
        for file in list_files(url):
                start_time = time()
                status, output = commands.getstatusoutput("gzip -c "+url+file+" > "+url+file+".gz2")
                elapsed_time = time() - start_time
                sizeOr=os.path.getsize(url+file)
                sizeCom=os.path.getsize(url+file+".gz2")
                ratio=float(float(sizeCom)/float(sizeOr))*100
                fichero.write(file+'.gz2 '+str(sizeOr)+' '+str(sizeCom)+' '+str(ratio)+' '+str(elapsed_time)+'\n')
        fichero.close()

def compress_lzhma(url):
        fichero=open('lzhma.txt','w')
	cont=0
        for file in list_files(url):
                start_time = time()
		if(cont==0):
			os.chdir("lzham_codec/bin_linux")
		cont=cont+1
                status, output = commands.getstatusoutput("./lzhamtest c ../../"+url+file+" ../../"+url+file+".lzhma")
               	elapsed_time = time() - start_time
                sizeOr=os.path.getsize("../../"+url+file)
                sizeCom=os.path.getsize("../../"+url+file+".lzhma")
                ratio=float(float(sizeCom)/float(sizeOr))*100
                fichero.write(file+'.lzhma '+str(sizeOr)+' '+str(sizeCom)+' '+str(ratio)+' '+str(elapsed_time)+'\n')
	fichero.close()

url='trabajo/files/'
limpia()
compress_bzip2(url)
limpia()
compress_zopfli(url)
limpia()
compress_LZMA(url)
limpia()
compress_brotli(url)
limpia()
compress_gzip(url)
limpia()
compress_lzhma(url)
