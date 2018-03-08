import json
import nltk
from nltk import word_tokenize
import numpy as np
from nltk import pos_tag
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.metrics import roc_curve
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn import svm
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import string
import pickle
import os

path = "/Users/yuyanzhang/Desktop/CMU/11791/Project/BioasqArchitecture-master/input/BioASQ-trainingDataset5b.json"
pattern_num = 7

def load_data(path):
	with open(path) as f:
		json_file = json.load(f)['questions']
	return json_file

def prep(json_file):
	ques = []
	target = []
	for data in json_file:
		ans = data['body']
		if (isinstance(ans, list)):
			ans = ans[0]
		cat = data['type']
		ques.append(ans)
		target.append(cat)
	return ques,target

#Takes a tokenized question
def extract_ques_word(data):
	wh_list = {"what":0,"which":1,"when":2,"where":3,"who":4,"how":5,"why":6,"is":7,"or":8,"are":9,"list":10,".":11,",":12,"?":13}
	rt_list = [0]*14
	for word in data:
		if word.lower() in wh_list.keys():
			rt_list[wh_list[word.lower()]] += 1
	return rt_list

#Takes a tokenized question
def extract_meta_data(data):
    #Number of tokens
    num_token = (float)(len(data))
    row_pos_tag = pos_tag(data)
    #Number of nouns, verbs, adjectives, and adverbs
    num_noun = len([token for token,pos in row_pos_tag if pos.startswith('N')])
    num_verb = len([token for token,pos in row_pos_tag if pos.startswith('V')])
    num_adj = len([token for token,pos in row_pos_tag if pos.startswith('J')])
    num_adverb = len([token for token,pos in row_pos_tag if pos.startswith('R')])
    #Number of words starting with uppercase
    num_upper = 0
    #Compute the ratio of each feature and total number of tokens
    #feature = [num_token, num_noun/num_token, num_verb/num_token, num_adj/num_token, num_adverb/num_token]
    feature = [num_token,num_noun,num_verb,num_adj,num_adverb]
    return feature    

#Takes the entire untokenized corpus and extracts first n words in the question
def first_n_gram(train,n):
	word = []
	for data in train:
		ques_token  = [w for w in word_tokenize(data) if w not in stopwords.words('english')]
		word.append(" ".join(ques_token[:min(n,len(ques_token))]))
	return word

#Takes the first n words for each question and generate the vectorized feature space
def vectorize(corpus,n,save_path=None):
	vectorizer = TfidfVectorizer(ngram_range=(1, n))
	X = vectorizer.fit_transform(corpus)
	if save_path != None:
		print("Saving vectorization at: ", save_path)
		pickle.dump(vectorizer, open(save_path, 'wb'))
	return X


def extract_pattern(ques):
	#7 Patterns for questions
	
	#0 DESC:def pattern 1 The question begins with what is/areand follows by an optionala,an, ortheand then follows by one or two words.
	#1 DESC:def pattern 2 The question begins with what do/does and ends with mean.
	#2 ABBR:exp patternThe question begins withWhat does/doand endswithstand for.
	#3 ENTY:substance pattern The question  begins  with what  is/are and ends with composed of/made of/made out of.
	#4 DESC:desc pattern The  question  begins  with what  does and  ends with do.
	#5 DESC:reason pattern 1 The question begins with what causes/cause
	#6 DESC:reason pattern 2 The  question  begins  with What  is/areandends withused for

	pattern = [0]*pattern_num
	ques = ques.lower()
	if "what is" in ques or "what are" in ques:
		idx = ques.find("what is")
		if idx == -1:
			idx = ques.find("what are")
		# ENTY pattern
		if "composed of" in ques[idx+1:len(ques)] or "made of" in ques[idx+1:len(ques)] or "made out of" in ques[idx+1:len(ques)]:
			pattern[3] = 1
		#Reason pattern 2
		elif "used for" in ques[idx+1:len(ques)]:
			pattern[6] = 1
		else:
			#DESC: def pattern 1
			pattern[0] = 1

	if "what do" in ques or "what does" in ques:
		idx = ques.find("what do")
		if idx == -1:
			idx = ques.find("what does")
		#DESC: def pattern 2
		if "mean" in ques[idx+1:len(ques)]:
			pattern[1] = 1
		#ABBR:exp pattern
		if "stand for" in ques[idx+1:len(ques)] or "stands for" in ques[idx+1:len(ques)]:
			pattern[2] = 1
		#DESC:desc pattern
		if "do" in ques[idx+1:len(ques)]:
			pattern[4] = 1
	# Reason Pattern 1
	if "what causes" in ques or "what cause" in ques:
		pattern[5] = 1

	return pattern

