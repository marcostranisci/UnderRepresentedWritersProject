#!/usr/bin/env python

import csv
import wikipedia
import sys
import requests
import logging as log
from time import sleep
from wikidata.client import Client
import os

WPAPI = 'https://en.wikipedia.org/w/api.php'
OUTPUT = 'risultati.csv'
TIMEOUT = 0.5


def get_wikidata_id(page_title):
    response = requests.get(WPAPI, params={
        'action': 'query',
        'prop': 'pageprops',
        'ppprop': 'wikibase_item',
        'redirects': 1,
        'format': 'json',
        'titles': page_title
    })
    sleep(TIMEOUT)
    try:
        return list(response.json()['query']['pages'].values())[0]['pageprops']['wikibase_item']
    except:
        return None


def get_wikidata_country(wdid):
    entity = wd.get(wdid, load=True)
    sleep(TIMEOUT)
    try:
        return entity[country_prop]
    except:
        return None


log.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=log.INFO,
    datefmt='%d/%m/%Y %H:%M:%S'
)

if len(sys.argv) < 2:
    log.error("usage: ner.py DATA.csv")
    sys.exit(1)

log.info("initializing Wikidata client")
wd = Client()
country_prop = wd.get('P17')

log.info("reading input data")
entities = set()
with open(sys.argv[1]) as f:
    reader = csv.DictReader(f)
    for row in reader:
        entities.add((row['places'],row['tags']))
log.info("extracted {0} named entities".format(len(entities)))

processed = set()
if os.path.isfile(OUTPUT):
    log.info("found output file {0}, continuing".format(OUTPUT))
    with open(OUTPUT) as f:
        reader = csv.DictReader(f)
        for row in reader:
            processed.add((row['entity_name'], row['entity_tag']))
    fo = open(OUTPUT, "a")
else:
    log.info("output file not found, creating new one: {0}".format(OUTPUT))

    fo = open(OUTPUT, "w")

writer = csv.DictWriter(fo, fieldnames=[
    "entity_name",
    "entity_tag",
    "wp_page",
    "wd_id",
    "wd_country",
    "wd_country_id"
])

if len(processed) == 0:
    writer.writeheader()

for entity_name, entity_tag in entities:
    pages = wikipedia.search(entity_name)
    sleep(TIMEOUT)
    log.info("found {0} Wikipedia results for {1}".format(len(pages), entity_name))

    found_country = False
    for page in pages:

        if not found_country:
            wdid = get_wikidata_id(page)
            if wdid is None:
                continue
            log.info("checking Wikidata for {0}".format(page))
            country = get_wikidata_country(wdid)
            if not country is None:
                row = {
                    "entity_name": entity_name,
                    "entity_tag": entity_tag,
                    "wp_page": page,
                    "wd_id": wdid,
                    "wd_country": country.id,
                    "wd_country_id": country.label
                }
                if (row['entity_name'], row['entity_tag']) not in processed:
                    writer.writerow(row)
                found_country = True
    processed.add((row['entity_name'], row['entity_tag']))
    log.info("progress: {0}/{1}".format(len(processed), len(entities)))
fo.close()
