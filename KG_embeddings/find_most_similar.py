import pandas as pd
import argparse,yaml
from sklearn.metrics.pairwise import cosine_similarity
import logging as log
from difflib import SequenceMatcher

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
mappings = mappings.merge(ents[[id_col,'label']])

embeddings.columns = [x for x in range(int(args.dim))]
embeddings = embeddings.reset_index()
embeddings = embeddings.rename(columns={'index':'idx'})
embeddings = mappings.merge(embeddings)

embeddings = {row[0]:row[3:] for row in embeddings.iloc[:].values}

def create_suggestion(name,list_of_names):

    similar_names = [(x,SequenceMatcher(None,name,x).ratio()) for x in list_of_names]
    similar_names = sorted(
    similar_names,
    key=lambda t:t[1],
    reverse=True
    )
    similar_names = '\n- {}'.format('\n- '.join([x[0] for x in similar_names[:10]]))

    message = "Sorry, we didn't find the entity with this name: {}.\nPheraps you were looking for one of these entities? {}".format(name,similar_names)

    return message

def find_similarity(name):
    id_col = '_author_id' if args.ent=='authors' else '_id'
    id_ = mappings[mappings.label==name][id_col].values
    if len(id_)==0:
        suggestion = create_suggestion(name,mappings.label.tolist())
        return suggestion
    else:
        ent = embeddings[id_[0]]

        most_similar = list()
        for a,b in embeddings.items():

            sim = cosine_similarity([ent,b])
            most_similar.append((a,sim[0][1]))

            most_similar = sorted(
            most_similar,
            key=lambda t:t[1],
            reverse=True
            )

        most_similar = '\n- {}'.format('\n- '.join([ents[ents[id_col]==x[0]].label.values[0] for x in most_similar[1:11]]))
        message = "Here you can find the most similar authors to {}:{}".format(name,most_similar)

        return message

while True:
    log.info('Write the name of 1 {} to find the 10 most similar (or type exit):'.format(args.ent[:-1]))
    name = input()

    if name=='exit':False

    else:
        result = find_similarity(name)
        log.info(result)
