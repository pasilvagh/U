# -*- coding: utf-8

import time

#path to
test_dataset = "/home/admin/compresion/dataset/test_set_tweets.txt"
training_dataset = "/home/admin/compresion/dataset/training_set_tweets.txt"
		
tweetstest = []
tweetstrai = []
#open files
try:
	t1 = time.clock()
	#output filename
	w1 = open("todostweets", "a")
	f1 = open(test_dataset, "r")
	lines = f1.readlines()
	for line in lines:
		lst = line.split()[2:-2]
		joined = " ".join(lst)
		tweetstest.append(joined)
	for tweet in tweetstest:
		w1.write(tweet + "\n")
	f1.close()
	t2 = time.clock()
	print("tiempo para tweets de test", t2 - t1)

	f2 = open(training_dataset, "r")
	lines = f2.readlines()
        for line in lines:
                lst = line.split()[2:-2]
                joined = " ".join(lst)
                tweetstrai.append(joined)
        for tweet in tweetstrai:
                w1.write(tweet + "\n")
	f2.close()
	t3 = time.clock()
	print("tiempo para tweets de training", t3 - t2)

	w1.close()
	

except IOError as mess:
	print "Error in files"
	print(mess)