#Takes the entire untokenized corpus
def extract_head_word(train):
	head_word = []

	for ques in train:
		ques = ques.lower()
		ques_token = [word for word in word_tokenize(ques.lower())]
		if "when" in ques or "where" in ques or "why" in ques:
			pass
		if "how" in ques:
			try:
				head_word.append(ques_token[min((ques_token.index("how")+1), len(ques_token)-1)])
				continue
			except:
				pass
	
			
		elif "what" in ques:
			#Check each pattern except for the HUM:desc pattern
			pattern = extract_pattern(ques)
			if sum(pattern) == 0:
				pass
			else:
				head_word.append((str)(pattern.index(1)))
				continue
		
		ques_pos_tag = pos_tag(ques_token)
		num_noun = [token for token,pos in ques_pos_tag if pos.startswith('N')]
		if len(num_noun) != 0:
			head_word.append(num_noun[0])
			continue

		head_word.append("NA")
	
	return head_word





def gen_feature(question_list):
	X = vectorize(first_n_gram(question_list, 4),2, save_path="ngram_vec.pickle").toarray() #Ngram patterns of first n words
	head_word = vectorize(extract_head_word(question_list),1,save_path="head_word_vec.pickle").toarray() #Headword
	feature_list = [] #Other features
	for ques in question_list:
		feature = []
		ques_token = word_tokenize(ques)
		feature.extend(extract_ques_word(ques_token)) #Presence of wh words etc.
		feature.extend(extract_pattern(ques)) #Question pattern
		
		#feature.extend(extract_meta_data(ques_token)) #Metadata of text
		feature_list.append(feature)
	feature_space = np.c_[X,np.array(head_word),np.array(feature_list)]
	return feature_space


def cross_val(X,target,fold):
	print("Cross validating")
	clf = svm.SVC(kernel='linear', C=1)
	#clf = RandomForestClassifier()
	scores = cross_val_score(clf, X, target, cv=fold,n_jobs=5, scoring='f1_samples')
	print(np.mean(scores))

def fit_model(X,target):
	clf = svm.SVC(kernel='linear',C=1)
	clf.fit(X,target)
	return clf

def count_sent(string):
	num_sent = string.count('.')
	if num_sent==0:
		if len(string) != 0:
			num_sent = 1
	return num_sent

if __name__ == '__main__':
	train = load_data(path)
	#ques,target = prep(data)
	#X = gen_feature(ques)
	#cross_val(X,target,5)
	# clf = svm.SVC(kernel='linear',C=1)
	# clf.fit(X,target)
	# pickle.dump(clf, open("question_classifier.pickle", 'wb'))
	
	cat_dict = {}
	for data in train:
		ans = data['ideal_answer']
		if (isinstance(ans, list)):
			ans = ans[0]
		cat = data['type']
		# if not cat_dict.has_key(cat):
		# 	cat_dict[cat] = [len(word_tokenize(ans))]
		# else:
		# 	cat_dict[cat].append(len(word_tokenize(ans)))
		if not cat_dict.has_key(cat):
			cat_dict[cat] = [count_sent(ans)]
		else:
			cat_dict[cat].append(count_sent(ans))


	print(cat_dict.keys())
	import matplotlib.pyplot as plt
	from scipy import stats
	import plotly.plotly as py
	for k,v in cat_dict.items():
		print(k)
		print('mean', np.mean(np.array(cat_dict[k])))
		print('median',np.median(np.array(cat_dict[k])))
		print('mode',stats.mode(np.array(cat_dict[k]))[0])
		print('std',np.std(np.array(cat_dict[k])))
		print(np.mean(np.array(cat_dict[k])+np.std(np.array(cat_dict[k]))))
	k = 'list'
	v = cat_dict[k]
	plt.hist(v)
	plt.title(k)
	plt.xlabel("Number of sentences")
	plt.ylabel("Frequency")
	plt.savefig("".join([k,".png"]))
		
	#
	#
	#
	# ques_train, ques_test, X_train, X_test, y_train, y_test = train_test_split(ques, X, target, test_size=0.33, random_state=42)
	# clf = fit_model(X_train,y_train)
	# pred = clf.predict(X_test)
	# print(accuracy_score(pred,y_test))

	# #Error analysis
	# for k in range(len(y_test)):
	# 	if pred[k] != y_test[k]:
	# 		print("true: ", y_test[k],"pred: ",pred[k],"ques: ",ques_test[k])
	# 		print





#########Notes#############
	#balanced dataset
	#factoid,486
	#list,413
	#yesno,500
	#summary,400

	#Random forest, SVM
	#ques_word, meta: 0.672044803158, 0.714288819101
	##ques_word: 0.707615928106, 0.709281072985
	#
	#
	#Add "list":10: 0.763167055473 (SVM)
	#
	#Add first 2 words (up to n gram patterns), (to accomodate for what is, how many etc.), 0.777093101713(SVM), 0.755435591495(RF)
	#Up to 3 words, 2gram: 0.799307706421
	#up to 4 words, 2gram: 0.797650316232
	#
	#
	#+Pattern+metadata: 0.818225980825
	#+head_word: 0.828218303296
