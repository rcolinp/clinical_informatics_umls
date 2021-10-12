"""
SUMMARY
-------

This .py assumes you are querying the SQLite database found at the relative path ->../sqlite/umls.db. 
This database is created via the following shell script located within that same directory. -->..sqlite/create_sqlite_db.sh.
  --> invoke that shell script via `sh create_sqlite_db_.sh ../UMLS/subset/2021AA` (where the path argument is path to local .RRF files) 

Note: If using MySQL, Oracle or PostgreSQL, you'll need to adjust the connection object ('conn') appropriately to your datasource. Dependencies for MySQL, PostgreSQL and MariaDB are all included in the pyproject.toml file. (i.e. mysql.connector, psycopg2-binary, SQLAlchemy, mariadb, pymysql, etc...).
An example connection object for MySQL & PostgresSQL connection have been included below for reference.

****************************************************
MySQL connection: 

import mysql.connector

mconn = mysql.connector.connect(
    host=hostname,
    user=username,
    password=password,
    database=database <-- schema name with loaded UMLS subset
)
****************************************************
PostgresSQL connection (using psycopg2):

import psycopg2

pgconn = psycopg2.connect(
    host=host,
    user=username,
    password=password,
    database=database
    )
    
"""

import sys
import os
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
import numpy as np
import pandas as pd
import sqlite3


# Establish database connection using local SQLite
db_name = "umls.db"
relative_path_to_sqlite = "../sqlite/"
conn = sqlite3.connect(os.path.join(relative_path_to_sqlite, db_name))

# **************************************************************
# GRAPH LABELS & NODES
# **************************************************************

# **************************************************************
# GRAPH LABELS:
# LABELS = ["SemanticType", "Code", "Atom", "Concept", ATC", "GO",
#           "HGNC", "ICD9CM", "ICD10CM", "ICD10PCS", "ICDO3", "MED-RT",
#           "NCI", "RXNORM", "SNOMEDCT_US"]
# **************************************************************

# Label: SemanticType
# import: semanticTypeNode.csv
semantic_node = '''
SELECT DISTINCT TUI
              , STY
              , STN  
              , 'SemanticType'  as ":LABEL"
FROM MRSTY;
'''

semanticTypeNode = pd.read_sql_query(
    semantic_node, conn).drop_duplicates().replace(np.nan, "")

semanticTypeNode.columns = ["SemanticTypeId:ID", "sty", "stn", ":LABEL"]

semanticTypeNode.to_csv(path_or_buf="../../../../import/semanticTypeNode.csv",
                        header=True,
                        index=False)
print("semanticTypeNode.csv successfully written out...")

# **************************************************************
# Label: Concept
# import: conceptNode.csv
concept_node = '''
SELECT DISTINCT CUI
              , STR
              , 'Concept' AS ":LABEL"
FROM MRCONSO
WHERE ISPREF = 'Y'
    AND STT = 'PF'
    AND TS = 'P'
    AND SUPPRESS = 'N'
    AND SAB IN ('ATC', 'GO', 'HGNC', 'ICD9CM', 'ICD10CM', 'ICD10PCS', 'MED-RT', 'NCI', 'RXNORM', 'SNOMEDCT_US')
    AND LAT = 'ENG';
    '''

conceptNode = pd.read_sql_query(
    concept_node, conn).drop_duplicates().replace(np.nan, '')

conceptNode.columns = ["ConceptId:ID", "name", ":LABEL"]

conceptNode.to_csv(path_or_buf='../../../../import/conceptNode.csv',
                   header=True,
                   index=False)
print("conceptNode.csv successfully written out...")
# **************************************************************
# Label: Atom
# import: atomNode.csv
atom_node = '''
SELECT DISTINCT AUI
              , STR
              , SAB
              , CODE
              , TTY
              , ISPREF
              , TS
              , STT
              , 'Atom' AS ":LABEL"
FROM MRCONSO
WHERE SAB IN ('ATC', 'GO', 'HGNC', 'ICD9CM', 'ICD10CM', 'ICD10PCS', 'MED-RT', 'NCI', 'RXNORM', 'SNOMEDCT_US')
  AND SUPPRESS = 'N'
  AND LAT = 'ENG';
  '''

