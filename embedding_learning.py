from pykeen.triples import TriplesFactory
from pykeen.pipeline import pipeline
from pykeen.datasets.nations import NATIONS_TRAIN_PATH, NATIONS_TEST_PATH
import numpy
import pandas as pd
from sklearn.model_selection import train_test_split

import os
from os import path

import pickle
import torch


datasets = ['wd_works', 'gr_works', 'ol_sample']
emb_models = ['TransE', 'TransR', 'CompGCN', 'DistMult','RESCAL']
emb_dims = [64, 128]
emb_epochs = 20


for emb_dim in emb_dims:

    for emb_model in emb_models:

        for dataset in datasets:  

            folder = 'dataset='+dataset+'_model='+emb_model+'_dim='+str(emb_dim)+'_epochs='+str(emb_epochs)

            train_path = dataset + '/' + dataset + '_train.tsv'
            test_path = dataset + '/' + dataset + '_test.tsv'

            try:      

                print("Starting learning:", folder)

                outfile = folder + '/embeddings.tsv'                


                emb_training = TriplesFactory.from_path(
                    train_path,
                    create_inverse_triples=True,
                )

                emb_testing = TriplesFactory.from_path(
                    test_path,
                    entity_to_id=emb_training.entity_to_id,
                    relation_to_id=emb_training.relation_to_id,
                    create_inverse_triples=True,
                )

                result = pipeline(
                    training=emb_training,
                    testing=emb_testing,
                    model=emb_model,
                    model_kwargs=dict(embedding_dim=emb_dim),
                    epochs=emb_epochs, 
                )


                torch.save(result, folder+'/pipeline_result.dat')

                map_ent = pd.DataFrame(data=list(emb_training.entity_to_id.items()))
                map_ent.to_csv(folder+'/entities_to_id.tsv', sep='\t', header=False, index=False)
                map_ent = pd.DataFrame(data=list(emb_training.relation_to_id.items()))
                map_ent.to_csv(folder+'/relations_to_id.tsv', sep='\t', header=False, index=False)


                # save mappings
                result.save_to_directory('folder', save_training=True, save_metadata=True)

                # extract embeddings with gpu
                entity_embedding_tensor = result.model.entity_representations[0](indices = None)
                # save entity embeddings to a .tsv file (gpu)
                df = pd.DataFrame(data=entity_embedding_tensor.cpu().data.numpy())

                # extract embeddings with cpu
                #entity_embedding_tensor = result.model.entity_representations[0](indices=None).detach().numpy()
                # save entity embeddings to a .tsv file (cpu)
                #df = pd.DataFrame(data=entity_embedding_tensor.astype(float))

                df.to_csv(outfile, sep='\t', header=False, index=False)
            
            except:

                print('An error occoured: ' + folder)