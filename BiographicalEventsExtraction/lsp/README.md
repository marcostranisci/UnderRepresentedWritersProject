<h3> Pipeline</h3>

#prende in input una biografia e restituisce un elenco di frasi e un elenco di entità estratte con Spacy<br>
python preprocessing.py chimamanda.txt

#prende in input un elenco di entità e restituisce un file con ogni entità associata al paese di appartenenza<br>
python NER.py entities.csv

#prende in input un elenco di frasi e di entità linkate e restituisce un file con frasi e LSP<br>
python predictLSP.py risultati.csv sents_chimamanda.txt
