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

##### Neo4j Desktop Setup & Data Import

- Data Import:

```SHELL
./bin/neo4j-admin import --database=neo4j --max-memory=100G \
--nodes='import/conceptNode.csv' \
--nodes='import/atomNode.csv' \
--nodes='import/codeNode.csv' \
--nodes='import/semanticTypeNode.csv' \
--nodes='import/attributeNode.csv' \
--relationships='import/has_sty.csv' \
--relationships='import/is_sty_of.csv' \
--relationships='import/has_umls_aui.csv' \
--relationships='import/has_cui.csv' \
--relationships='import/has_child_code.csv' \
--relationships='import/code_has_attribute.csv' \
--relationships='import/sty_isa.csv' \
--relationships='import/cui_cui_rel.csv' \
--skip-bad-relationships=true \
--skip-duplicate-nodes=true \
--processors=12 \
--high-io=true \
--cache-on-heap=true \
--trim-strings=true
```
