#!/bin/bash/env/python

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


def extract_nodes_edges():
    """
    Summary:
    --------

    Parameters:
    -----------

    Returns:
    --------

    """
    # Establish database connection using local SQLite
    db_name = "umls.db"
    db_dir = "../sqlite/"
    conn = sqlite3.connect(os.path.join(db_dir, db_name))

    # **************************************************************
    # GRAPH LABELS & NODES
    # **************************************************************

    # **************************************************************
    # GRAPH LABELS:
    # LABELS = ["SemanticType", "Code", "Atom", "Concept", "StringForm",
    #           "ATC", "GO", "HGNC", "ICD9CM", "ICD10CM", "ICD10PCS", "ICDO3",
    #           "LNC", "MDR", "MED-RT", "NCBI", "NCI", "RXNORM", "SNOMEDCT_US"]
    # **************************************************************

    # Label: SemanticType
    # Import: semanticTypeNode.csv
    semantic_node = """
    SELECT DISTINCT TUI
                  , STY
                  , STN  
                  , 'SemanticType'  as ":LABEL"
    FROM MRSTY;
    """

    semanticTypeNode = pd.read_sql_query(
        semantic_node, conn).drop_duplicates().replace(np.nan, "")

    semanticTypeNode.columns = ["SemanticTypeId:ID", "sty", "stn", ":LABEL"]

    semanticTypeNode.to_csv(path_or_buf="../../../../import/semanticTypeNode.csv",
                            header=True,
                            index=False)
    print("semanticTypeNode.csv successfully written out...")

    # **************************************************************
    # Label: Concept
    # Import: conceptNode.csv
    concept_node = """
    SELECT DISTINCT CUI
                  , 'Concept' AS ":LABEL"
    FROM MRCONSO
    WHERE SAB IN ('ATC', 'GO', 'HGNC', 'ICD9CM', 
                  'ICD10CM', 'ICD10PCS', 'LNC', 'MED-RT', 
                  'MDR', 'NCI', 'NCBI', 'RXNORM', 'SNOMEDCT_US')
        AND SUPPRESS = 'N'
        AND LAT = 'ENG';
        """

    conceptNode = pd.read_sql_query(
        concept_node, conn).drop_duplicates().replace(np.nan, '')

    conceptNode.columns = ["ConceptId:ID", ":LABEL"]

    conceptNode.to_csv(path_or_buf="../../../../import/conceptNode.csv",
                       header=True,
                       index=False)
    print("conceptNode.csv successfully written out...")
    # **************************************************************
    # Label: StringForm
    # Import: stringNode.csv
    string_node = """
    SELECT DISTINCT SUI
                  , STR
                  , 'StringForm' AS ":LABEL"
    FROM MRCONSO 
    WHERE SAB IN ('ATC', 'GO', 'HGNC', 'ICD9CM', 
                  'ICD10CM', 'ICD10PCS', 'LNC', 'MED-RT', 
                  'MDR', 'NCI', 'NCBI', 'RXNORM', 'SNOMEDCT_US') 
        AND SUPPRESS = 'N' 
        AND LAT = 'ENG';
        """
    stringNode = pd.read_sql_query(
        string_node, conn).drop_duplicates().replace(np.nan, "")
    stringNode.columns = ["StringFormId:ID", "name", ":LABEL"]
    stringNode.to_csv(path_or_buf='../../../../import/stringNode.csv',
                      header=True,
                      index=False)
    print("stringNode.csv successfully written out...")
    # **************************************************************
    # Label: Atom
    # Import: atomNode.csv
    atom_node = """
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
    WHERE SAB IN ('ATC', 'GO', 'HGNC', 'ICD9CM', 
                  'ICD10CM', 'ICD10PCS', 'LNC', 'MED-RT', 
                  'MDR', 'NCI', 'NCBI', 'RXNORM', 'SNOMEDCT_US')
        AND SUPPRESS = 'N'
        AND LAT = 'ENG';
        """

    atomNode = pd.read_sql_query(atom_node, conn).drop_duplicates(
        subset=['AUI']).replace(np.nan, "")

    atomNode.columns = ["AtomId:ID", "name", "vocab", "code",
                        "tty", "isPref", "ts", "stt", ":LABEL"]

    atomNode.to_csv(path_or_buf="../../../../import/atomNode.csv",
                    header=True,
                    index=False)
    print("atomNode.csv successfully written out...")
    # **************************************************************
    # Label: Code
    # Import: codeNode.csv
    code = """
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
    WHERE SAB IN ('ATC', 'GO', 'HGNC', 'ICD9CM', 
                  'ICD10CM', 'ICD10PCS', 'LNC', 'MED-RT', 
                  'MDR', 'NCI', 'NCBI', 'RXNORM', 'SNOMEDCT_US')
        AND MRCONSO.SUPPRESS = 'N';
        """
    codeNode = pd.read_sql_query(code, conn).drop_duplicates().replace(
        np.nan, '')
    codeNode.columns = ['SourceCodeId:ID', 'vocab', 'code', ':LABEL']
    codeNode.to_csv(path_or_buf="../../../../import/codeNode.csv",
                    header=True,
                    index=False)
    print("codeNode.csv successfully written out...")
    # **************************************************************
    # GRAPH EDGES/RELATIONSHIPS
    # **************************************************************
    # has_sty.csv
    has_sty = """
    SELECT DISTINCT CUI
                  , TUI
                  , 'HAS_STY' AS ":TYPE" 
    FROM MRSTY;
    """

    has_sty_rel = pd.read_sql_query(
        has_sty, conn).drop_duplicates().replace(np.nan, '')

    has_sty_rel.columns = [':START_ID', ':END_ID', ':TYPE']

    has_sty_rel.to_csv(path_or_buf="../../../../import/has_sty.csv",
                       header=True,
                       index=False)
    print("has_sty.csv successfully written out...")
    # **************************************************************
    # import: code_string_rel.csv
    string_code = """
    SELECT DISTINCT c.SUI
                  , (c.SAB || '#' || c.CODE)
                  , c.TTY
    FROM mrrank rank
       , mrconso c
    WHERE c.SAB IN ('ATC', 'GO', 'HGNC', 'ICD9CM', 
                    'ICD10CM', 'ICD10PCS', 'LNC', 'MED-RT', 
                    'MDR', 'NCI', 'NCBI', 'RXNORM', 'SNOMEDCT_US')
        AND c.TTY NOT IN ('CCS', 'MTH_OS', 'XM', 'MTH_SYGB', 'SB', 
                          'PTGB', 'SYGB', 'MTH_LN', 'MTH_PTGB', 
                          'MTH_FN', 'MTH_SMQ', 'MTH_HX', 'MTH_HG', 
                          'MTH_HT', 'MTH_LLT', 'MTH_CN', 'MTH_ACR', 
                          'MTH_ET', 'MTH_PT', 'MTH_SY')
        AND c.SAB = rank.SAB
        AND c.TTY = rank.TTY
        AND c.SUPPRESS = rank.SUPPRESS
        AND c.LAT = 'ENG';
        """
    code_string_rel = pd.read_sql_query(
        string_code, conn).drop_duplicates().replace(np.nan, "")
    code_string_rel.columns = [':END_ID', ':START_ID', ':TYPE']
    code_string_rel.to_csv(path_or_buf='../../../../import/code_string_rel.csv',
                           header=True,
                           index=False)
    print("code_string_rel.csv successfully written out...")
    # **************************************************************
    # import: concept_string_rel.csv
    concept_string = """
    SELECT DISTINCT CUI
                  , SUI
                  , 'HAS_LABEL' AS ":TYPE" 
    FROM MRCONSO 
    WHERE SAB IN ('ATC', 'GO', 'HGNC', 'ICD9CM', 
                  'ICD10CM', 'ICD10PCS', 'LNC', 'MED-RT', 
                  'MDR', 'NCI', 'NCBI', 'RXNORM', 'SNOMEDCT_US')
        AND SUPPRESS = 'N'
        AND ISPREF = 'Y' 
        AND STT = 'PF' 
        AND TS = 'P' 
        AND LAT = 'ENG';
        """
    concept_string_rel = pd.read_sql_query(
        concept_string, conn).drop_duplicates().replace(np.nan, "")
    concept_string_rel.columns = [":START_ID", ":END_ID", ":TYPE"]
    concept_string_rel.to_csv(path_or_buf='../../../../import/concept_string_rel.csv',
                              header=True,
                              index=False)
    print("concept_string_rel.csv successfully written out...")
    # **************************************************************
    # import: has_umls_atom.csv
    has_umls_aui = """
    SELECT DISTINCT (SAB || '#' || CODE) AS ":START_ID"
                  , AUI                  AS ":END_ID"
                  , 'HAS_UMLS_AUI'       AS ":TYPE"
    FROM MRCONSO
    WHERE SAB IN ('ATC', 'GO', 'HGNC', 'ICD9CM', 
                  'ICD10CM', 'ICD10PCS', 'LNC', 'MED-RT', 
                  'MDR', 'NCI', 'NCBI', 'RXNORM', 'SNOMEDCT_US')
        AND SUPPRESS = 'N'
        AND LAT = 'ENG';
        """

    has_umls_aui_rel = pd.read_sql_query(
        has_umls_aui, conn).drop_duplicates().replace(np.nan, "")

    has_umls_aui_rel.to_csv(path_or_buf="../../../../import/has_umls_aui.csv",
                            header=True,
                            index=False)
    print("has_umls_aui.csv successfully written out...")
    # **************************************************************
    # has_string.csv
    # Each umls_aui within UMLS maps to a single umls_cui (umls_aui is primary key in UMLS.MRCONSO)
    # Each row of UMLS.MRCONSO represents each UMLS Atom (AUI) -> 1 Atom (AUI) can only map to a single UMLS Concept (CUI).
    # Furthermore, each UMLS Concept (CUI) is not limited to mapping to >=1 UMLS Atom (AUI)
    # AUI -> CUI mapping/relationship -> *including this* as both directions in the graph is not required and AUI -> CUI mapping preserves distinct source side of relationship

    # It is preferable in a graph model to specify direction only when direction has a semantic meaning (i.e. forward doesn't imply backward)
    # Since 'has_string' implies 'HAS_AUI' (inverse) -> there is minimal/no value in including both 'has_string' & 'HAS_AUI'.
    # --> Adding only 'has_string' (AUI)-[has_string]->(CUI) OR exact cypher being: `(Atom)-[:has_string]->(Concept)`

    has_concept = """
    SELECT DISTINCT AUI
                  , CUI
                  , 'HAS_CUI' AS ":TYPE" 
    FROM MRCONSO 
    WHERE SAB IN ('ATC', 'GO', 'HGNC', 'ICD9CM', 
                'ICD10CM', 'ICD10PCS', 'LNC', 'MED-RT', 
                'MDR', 'NCI', 'NCBI', 'RXNORM', 'SNOMEDCT_US')
        AND SUPPRESS = 'N'
        AND LAT = 'ENG';
        """
    has_concept_rel = pd.read_sql_query(
        has_concept, conn).drop_duplicates().replace(np.nan, '')
    has_concept_rel.columns = [":START_ID", ":END_ID", ":TYPE"]

    has_concept_rel.to_csv(path_or_buf="../../../../import/has_concept_rel.csv",
                           header=True,
                           index=False)
    print("has_concept_rel.csv successfully written out...")
    # **************************************************************
    # tui_tui_rel.csv
    tui_tui = """
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
        """

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
    # concept_concept_rel.csv

    # We will filter out REL = 'SIB' as the relationship in UMLS does not provide much utility & will increase size of graph considerably
    # UMLS.MRREL.RELA is sometimes NULL but UMLS.MRREL.REL & UMLS.MRREL.RELA cannot both be null (1 has to exist)
    # CASE statement ensures that when RELA is NULL, :TYPE is assigned REL as its value
    # 'vocab' assigned to be a property of the relationship (i.e. Concept -- Concept relationship can be filtered to the vocabulary for which the relationship exists)

    concept_concept = """
    WITH q AS (
        SELECT DISTINCT SAB
        FROM MRCONSO
        WHERE SAB IN ('ATC', 'GO', 'HGNC', 'ICD9CM', 
                      'ICD10CM', 'ICD10PCS', 'LNC', 'MED-RT', 
                      'MDR', 'NCI', 'NCBI', 'RXNORM', 'SNOMEDCT_US')
            AND SUPPRESS = 'N'
            AND LAT = 'ENG')
    SELECT DISTINCT r.CUI2
                  , r.CUI1
                  , CASE
                        WHEN r.RELA = ''
                            THEN r.REL
                        ELSE r.RELA END AS ":TYPE"
                  , r.SAB               AS "vocab"
    FROM MRREL r
            INNER JOIN q ON r.SAB = q.SAB
    WHERE r.SUPPRESS = 'N'
        AND r.REL != 'SIB';
    """

    concept_concept_rel_df = pd.read_sql_query(concept_concept, conn)

    concept_concept_rel_df.columns = [":START_ID", ":END_ID", ":TYPE", "vocab"]

    # start_id should not equal end_id -> remove them & then drop duplicates and replace nan with ''
    concept_concept_rel = concept_concept_rel_df[concept_concept_rel_df[':START_ID'] !=
                                                 concept_concept_rel_df[':END_ID']].drop_duplicates().replace(np.nan, "")

    concept_concept_rel[":TYPE"] = concept_concept_rel[":TYPE"].str.upper()
    concept_concept_rel[':TYPE'] = concept_concept_rel[':TYPE'].str.replace(
        '-', '_')

    concept_concept_rel.to_csv(path_or_buf="../../../../import/concept_concept_rel.csv",
                               header=True,
                               index=False)
    print("concept_concept_rel.csv successfully written out...")
    # **************************************************************
    # cui_code_rel.csv
    cui_code_rel = """
    SELECT DISTINCT CUI
                  , (SAB || '#' || CODE)  AS ":END_ID"
                  , 'HAS_SOURCE_CODE'     AS ":TYPE" 
    FROM MRCONSO 
    WHERE SUPPRESS = 'N' 
        AND SAB IN ('ATC', 'GO', 'HGNC', 'ICD9CM', 
                    'ICD10CM', 'ICD10PCS', 'LNC', 'MED-RT', 
                    'MDR', 'NCI', 'NCBI', 'RXNORM', 'SNOMEDCT_US')
        AND LAT = 'ENG';
        """

    has_source_code = pd.read_sql_query(
        cui_code_rel, conn).drop_duplicates().replace(np.nan, '')

    has_source_code.columns = [':START_ID', ':END_ID', ':TYPE']

    has_source_code.to_csv(path_or_buf="../../../../import/cui_code_rel.csv",
                           header=True,
                           index=False)

    # Keep a copy to use to add ICDO3 as vocab to codeNode.csv & a Concept --> Code mapping via has_source_code.csv
    has_source_code_copy = has_source_code.copy()
    print("cui_code_rel.csv successfully written out...")
    # **************************************************************
    # Append both codeNode.csv & cui_code_rel.csv w/ ICDO3 Topography & Morphology Codes that are attributes of NCI Thesaurus (NCI)
    # to do: Incorporate all of ICDO3 via its native release and not UMLS. UMLS is not complete (~90% complete).
    icdo = """
    SELECT DISTINCT ATV
                  , (SAB||'#'||CODE)
                  , SAB
    FROM MRSAT 
    WHERE SAB = 'NCI' 
        AND ATN = 'ICD-O-3_CODE'
        AND SUPPRESS = 'N'
        AND ATV != '0000/0';
        """

    icdo_df = pd.read_sql_query(
        icdo, conn).drop_duplicates().replace(np.nan, '')

    icdo_df.columns = ['code', ':END_ID', 'vocab']
    icdo_df['vocab'] = 'ICDO3'
    icdo_df['CodeId:ID'] = icdo_df['vocab'] + "#" + icdo_df['code']
    icdo_df[':LABEL'] = ('Code' + ';' + icdo_df['vocab'])
    icdo_df[['CodeId:ID', 'vocab', 'code', ':LABEL']].to_csv(path_or_buf="../../../../import/codeNode.csv",
                                                             mode='a',
                                                             header=False,
                                                             index=False)
    cui_code_rel_icdo_append = icdo_df.merge(has_source_code_copy,
                                             how='inner',
                                             on=':END_ID')

    cui_code_rel_icdo_append[':TYPE'] = 'HAS_SOURCE_CODE'
    cui_code_rel_append = cui_code_rel_icdo_append[[':START_ID', 'CodeId:ID', ':TYPE']].rename(
        {'CodeId:ID': ':END_ID'}, axis=1).drop_duplicates().replace(np.nan, '')

    cui_code_rel_append.to_csv(path_or_buf="../../../../import/cui_code_rel.csv",
                               mode='a',
                               header=False,
                               index=False)
    # **************************************************************
    # child_of_rel.csv -> alternative option to running edges_part2.py
    child_of = """
    SELECT DISTINCT h.PAUI     AS PAUI
                  , c.AUI      AS AUI2
                  , 'CHILD_OF' AS ":TYPE"
    FROM MRHIER h
            JOIN MRCONSO c ON h.AUI = c.AUI
            JOIN MRCONSO c2 ON h.PAUI = c2.AUI
    WHERE h.SAB IN ('ATC', 'GO', 'HGNC', 'ICD9CM', 
                    'ICD10CM', 'ICD10PCS', 'LNC', 'MED-RT', 
                    'MDR', 'NCI', 'NCBI', 'RXNORM', 'SNOMEDCT_US')
        AND c.SUPPRESS = 'N'
        AND c2.SUPPRESS = 'N'
        AND c.LAT = 'ENG'
        AND c2.LAT = 'ENG'
        AND c.CODE != c2.CODE;
        """

    child_of_rel = pd.read_sql_query(child_of, conn)

    child_of_rel.columns = [":START_ID", ":END_ID", ":TYPE"]

    # start_id should not equal end_id -> remove them & then drop duplicates and replace nan with ''
    child_of_rel = child_of_rel[child_of_rel[':START_ID'] !=
                                child_of_rel[':END_ID']].drop_duplicates().replace(np.nan, "")

    child_of_rel.to_csv(path_or_buf="../../../../import/child_of_rel.csv",
                        header=True,
                        index=False)
    print("child_of_rel.csv successfully written out...")


    # **************************************************************
extract_nodes_edges()

################################################################
# NOTE: Do not include both output of `edges_part2.py` and the last output .csv via this .py. Both are redundant but one or other should be included.
################################################################
