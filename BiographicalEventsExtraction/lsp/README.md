<h3> Pipeline</h3>

#It takes in input a biography and returns a list of sentences extracted with Spacy<br>
python preprocessing.py chimamanda.txt

#It takes in input a list of entities and returns a file with each entity associated with its country<br>
python NER.py entities.csv

#It takes in input a list of sentences and entities and returns a file with sentences and Lexico Semantic Patterns<br>
python predictLSP.py risultati.csv sents_chimamanda.txt
