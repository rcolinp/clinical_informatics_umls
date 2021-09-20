"""
SUMMARY
-------

This .py assumes you are querying the SQLite database found at the relative path ->../sqlite/umls.db. 
This database is created via the following shell script located within that same directory. -->..sqlite/create_sqlite_db.sh.
  --> invoke that shell script via `sh create_sqlite_db_.sh ../UMLS/subset/2021AA` (where the path argument is path to local .RRF files) 

The sqlite3 database created contains two tables not created via UMLS® MetamorphoSys. 

The two additional tables are as follows: [hierarchy, lookup]. 
    -> This optimization reduces dependency of several expensive joins on a couple of the larger tables in the db.
    -> [MRHIER, MRCONSO, MRSTY]. Please note this will require more local disk space. (tables are not required) 

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
semanticTypeNode.to_csv(path_or_buf="../../../../import/SemanticTypeNode.csv",
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
                  WHERE SAB IN ('ATC', 'GO', 'HGNC', 'HPO', 'ICD10CM', 
                                'ICD10PCS', 'LNC', 'MDR', 'MED-RT', 'MSH', 
                                'NCBI', 'NCI', 'OMIM', 'PDQ', 'RXNORM', 
                                'SNOMEDCT_US', 'SRC')
                      AND SUPPRESS = 'N'
                      AND ISPREF = 'Y'
                      AND TS = 'P'
                      AND STT = 'PF';
                      '''
conceptNode = pd.read_sql_query(
    concept_node, conn).drop_duplicates().replace(np.nan, "")
conceptNode.columns = ["ConceptId:ID", "name", ":LABEL"]
conceptNode.to_csv(path_or_buf="../../../../import/conceptNode.csv",
                   header=True,
                   index=False)
print("conceptNode.csv successfully written out...")
# **************************************************************
# Label: Atom
# import: atomNode.csv
atom_node = '''
              SELECT DISTINCT AUI                    AS "AtomId:ID"
                            , STR                    
                            , SAB                    
                            , TTY                    
                            , ISPREF             
                            , TS                     
                            , 'Atom'                 AS ":LABEL"
              FROM MRCONSO 
              WHERE SAB IN ('ATC', 'GO', 'HGNC', 'HPO', 'ICD10CM', 
                            'ICD10PCS', 'LNC', 'MDR', 'MED-RT', 'MSH', 
                            'NCBI', 'NCI', 'OMIM', 'PDQ', 'RXNORM', 
                            'SNOMEDCT_US', 'SRC')
                  AND SUPPRESS = 'N';
                  '''
atomNode = pd.read_sql_query(atom_node, conn).drop_duplicates(
    subset=['AtomId:ID']).replace(np.nan, "")
atomNode.columns = ["AtomId:ID", "name",
                    "vocab", "tty", "isPref", "ts", ":LABEL"]
atomNode.to_csv(path_or_buf="../../../../import/atomNode.csv",
                header=True,
                index=False)
print("atomNode.csv successfully written out...")
# **************************************************************
# Label: Code
# import: codeNode.csv
code_node = '''
                WITH filter_cuis AS 
                        (SELECT DISTINCT CUI
                         FROM MRCONSO 
                         WHERE SAB IN ('ATC', 'GO', 'HGNC', 'HPO', 'ICD10CM', 
                                       'ICD10PCS', 'LNC', 'MDR', 'MED-RT', 'MSH', 
                                       'NCBI', 'NCI', 'OMIM', 'PDQ', 'RXNORM', 
                                       'SNOMEDCT_US', 'SRC')
                             AND ISPREF = 'Y' 
                             AND STT = 'PF' 
                             AND TS = 'P' 
                             AND SUPPRESS = 'N') 
                SELECT DISTINCT (SAB || '#' || CODE) AS "SourceCodeId:ID"
                              , STR 
                              , SAB
                              , CODE
                              , ('SourceCode' || ';' || SAB) AS ":LABEL"
                FROM MRCONSO 
                        INNER JOIN filter_cuis ON MRCONSO.CUI = filter_cuis.CUI
                WHERE SAB IN ('ATC', 'GO', 'HGNC', 'HPO', 'ICD10CM', 
                              'ICD10PCS', 'LNC', 'MDR', 'MED-RT', 'MSH', 
                              'NCBI', 'NCI', 'OMIM', 'PDQ', 'RXNORM', 
                              'SNOMEDCT_US', 'SRC')
                    AND SUPPRESS = 'N';
                    '''
codeNode = pd.read_sql_query(code_node, conn).drop_duplicates(
    ["SourceCodeId:ID"]).replace(np.nan, "")
codeNode.columns = ["SourceCodeId:ID", "name", "vocab", "code", ":LABEL"]
codeNode.to_csv(path_or_buf="../../../../import/codeNode.csv",
                header=True,
                index=False)
print("codeNode.csv successfully written out...")
# **************************************************************
# Labels: ['ICDO3', 'ENSEMBL', 'ENTREZ', 'NDC']
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
               AND s.SAB IN ('ATC', 'GO', 'HGNC', 'HPO', 'ICD10CM', 
                             'ICD10PCS', 'LNC', 'MDR', 'MED-RT', 'MSH', 
                             'NCBI', 'NCI', 'OMIM', 'PDQ', 'RXNORM', 
                             'SNOMEDCT_US', 'SRC')
               AND c.SUPPRESS = 'N'
               AND c.STT = 'PF'
               AND c.ISPREF = 'Y'
               AND c.TS = 'P';
               '''
attributeNode = pd.read_sql_query(atui_node, conn).drop_duplicates().replace(
    np.nan, "")
attributeNode.columns = ['AttributeId:ID', 'attribute', ':LABEL']
attributeNode.to_csv(path_or_buf="../../../../import/attributeNode.csv",
                     header=True,
                     index=False)
print("attributeNode.csv successfully written out...")

# **************************************************************
# GRAPH EDGES/RELATIONSHIPS
# **************************************************************
# has_sty.csv & sty_of.csv
has_sty_rel = '''
                SELECT DISTINCT s.CUI          AS ":START_ID"
                              , s.TUI          AS ":END_ID"
                              , 'HAS_STY'      AS ":TYPE"
                FROM MRSTY s
                         JOIN MRCONSO c ON s.CUI = c.CUI
                WHERE c.SAB IN ('ATC', 'GO', 'HGNC', 'HPO', 'ICD10CM', 
                                'ICD10PCS', 'LNC', 'MDR', 'MED-RT', 'MSH', 
                                'NCBI', 'NCI', 'OMIM', 'PDQ', 'RXNORM', 
                                'SNOMEDCT_US', 'SRC')
                    AND c.SUPPRESS = 'N'
                    AND c.ISPREF = 'Y'
                    AND c.TS = 'P'
                    AND c.STT = 'PF';
                    '''
has_sty = pd.read_sql_query(
    has_sty_rel, conn).drop_duplicates().replace(np.nan, "")
has_sty.to_csv(path_or_buf='../../../../import/has_sty.csv',
               header=True,
               index=False)
is_sty_of = has_sty[[':END_ID', ':START_ID', ':TYPE']]
is_sty_of[':TYPE'] = 'IS_STY_OF'
is_sty_of.columns = [':START_ID', ':END_ID', ':TYPE']
is_sty_of.to_csv(path_or_buf="../../../../import/is_sty_of.csv",
                 header=True,
                 index=False)
print("is_sty_of.csv & has_sty.csv successfully written out...")
# **************************************************************
# has_umls_atom.csv
has_umls_aui = '''
                 SELECT DISTINCT (SAB || '#' || CODE)     AS ":START_ID"
                                , AUI                     AS ":END_ID"
                                , 'HAS_UMLS_ATOM'         AS ":TYPE"
                 FROM MRCONSO
                 WHERE SAB IN ('ATC', 'GO', 'HGNC', 'HPO', 'ICD10CM', 
                               'ICD10PCS', 'LNC', 'MDR', 'MED-RT', 'MSH', 
                               'NCBI', 'NCI', 'OMIM', 'PDQ', 'RXNORM', 
                               'SNOMEDCT_US', 'SRC')
                     AND SUPPRESS = 'N';
                     '''
has_umls_atom = pd.read_sql_query(
    has_umls_aui, conn).drop_duplicates().replace(np.nan, "")
has_umls_atom.to_csv(path_or_buf="../../../../import/has_umls_atom.csv",
                     header=True,
                     index=False)
print("has_umls_atom.csv successfully written out...")
# **************************************************************
# has_cui.csv
has_cui = '''
            SELECT DISTINCT AUI  
                          , CUI      
                          , 'HAS_CUI'     AS ":TYPE"
            FROM MRCONSO
            WHERE SAB IN ('ATC', 'GO', 'HGNC', 'HPO', 'ICD10CM', 
                          'ICD10PCS', 'LNC', 'MDR', 'MED-RT', 'MSH', 
                          'NCBI', 'NCI', 'OMIM', 'PDQ', 'RXNORM', 
                          'SNOMEDCT_US', 'SRC')
                 AND SUPPRESS = 'N';
                 '''
has_cui_rel = pd.read_sql_query(
    has_cui, conn).drop_duplicates().replace(np.nan, "")
has_cui_rel.columns = [":START_ID", ":END_ID", ":TYPE"]
has_cui_rel.to_csv(path_or_buf="../../../../import/has_cui.csv",
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
            WHERE SAB IN ('ATC', 'GO', 'HGNC', 'HPO', 'ICD10CM', 
                          'ICD10PCS', 'LNC', 'MDR', 'MED-RT', 'MSH', 
                          'NCBI', 'NCI', 'OMIM', 'PDQ', 'RXNORM', 
                          'SNOMEDCT_US', 'SRC')
                 AND SUPPRESS = 'N'
                 AND TS = 'P'
                 AND STT = 'PF'
                 AND ISPREF = 'Y';
                 '''
has_aui_rel = pd.read_sql_query(
    has_aui, conn).drop_duplicates().replace(np.nan, "")
has_aui_rel.columns = [':START_ID', ':END_ID', ':TYPE']
has_aui_rel.to_csv(path_or_buf='../../../../import/has_aui.csv',
                   header=True,
                   index=False)
print("has_aui.csv successfully written out...")
# **************************************************************
# code_has_child.csv
has_child = '''
              SELECT DISTINCT (SAB || '#' || CODE)   AS ":START_ID"
                            , (SAB2 || '#' || CODE2) AS ":END_ID"
                            , 'HAS_CHILD'            AS ":TYPE"
              FROM HIERARCHY
              WHERE SAB IN ('ATC', 'GO', 'HGNC', 'HPO', 'ICD10CM', 
                            'ICD10PCS', 'LNC', 'MDR', 'MED-RT', 'MSH', 
                            'NCBI', 'NCI', 'OMIM', 'PDQ', 'RXNORM', 
                            'SNOMEDCT_US', 'SRC')
              AND CODE != CODE2;
              '''
has_child_code = pd.read_sql_query(
    has_child, conn).drop_duplicates().replace(np.nan, "")
has_child_code.to_csv(path_or_buf="../../../../import/has_child_code.csv",
                      header=True,
                      index=False)
print("has_child_code.csv successfully written out...")
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
              WHERE SAB IN ('ATC', 'GO', 'HGNC', 'HPO', 'ICD10CM', 
                            'ICD10PCS', 'LNC', 'MDR', 'MED-RT', 'MSH', 
                            'NCBI', 'NCI', 'OMIM', 'PDQ', 'RXNORM', 
                            'SNOMEDCT_US', 'SRC')
                  AND ATN IN ('ICD-O-3_CODE', 'NDC')
                  AND SUPPRESS = 'N';
                  '''
code_has_attribute = pd.read_sql_query(
    has_attr, conn).drop_duplicates().replace(np.nan, "")
code_has_attribute.to_csv(path_or_buf="../../../../import/code_has_attribute.csv",
                          header=True,
                          index=False)
print("code_has_attribute.csv successfully written out...")
# **************************************************************
# semanticType_isa_rel.csv
sty_isa_rel = '''
                 WITH srdef_query AS (SELECT DISTINCT UI
                                      FROM SRDEF
                                      WHERE RT = 'STY')
                 SELECT DISTINCT UI3                    AS ":END_ID"
                               , UI1                    AS ":START_ID"
                               , 'STY_HAS_CHILD'        AS ":TYPE"
                 FROM SRSTRE1
                         INNER JOIN srdef_query ON UI1 = srdef_query.UI
                 WHERE UI2 = 'T186';
                 '''
sty_isa = pd.read_sql_query(
    sty_isa_rel, conn).drop_duplicates().replace(np.nan, "")
sty_isa.to_csv(path_or_buf="../../../../import/sty_isa.csv",
               header=True,
               index=False)
print("sty_isa.csv successfully written out...")
# **************************************************************
# #cui_cui_rel.csv
cui_cui_re = '''
                SELECT DISTINCT CUI2
                              , CUI1
                              , CASE
                                    WHEN RELA = ''
                                  THEN REL
                                ELSE RELA END AS ":TYPE"
                                
                FROM MRCONSO c
                        JOIN MRREL r ON c.AUI = r.AUI1
                        JOIN MRCONSO c2 ON r.AUI2 = c2.AUI
                WHERE c.SAB IN ('ATC', 'GO', 'HGNC', 'HPO', 'ICD10CM', 
                              'ICD10PCS', 'LNC', 'MDR', 'MED-RT', 'MSH', 
                              'NCBI', 'NCI', 'OMIM', 'PDQ', 'RXNORM', 
                              'SNOMEDCT_US', 'SRC')
                    AND c2.SAB IN ('ATC', 'GO', 'HGNC', 'HPO', 'ICD10CM', 
                                   'ICD10PCS', 'LNC', 'MDR', 'MED-RT', 'MSH', 
                                   'NCBI', 'NCI', 'OMIM', 'PDQ', 'RXNORM', 
                                   'SNOMEDCT_US', 'SRC')
                    AND c.SUPPRESS = 'N'
                    AND c2.SUPPRESS = 'N'
                    AND c.ISPREF = 'Y'
                    AND c2.ISPREF = 'Y'
                    AND c.TS = 'P'
                    AND c2.TS = 'P'
                    AND c.STT = 'PF'
                    AND c2.STT = 'PF'
                    AND REL NOT IN ('SIB', 'SY');
                    '''

cui_cui = pd.read_sql_query(cui_cui_re, conn)
cui_cui.columns = [':START_ID', ':END_ID', ':TYPE']
cui_cui_rel_df = cui_cui[cui_cui[':START_ID'] !=
                         cui_cui[':END_ID']].drop_duplicates().replace(np.nan, "")
cui_cui_rel_df[":TYPE"] = cui_cui_rel_df[":TYPE"].str.upper()
cui_cui_rel_df.to_csv(path_or_buf="../../../../import/cui_cui_rel.csv",
                      header=True,
                      index=False)
print("cui_cui_rel.csv successfully written out...")
# **************************************************************
# cui_atui_rel.csv
cui_atui_rel = '''
                  SELECT DISTINCT s.ATUI
                                , c.CUI
                                , 'CUI_HAS_ATTRIBUTE' AS ":TYPE"
                  FROM MRCONSO c
                            JOIN MRSAT s ON c.CUI = s.CUI
                  WHERE c.SAB IN ('ATC', 'GO', 'HGNC', 'HPO', 'ICD10CM', 
                                  'ICD10PCS', 'LNC', 'MDR', 'MED-RT', 'MSH', 
                                  'NCBI', 'NCI', 'OMIM', 'PDQ', 'RXNORM', 
                                  'SNOMEDCT_US', 'SRC')
                      AND s.ATN IN ('ICD-O-3_CODE', 'NDC')
                      AND c.SUPPRESS = 'N'
                      AND c.STT = 'PF'
                      AND c.TS = 'P'
                      AND c.ISPREF = 'Y';
                      '''
cui_attribute_rel = pd.read_sql_query(
    cui_atui_rel, conn).drop_duplicates().replace(np.nan, "")
cui_attribute_rel.columns = [':END_ID', ':START_ID', ':TYPE']
cui_attribute_rel.to_csv(path_or_buf='../../../../import/cui_attribute_rel.csv',
                         header=True,
                         index=False)
print("cui_attribute_rel.csv successfully written out...")
# **************************************************************
# attribute_aui_rel.csv
atv_aui_rel = """
                SELECT DISTINCT s.ATUI             
                              , c.AUI
                              , 'ATTRIBUTE_HAS_AUI' AS ":TYPE"
                FROM MRSAT s
                        INNER JOIN MRCONSO c ON s.CUI = c.CUI
                WHERE c.SAB IN ('ATC', 'GO', 'HGNC', 'HPO', 'ICD10CM', 
                                'ICD10PCS', 'LNC', 'MDR', 'MED-RT', 'MSH', 
                                'NCBI', 'NCI', 'OMIM', 'PDQ', 'RXNORM', 
                                'SNOMEDCT_US', 'SRC')
                      AND s.SUPPRESS = 'N'
                      AND s.ATN IN ('ICD-O-3_CODE', 'NDC')
                      AND c.SUPPRESS = 'N';
                      """
attribute_aui_rel = pd.read_sql_query(
    atv_aui_rel, conn).drop_duplicates().replace(np.nan, "")
attribute_aui_rel.columns = [':START_ID', ':END_ID', ':TYPE']
attribute_aui_rel.to_csv(path_or_buf="../../../../import/attribute_aui_rel.csv",
                         header=True,
                         index=False)
print("attribute_aui_rel.csv successfully written out...")
