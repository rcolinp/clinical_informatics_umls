# Clinical Informatics UMLS®

**Preview of v1 Neo4j UMLS Graph to be created: (Repo/Graph is a work in progress)**
![UMLS® Neo4j Graph Schema](images/schema_dark.png)

Schema Overview:

There are 4 main elements within the graph which have been extracted from UMLS and portrayed as a Neo4j Property Graph.

- The UMLS atomic unique identifier (AUI - Atom)
- The UMLS concept unique identifier (CUI - Concept)
- The UMLS semantic unique identifier (TUI - SemanticType)
- The source vocabulary concept unique identifier (CODE - SourceVocabulary)
  - Source vocabularies within UMLS which are demonstrated within this v1 graph can be found in the schema illustration above. I.e. NCI Thesaurus (NCI), SNOMEDCT_US, ICDO3, ICD10CM, GO, RXNORM, ATC, etc...

This schema is only one method of representing the UMLS as a label property graph. Key design features of the graph:

- This design leverages the primary key within UMLS (umls_aui - Atom) as a bridge to crosswalk source vocabulary concepts to common concept unique identifiers (umls_cui - Concept) which are shared between other source vocabularies contained in the graph. Additionally, both intra and inter hierarchial relationships from each distinct source vocabulary & from a vocabulary agnostic point of view can be traversed and queried.