atomNode = pd.read_sql_query(atom_node, conn).drop_duplicates(
    subset=['AUI']).replace(np.nan, "")

atomNode.columns = ["AtomId:ID", "name", "vocab",
                    "code", "tty", "ispref", "ts", "stt", ":LABEL"]

atomNode.to_csv(path_or_buf="../../../../import/atomNode.csv",
                header=True,
                index=False)
print("atomNode.csv successfully written out...")
# **************************************************************
# Label: Code
# import: codeNode.csv
code = '''
WITH cuis AS (SELECT DISTINCT CUI
              FROM MRCONSO
              WHERE MRCONSO.ISPREF = 'Y'
                AND MRCONSO.SUPPRESS = 'N'
                AND MRCONSO.LAT = 'ENG'
                AND MRCONSO.TS = 'P'
                AND MRCONSO.STT = 'PF')
SELECT DISTINCT (MRCONSO.SAB || '#' || MRCONSO.CODE) AS "CodeId:ID"
              , MRCONSO.SAB
              , MRCONSO.CODE
              , ('Code' || ';' || MRCONSO.SAB)       AS ":LABEL"
FROM MRCONSO
         INNER JOIN cuis
                    ON MRCONSO.CUI = cuis.CUI
WHERE SAB IN ('ATC', 'GO', 'HGNC', 'ICD9CM', 'ICD10CM', 
              'ICD10PCS', 'MED-RT', 'NCI', 'RXNORM', 'SNOMEDCT_US')
  AND MRCONSO.SUPPRESS = 'N';
  '''
codeNode = pd.read_sql_query(code, conn).drop_duplicates().replace(
    np.nan, '')
codeNode.columns = ['CodeId:ID', 'vocab', 'code', ':LABEL']
codeNode.to_csv(path_or_buf='../../../../import/codeNode.csv',
                header=True,
                index=False)
print("codeNode.csv successfully written out...")
# **************************************************************
# GRAPH EDGES/RELATIONSHIPS
# **************************************************************
# has_sty.csv & sty_of.csv
has_sty = '''
SELECT DISTINCT CUI
              , TUI
              , 'HAS_STY' AS ":TYPE" 
FROM MRSTY;
'''
is_sty_of = '''
SELECT DISTINCT TUI
              , CUI
              , 'IS_STY_OF' AS ":TYPE" 
FROM MRSTY;
'''

has_sty_rel = pd.read_sql_query(
    has_sty, conn).drop_duplicates().replace(np.nan, '')
is_sty_of_rel = pd.read_sql_query(
    is_sty_of, conn).drop_duplicates().replace(np.nan, '')

has_sty_rel.columns = [':START_ID', ':END_ID', ':TYPE']
is_sty_of_rel.columns = [':START_ID', ':END_ID', ':TYPE']

has_sty_rel.to_csv(path_or_buf='../../../../import/has_sty.csv',
                   header=True,
                   index=False)
is_sty_of_rel.to_csv(path_or_buf='../../../../import/is_sty_of.csv',
                     header=True,
                     index=False)
print("is_sty_of.csv & has_sty.csv successfully written out...")
# **************************************************************
# has_umls_atom.csv
has_umls_aui = '''
SELECT DISTINCT (SAB || '#' || CODE) AS ":START_ID"
              , AUI                  AS ":END_ID"
              , 'HAS_UMLS_AUI'       AS ":TYPE"
FROM MRCONSO
WHERE SAB IN ('ATC', 'GO', 'HGNC', 'ICD9CM', 'ICD10CM',
              'ICD10PCS', 'MED-RT', 'NCI', 'RXNORM', 'SNOMEDCT_US')
  AND SUPPRESS = 'N';
  '''

has_umls_aui_rel = pd.read_sql_query(
    has_umls_aui, conn).drop_duplicates().replace(np.nan, "")

has_umls_aui_rel.to_csv(path_or_buf="../../../../import/has_umls_aui.csv",
                        header=True,
                        index=False)
print("has_umls_aui.csv successfully written out...")
# **************************************************************
# has_cui.csv
# Each umls_aui within UMLS has 1 distinct umls_cui -> umls_aui is primary key in UMLS.MRCONSO
# AUI -> CUI is a many:1 mapping
# CUI -> AUI is a 1:many mapping

