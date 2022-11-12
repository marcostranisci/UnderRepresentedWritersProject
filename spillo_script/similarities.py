import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os


#dataset=gr_works_model=CompGCN_dim=64_epochs=20

datasets = ['wd_works', 'gr_works']
models = ['TransE', 'TransR', 'CompGCN', 'RESCAL', 'DistMult']
sizes = [64, 128, 256]

# items in wikidata
wd_items = ['<https://purl.archive.org/urbooks#urb_wd_work_179>',
     '<https://purl.archive.org/urbooks#urb_wd_work_134814>',
     '<https://purl.archive.org/urbooks#urb_wd_work_97>']

# items in goodreads
gr_items = ['<https://purl.archive.org/urbooks#urb_gr_work_75943>',
            '<https://purl.archive.org/urbooks#urb_gr_work_4366>',
            '<https://purl.archive.org/urbooks#urb_gr_work_144544>']

log_out = open('ouput.txt', 'w', encoding='utf-8')

for dataset in datasets:
    for model in models:
        for size in sizes:
            folder = 'kge/dataset='+dataset+'_model='+model+'_dim='+str(size)+'_epochs=20/'
            
            if not os.path.exists(folder):
                continue
                
            # load all embeddings
            mat = np.loadtxt(folder+'embeddings.tsv', dtype='float', delimiter='\t')
            print('Embeddings loaded')
            
            # create maps of matrix row -> entity and entity -> matrix row
            e2id = {}
            id2e = {}
            
            # create map of names of entities
            mapping = {}
            
            # populate maps
            fin = open(folder+'entities_to_id.tsv', 'r', encoding='utf-8')
            fin.readline()
            
            for line in fin:
                id = line.strip().split('\t')[1]
                ent = line.strip().split('\t')[0]    
                
                e2id[ent] = id
                id2e[id] = ent
                
            fin.close()
            
            # mapping files, obtained by filtering datasets
            # using the relation "rdf-schema#label"
            
            # can be replaced by other maps obtained in other ways
            if 'gr' in dataset:
                file_map = 'map_gr.tsv'
            elif 'wd' in dataset:
                file_map = 'map_wd.tsv'
            
            fin = open(file_map, 'r', encoding='utf-8')
            
            # work/subject id -> name
            for line in fin:
                tokens = line.strip().split(' ', 2)
                mapping[tokens[0]] = tokens[2]
            
            fin.close()
            
            print('Maps loaded')
            
            # required embedding            
            if 'gr' in dataset:
                items = gr_items
            elif 'wd' in dataset:
                items = wd_items
                
            # knn
            k = 15
            
            errors = 0
            for item in items:
                
                # selecting the required embedding
                x = mat[int(e2id[item])]
                
                # map of similarities
                similarities = {}
                i=0
                
                # compute all similarities
                for emb in mat:
                    sim = cosine_similarity([x, emb])
                    similarities[i] = sim[0][1]
                    i+=1
                
    
                
                # sort in reverse order similarities and 
                # print id and similarity score of the top-k similar embeddings
                top_k = sorted(similarities.items(), key=lambda item: item[1], reverse=True)[1:k+1]
                
                print(folder)
                print("Most similar items to " + mapping[item])
                log_out.write(folder+'\n')
                log_out.write("Most similar items to " + mapping[item] + '\n')
                
                for couple in top_k:
                    
                    # try-except necessary since the m-th entity in the top-k 
                    # might not be a work (so it is not in the mapping)
                    # that's why you could change the mapping files
                    try:
                        log_out.write('\t' + mapping[id2e[str(couple[0])]] + '\t' + str(couple[1])+'\n')
                        print('\t' + mapping[id2e[str(couple[0])]] + '\t' + str(couple[1]))
                    except:
                        errors += 1
                print("Errors: " + str(errors) + '\n')

log_out.flush()
log_out.close()
