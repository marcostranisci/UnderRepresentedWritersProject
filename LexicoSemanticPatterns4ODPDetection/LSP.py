import json
import re
import csv
import numpy as np
import pandas as pd
import spacy
import wikipedia
def implement_spacy_model(a_lang,a_size):
    nlp = spacy.load(a_lang+'_core_web_'+a_size)
    return nlp

def get_bio(a_name):

    page = wikipedia.page(a_name)
    a_bio = page.content

    return a_bio

def infer_verbs_from_uvi(id):
    df = pd.read_csv('class_id_verbs.csv')

    verbs = df[df['class_id'] == id]['verbs'].values[0]
    class_ = df[df['class_id']==id]['ODP'].values[0]

    return id,verbs,class_
l =list()


def create_lsp(a_rule):

    full_rule = " ".join(a_rule)

    id,verbs,odp = infer_verbs_from_uvi(a_rule[2])
    if a_rule[3]!= 'x':
        verb = '(?=.*('+verbs+')\s('+a_rule[3]+'))'
        del a_rule[2:4]
        lsp = ['(?=.*'+x+')' for x in a_rule if x!='x']
        lsp.append(verb)
        lsp = "".join(lsp)+'.*'
    else:
        lsp = "".join(['(?=.*' + x + ')' for x in a_rule if x != 'x'])+'.*'
    return lsp,odp,full_rule




def preproc_bio(a_bio):
    life_events = list()
    doc = nlp(a_bio)
    for sent in doc.sents:
        ner = [(x.text,x.label_) for x in sent.ents if x.label_ == 'GPE' or x.label_ == 'ORG']
        verb = [x.lemma_ for x in sent if x.pos_ == 'VERB' or x.pos_ == 'AUX']
        if len(ner) > 0 and len(verb)>0:
            life_events.append(sent.text)
        else:
            life_events.append(np.NaN)

    return life_events


def searchable_sent(a_sent):
    tokens = list()
    sent = nlp(a_sent)
    for x in sent:
        if x.pos_=='VERB':
            tokens.append(x.lemma_)
        elif x.ent_type_ == 'ORG' or x.ent_type_ == 'GPE':
            tokens.append(x.ent_type_,)
        elif x.dep_ == 'prep':
            tokens.append(x.lemma_)
        elif x.dep_ != 'punct' and x.dep_ != 'det':
            tokens.append(x.dep_)
    searchable = " ".join(tokens)

    return searchable,a_sent


def predict_lsp(a_sent,lsps):
    odps = list()
    for item in lsps:
        if re.search(item[0],a_sent[0]):
            sent = a_sent[1]
            odp = item[1]
            odps.extend((item[2],sent,odp))
    if len(odps)>0:
        #print(odps)
        final_odp=odps
    else:
        final_odp = 'no_odp'

    #print(item)
    return final_odp

spamreader = pd.read_csv('class_id.csv')





nlp = implement_spacy_model('en','lg')
bio = get_bio('Mark Mathabane')
sentences = preproc_bio(bio)
#print(sentences)
toBeSearched_sents = [searchable_sent(x) for x in sentences if x is not np.NaN]
rules = list(set([tuple(x) for x in csv.reader(open('regoleDEF_2.csv'))]))
lsps= [create_lsp(list(x)) for x in rules]
predictedLsp = [predict_lsp(x,lsps) for x in toBeSearched_sents if x is not np.NaN]

print(predictedLsp)
#lsp,odp = [create_lsp(list(x)) for x in rules]



