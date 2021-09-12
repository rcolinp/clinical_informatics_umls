# Clinical Informatics UMLS

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

### Ontologies Included/Within Scope of Project

- Anatomical Therapeutic Chemical Classification System
  - ATC
    - NIH/UMLS Vocabulary Documentation:
      - [ATC (Anatomical Therapeutic Chemical Classification System) - Synopsis](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/ATC/index.html)
- DrugBank
  - DRUGBANK
    - NIH/UMLS Vocabulary Documentation:
      - [DRUGBANK (DrugBank) - Synopsis](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/DRUGBANK/index.html)
- Gene Ontology
  - GO
    - NIH/UMLS Vocabulary Documentation:
      - [GO (Gene Ontology) - Synopsis](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/GO/index.html)
- HUGO Gene Nomenclature Committee
  - HGNC
    - NIH/UMLS Vocabulary Documentation:
      - [HGNC (HUGO Gene Nomenclature Committee) - Synopsis](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/HGNC/index.html)
- International Classification of Diseases, Ninth Revision, Clinical Modification
  - ICD9CM
    - NIH/UMLS Vocabulary Documentation:
      - [ICD9CM (International Classification of Diseases, Ninth Revision, Clinical Modification) - Synopsis](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/ICD9CM/index.html)
- International Classification of Diseases, Tenth Revision, Clinical Modification
  - ICD10CM
    - NIH/UMLS Vocabulary Documentation:
      - [ICD10CM (International Classification of Diseases, Tenth Revision, Clinical Modification) - Synopsis](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/ICD10CM/index.html)
- ICD-10 Procedure Coding System
  - ICD10PCS
    - NIH/UMLS Vocabulary Documentation:
      - [ICD10PCS (ICD-10 Procedure Coding System) - Synopsis](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/ICD10PCS/index.html)
- MedDRA
  - MDR
    - NIH/UMLS Vocabulary Documentation:
      - [MDR (MedDRA) - Synopsis](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/MDR/index.html)
- Medication Reference Terminology
  - MED-RT
    - NIH/UMLS Vocabulary Documentation:
      - [MED-RT (Medication Reference Terminology) - Synopsis](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/MED-RT/index.html)
- National Cancer Institute Thesaurus
  - NCI
    - NIH/UMLS Vocabulary Documentation:
      - [NCI (NCI Thesaurus) - Synopsis](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/NCI/index.html)
- RXNORM
  - RXNORM
    - NIH/UMLS Vocabulary Documentation:
      - [RXNORM (RXNORM) - Synopsis](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/RXNORM/index.html)

- SNOMED CT, US Edition
  - SNOMEDCT_US
    - NIH/UMLS Vocabulary Documentation:
      - [SNOMEDCT_US (SNOMED CT, US Edition) - Synopsis](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/SNOMEDCT_US/index.html)

#### Python Environment Setup

This project has an included `pyproject.toml` as the python packaging and dependency management has been setup using [Poetry](https://python-poetry.org/). If unfamiliar with [Poetry](https://python-poetry.org/), please visit the offical documentation provided.

- Create a virtual environment within project directory:
`python3 -m venv venv`

- Activate the virtual environment:
`source venv/bin/activate`

- Install all python packaging and dependencies into virtual environment:
`poetry install`

##### Neo4j Docker Setup & Data Import

Docker Image:

```shell
docker run -it --name=umls -d \
    --publish="7474:7474" --publish="7687:7687" \
    --volume=$HOME/neo4j:/data \
    --volume=$HOME/import:/var/lib/neo4j/import \
    --volume=$HOME/neo4j/plugins:/plugins \
    --env=NEO4J_ACCEPT_LICENSE_AGREEMENT=yes \
    --env=apoc_import_file_enabled=true \
    --env=apoc_export_file_enabled=true \
    --env=apoc_import_file_use_neo4j__config=true \
    --env=NEO4JLABS_PLUGINS='["apoc", "graph-data-science"]' \
    --env=NEO4J_AUTH=neo4j/umls \
    neo4j:4.3-enterprise
```

##### Import Data Into Neo4j Graph

- Importing the .csv files will require use of Neo4j's `neo4j-admin import` tool

  - Required for imports > 10 million nodes/edges

- Execute the following commands within your terminal:

  - `docker exec -it umls /bin/bash`

    - your terminal should look something similar to following: `root@a12345678abc1:/var/lib/neo4j#`

      - The character string following `root@` should be the Docker ContainerID.

      - This is where we can utilize the `neo4j-admin import` tool

- Ensure you have correctly mounted volumes appropriately & the `import` directory is not not located within the directory `neo4j`.

- While inside docker containers command-line, execute the following prior to import:
  - `rm -rf data/databases/`
  - `rm -rf data/transactions/`
  - Now import .csv data & create the UMLS graph via following:

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
    --relationships='import/has_child_code.csv' \
    --relationships='import/code_has_attribute.csv' \
    --relationships='import/sty_isa.csv' \
    --relationships='import/cui_cui_rel.csv' \
    --skip-bad-relationships=true \
    --skip-duplicate-nodes=true 
```

Here is a snippet of what the above commands should look like:

```shell
robpiombino@Robs-MBP neo4j % docker ps
CONTAINER ID   IMAGE                  COMMAND                  CREATED       STATUS          PORTS                                                                                            NAMES
0f1a4369eb8b   neo4j:4.3-enterprise   "/sbin/tini -g -- /d…"   3 hours ago   Up 13 minutes   0.0.0.0:7474->7474/tcp, :::7474->7474/tcp, 7473/tcp, 0.0.0.0:7687->7687/tcp, :::7687->7687/tcp   umls
robpiombino@Robs-MBP neo4j % docker exec -it umls /bin/bash
root@0f1a4369eb8b:/var/lib/neo4j# rm -rf data/databases/
root@0f1a4369eb8b:/var/lib/neo4j# rm -rf data/transactions/
root@0f1a4369eb8b:/var/lib/neo4j# ./bin/neo4j-admin import \
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
    --relationships='import/has_child_code.csv' \
    --relationships='import/code_has_attribute.csv' \
    --relationships='import/sty_isa.csv' \
    --relationships='import/cui_cui_rel.csv' \
    --skip-bad-relationships=true \
    --skip-duplicate-nodes=true 
Selecting JVM - Version:11.0.12, Name:OpenJDK 64-Bit Server VM, Vendor:Oracle Corporation
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
  /var/lib/neo4j/import/has_child_code.csv
  /var/lib/neo4j/import/code_has_attribute.csv
  /var/lib/neo4j/import/sty_isa.csv
  /var/lib/neo4j/import/cui_cui_rel.csv
```

Upon successful import, the following will be displayed:

```shell
IMPORT DONE in 4m 43s 153ms. 
Imported:
  6312676 nodes
  13876409 relationships
  33919728 properties
Peak memory usage: 246.3MiB
```

Exit docker command-line via:

- `exit;`
Need to restart the container:

- `docker restart umls`

- Once container has been restarted (s/p successful import), go ahead and Navigate to [Neo4j Browser](http://localhost:7474/) within a browser & login using the credentials set via the environmental variable `env=NEO4J_AUTH=neo4j/umls`.
  - username: `neo4j`
  - password: `umls`

##### Querying the UMLS as a Neo4j Graph

Checkout the notebooks directory where the graph will be queried via both official `neo4j` python driver & community supported python driver `py2neo`.
