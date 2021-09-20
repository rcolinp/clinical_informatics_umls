# Clinical Informatics UMLS®

In this repository, a thorough exploration of some of the largest and/or most relevant biomedical ontologies within the Unified Medical Language System® (UMLS®) pertaining to oncology will be done.

The scope of material covered in this repository will pertain specifically to healthcare, biotechnology & pharmaceutics, with a heavy focus around oncology & cancer.

The UMLS® ontologies within the scope of this repository contain rich semantics, concept hierarchies & semantic relationships which put them on the forefront of empowering AI & subject matter experts towards smarter treatment decisions & interoperability of biomedical data within healthcare.

A subset of the UMLS® 2021AA full release (available as of 05/03/2021), containing pertinent present day industry standard biomedical ontologies have been chosen for this project (complete list to follow in next section). The relational structure of UMLS® will be transformed from its native Rich Release Format (RRF) to more intuitive relational structures in addition to noSQL graphs. Specifically using the worlds leading graph data model, Neo4j (label property graph).

## What is the UMLS® & Why is it Important?

- "The UMLS® integrates and distributes key terminology, classification and coding standards, and associated resources to promote creation of more effective and interoperable biomedical information systems and services, including electronic health records."
  - [UMLS®](https://www.nlm.nih.gov/research/umls/index.html)

- The UMLS®, or Unified Medical Language System®, is a set of files and software that brings together many health and biomedical vocabularies and standards to enable interoperability between computer systems.
  - [UMLS®](https://www.nlm.nih.gov/research/umls/index.html)

- UMLS® contains over 200+ industry standard biomedical vocabularies & ontologies. Check out contents (ontologies/vocabularies) contained within UMLS® via following link:
  - [UMLS® Release Ontologies & Vocabularies](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/index.html)

### Ontologies Within Scope of Repository

- **Anatomical Therapeutic Chemical Classification System:**
  - Abbreviation -> **ATC**
    - NIH/UMLS Vocabulary Documentation:
      - [ATC (Anatomical Therapeutic Chemical Classification System) - Synopsis](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/ATC/index.html)
- **Gene Ontology:**
  - Abbreviation -> **GO**
    - NIH/UMLS Vocabulary Documentation:
      - [GO (Gene Ontology) - Synopsis](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/GO/index.html)
- **HUGO Gene Nomenclature Committee:**
  - Abbreviation -> **HGNC**
    - NIH/UMLS Vocabulary Documentation:
      - [HGNC (HUGO Gene Nomenclature Committee) - Synopsis](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/HGNC/index.html)
- **Human Phenotype Ontology:**
  - Abbreviation -> **HPO**
    - NIH/UMLS Vocabulary Documentation:
      - [HPO (Human Phenotype Ontology) - Synopsis](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/HPO/index.html)
- **International Classification of Diseases, Ninth Revision, Clinical Modification:**
  - Abbreviation -> **ICD9CM**
    - NIH/UMLS Vocabulary Documentation:
      - [ICD9CM (International Classification of Diseases, Ninth Revision, Clinical Modification) - Synopsis](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/ICD9CM/index.html)
- **International Classification of Diseases, Tenth Revision, Clinical Modification:**
  - Abbreviation -> **ICD10CM**
    - NIH/UMLS Vocabulary Documentation:
      - [ICD10CM (International Classification of Diseases, Tenth Revision, Clinical Modification) - Synopsis](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/ICD10CM/index.html)
- **ICD-10 Procedure Coding System:**
  - Abbreviation -> **ICD10PCS**
    - NIH/UMLS Vocabulary Documentation:
      - [ICD10PCS (ICD-10 Procedure Coding System) - Synopsis](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/ICD10PCS/index.html)
- **LOINC:**
  - Abbreviation -> **LNC**
    - NIH/UMLS Vocabulary Documentation:
      - [LNC (LOINC) - Synopsis](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/LNC/index.html)
- **MedDRA:**
  - Abbreviation -> **MDR**
    - NIH/UMLS Vocabulary Documentation:
      - [MDR (MedDRA) - Synopsis](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/MDR/index.html)
- **Medication Reference Terminology:**
  - Abbreviation -> **MED-RT**
    - NIH/UMLS Vocabulary Documentation:
      - [MED-RT (Medication Reference Terminology) - Synopsis](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/MED-RT/index.html)
- **MeSH:**
  - Abbreviation -> **MSH**
    - NIH/UMLS Vocabulary Documentation:
      - [MSH (MeSH) - Synopsis](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/MSH/index.html)
- **NCBI Taxonomy:**
  - Abbreviation -> **NCBI**
    - NIH/UMLS Vocabulary Documentation:
      - [NCBI (NCBI Taxonomy) - Synopsis](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/NCBI/index.html)
- **National Cancer Institute Thesaurus:**
  - Abbreviation -> **NCI**
    - NIH/UMLS Vocabulary Documentation:
      - [NCI (NCI Thesaurus) - Synopsis](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/NCI/index.html)
- **Physician Data Query:**
  - Abbreviation -> **PDQ**
    - NIH/UMLS Vocabulary Documentation:
      - [PDQ (Physician Data Query) - Synopsis](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/PDQ/index.html)
- **RXNORM:**
  - Abbreviation -> **RXNORM**
    - NIH/UMLS Vocabulary Documentation:
      - [RXNORM (RXNORM) - Synopsis](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/RXNORM/index.html)
- **SNOMED CT, US Edition:**
  - Abbreviation -> **SNOMEDCT_US**
    - NIH/UMLS Vocabulary Documentation:
      - [SNOMEDCT_US (SNOMED CT, US Edition) - Synopsis](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/SNOMEDCT_US/index.html)
- **Source Terminology Names (UMLS):**
  - Abbreviation -> **SRC**
    - NIH/UMLS Vocabulary Documentation:
      - [SRC (Source Terminology Names (UMLS)) - Synopsis](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/SRC/index.html)

#### Python Environment Setup

Strongly recommend use of [pyenv](https://github.com/pyenv/pyenv) to enable easy switches between multiple versions of Python.

- Python >=3.8 required based on `pyproject.toml`

- Python v3.8.6 with version management via [pyenv](https://github.com/pyenv/pyenv) & python packing packing and dependency management via [Poetry](https://python-poetry.org/).
  - [pyenv](https://github.com/pyenv/pyenv) strongly recommended to allow flexibility of which version of python you are using (general recommendation for anyone using Python as-well `:)`!
    - If unfamiliar with [pyenv](https://github.com/pyenv/pyenv) AND/OR [Poetry](https://python-poetry.org/), please check out their respective official docs.
      - Check out respective links if unfamiliar as [pyenv](https://github.com/pyenv/pyenv) AND/OR [Poetry](https://python-poetry.org/) setup & use will not be covered within this repository.

This project has an included `pyproject.toml` as the python packaging and dependency management has been setup using [Poetry](https://python-poetry.org/). If unfamiliar with [Poetry](https://python-poetry.org/), please visit the official documentation provided.

- Create a virtual environment within project directory:
`python3 -m venv venv`

- Activate the virtual environment:
`source venv/bin/activate`

- Install all python packaging and dependencies into virtual environment:
`poetry install`

- Or execute `poetry shell` to create & activate a virtual environment.

- Install packaging and dependencies into that environment via `poetry install`

##### Neo4j Docker Setup & Data Import

Docker Image:

```shell
docker run \
    --detach \
    --publish=7474:7474 --publish=7687:7687 \
    --volume=$HOME/neo4j:/data \
    --volume=$HOME/import:/var/lib/neo4j/import \
    --volume=$HOME/neo4j/plugins:/plugins \
    --env=NEO4J_ACCEPT_LICENSE_AGREEMENT=yes \
    --env=apoc_import_file_enabled=true \
    --env=apoc_export_file_enabled=true \
    --env=apoc_import_file_use_neo4j__config=true \
    --env=NEO4JLABS_PLUGINS='["apoc", "graph-data-science"]' \
    --env=NEO4J_AUTH=neo4j/<insert password> \
    --env=NEO4J_dbms_memory_heap_initial__size=1.002G \
    --env=NEO4J_dbms_memory_heap_max__size=1.002G \
    neo4j:enterprise
```

##### Import Data Into Neo4j Graph

- Importing the .csv files will require use of Neo4j's `neo4j-admin import` tool

  - Required for imports > 10 million nodes/edges

- Execute the following commands within your terminal:

  - `docker exec -it <CONTAINER ID> /bin/bash`

    - Your terminal should appear as follows:

      - `root@<CONTAINER ID>:/var/lib/neo4j#`

      - The character string following `root@` should be the Docker `CONTAINER ID`.

      - This is where we can invoke `neo4j-admin import`.

- Ensure you have correctly mounted volumes appropriately & the `import` directory is not not located within the directory `neo4j`.

- **While inside docker containers command-line, execute the following prior to import:**
  - `rm -rf data/databases/`
  - `rm -rf data/transactions/`
- **NOTE:** This is a required step when using `neo4j-admin import`.
  - By invoking this command to import data, the database for your data must not already exist as well.

- Now the database can be created & imported into. Execute the following:

```shell
    ./bin/neo4j-admin import \
    --database=neo4j \
    --nodes='import/conceptNode.csv' \
    --nodes='import/atomNode.csv' \
    --nodes='import/codeNode.csv' \
    --nodes='import/semanticTypeNode.csv' \
    --nodes='import/attributeNode.csv' \
    --relationships='import/has_sty.csv' \
    --relationships='import/is_sty_of.csv' \
    --relationships='import/has_umls_atom.csv' \
    --relationships='import/has_cui.csv' \
    --relationships='import/has_aui_rel.csv' \
    --relationships='import/has_child_code.csv' \
    --relationships='import/code_has_attribute.csv' \
    --relationships='import/sty_isa.csv' \
    --relationships='import/cui_cui_rel.csv' \
    --relationships='import/cui_attribute_rel.csv' \
    --relationships='import/attribute_aui_rel.csv' \
    --skip-bad-relationships=true \
    --skip-duplicate-nodes=true \
    --trim-strings=true 
```

Here are a few snippets of what the above commands should look like (including both inputs & outputs):

```shell
% docker exec -it <CONTAINER ID> /bin/bash
/var/lib/neo4j# rm -rf data/databases/
/var/lib/neo4j# rm -rf data/transactions/
/var/lib/neo4j# ./bin/neo4j-admin import \
    --database=neo4j \
    --nodes='import/conceptNode.csv' \
    --nodes='import/atomNode.csv' \
    --nodes='import/codeNode.csv' \
    --nodes='import/semanticTypeNode.csv' \
    --nodes='import/attributeNode.csv' \
    --relationships='import/has_sty.csv' \
    --relationships='import/is_sty_of.csv' \
    --relationships='import/has_umls_atom.csv' \
    --relationships='import/has_cui.csv' \
    --relationships='import/has_aui_rel.csv' \
    --relationships='import/has_child_code.csv' \
    --relationships='import/code_has_attribute.csv' \
    --relationships='import/sty_isa.csv' \
    --relationships='import/cui_cui_rel.csv' \
    --relationships='import/cui_attribute_rel.csv' \
    --relationships='import/attribute_aui_rel.csv' \
    --skip-bad-relationships=true \
    --skip-duplicate-nodes=true \
    --trim-strings=true 
```

Output:

```shell  
Neo4j version: 4.3.3
Importing the contents of these files into /data/databases/neo4j:
Nodes:
  /var/lib/neo4j/import/conceptNode.csv
  /var/lib/neo4j/import/atomNode.csv
  /var/lib/neo4j/import/codeNode.csv
  /var/lib/neo4j/import/semanticTypeNode.csv
  /var/lib/neo4j/import/attributeNode.csv

Relationships:
  /var/lib/neo4j/import/has_sty.csv
  /var/lib/neo4j/import/is_sty_of.csv
  /var/lib/neo4j/import/has_umls_atom.csv
  /var/lib/neo4j/import/has_cui.csv
  /var/lib/neo4j/import/has_aui_rel.csv
  /var/lib/neo4j/import/has_child_code.csv
  /var/lib/neo4j/import/code_has_attribute.csv
  /var/lib/neo4j/import/sty_isa.csv
  /var/lib/neo4j/import/cui_cui_rel.csv
  /var/lib/neo4j/import/cui_attribute_rel.csv
  /var/lib/neo4j/import/attribute_aui_rel.csv
  ...
```

Upon successful import, the following will be displayed:

```shell
IMPORT DONE in 6m 44s 277ms. 
Imported:
  13032449 nodes
  31565024 relationships
  63630232 properties
Peak memory usage: 232.4MiB
```

Exit docker command-line via:

- `exit;`
Need to restart the container:

- `docker restart <CONTAINER ID>`

- Once container has been restarted (s/p successful import), go ahead and Navigate to [Neo4j Browser](http://localhost:7474/) within a browser & login using the credentials set via the environmental variable `env=NEO4J_AUTH=neo4j/<password>`.
  - user: `neo4j` (default is `neo4j` -> set in `--env=NEO4J_AUTH=neo4j/<password>`)
  - pass: `<password>` -> set prior via `--env=NEO4J_AUTH=neo4j/<password>`)

##### Querying the UMLS as a Neo4j Graph

Checkout the notebooks directory where the graph will be queried via both official `neo4j` python driver & community supported python driver `py2neo`.