- The entire UMLS semantic network has been integrated into the graph via directed relationships to & from Concept & SemanticType. The semantic network being the semantic relations across UMLS's SemanticTypes. See below a visualization of the UMLS's semantic network in context of `Amino Acid, Peptide, or Protein` shortest path to the `top concept of` -> `Entity`. (Via following cypher query:
  - `match path = (a:SemanticType {sty: "Entity"})<-[:ISA*]-(b:SemanticType {sty: "Amino Acid, Peptide, or Protein"}) return path`
    - Distinct from the ISA relationships that exist between concepts, within UMLS the same semantic relationships exist between the concepts semantic definitions/meanings as well.

![UMLS® Semantic Network Example](images/amino_acid_peptide_protein_to_root.png)

- This provides a unique ability to leverage UMLS's semantic network in relation to its hierarchial and concept-concept/code-code relationships.

## Unified Medical Language System® (UMLS®) & Interoperability

In this repository, an exploration of a handful of the largest and/or industry relevant biomedical ontologies (within the Unified Medical Language System® (UMLS®)).

**Disclaimer** - while this repository is open to anyone & has been created to share knowledge, educate & provide to open source community. In order to access the data covered, you must be a UMLS® license holder. Please visit [How to License and Access the Unified Medical Language System® (UMLS®) Data](https://www.nlm.nih.gov/databases/umls.html) to learn more.

The scope of material covered in this repository will pertain specifically to healthcare, biotechnology & pharmaceutics. Largely in regards to oncology.

The UMLS® ontologies/vocabularies within the scope of this repository has been limited due to the enormous size of UMLS® (containing >200+ vocabularies). Despite the "limited" scope, the vocabularies chosen to be included all live at the forefront of bringing interoperability to healthcare. These ontologies contain rich semantics such as concept hierarchies and semantic relationships which leave them at the forefront of industry use.

As described above, a "subset" of the UMLS® 2021AA full release (available as of 05/03/2021 -> next release (2021AB will be available November, 2021), containing pertinent present day industry standard biomedical ontologies have been chosen for this project (complete list to follow in next section). UMLS® License holders are provided an ability to create "subsets" of the data within the UMLS®. These subsets are provided in their native rich release format (RRF) & a relational database structure.

A part of this repository will dedicated to how a subset of UMLS® can be transformed from its native Rich Release Format (RRF) to more intuitive and common relational structures such as MySQL, PostgresSQL & SQLite (all covered in this repository). Additionally, this repository will explore how the relational structure built can be modeled as a noSQL graph (will be using [Neo4j](https://neo4j.com/) - a label property graph & the world's leading graph database).

The UMLS® provides a robust collection of interconnected data. In effort of studying this rich collection of "interconnected data", this repository will explore first creating a UMLS® subset as a relational database (SQLite, MySQL & PostgresSQL), querying that relational model & how to transform the relational model to a Neo4j graph database.

### What is the UMLS® & Why is it Important?

- "The UMLS® integrates and distributes key terminology, classification and coding standards, and associated resources to promote creation of more effective and interoperable biomedical information systems and services, including electronic health records."
  - [UMLS®](https://www.nlm.nih.gov/research/umls/index.html)

- The UMLS®, or Unified Medical Language System®, is a set of files and software that brings together many health and biomedical vocabularies and standards to enable interoperability between computer systems.
  - [UMLS®](https://www.nlm.nih.gov/research/umls/index.html)

- UMLS® contains over 200+ industry standard biomedical vocabularies & ontologies. Check out contents (ontologies/vocabularies) contained within UMLS® via following link:
  - [UMLS® Release Ontologies & Vocabularies](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/index.html)

#### Ontologies Within Scope of Repository

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

##### Python Environment Setup

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
docker run --name=umls \
    --publish=7474:7474 --publish=7687:7687 \
    -d \
    --volume=$HOME/neo4j/data:/data \
    --volume=$HOME/import:/var/lib/neo4j/import \
    --volume=$HOME/neo4j/plugins:/plugins \
    --env=NEO4J_ACCEPT_LICENSE_AGREEMENT=yes \
    --env=NEO4J_dbms_backup_enabled=true \
    --env=apoc_import_file_enabled=true \
    --env=apoc_export_file_enabled=true \
    --env=apoc_import_file_use_neo4j__config=true \
    --env=apoc_export_file_use_neo4j__config=true \
    --env=NEO4JLABS_PLUGINS='["apoc", "graph-data-science"]' \
    --env=NEO4J_dbms_memory_heap_initial_tx_state_memory__allocation=ON_HEAP \
    --env=NEO4J__dbms_jvm_additional=-Dunsupported.dbms.udc.source=debian
    --env=NEO4J_AUTH=neo4j/<INSERT PWD> \
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
    --nodes='import/SemanticTypeNode.csv' \
    --relationships='import/has_sty.csv' \
    --relationships='import/has_umls_aui.csv' \
    --relationships='import/has_cui.csv' \
    --relationships='import/tui_tui_rel.csv' \
    --relationships='import/child_of_rel.csv' \
    --relationships='import/cui_cui_rel.csv' \
    --relationships='import/cui_code_rel.csv' \
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
    --nodes='import/SemanticTypeNode.csv' \
    --relationships='import/has_sty.csv' \
    --relationships='import/has_umls_aui.csv' \
    --relationships='import/has_cui.csv' \
    --relationships='import/tui_tui_rel.csv' \
    --relationships='import/child_of_rel.csv' \
    --relationships='import/cui_cui_rel.csv' \
    --relationships='import/cui_code_rel.csv' \
    --skip-bad-relationships=true \
    --skip-duplicate-nodes=true \
    --trim-strings=true 
```

Output:

```shell  
Neo4j version: 4.3.5
Importing the contents of these files into /var/lib/neo4j/data/databases/neo4j:
Nodes:
  /var/lib/neo4j/import/conceptNode.csv
  /var/lib/neo4j/import/atomNode.csv
  /var/lib/neo4j/import/codeNode.csv
  /var/lib/neo4j/import/SemanticTypeNode.csv

Relationships:
  /var/lib/neo4j/import/has_sty.csv
  /var/lib/neo4j/import/has_umls_aui.csv
  /var/lib/neo4j/import/has_cui.csv
  /var/lib/neo4j/import/tui_tui_rel.csv
  /var/lib/neo4j/import/child_of_rel.csv
  /var/lib/neo4j/import/cui_cui_rel.csv
  /var/lib/neo4j/import/cui_code_rel.csv
  ...

  Estimated number of nodes: 5.01 M
  Estimated number of node properties: 27.24 M
  Estimated number of relationships: 37.23 M
  Estimated number of relationship properties: 15.80 M
  Estimated disk space usage: 2.567GiB
  Estimated required memory usage: 1.058GiB
  ...
(1/4) Nodes import
  ...
(2/4) Relationship import
  ...
(3/4) Relationship linking
  ...
(4/4) Post processing
  ...
IMPORT DONE in 2m 47s 283ms. 
Imported:
  4112426 nodes
  18522117 relationships
  25868020 properties
Peak memory usage: 1.071GiB
```

Exit docker command-line via:

- `exit`

Need to restart the container:

- `docker restart <CONTAINER ID>`

- Once container has been restarted (s/p successful import), go ahead and Navigate to [Neo4j Browser](http://localhost:7474/) within a browser & login using the credentials set via the environmental variable `env=NEO4J_AUTH=neo4j/<password>`.
  - user: `neo4j` (default is `neo4j` -> set in `--env=NEO4J_AUTH=neo4j/<password>`)
  - pass: `<password>` -> set prior via `--env=NEO4J_AUTH=neo4j/<password>`)

##### Querying the UMLS as a Neo4j Graph

Checkout the notebooks directory where the graph will be queried via both official `neo4j` python driver & community supported python driver `py2neo`.
