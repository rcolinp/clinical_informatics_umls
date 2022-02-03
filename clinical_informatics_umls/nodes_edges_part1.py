# !/usr/bin/env python

"""
This .py assumes you are querying one of the SQLite databases found via relative
path ->../sqlite/ -> (umls.db or umls_py.db)
SQLite database can be created via the following python script \
`create_sqlite_db.py`
(or via the following shell script ../sqlite/create_sqlite_db.sh.)
--> invoke that shell script via `sh create_sqlite_db_.sh ../UMLS/subset/2021AB`
Note: If using MySQL, Oracle or PostgreSQL, you'll need to adjust the \
connection object ('conn')
appropriately to the datastore of your choice.

Dependencies for MySQL, PostgreSQL and MariaDB are all included in the \
pyproject.toml file.
	(i.e. PyMySql, mysql-connector, psycopg2-binary, SQLAlchemy, mariadb etc...)
An example connection object for MySQL & PostgresSQL connection have been
	included below for reference.

****************************************************
MySQL connection:
import pymysql
mconn = pymysql.connect(
	hostname=hostname,
	user=username,
	password=password,
	database=database  # <-- schema name with loaded UMLS subset
)

****************************************************

PostgresSQL connection (using psycopg2):
import psycopg2
pgconn = psycopg2.connect(
	host=hostname,
	username=username,
	password=password,
	db_name=database
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

# umls_py.db SQLite database path (db_dir : str) & name (db_name : str)
db_dir = "../sqlite/"
db_name = "umls_py.db"

################################################################
# EXTRACT NEO4J GRAPH LABELS, NODES, PROPERTIES & RELATIONSHIPS
################################################################


def extract_nodes_edges(db_dir: str, db_name: str):
    """
    Summary:
    --------
    Query sqlite3 database created and extract all nodes/edges into .csv format.

    Parameters:
    -----------
        db_dir : str.
    Relative directory containing sqlite3 database 'umls_py.db'
        db_name : str.
    Name of sqlite3 database ("umls_py.db')

    Returns:
    --------

    """

    # Establish database connection
    db = os.path.join(os.path.dirname(db_dir), db_name)
    conn = sqlite3.connect(db)  # Create connection object

    ################################################################
    ################################################################

    # Label: SemanticType
    # Import: semanticTypeNode.csv
    semantic_node = """SELECT DISTINCT s.TUI, s.STY, s.STN, 'TUI' AS ":LABEL"
	FROM MRSTY s
	JOIN MRCONSO c ON s.CUI = c.CUI
	WHERE c.SAB IN ('ATC','GO','HPO','ICD9CM','ICD10CM','NCI','RXNORM','SNOMEDCT_US')
	    AND c.SUPPRESS = 'N'
		AND c.LAT = 'ENG';"""

    semanticTypeNode = (
        pd.read_sql_query(semantic_node, conn).drop_duplicates().replace(np.nan, "")
    )

    semanticTypeNode.columns = ["TUI:ID", "STY", "STN", ":LABEL"]

    semanticTypeNode.to_csv(
        path_or_buf="../../../../import/semanticTypeNode.csv", header=True, index=False
    )

    print("semanticTypeNode.csv successfully written out...")

    ################################################################

    # Label: Concept
    # Import: conceptNode.csv
    concept_node = """SELECT DISTINCT CUI, STR, 'Concept' AS ':LABEL'
    FROM MRCONSO
    WHERE SAB IN ('ATC','GO','HPO','ICD9CM','ICD10CM','NCI','RXNORM','SNOMEDCT_US')
        AND SUPPRESS = 'N'
        AND LAT = 'ENG'
        AND ISPREF = 'Y'
        AND TS = 'P'
        AND STT = 'PF';"""

    conceptNode = (
        pd.read_sql_query(concept_node, conn).drop_duplicates().replace(np.nan, "")
    )

    conceptNode.columns = ["Concept:ID", "STR", ":LABEL"]

    conceptNode.to_csv(
        path_or_buf="../../../../import/conceptNode.csv", header=True, index=False
    )

    print("conceptNode.csv successfully written out...")

    ################################################################

    # Label: Atom
    # Import: atomNode.csv
    atom_node = """SELECT DISTINCT AUI,STR,SAB,CODE,TTY,ISPREF,TS,'AUI'
	FROM MRCONSO
	WHERE SAB IN ('ATC','GO','HPO','ICD9CM','ICD10CM','NCI','RXNORM','SNOMEDCT_US')
		AND SUPPRESS = 'N'
		AND LAT = 'ENG';"""

    atomNode = (
        pd.read_sql_query(atom_node, conn)
        .drop_duplicates(subset=["AUI"])
        .replace(np.nan, "")
    )

    atomNode.columns = ["AUI:ID", "STR", "SAB", "CODE", "TTY", "ISPREF", "TS", ":LABEL"]

    atomNode.to_csv(
        path_or_buf="../../../../import/atomNode.csv", header=True, index=False
    )

    print("atomNode.csv successfully written out...")

    ################################################################

    # Label: Code
    # Import: codeNode.csv
    code_node = """SELECT DISTINCT (SAB||'#'||CODE), SAB, CODE, ('Code'||';'||SAB)
	FROM MRCONSO
	WHERE SAB IN ('ATC','GO','HPO','ICD9CM','ICD10CM','NCI','RXNORM','SNOMEDCT_US')
		AND SUPPRESS = 'N'
		AND LAT = 'ENG';"""

    codeNode = pd.read_sql_query(code_node, conn).drop_duplicates().replace(np.nan, "")

    codeNode.columns = ["Code:ID", "SAB", "CODE", ":LABEL"]

    codeNode.to_csv(
        path_or_buf="../../../../import/codeNode.csv", header=True, index=False
    )

    print("codeNode.csv successfully written out...")
    ################################################################
    # GRAPH EDGES/RELATIONSHIPS
    ################################################################

    # has_sty.csv
    has_sty_r = """SELECT DISTINCT MRCONSO.CUI, MRSTY.TUI, 'HAS_STY' AS ":TYPE"
	FROM MRSTY
	JOIN MRCONSO ON MRSTY.CUI = MRCONSO.CUI
	WHERE MRCONSO.SAB IN ('ATC','GO','HPO','ICD9CM','ICD10CM','NCI','RXNORM','SNOMEDCT_US')
	    AND MRCONSO.SUPPRESS = 'N'
	    AND MRCONSO.LAT = 'ENG';"""

    has_sty_rel = (
        pd.read_sql_query(has_sty_r, conn).drop_duplicates().replace(np.nan, "")
    )

    has_sty_rel.columns = [":START_ID", ":END_ID", ":TYPE"]

    has_sty_rel.to_csv(
        path_or_buf="../../../../import/has_sty_rel.csv", header=True, index=False
    )

    print("has_sty_rel.csv successfully written out...")

    ################################################################

    # import: has_aui_rel.csv

    has_umls_aui = """SELECT DISTINCT (SAB || '#' || CODE), AUI, 'HAS_AUI'
	FROM MRCONSO
	WHERE SAB IN ('ATC','GO','HPO','ICD9CM','ICD10CM','NCI','RXNORM','SNOMEDCT_US')
		AND SUPPRESS = 'N'
		AND LAT = 'ENG';"""

    has_aui_rel = (
        pd.read_sql_query(has_umls_aui, conn).drop_duplicates().replace(np.nan, "")
    )

    has_aui_rel.columns = [":START_ID", ":END_ID", ":TYPE"]

    has_aui_rel.to_csv(
        path_or_buf="../../../../import/has_aui_rel.csv", header=True, index=False
    )
    print("has_aui_rel.csv successfully written out...")

    ################################################################

    # has_cui_rel.csv
    # Each umls_aui within UMLS maps to a single umls_cui \
    # (umls_aui is primary key in UMLS.MRCONSO)
    # Each row of UMLS.MRCONSO represents each UMLS Atom (AUI) -> 1 Atom (AUI) \
    # can only map to a single UMLS Concept (CUI).
    # Furthermore, each UMLS Concept (CUI) is not limited to mapping to \
    # >=1 UMLS Atom (AUI)
    # AUI -> CUI mapping/relationship -> *including this* as both directions \
    # in the graph is not required and AUI -> CUI mapping preserves distinct source side of relationship

    # It is preferable in a graph model to specify direction only when direction has \
    # a semantic meaning (i.e. forward doesn't imply backward)
    # Since 'has_string' implies 'HAS_AUI' (inverse) -> there is minimal/no value in \
    # including both 'has_string' & 'HAS_AUI'.
    # --> Adding only 'has_string' (AUI)-[has_string]->(CUI) OR exact cypher being: \
    # `(Atom)-[:has_string]->(Concept)`

    has_concept = """SELECT DISTINCT AUI, CUI, 'HAS_CUI'
	FROM MRCONSO
	WHERE SAB IN ('ATC','GO','HPO','ICD9CM','ICD10CM','NCI','RXNORM','SNOMEDCT_US')
		AND SUPPRESS = 'N'
		AND LAT = 'ENG';"""

    has_cui_rel = (
        pd.read_sql_query(has_concept, conn).drop_duplicates().replace(np.nan, "")
    )

    has_cui_rel.columns = [":START_ID", ":END_ID", ":TYPE"]

    has_cui_rel.to_csv(
        path_or_buf="../../../../import/has_cui_rel.csv", header=True, index=False
    )

    print("has_cui_rel.csv successfully written out...")

    ################################################################

    # import: tui_tui_rel.csv
    # Limit to SRSTR.RL = 'ISA' -> most useful part of semantic network
    tui_tui = """SELECT DISTINCT s2.UI, s3.UI, s.RL
	FROM SRSTR s
	JOIN SRDEF s2 ON s.STY_RL1 = s2.STY_RL
	JOIN SRDEF s3 ON s.STY_RL2 = s3.STY_RL
	WHERE s2.UI != s3.UI
	    AND s.RL = 'isa';"""

    tui_tui_rel_df = (
        pd.read_sql_query(tui_tui, conn).drop_duplicates().replace(np.nan, "")
    )

    tui_tui_rel_df.columns = [":START_ID", ":END_ID", ":TYPE"]
    tui_tui_rel = (
        tui_tui_rel_df[tui_tui_rel_df[":START_ID"] != tui_tui_rel_df[":END_ID"]]
        .drop_duplicates()
        .replace(np.nan, "")
    )
    tui_tui_rel[":TYPE"] = tui_tui_rel[":TYPE"].str.upper()

    tui_tui_rel.to_csv(
        path_or_buf="../../../../import/tui_tui_rel.csv", header=True, index=False
    )

    print("tui_tui_rel.csv successfully written out...")

    ################################################################

    # import: concept_concept_rel.csv

    # We will filter out REL = 'SIB' as the relationship in UMLS \
    # does not provide much utility & will increase size of graph considerably
    # UMLS.MRREL.RELA is sometimes NULL but UMLS.MRREL.REL & UMLS.MRREL.RELA \
    # cannot both be null (1 has to exist)
    # CASE statement ensures that when RELA is NULL, :TYPE is assigned REL as \
    # its value
    # 'vocab' assigned to be a property of the relationship \
    # (i.e. Concept -- Concept relationship can be filtered to \
    # the vocabulary for which the relationship exists)
    concept_concept = """
                        WITH q AS
	                        (SELECT DISTINCT SAB
						     FROM MRCONSO
						     WHERE SAB IN (
                                            'ATC',
                                            'GO',
                                            'HPO',
                                            'ICD9CM',
                                            'ICD10CM',
                                            'NCI',
                                            'RXNORM',
                                            'SNOMEDCT_US'
                                            )
						     AND SUPPRESS = 'N'
						     AND LAT = 'ENG')
	SELECT r.CUI2, r.CUI1, CASE WHEN r.RELA = '' THEN r.REL ELSE r.RELA END AS ":TYPE", r.SAB
	FROM MRREL r
	JOIN q ON r.SAB = q.SAB
	WHERE r.SUPPRESS = 'N'
	GROUP BY r.CUI2,r.CUI1,":TYPE",r.SAB;"""

    concept_concept_rel = pd.read_sql_query(concept_concept, conn)

    concept_concept_rel.columns = [":START_ID", ":END_ID", ":TYPE", "SAB"]

    # start_id should not equal end_id -> remove them & then drop duplicates \
    # and replace nan with ''

    concept_concept_rel = (
        concept_concept_rel[
            (concept_concept_rel[":START_ID"] != concept_concept_rel[":END_ID"])
            & (concept_concept_rel[":TYPE"] != "SIB")
        ]
        .drop_duplicates()
        .replace(np.nan, "")
    )

    concept_concept_rel[":TYPE"] = concept_concept_rel[":TYPE"].str.upper()
    concept_concept_rel[":TYPE"] = concept_concept_rel[":TYPE"].str.replace("-", "_")

    concept_concept_rel.to_csv(
        path_or_buf="../../../../import/concept_concept_rel.csv",
        header=True,
        index=False,
    )

    print("concept_concept_rel.csv successfully written out...")

    ################################################################

    # import: child_of_rel.csv -> alternative option to running edges_part2.py
    child_of = """SELECT DISTINCT h.PAUI, c.AUI, 'CHILD_OF'
	FROM MRHIER h
	JOIN MRCONSO c ON h.AUI = c.AUI
    JOIN MRCONSO c2 ON h.PAUI = c2.AUI
	WHERE h.SAB IN ('ATC','GO','HPO','ICD9CM','ICD10CM','NCI','RXNORM','SNOMEDCT_US')
	    AND c.SUPPRESS = 'N'
		AND c2.SUPPRESS = 'N'
		AND c.LAT = 'ENG'
		AND c2.LAT = 'ENG'
		AND c.CODE != c2.CODE;"""

    child_of_rel = pd.read_sql_query(child_of, conn)

    child_of_rel.columns = [":START_ID", ":END_ID", ":TYPE"]

    child_of_rel = (
        child_of_rel[child_of_rel[":START_ID"] != child_of_rel[":END_ID"]]
        .drop_duplicates()
        .replace(np.nan, "")
    )

    child_of_rel.to_csv(
        path_or_buf="../../../../import/child_of_rel.csv", header=True, index=False
    )

    print("child_of_rel.csv successfully written out...")

    ################################################################

    # import: cui_code_rel.csv
    cui_code_rel = """SELECT DISTINCT CUI, (SAB || '#' || CODE), 'HAS_SOURCE_CODE'
	FROM MRCONSO
	WHERE SAB IN ('ATC','GO','HPO','ICD9CM','ICD10CM','NCI','RXNORM','SNOMEDCT_US')
	    AND SUPPRESS = 'N'
		AND LAT = 'ENG';"""

    has_source_code = (
        pd.read_sql_query(cui_code_rel, conn).drop_duplicates().replace(np.nan, "")
    )

    has_source_code.columns = [":START_ID", ":END_ID", ":TYPE"]

    has_source_code.to_csv(
        path_or_buf="../../../../import/cui_code_rel.csv", header=True, index=False
    )

    has_source_code_copy = has_source_code.copy()

    print("cui_code_rel.csv successfully written out...")

    ################################################################

    # Append both codeNode.csv & cui_code_rel.csv w/ ICDO3T & ICDO3M CODEs
    icdo = """SELECT DISTINCT ATV, (SAB||'#'||CODE), SAB
	FROM MRSAT
	WHERE SAB = 'NCI'
	    AND ATN = 'ICD-O-3_CODE'
	    AND SUPPRESS = 'N'
	    AND ATV != '0000/0';"""

    icdo_df = pd.read_sql_query(icdo, conn).drop_duplicates().replace(np.nan, "")

    icdo_df.columns = ["CODE", ":END_ID", "SAB"]
    icdo_df["SAB"] = "ICDO3"
    icdo_df["Code:ID"] = icdo_df["SAB"] + "#" + icdo_df["CODE"]
    icdo_df[":LABEL"] = "Code" + ";" + icdo_df["SAB"]
    icdo_df[["Code:ID", "SAB", "CODE", ":LABEL"]].to_csv(
        path_or_buf="../../../../import/codeNode.csv",
        mode="a",
        header=False,
        index=False,
    )
    cui_code_rel_icdo_append = icdo_df.merge(
        has_source_code_copy, how="inner", on=":END_ID"
    )

    cui_code_rel_icdo_append[":TYPE"] = "HAS_SOURCE_CODE"
    cui_code_rel_append = (
        cui_code_rel_icdo_append[[":START_ID", "Code:ID", ":TYPE"]]
        .rename({"Code:ID": ":END_ID"}, axis=1)
        .drop_duplicates()
        .replace(np.nan, "")
    )

    cui_code_rel_append.to_csv(
        path_or_buf="../../../../import/cui_code_rel.csv",
        mode="a",
        header=False,
        index=False,
    )

    print("cui_code_rel.csv successfully appended and written out...")


if __name__ == "__main__":
    extract_nodes_edges(db_dir, db_name)

################################################################
# NOTE: Do not include both output of `edges_part2.py` and the last output \
# .csv via this .py. Both are redundant but one or other should be included.
################################################################
