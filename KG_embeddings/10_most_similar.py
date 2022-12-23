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
mappings = mappings.merge(ents)

embeddings.columns = [x for x in range(int(args.dim))]
embeddings = embeddings.reset_index()
embeddings = embeddings.rename(columns={'index':'idx'})
embeddings = mappings.merge(embeddings)

print(len(mappings[mappings.underrepresented=='Transnational'])/len(mappings),len(mappings))
