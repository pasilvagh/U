# -*- coding: utf-

import random, time

#quantity of lines
quant = [10, 100, 1000, 10000, 100000]

#t = time.clock()
#create a seed according to the pc'c clock
#random.seed(t)

try:
	f = open("todostweets", "r")
	filelines = f.readlines()
	for lines in quant:
		for k in range(0,5):
			w = open("files/" + str(lines) + "_" +str(k)+".txt", "w")
			#this part can be improved...maybe using an external sampling algorithm
			t = time.clock()
			random.seed(t)
			random_choice = random.sample(filelines, lines)
			for line in random_choice:
                                lineTemp=line.replace('\n','')
                                if(lineTemp!=''):
					w.write(lineTemp)
                                	w.write('\n')
			w.close()
	f.close()

except IOError as mess:
	print "Error in files"
	print(mess)



