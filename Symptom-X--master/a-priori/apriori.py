
import csv
import itertools


def generate_itemsets(itemsets,buckets,pass_):
	""" Generates different combinations of items in every pass of a-priori.
		Sends it to get_support() to get the support of each of these combinations 
		and see whether the support is greater than the support threshold."""
	if pass_ == 1:
		list_ = []
		for bucket in buckets:
			list_ = list_ + bucket

		items= set(list_)
		get_support(items,buckets,pass_)

	else:
		items = []
		for i in itemsets:
			if type(i) is list:
				for itr in i:
					if itr not in items:
						items.append(itr)
			else:
				items.append(i)

		cmb = itertools.combinations(items,pass_)
		list_ = [list(elem) for elem in cmb]

		print ("LIST BEGIN")
		print (list_)
		
		get_support(list_,buckets,pass_)

def get_support(items,buckets,pass_):
	"""Extract support values for every itemset.
		Stores and passes them to frequent_itemsets.
	"""
	dict_main = {}
	ctr = 0
	for i in items:
		dict_main[ctr] = i
		ctr = ctr + 1

	dict_ = {}
	for key,values in dict_main.iteritems():
		dict_[key] = 0
		for bucket in buckets:
			if type(values) is list:
				if all(val in bucket for val in values):
					dict_[key] = int(dict_[key]) + 1
			else:
				if values in bucket:
					dict_[key] = int(dict_[key]) + 1

	
	frequent_itemset = frequent_itemsets(dict_,pass_)

	frequent = []
	for f in frequent_itemset:
		frequent.append(dict_main[f])

	print (frequent)

	if frequent_itemset:
		pass_ = pass_ + 1
		generate_itemsets(frequent,buckets,pass_)
	else: 
		print ("A-priori passes completed.")

def frequent_itemsets(dict_,pass_):
	""" Decides whether the itemset is Frequent or not.
		Edit the Support threshold required for the chaffing here.
	"""
	frequent = []
	for key,value in dict_.iteritems():
		if value>8:
			frequent.append(key)
	return frequent

def calculate_confidence(X,Y,buckets):
	occr_X = 0
	occr_Y = 0
	for bucket in buckets:
		if type(X) is list:
			if all(val in bucket for val in X):
				occr_X = int(occr_X) + 1
		else:
			if X in bucket:
				occr_X = int(occr_X) + 1

		if type(Y) is list:
			if all(val in bucket for val in Y):
				occr_Y = int(occr_Y) + 1
		else:
			if Y in bucket:
				occr_Y = int(occr_Y) + 1

	print ("X: ",X)
	print ("Y: ",Y)

	print ("Occurrence of X: ",occr_X)
	print ("Occurrence of Y: ",occr_Y)

	conf  = float(occr_Y)/float(occr_X)*100
	print ("Confidence given X implies Y: ", conf,"%")
	return conf

def get_disease(symptomlist,buckets):
	disease_score={}
	score = 0
	for bucket in buckets:
		score = set(symptomlist) & set(bucket)
		score = float(len(score))/float(len(symptomlist))*100
		if score>0:
			#print (score)
			disease = get_disease_given_bucket(bucket)
			#print (disease)
			disease_score[disease] = score
	print (disease_score)

	with open("disease_probabilityscores_from_symptomlist.csv","w") as csvfile:
		writer = csv.writer(csvfile)

		writer.writerow(["Symptomlist"])
		writer.writerow(symptomlist)
		writer.writerow(["Disease","Probability scores"])
		for key,value in disease_score.items():
			writer.writerow([key,value])

"""Assuming every bucket uniquely points to a disease"""
def get_disease_given_bucket(bucket):
	disease = ""
	#print ("ENTER")
	with open("bucketmap.csv","r") as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			row_clean = [i for i in row if i]
			bucket_clean = [i for i in bucket if i]
			if len(row_clean) == (len(bucket_clean)+1):
				if all(values in row_clean for values in bucket_clean):
					disease = row_clean[0]
					break

	return disease


buckets = []

with open("buckets.csv") as csvfile:
	reader = csv.reader(csvfile)

	for row in reader:
		buckets.append(row)
      


pass_ = 1
itemsets = []

# -*- coding: utf-8 -*-
import tkinter as tk

def symptomtaking():
    global entry_symptom1
    global entry_symptom2
    global entry_symptom3
    global entry_symptom4
    root = tk.Tk()
    root.title('Symptoms')
    
    label=tk.Label(root,text='Please Enter symptoms\n')
    label.grid(row=0,column=0)

    symptom1=tk.Label(root,text="Symptom-1")
    symptom2=tk.Label(root,text="Symptom-2")
    symptom3=tk.Label(root,text="Symptom-3")
    symptom4=tk.Label(root,text="Symptom-4")
    entry_symptom1 = tk.Entry(root)
    entry_symptom2 = tk.Entry(root)
    entry_symptom3 = tk.Entry(root)
    entry_symptom4 = tk.Entry(root)
    symptom1.grid(row=1,column=0)
    symptom2.grid(row=2,column=0)
    symptom3.grid(row=3,column=0)
    symptom4.grid(row=4,column=0)
    entry_symptom1.grid(row=1 , column=1)
    entry_symptom2.grid(row=2 , column=1)
    entry_symptom3.grid(row=3 , column=1)
    entry_symptom4.grid(row=4 , column=1)

    ok=tk.Button(root,text='Ok',command=Fssymptomtaking)
    ok.grid(columnspan=2)
    root.mainloop()

def Fssymptomtaking():
    with open("tempfile.txt","w") as f:
        f.write(entry_symptom1.get())
        f.write('\n')
        f.write(entry_symptom2.get())
        f.write('\n')
        f.write(entry_symptom3.get())
        f.write('\n')
        f.write(entry_symptom4.get())
        f.write('\n')
    with open("tempfile.txt") as f:
       data=f.readlines()
       a = data[0].rstrip()
       b = data[1].rstrip()
       c = data[2].rstrip()
       d = data[3].rstrip()
       #print(a)
       #print(b)
       symptomlist=[a,b,c,d]
       
       get_disease(symptomlist,buckets)
       
       
symptomtaking()
       
       





        
       



#generate_itemsets(itemsets,buckets,1) 
#calculate_confidence("suicidal","sleeplessness",buckets)

