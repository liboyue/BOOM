from SentenceOrderer import SentenceOrderer


class MajorityOrder(SentenceOrderer):
    def __init__(self):
        pass

    def orderSentences(self, sentences, snippets, info_dict):
        ordered_answer = []
        sents, snips = self.truncate(sentences, snippets, info_dict['max_length'])
        docs_seen = set()
        for i in range(len(sents)):
            rel_sents = [[sents[i], snips[i]['text'].index(sents[i])]]
            doc = snips[i]['document']
            if doc in docs_seen:
                continue
            for sent, snip in zip(sents[i+1:], snips[i+1:]):
                if snip['document'] == doc:
                    rel_sents.append([sent, snip['text'].index(sent)])
            rel_sents.sort(key=lambda x: x[1])
            ordered_answer += [sent[0] for sent in rel_sents]
            docs_seen.add(doc)
        return ordered_answer

    # TODO: Do we want a sentence length limit?
    def truncate(self, sentences, snippets, max_length):
        answer_length = 0
        answer_sentences = []
        answer_snippets = []
        for sentence, snippet in zip(sentences, snippets):
            sentence_length = len(sentence.split())
            if (answer_length + sentence_length <= max_length) and (sentence not in answer_sentences):
                answer_sentences.append(sentence)
                answer_snippets.append(snippet)
                answer_length += sentence_length
            else:
                continue
        return answer_sentences, answer_snippets

