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

    return None
