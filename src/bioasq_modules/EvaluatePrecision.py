import sys
import json
import os
import logging
from logging import config

from PyRouge.pyrouge import Rouge


def betterAnswer(baseline, new, questionBody):
	infile_true = open("./input/BioASQ-trainingDataset5b.json", 'r')
	data_true = json.load(infile_true)

	
	for (i, question_i) in enumerate(data_true['questions']):
		if question_i['body'].strip() == questionBody.strip():
				r = Rouge()
				manual_summmary =  question_i['ideal_answer'][0]
				[precision_base, recall_base, f_score_base] = r.rouge_l([baseline], [manual_summmary])	
				[precision_new, recall_new, f_score_new] = r.rouge_l([new], [manual_summmary])	

				print "============================================"
				print "Ideal_answer \n"
				print manual_summmary
				print "Fused_answer %f %f \n" %(precision_new, recall_new)
				print new
				print "Baseline_answer %f %f \n" %(precision_base, recall_base)
				print baseline



				print "============================================"
				if f_score_base < f_score_new:
					print "11111"
					return new
				else:
					print "22222"
					return baseline
	return None