'''
# Unit Test
sentences = ["Chromosomal and related Mendelian syndromes associated with Hirschsprung's disease.", 'The inheritance of Hirschsprung disease is generally consistent with sex-modified multifactorial inheritance with a lower threshold of expression in males', 'Hirschsprung disease (HSCR) is a multifactorial, non-mendelian disorder in which rare high-penetrance coding sequence mutations in the receptor tyrosine kinase RET contribute to risk in combination with mutations at other genes', "The non-Mendelian inheritance of sporadic non-syndromic Hirschsprung's disease proved to be complex; involvement of multiple loci was demonstrated in a multiplicative model", 'In the etiology of Hirschsprung disease various genes play a role; these are: RET, EDNRB, GDNF, EDN3 and SOX10, NTN3, ECE1, Mutations in these genes may result in dominant, recessive or multifactorial patterns of inheritance.', 'Furthermore, mutations in the RET gene are responsible for approximately half of the familial and some sporadic cases, strongly suggesting, on the one hand, the importance of non-coding variations and, on the other hand, that additional genes involved in the development of the enteric nervous system still await their discovery', "In this study, we review the identification of genes and loci involved in the non-syndromic common form and syndromic Mendelian forms of Hirschsprung's disease.", 'Therefore, HSCR has become a model for a complex oligo-/polygenic disorder in which the relationship between different genes creating a non-mendelian inheritance pattern still remains to be elucidated', 'Differential contributions of rare and common, coding and noncoding Ret mutations to multifactorial Hirschsprung disease liability.', 'On the basis of a skewed sex-ratio (M/F = 4/1) and a risk to relatives much higher than the incidence in the general population, HSCR has long been regarded as a sex-modified multifactorial disorder']
snippets = [{u'offsetInBeginSection': 0, u'offsetInEndSection': 83, u'text': u"Chromosomal and related Mendelian syndromes associated with Hirschsprung's disease. ", u'beginSection': u'title', u'document': u'http://www.ncbi.nlm.nih.gov/pubmed/23001136', u'endSection': u'title'}, {u'offsetInBeginSection': 858, u'offsetInEndSection': 1012, u'text': u'The inheritance of Hirschsprung disease is generally consistent with sex-modified multifactorial inheritance with a lower threshold of expression in males ', u'beginSection': u'abstract', u'document': u'http://www.ncbi.nlm.nih.gov/pubmed/6650562', u'endSection': u'abstract'}, {u'offsetInBeginSection': 131, u'offsetInEndSection': 358, u'text': u'Hirschsprung disease (HSCR) is a multifactorial, non-mendelian disorder in which rare high-penetrance coding sequence mutations in the receptor tyrosine kinase RET contribute to risk in combination with mutations at other genes ', u'beginSection': u'abstract', u'document': u'http://www.ncbi.nlm.nih.gov/pubmed/15829955', u'endSection': u'abstract'}, {u'offsetInBeginSection': 820, u'offsetInEndSection': 992, u'text': u"The non-Mendelian inheritance of sporadic non-syndromic Hirschsprung's disease proved to be complex; involvement of multiple loci was demonstrated in a multiplicative model ", u'beginSection': u'abstract', u'document': u'http://www.ncbi.nlm.nih.gov/pubmed/15617541', u'endSection': u'abstract'}, {u'offsetInBeginSection': 151, u'offsetInEndSection': 376, u'text': u'In the etiology of Hirschsprung disease various genes play a role; these are: RET, EDNRB, GDNF, EDN3 and SOX10, NTN3, ECE1, Mutations in these genes may result in dominant, recessive or multifactorial patterns of inheritance. ', u'beginSection': u'abstract', u'document': u'http://www.ncbi.nlm.nih.gov/pubmed/15858239', u'endSection': u'abstract'}, {u'offsetInBeginSection': 397, u'offsetInEndSection': 939, u'text': u'Coding sequence mutations in e.g. RET, GDNF, EDNRB, EDN3, and SOX10 lead to long-segment (L-HSCR) as well as syndromic HSCR but fail to explain the transmission of the much more common short-segment form (S-HSCR). Furthermore, mutations in the RET gene are responsible for approximately half of the familial and some sporadic cases, strongly suggesting, on the one hand, the importance of non-coding variations and, on the other hand, that additional genes involved in the development of the enteric nervous system still await their discovery ', u'beginSection': u'abstract', u'document': u'http://www.ncbi.nlm.nih.gov/pubmed/12239580', u'endSection': u'abstract'}, {u'offsetInBeginSection': 554, u'offsetInEndSection': 992, u'text': u"In this study, we review the identification of genes and loci involved in the non-syndromic common form and syndromic Mendelian forms of Hirschsprung's disease. The majority of the identified genes are related to Mendelian syndromic forms of Hirschsprung's disease. The non-Mendelian inheritance of sporadic non-syndromic Hirschsprung's disease proved to be complex; involvement of multiple loci was demonstrated in a multiplicative model ", u'beginSection': u'abstract', u'document': u'http://www.ncbi.nlm.nih.gov/pubmed/15617541', u'endSection': u'abstract'}, {u'offsetInBeginSection': 941, u'offsetInEndSection': 1279, u'text': u'For almost all of the identified HSCR genes incomplete penetrance of the HSCR phenotype has been reported, probably due to modifier loci. Therefore, HSCR has become a model for a complex oligo-/polygenic disorder in which the relationship between different genes creating a non-mendelian inheritance pattern still remains to be elucidated ', u'beginSection': u'abstract', u'document': u'http://www.ncbi.nlm.nih.gov/pubmed/12239580', u'endSection': u'abstract'}, {u'offsetInBeginSection': 0, u'offsetInEndSection': 131, u'text': u'Differential contributions of rare and common, coding and noncoding Ret mutations to multifactorial Hirschsprung disease liability. ', u'beginSection': u'title', u'document': u'http://www.ncbi.nlm.nih.gov/pubmed/20598273', u'endSection': u'title'}, {u'offsetInBeginSection': 417, u'offsetInEndSection': 615, u'text': u'On the basis of a skewed sex-ratio (M/F = 4/1) and a risk to relatives much higher than the incidence in the general population, HSCR has long been regarded as a sex-modified multifactorial disorder ', u'beginSection': u'abstract', u'document': u'http://www.ncbi.nlm.nih.gov/pubmed/8896569', u'endSection': u'abstract'}]

orderer = MajorityOrder()
tiler_info = {'max_length': 200, 'max_tokens': 200, 'k': 2, 'max_iter': 20}
answer = orderer.orderSentences(sentences, snippets, tiler_info)
n = len(answer)
print("\nOriginal Sentences\n")
for i in range(7):
    print(sentences[i])
    print('')
print("\nAnswer\n")
print(answer)
'''
