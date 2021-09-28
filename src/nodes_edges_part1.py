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
# LABELS = ["SemanticType", "Code", "Atom", "Concept", "Attribute",
#           "ATC", "GO", "HGNC", "ICD9CM", "ICD10CM", "ICD10PCS",
#           "ICDO3", "MED-RT", "NCI", "NDC", "RXNORM", "SNOMEDCT_US"]
# **************************************************************
# Label: SemanticType
# import: semanticsNode.csv
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

semanticTypeNode.to_csv(path_or_buf="./import/SemanticTypeNode.csv",
                        header=True,
                        index=False)
print("SemanticTypeNode.csv successfully written out...")
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
                     AND SAB IN
                         ('ATC', 'GO', 'HGNC', 'ICD9CM', 'ICD10CM',
                          'ICD10PCS', 'MED-RT', 'NCI', 'RXNORM', 'SNOMEDCT_US');
                          '''

conceptNode = pd.read_sql_query(
    concept_node, conn).drop_duplicates().replace(np.nan, '')

conceptNode.columns = ["ConceptId:ID", "name", ":LABEL"]

conceptNode.to_csv(path_or_buf='./import/conceptNode.csv',
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
                            , 'Atom'                 AS ":LABEL"
              FROM MRCONSO 
              WHERE SAB IN ('ATC', 'GO', 'HGNC', 'ICD9CM', 'ICD10CM',
                            'ICD10PCS', 'MED-RT', 'NCI', 'RXNORM', 'SNOMEDCT_US')
                  AND SUPPRESS = 'N';
                  '''

atomNode = pd.read_sql_query(atom_node, conn).drop_duplicates(
    subset=['AUI']).replace(np.nan, "")

atomNode.columns = ["AtomId:ID", "name", "vocab",
                    "code", "tty", "ispref", "ts", "stt", ":LABEL"]

atomNode.to_csv(path_or_buf="./import/atomNode.csv",
                header=True,
                index=False)
print("atomNode.csv successfully written out...")
# **************************************************************
# Label: Code
# import: codeNode.csv
code_node = '''
              WITH query AS (SELECT DISTINCT CUI
                             FROM MRCONSO
                             WHERE ISPREF = 'Y'
                                AND STT = 'PF'
                                AND TS = 'P'
                                AND SUPPRESS = 'N')
              SELECT DISTINCT (SAB || '#' || CODE) AS "CodeId:ID"
                            , SAB
                            , CODE
                            , ( 'Code' || ';'| SAB ) AS ":LABEL"
              FROM MRCONSO con
                    INNER JOIN QUERY ON con.CUI = query.CUI
              WHERE  SAB IN ('ATC', 'GO', 'HGNC', 'ICD9CM',
                             'ICD10CM', 'ICD10PCS', 'MED-RT', 'NCI',
                             'RXNORM', 'SNOMEDCT_US' )
                AND SUPPRESS = 'N';
                '''
codeNode = pd.read_sql_query(code_node, conn).drop_duplicates(
    ["CodeId:ID"]).replace(np.nan, "")

codeNode.columns = ["CodeId:ID", "vocab", "code", ":LABEL"]

codeNode.to_csv(path_or_buf="./import/codeNode.csv",
                header=True,
                index=False)
print("codeNode.csv successfully written out...")
# **************************************************************
# Labels: ['ICDO3', 'NDC']
# import: attributeNode.csv
atui_node = '''
               SELECT DISTINCT ATUI                                    
                             , ATV                                    
                             , CASE
                                   WHEN ('Attribute' || ';' || ATN) = 'Attribute;ICD-O-3_CODE'
                                       THEN 'Attribute;ICDO3'
                                    WHEN ('Attribute' || ';' || ATN) = 'Attribute;NDC'
                                        THEN 'Attribute;NDC'
                                    ELSE ('Attribute' || ';' || ATN) END AS ":LABEL"
               FROM MRSAT s
                       JOIN MRCONSO c ON s.CUI = c.CUI
               WHERE ATN IN ('ICD-O-3_CODE', 'NDC')
               AND s.SUPPRESS = 'N'
               AND s.SAB IN ('ATC', 'GO', 'HGNC', 'ICD9CM', 'ICD10CM', 
                             'ICD10PCS', 'MED-RT','NCI', 'RXNORM', 'SNOMEDCT_US')
               AND c.SUPPRESS = 'N'
               AND c.STT = 'PF'
               AND c.ISPREF = 'Y'
               AND c.TS = 'P';
               '''

attributeNode = pd.read_sql_query(atui_node, conn).drop_duplicates().replace(
    np.nan, "")

attributeNode.columns = ['AttributeId:ID', 'attribute', ':LABEL']

