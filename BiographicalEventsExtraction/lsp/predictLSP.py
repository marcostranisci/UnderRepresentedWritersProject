import os
import re
import sys
import csv
import logging as log

import pandas as pd
import spacy

OUTPUT = 'lspResults.csv'
nlp = spacy.load('en_core_web_lg')
entities = set()

def create_rules(a_file):
    df = pd.read_csv(a_file)
    rules = [(x[2],x[-1]) for x in df.iloc[:].values]

    return rules


def searchable_sent(a_sent):
    tokens = list()
    sent = nlp(a_sent)
    for x in sent:
        if x.pos_=='VERB':
            tokens.append(x.lemma_)
        if x.pos_ =='AUX' and x.dep_ =='ROOT':
            tokens.append(x.lemma_)
        elif x.text =='ORG' or x.text == 'GPE':
            tokens.append(x.text)
        elif x.pos_=='ADP':
            tokens.append(x.text)
        #elif x.ent_type_ == 'ORG' or x.ent_type_ == 'GPE':
            #tokens.append(x.ent_type_,)
        elif x.dep_ == 'prep':
            tokens.append(x.lemma_)
        elif x.dep_ != 'punct' and x.dep_ != 'det':
            tokens.append(x.dep_)
    searchable = " ".join(tokens)

    return searchable #,a_sent

rules = create_rules('LSPs_def.csv')

with open(sys.argv[1]) as doc_ents:
    reader = csv.DictReader(doc_ents)
    for row in reader:
        entities.add((row['entity_name'],row['entity_tag']))

doc_ents.close()

sentences = list()
with open(sys.argv[2]) as sents:
    for line in sents.readlines():
        #print(line)
        for ent in entities:
            if re.search(ent[0] + '[^a-zA-Z0-9]',line):
                line = re.sub(ent[0],ent[1],line)

        sentences.append(line)

processed = set()
if os.path.isfile(OUTPUT):
    log.info("found output file {0}, continuing".format(OUTPUT))
    with open(OUTPUT) as f:
        reader = csv.DictReader(f)
        for row in reader:
            processed.add((row['sentence'], row['odp']))
    fo = open(OUTPUT, "a")
else:
    log.info("output file not found, creating new one: {0}".format(OUTPUT))

    fo = open(OUTPUT, "w")
writer = csv.DictWriter(fo, fieldnames=[
    "sentence",
    "odp"
])
if len(processed) == 0:
    writer.writeheader()


to_be_searched = [(x,searchable_sent(x)) for x in sentences]

for sent in to_be_searched:
    for pattern in rules:
        if re.search(pattern[1],sent[1]):
            row = {
                "sentence": sent[0],
                "odp": pattern[0]
            }
            writer.writerow(row)

fo.close()