# Since it is preferable in a graph model to specify direction & has_aui/has_cui semantically are same we will only create 1 relationship
# We will create (AUI) - [HAS_CUI] -> (CUI) as the ':END_ID' preferably should be distinct.
# Creation of both directions will not benefit query traversals but will just will create a redundant rel & require larger disk space

has_cui = '''
SELECT DISTINCT AUI
              , CUI
              , 'HAS_CUI' AS ":TYPE"
FROM MRCONSO
WHERE SAB IN ('ATC', 'GO', 'HGNC', 'ICD9CM', 'ICD10CM',
              'ICD10PCS', 'MED-RT', 'NCI', 'RXNORM', 'SNOMEDCT_US')
  AND SUPPRESS = 'N'
  AND LAT = 'ENG'
  AND ISPREF = 'Y'
  AND TS = 'P'
  AND STT = 'PF';
  '''

has_cui_rel = pd.read_sql_query(
    has_cui, conn).drop_duplicates().replace(np.nan, "")

has_cui_rel.columns = [":START_ID", ":END_ID", ":TYPE"]

has_cui_rel.to_csv(path_or_buf="../../../../import/has_cui.csv",
                   header=True,
                   index=False)
print("has_cui.csv successfully written out...")
# **************************************************************
# tui_tui_rel.csv
tui_tui = '''
SELECT DISTINCT s2.UI
              , s3.UI
              , s.RL
FROM SRSTR s
         INNER JOIN SRDEF s2 ON s.STY_RL1 = s2.STY_RL
         INNER JOIN SRDEF s3 ON s.STY_RL2 = s3.STY_RL
WHERE s2.UI IS NOT NULL
  AND s3.UI IS NOT NULL
  AND s2.STY_RL != s3.STY_RL
  AND s2.UI != s3.UI
  AND s2.RT = 'STY'
  AND s3.RT = 'STY';
  '''

tui_tui_rel_df = pd.read_sql_query(
    tui_tui, conn).drop_duplicates().replace(np.nan, "")

tui_tui_rel_df.columns = [":START_ID", ':END_ID', ":TYPE"]
tui_tui_rel = tui_tui_rel_df[tui_tui_rel_df[':START_ID'] != tui_tui_rel_df[':END_ID']].drop_duplicates(
).replace(np.nan, '')
tui_tui_rel[':TYPE'] = tui_tui_rel[':TYPE'].str.upper()

tui_tui_rel.to_csv(path_or_buf="../../../../import/tui_tui_rel.csv",
                   header=True,
                   index=False)
print("tui_tui_rel.csv successfully written out...")
# **************************************************************
# cui_cui_rel.csv

# We will filter out REL = 'SIB' as the relationship in UMLS does not provide much utility & will increase size of graph considerably
# UMLS.MRREL.RELA is sometimes NULL but UMLS.MRREL.REL & UMLS.MRREL.RELA cannot both be null (1 has to exist)
# CASE statement ensures that when RELA is NULL, :TYPE is assigned REL as its value
# 'vocab' assigned to be a property of the relationship (i.e. Concept -- Concept relationship can be filtered to the vocabulary for which the relationship exists)

cui_cui = """
WITH q AS (
    SELECT DISTINCT SAB
    FROM MRCONSO
    WHERE SAB IN (
                  'ATC',
                  'GO',
                  'HGNC',
                  'ICD9CM',
                  'ICD10CM',
                  'ICD10PCS',
                  'MED-RT',
                  'NCI',
                  'RXNORM',
                  'SNOMEDCT_US'
        )
      AND SUPPRESS = 'N'
)
SELECT DISTINCT r.CUI2
              , r.CUI1
              , CASE
                    WHEN r.RELA = ''
                        THEN r.REL
                    ELSE r.RELA END AS ":TYPE"
              , r.SAB               as "vocab"
FROM MRREL r
         INNER JOIN q ON r.SAB = q.SAB
WHERE r.SUPPRESS = 'N'
  AND r.REL != 'SIB';
  """

