import sys
import json
import os
from nltk.tokenize import sent_tokenize, word_tokenize

import pyrouge
from pyrouge import Rouge155

import logging
from logging import config

'''
@Author: Khyathi Raghavi Chandu
@Date: October 17 2017

This code contains the wrapper around the ROUGE Evaluation to provide ROUGE-2 and Rouge-SU4.
'''

logging.config.fileConfig('logging.ini')
logger = logging.getLogger('bioAsqLogger')




class Evaluator:
	def __init__(self):
		self.filePath = "../input/BioASQ-trainingDataset5b.json"
		self.systemDirectory = "./system/"
		self.goldDirectory = "./gold/"

	def extractIdealAnswer(self, questionBody):
		infile = open(self.filePath, 'r')
		data = json.load(infile)
		for (i, question) in enumerate(data['questions']):
			if question['body'].strip() == questionBody.strip():
				return question['ideal_answer'][0]
		return None

	def fillSummaries(self, questionBody, finalSummary):
		goldIdealAnswer = self.extractIdealAnswer(questionBody)
		if goldIdealAnswer == None:
			return "No gold summary available"
		elif finalSummary == "":
			return "No system symmary available"
		else:
			modelFile = open(str(self.goldDirectory)+"bioasq.1.txt",'w+')
			for sentence in sent_tokenize(goldIdealAnswer):
				modelFile.write(sentence+"\n")
			systemFile = open(str(self.systemDirectory)+"bioasq.1.txt",'w+')
			for sentence in sent_tokenize(finalSummary):
				systemFile.write(sentence+"\n")
		return goldIdealAnswer
	
	def parseRougeOutput(self, output):
		r2 = None
		rsu = None
		lines = output.strip().split("\n")
		for line in lines:
			#print line
			if "1 ROUGE-2 Average_F:" in line:
				r2 = line.strip().split(":")[1].split("(")[0]
			if "ROUGE-S* Average_F:" in line:
				rsu = line.strip().split(":")[1].split("(")[0]
		return r2, rsu


	def calculateRouge(self, questionBody, finalSummary):
		goldIdealAnswer = self.fillSummaries(questionBody, finalSummary)
		r = Rouge155("/home/khyathi/installations/RELEASE-1.5.5")
		r.system_dir = self.systemDirectory #our summaries
		r.model_dir = self.goldDirectory #gold summaries
		r.system_filename_pattern = "bioasq.(\d+).txt"
		r.model_filename_pattern = "bioasq.#ID#.txt"

		output = r.convert_and_evaluate()
		r2, rsu = self.parseRougeOutput(output)
		return goldIdealAnswer, r2, rsu
		#print type(output)