attributeNode.to_csv(path_or_buf="./import/attributeNode.csv",
                     header=True,
                     index=False)
print("attributeNode.csv successfully written out...")
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

has_sty_rel.to_csv(path_or_buf='./import/has_sty.csv',
                   header=True,
                   index=False)
is_sty_of_rel.to_csv(path_or_buf='./import/is_sty_of.csv',
                     header=True,
                     index=False)
print("is_sty_of.csv & has_sty.csv successfully written out...")
# **************************************************************
# has_umls_atom.csv
has_umls_aui = '''
                 SELECT DISTINCT (SAB || '#' || CODE)    AS ":START_ID"
                                , AUI                    AS ":END_ID"
                                , 'HAS_UMLS_AUI'         AS ":TYPE"
                 FROM MRCONSO
                 WHERE SAB IN ('ATC', 'GO', 'HGNC', 'ICD9CM', 'ICD10CM', 
                               'ICD10PCS', 'MED-RT','NCI', 'RXNORM', 'SNOMEDCT_US')
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
has_cui = '''
            SELECT DISTINCT AUI  
                          , CUI      
                          , 'HAS_CUI'     AS ":TYPE"
            FROM MRCONSO
            WHERE SAB IN ('ATC', 'GO', 'HGNC', 'ICD9CM', 'ICD10CM', 
                          'ICD10PCS', 'MED-RT','NCI', 'RXNORM', 'SNOMEDCT_US')
                 AND SUPPRESS = 'N'
                 AND ISPREF = 'Y'
                 AND TS = 'P'
                 AND STT = 'PF';
                 '''

has_cui_rel = pd.read_sql_query(
    has_cui, conn).drop_duplicates().replace(np.nan, "")

has_cui_rel.columns = [":START_ID", ":END_ID", ":TYPE"]

has_cui_rel.to_csv(path_or_buf="./import/has_cui.csv",
                   header=True,
                   index=False)
print("has_cui.csv successfully written out...")
# **************************************************************
# has_aui.csv
has_aui = '''
            SELECT DISTINCT CUI  
                          , AUI      
                          , 'HAS_AUI'     AS ":TYPE"
            FROM MRCONSO
            WHERE SAB IN ('ATC', 'GO', 'HGNC', 'ICD9CM', 'ICD10CM', 
                          'ICD10PCS', 'MED-RT','NCI', 'RXNORM', 'SNOMEDCT_US')
                 AND SUPPRESS = 'N';
                 '''

has_aui_rel = pd.read_sql_query(
    has_aui, conn).drop_duplicates().replace(np.nan, "")

has_aui_rel.columns = [':START_ID', ':END_ID', ':TYPE']

has_aui_rel.to_csv(path_or_buf='./import/has_aui.csv',
                   header=True,
                   index=False)
print("has_aui.csv successfully written out...")
# **************************************************************
# code_has_attribute.csv
has_attr = '''
              SELECT DISTINCT ATUI                            AS ":END_ID"
                            , (SAB || '#' || CODE)            AS ":START_ID"
                            , CASE 
                               WHEN ATN = 'ICD-O-3_CODE' 
                                   THEN 'HAS_ICDO3_ATTRIBUTE'
                                WHEN ATN = 'NDC'
                                    THEN 'HAS_NDC_ATTRIBUTE'
                                ELSE ATN END                  AS ":TYPE"
              FROM MRSAT
              WHERE SAB IN ('ATC', 'GO', 'HGNC', 'ICD9CM', 'ICD10CM', 
                            'ICD10PCS', 'MED-RT','NCI', 'RXNORM', 'SNOMEDCT_US')
                  AND ATN IN ('ICD-O-3_CODE', 'NDC')
                  AND SUPPRESS = 'N';
                  '''

code_has_attribute = pd.read_sql_query(
    has_attr, conn).drop_duplicates().replace(np.nan, "")

code_has_attribute.columns = [":END_ID", ":START_ID", ":TYPE"]

code_has_attribute.to_csv(path_or_buf="./import/code_has_attribute.csv",
                          header=True,
                          index=False)
print("code_has_attribute.csv successfully written out...")
# **************************************************************
# tui_tui_rel.csv
tui_tui_rel = '''
                 WITH srdef_query AS (SELECT DISTINCT UI
                                      FROM SRDEF
                                      WHERE RT = 'STY')
                 SELECT DISTINCT UI3                    AS ":END_ID"
                               , UI1                    AS ":START_ID"
                               , 'STY_ISA'              AS ":TYPE"
                 FROM SRSTRE1
                         INNER JOIN srdef_query ON UI1 = srdef_query.UI
                 WHERE UI2 = 'T186';
                 '''

tui_tui_rel_df = pd.read_sql_query(
    tui_tui_rel, conn).drop_duplicates().replace(np.nan, "")

tui_tui_rel_df.columns = [":END_ID", ":START_ID", ":TYPE"]

tui_tui_rel_df.to_csv(path_or_buf="./import/tui_tui_rel.csv",
                      header=True,
                      index=False)
print("tui_tui_rel.csv successfully written out...")
# **************************************************************
# #cui_cui_rel.csv
cui_cui_rel = '''
                WITH query AS (
                    SELECT DISTINCT SAB
                    FROM MRCONSO
                    WHERE SUPPRESS = 'N'
                        AND SAB IN (
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
                )
                SELECT DISTINCT CUI2,
                    CUI1,
                    CASE
                        WHEN RELA = '' THEN REL
                        ELSE RELA
                    END AS ":TYPE",
                    MRREL.SAB
                FROM MRREL
                    INNER JOIN query ON MRREL.SAB = query.SAB
                WHERE SUPPRESS = 'N'
                    AND CUI1 != CUI2
                    AND REL NOT IN ('SIB', 'SY');
                    '''

cui_cui_rel_df = pd.read_sql_query(cui_cui_rel, conn)

cui_cui_rel_df.columns = [':START_ID', ':END_ID', ':TYPE']

cui_cui_rel_df = cui_cui_rel_df[cui_cui_rel_df[':START_ID'] !=
                                cui_cui_rel_df[':END_ID']].drop_duplicates().replace(np.nan, "")

cui_cui_rel_df[":TYPE"] = cui_cui_rel_df[":TYPE"].str.upper()

cui_cui_rel_df.to_csv(path_or_buf="./import/cui_cui_rel.csv",
                      header=True,
                      index=False)
cui_cui_rel_copy = cui_cui_rel_df.copy()
print("cui_cui_rel.csv successfully written out...")
# **************************************************************
cui_code_rel = '''
                 SELECT DISTINCT CUI, (SAB || '#' || CODE), 'HAS_SOURCE_CODE' AS ":TYPE" 
                 FROM MRCONSO 
                 WHERE SUPPRESS = 'N' 
                     AND SAB IN ('ATC', 'GO', 'HGNC', 'ICD9CM', 'ICD10CM', 'ICD10PCS', 
                                 'MED-RT', 'NCI', 'RXNORM', 'SNOMEDCT_US');
                                 '''

has_source_code = pd.read_sql_query(
    cui_code_rel, conn).drop_duplicates().replace(np.nan, '')

has_source_code.columns = [':START_ID', ':END_ID', ':TYPE']

has_source_code.to_csv(path_or_buf='./import/cui_code_rel.csv',
                       header=True,
                       index=False)

# Keep a copy to use to add ICDO3 & NDC Attributes
has_source_code_copy = has_source_code.copy()
print("cui_code_rel.csv successfully written out...")
# **************************************************************
query = '''
           SELECT DISTINCT ATV
                         , (SAB||'#'||CODE)
                         , CASE
                            WHEN SAB = 'NCI'
                                THEN SAB = 'ICDO3'
                            WHEN SAB = 'RXNORM
           FROM MRSAT 
           WHERE SAB = 'NCI' 
               AND ATN IN ('ICD-O-3_CODE') 
               AND SUPPRESS = 'N'
               AND ATV != '0000/0';
               '''
               
df = pd.read_sql_query(query, conn).drop_duplicates().replace(
    np.nan, '').sort_values('ATV')

df.columns = ['code', ':END_ID', 'vocab']
df['vocab'] = 'ICDO3'
df['CodeId:ID'] = df['SAB'] + "#" + df['CODE']
df[':LABEL'] = ('Code' + ';' + df['vocab'])
df[['CodeId:ID', 'vocab', 'code', ':LABEL']].to_csv(path_or_buf='./import/codeNode.csv', mode='a', header=False, index=False)

df = df.merge(has_source_code_copy, how='inner', on=':END_ID')
df[':TYPE'] = 'HAS_SOURCE_CODE'
df = df[[':START_ID', 'CodeId:ID', ':TYPE']].rename(
    {'CodeId:ID': ':END_ID'}, axis=1).drop_duplicates().replace(np.nan, '')

df.to_csv(path_or_buf='./import/cui_code_rel.csv',
          mode='a',
          header=False,
          index=False)

# NOTE: Please run `python edges_part2.py` to ensure all nodes/edges have been accounted for prior to importing .csv data
# --> 'edges_part2.py' will create all PARENT AUI (PAUI) --> AUI relationships for all vocabularies included in the graph. This requires exploding MRHIER.RRF to get all 'paths to root' for all atoms & their associated context views (for provided vocabularies). This script will create 1 .csv file named 'paui_of.csv' for the edge 'PAUI_OF' (AKA PARENT_AUI_OF).