cui_cui_rel_df = pd.read_sql_query(cui_cui, conn)

cui_cui_rel_df.columns = [":START_ID", ":END_ID", ":TYPE", "vocab"]

# start_id should not equal end_id -> remove them & then drop duplicates and replace nan with ''
cui_cui_rel = cui_cui_rel_df[cui_cui_rel_df[':START_ID'] !=
                             cui_cui_rel_df[':END_ID']].drop_duplicates().replace(np.nan, "")

cui_cui_rel[":TYPE"] = cui_cui_rel[":TYPE"].str.upper()
cui_cui_rel[':TYPE'] = cui_cui_rel[':TYPE'].str.replace('-', '_')

cui_cui_rel.to_csv(path_or_buf="../../../../import/cui_cui_rel.csv",
                   header=True,
                   index=False)
print("cui_cui_rel.csv successfully written out...")
# **************************************************************
# cui_code_rel.csv
cui_code_rel = '''
SELECT DISTINCT CUI
              , (SAB || '#' || CODE)  AS ":END_ID"
              , 'HAS_SOURCE_CODE'     AS ":TYPE" 
FROM MRCONSO 
WHERE SUPPRESS = 'N' 
    AND SAB IN ('ATC', 'GO', 'HGNC', 'ICD9CM', 'ICD10CM', 'ICD10PCS', 
                'MED-RT', 'NCI', 'RXNORM', 'SNOMEDCT_US');
                '''

has_source_code = pd.read_sql_query(
    cui_code_rel, conn).drop_duplicates().replace(np.nan, '')

has_source_code.columns = [':START_ID', ':END_ID', ':TYPE']

has_source_code.to_csv(path_or_buf='../../../../import/cui_code_rel.csv',
                       header=True,
                       index=False)

# Keep a copy to use to add ICDO3 as vocab to codeNode.csv & a Concept --> Code mapping via has_source_code.csv
has_source_code_copy = has_source_code.copy()
print("cui_code_rel.csv successfully written out...")
# **************************************************************
icdo = '''
SELECT DISTINCT ATV
              , (SAB||'#'||CODE)
              , SAB
FROM MRSAT 
WHERE SAB = 'NCI' 
    AND ATN = 'ICD-O-3_CODE'
    AND SUPPRESS = 'N'
    AND ATV != '0000/0';
    '''

icdo_df = pd.read_sql_query(icdo, conn).drop_duplicates().replace(np.nan, '')

icdo_df.columns = ['code', ':END_ID', 'vocab']
icdo_df['vocab'] = 'ICDO3'
icdo_df['CodeId:ID'] = icdo_df['vocab'] + "#" + icdo_df['code']
icdo_df[':LABEL'] = ('Code' + ';' + icdo_df['vocab'])
icdo_df[['CodeId:ID', 'vocab', 'code', ':LABEL']].to_csv(path_or_buf='../../../../import/codeNode.csv',
                                                         mode='a',
                                                         header=False,
                                                         index=False)
cui_code_rel_icdo_append = icdo_df.merge(has_source_code_copy,
                                         how='inner',
                                         on=':END_ID')

cui_code_rel_icdo_append[':TYPE'] = 'HAS_SOURCE_CODE'
cui_code_rel_append = cui_code_rel_icdo_append[[':START_ID', 'CodeId:ID', ':TYPE']].rename(
    {'CodeId:ID': ':END_ID'}, axis=1).drop_duplicates().replace(np.nan, '')

cui_code_rel_append.to_csv(path_or_buf='../../../../import/cui_code_rel.csv',
                           mode='a',
                           header=False,
                           index=False)
# **************************************************************
# NOTE: Please run `python edges_part2.py` to ensure all nodes/edges have been accounted for prior to importing .csv data

# 'edges_part2.py' will create 1 .csv file containing all PARENT AUI (PAUI) --> AUI relationships and vocabularies. A CHILD_OF relationship at the atom level of UMLS.

# This requires exploding MRHIER.RRF to get all paths from 'root atom (top concept of) to atom' for all atoms & their associated context views.
# The script will create 1 .csv file named 'child_of.csv' for the edge 'CHILD_OF' i.e. -> (Atom)-[CHILD_OF]->(Atom)
