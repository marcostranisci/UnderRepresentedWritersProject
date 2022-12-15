import pandas as pd
import argparse,yaml
from sklearn.metrics.pairwise import cosine_similarity
import logging as log
from difflib import SequenceMatcher
import random
from decimal import *

log.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=log.INFO,
    datefmt='%d/%m/%Y %H:%M:%S'
)

parser = argparse.ArgumentParser()
parser.add_argument("--dataset",type=str,default='wd', help='you can choose between: gr=Goodreads wd=Wikipedia and ol=OpenLibrary')
parser.add_argument("--model",type=str,default='DistMult', help='choose between these five available models: DistMult RESCAL TransE TransR CompGCN')
parser.add_argument("--dim",type=str,default='64', help='choose between two dimensions: 128, 64')
parser.add_argument("--ent",type=str,default='authors',help='choos between: authors, works')
args = parser.parse_args()


with open('config.yaml') as f:
    params = yaml.load(f, Loader=yaml.FullLoader)

embeddings = pd.read_csv(params['data']['embedding_path'].format(args.dataset,args.model,args.dim),sep='\t')
mappings = pd.read_csv(params['data']['mapping_path'].format(args.dataset,args.model,args.dim),sep='\t')

id_col = '_author_id' if args.ent=='authors' else '_id'

mappings.columns = [id_col,'idx']
mappings[id_col] = mappings[id_col].apply(lambda x:x.split('#')[-1][:-1])

ents = pd.read_csv(params['data'][args.ent])
mappings = mappings.merge(ents)

embeddings.columns = [x for x in range(int(args.dim))]
embeddings = embeddings.reset_index()
embeddings = embeddings.rename(columns={'index':'idx'})
embeddings = mappings.merge(embeddings)

embeddings = {row[0]:row[4:] for row in embeddings.iloc[:].values}

def compute_percentage(a_df,a_number):

    n_authors = len(a_df[:a_number][a_df[:a_number].underrepresented==1])
    perc_sample = round(len(a_df[:a_number][a_df[:a_number].underrepresented==1])/a_number,3)

    return perc_sample,n_authors

def average_map(a_df,a_number):

    a_df = a_df[:a_number]
    t = 0
    a = 0
    scores = a_df.underrepresented.tolist()
    map_av = list()
    for score in scores:
        a+=1
        t+=1 if score ==1 else t
        weight = float(Decimal(t)/Decimal(a))
        if score == 0: map_av.append(0)
        else: map_av.append(round(weight,3))
    map_av = round(sum(map_av)/a_number,3)
    return map_av






def find_similarity(id_):

    ent = embeddings[id_]

    most_similar = list()
    for a,b in embeddings.items():

        sim = cosine_similarity([ent,b])
        most_similar.append((a,sim[0][1]))

        most_similar = sorted(
        most_similar,
        key=lambda t:t[1],
        reverse=True
            )
    df = pd.DataFrame(most_similar,columns=[id_col,'similarity'])
    df = df.merge(mappings[[id_col,'underrepresented']])
    df.underrepresented = df.underrepresented.apply(lambda x:1 if x=='Transnational' else 0)
    sample_10 = int(len(mappings)/10)
    sample_05 = int(len(mappings)/20)
    sample_01 = int(len(mappings)/100)

    perc_01 = compute_percentage(df,sample_01)
    #map_av_01 = average_map(df,sample_01)
    perc_10 = compute_percentage(df,sample_10)
    #map_av_10 = average_map(df,sample_10)
    perc_05 = compute_percentage(df,sample_05)
    #map_av_05 = average_map(df,sample_05)
    log.info('results: {}, {}, {}'.format(perc_01,perc_05,perc_10))
    all_metrics = [perc_01[0],perc_01[1],perc_05[0],perc_05[1],perc_10[0],perc_10[1]]
    return all_metrics

authors = mappings[mappings.underrepresented=='Western'][id_col].tolist()

n = 16
random.seed(n)

random.shuffle(authors)
l = list()
for author in authors[:250]:
    sim = find_similarity(author)
    l.append(sim)


pd.DataFrame(l,columns=['p_01','a_01','p_05','a_05','p_10','a_10']).to_csv('most_sim_new/new_metrics_{}_{}_{}.csv'.format(args.dataset,args.model,n),index=False)
