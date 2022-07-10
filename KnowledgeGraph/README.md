## The URW-KG
In this folder you can find all the information about the Under-Represented Writers Knowledge Graph (URW-KG)

### The Knowledge Graph
In this folder you can access to [all the .ttl files that compose the Knowledge Graph](https://drive.google.com/drive/folders/1YZ1a5vfcm_s-k9xl7W5jdBOD0uLb5MmP?usp=sharing). Files have been materialized with Ontop (see below)

### Ontop Mappings

For populating the ontology we used [Ontop](https://ontop-vkg.org/), a Virtual Knowledge Graph system that allows to materialize triples from a relational database. In the folder [all_mappings](./all_mappings) you can find all the r2rml files used for converting SQL database to the KG. For testing the mapping you must:
1. Download and extract the [Ontop Command Line Interface](https://ontop-vkg.org/guide/cli) in this folder. It will create a folder of the type: ontop-cli-x.x.x.
2. Download the [MYSQL Jbc driver](https://dev.mysql.com/downloads/connector/j/) and put it in the jdbc folder.
3. Download the [SQL dump](https://drive.google.com/drive/folders/105fXg-ftZldQBNVzPCdDwZzZGLOteeA5?usp=sharing) and import it in your MYSQL database.
4. Copy the urwriters.owl, the urbooks.owl, and urwriters.properties files in the Ontop folder.
5. Edit the urwriters.properties file with the name and the password of your MYSQL admin.  
6. Try to run the following command, that should map the relational database to a .ttl file:

```
ontop-cli-x.x.x/ontop materialize -t urwriters.owl -p urwriters.properties -m all_mappings/urwriters-mappings_wd_works.r2ml -f turtle --disable-reasoning -o urwriters_mapped.ttl
```

#### Summary of the mapping files
In the table below all the r2rml mapping files are listed together with the type of entities they map and the source of knowledge

|**mapping file**|**mapped entities**|**Source**|
|-----------------|------------------|----------|
|urwriters-mapping_wd_works.r2ml|all works and properties about works|Wikidata|
|urwriters-mapping_wd_authors.r2ml|all authors and properties about authors|Wikidata|
|urwriters-mapping_ol_works.r2ml|all works|OpenLibrary|
|urwriters-mapping_ol_editions.r2ml|all editions|OpenLibrary|
|urwriters-mapping_ol_works_editions.r2ml|all the works associated to their editions|OpenLibrary|
|urwriters-mapping_ol_works_authors.r2ml|all the works associated to their authors|OpenLibrary|
|urwriters-mapping_ol_works_subjects_01.r2ml|all the works associated to their subject|OpenLibrary|
|urwriters-mapping_ol_works_subjects_02.r2ml|all the works associated to their subject|OpenLibrary|
|urwriters-mapping_ol_works_subjects_places.r2ml|all the works associated to their subject places|OpenLibrary|
|urwriters-mapping_ol_editions_language.r2ml|all the editions and their language|OpenLibrary|
|urwriters-mapping_ol_publication_events.r2ml|all the information about the publications of a work|OpenLibrary|
|urwriters-mapping_gr_works.r2ml|all works|Goodreads|
|urwriters-mapping_gr_works_authors.r2ml|all the works associated to their authors|Goodreads|
|urwriters-mapping_gr_prizes.r2ml|all literary prizes and their winners|Goodreads|
|urwriters-mapping_gb_editions.r2ml|all editions|Google Books|
|urwriters-mapping_gb_editions_eq2_ol_gr.r2ml|all editions mapped with Goodreads and OpenLibrary|Google Books|
|urwriters-mapping_gb_editions_language_subject.r2ml|all editions, their language, and subject|Google Books|
|urwriters-mapping_gb_publishers_descriptions.r2ml|all editions, their synopsis, and publishers|Google Books|
|urwriters-mapping_gb_publication_events.r2ml|all the information about the publications of an edition|Google Books|
|urwriters-mapping_countries_years_langs.r2ml|all languages, countries, and years|all resources|

### SPARQL endpoint
Due to some memory issues the SPARQL enpoint is not fully accessible yet. However, you can perform some queries from [this page](https://underrepresented.di.unito.it/index.php/sparql-queries/)
