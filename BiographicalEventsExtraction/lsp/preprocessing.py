import logging as log
import sys
import spacy
import os
import csv
OUTPUT ='entities.csv'
nlp = spacy.load('en_core_web_lg')


log.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=log.INFO,
    datefmt='%d/%m/%Y %H:%M:%S'
)



processed = set()
if os.path.isfile(OUTPUT):
    log.info("found output file {0}, continuing".format(OUTPUT))
    with open(OUTPUT) as f:
        reader = csv.DictReader(f)
        for row in reader:
            processed.add((row['places'], row['tags']))
    fo = open(OUTPUT, "a")
else:
    log.info("output file not found, creating new one: {0}".format(OUTPUT))

    fo = open(OUTPUT, "w")
writer = csv.DictWriter(fo, fieldnames=[
    "places",
    "tags"
])
if len(processed) == 0:
    writer.writeheader()

with open(sys.argv[1]) as bio:
    biof = open('sents_'+bio.name,mode='w')
    tokenized = nlp(bio.read())
    for sent in tokenized.sents:
        biof.write(sent.text)
    for w in tokenized.ents:
        if w.label_ == 'ORG' or w.label_ == 'GPE':
            row = {
                "places":w.text,
                "tags":w.label_
            }
            if (row['places'],row['tags']) not in processed:
                writer.writerow(row)
                processed.add((row['places'],row['tags']))


fo.close()
biof.close()

