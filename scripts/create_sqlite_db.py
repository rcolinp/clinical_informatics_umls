#!/usr/bin/env python3
"""
Summary:
--------
Similar to ../sqlite/create_sqlite_db.sh...
The following script 'create_sqlite_db.py' provides a means of creating a loaded sqlite3 database containing UMLS's 2021AB release.

"""

import sys
import os
import sqlite3
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
from io import StringIO

umls_tables = "../../../UMLS/subset/2021AB/META/"
success = False
db_path = '../sqlite/umls_py.db'
conn = None

MRCONSO_TABLE_FILE = None
MRHIER_TABLE_FILE = None
MRRANK_TABLE_FILE = None
MRREL_TABLE_FILE = None
SRDEF_TABLE_FILE = None
SRSTRE1_TABLE_FILE = None
SRSTRE2_TABLE_FILE = None
SRSTR_TABLE_FILE = None
MRSAB_TABLE_FILE = None
MRSTY_TABLE_FILE = None
# MRMAP_TABLE_FILE = None
# MRSMAP_TABLE_FILE = None
# MRSAT_TABLE_FILE = None
# this ensure files are closed properly and umls_py.db is removed if not successful


def umls_db_cleanup():
    """"""
    global success
    global conn
    global db_path

    global MRCONSO_TABLE_FILE
    global MRHIER_TABLE_FILE
    global MRRANK_TABLE_FILE
    global MRREL_TABLE_FILE
    global SRDEF_TABLE_FILE
    global SRSTRE1_TABLE_FILE
    global SRSTRE2_TABLE_FILE
    global SRSTR_TABLE_FILE
    global MRSAB_TABLE_FILE
    global MRSTY_TABLE_FILE
    # global MRMAP_TABLE_FILE
    # global MRSMAP_TABLE_FILE
    # global MRSAT_TABLE_FILE

    if conn is not None:
        conn.close()

    if MRCONSO_TABLE_FILE is not None:
        MRCONSO_TABLE_FILE.close()

    if MRHIER_TABLE_FILE is not None:
        MRHIER_TABLE_FILE.close()

    if MRRANK_TABLE_FILE is not None:
        MRRANK_TABLE_FILE.close()

    if MRREL_TABLE_FILE is not None:
        MRREL_TABLE_FILE.close()

    if SRDEF_TABLE_FILE is not None:
        SRDEF_TABLE_FILE.close()

    if SRSTR_TABLE_FILE is not None:
        SRSTR_TABLE_FILE.close()

    if SRSTRE1_TABLE_FILE is not None:
        SRSTRE1_TABLE_FILE.close()

    if SRSTRE2_TABLE_FILE is not None:
        SRSTRE2_TABLE_FILE.close()

    if MRSAB_TABLE_FILE is not None:
        MRSAB_TABLE_FILE.close()

    if MRSTY_TABLE_FILE is not None:
        MRSTY_TABLE_FILE.close()

    # if MRMAP_TABLE_FILE is not None:
    #     MRMAP_TABLE_FILE.close()

    # if MRSMAP_TABLE_FILE is not None:
    #     MRSMAP_TABLE_FILE.close()

    # if MRSAT_TABLE_FILE is not None:
    #     MRSAT_TABLE_FILE.close()

    if success is False:

        # remove db
        if db_path is not None:
            os.remove(db_path)

            print('\n\tError: umls_py.db was not created successfully.\n')


def create_db():
    """"""

    global success
    global conn
    global db_path

    global MRCONSO_TABLE_FILE
    global MRHIER_TABLE_FILE
    global MRRANK_TABLE_FILE
    global MRREL_TABLE_FILE
    global SRDEF_TABLE_FILE
    global SRSTRE1_TABLE_FILE
    global SRSTRE2_TABLE_FILE
    global SRSTR_TABLE_FILE
    global MRSAB_TABLE_FILE
    global MRSTY_TABLE_FILE
    # global MRMAP_TABLE_FILE
    # global MRSMAP_TABLE_FILE
    # global MRSAT_TABLE_FILE

    print("\ncreating umls_py.db")
    db_path = '../sqlite/umls_py.db'
    conn = sqlite3.connect(db_path)
    conn.text_factory = StringIO

    print("opening files")
    # load data in UMLS RRF files.

    try:
        mrsty_path = os.path.join(umls_tables, 'MRSTY.RRF')
        MRSTY_TABLE_FILE = open(mrsty_path, "r")
    except IOError:
        print("No file to use for creating MRSTY.RRF table")
        sys.exit()

    try:
        mrconso_path = os.path.join(umls_tables, 'MRCONSO.RRF')
        MRCONSO_TABLE_FILE = open(mrconso_path, "r")
    except IOError:
        print("\nNo file to use for creating MRCONSO.RRF table\n")
        sys.exit()

    try:
        mrhier_path = os.path.join(umls_tables, 'MRHIER.RRF')
        MRHIER_TABLE_FILE = open(mrhier_path, "r")
    except IOError:
        print("\nNo file to use for creating MRHIER.RRF table\n")
        sys.exit()

    try:
        mrrank_path = os.path.join(umls_tables, 'MRRANK.RRF')
        MRRANK_TABLE_FILE = open(mrrank_path, "r")
    except IOError:
        print("\nNo file to use for creating MRRANK.RRF table\n")
        sys.exit()

    try:
        mrrel_path = os.path.join(umls_tables, 'MRREL.RRF')
        MRREL_TABLE_FILE = open(mrrel_path, "r")
    except IOError:
        print("\nNo file to use for creating MRREL.RRF table\n")
        sys.exit()

    try:
        srdef_path = os.path.join(umls_tables, 'SRDEF')
        SRDEF_TABLE_FILE = open(srdef_path, "r")
    except IOError:
        print("\nNo file to use for creating SRDEF table\n")
        sys.exit()

    try:
        srstr_path = os.path.join(umls_tables, 'SRSTR')
        SRSTR_TABLE_FILE = open(srstr_path, "r")
    except IOError:
        print("\nNo file to use for creating SRSTR table\n")
        sys.exit()

    try:
        srstre1_path = os.path.join(umls_tables, 'SRSTRE1')
        SRSTRE1_TABLE_FILE = open(srstre1_path, "r")
    except IOError:
        print("\nNo file to use for creating SRSTRE1 table\n")
        sys.exit()

    try:
        srstre2_path = os.path.join(umls_tables, 'SRSTRE2')
        SRSTRE2_TABLE_FILE = open(srstre2_path, "r")
    except IOError:
        print("\nNo file to use for creating SRSTRE2 table\n")
        sys.exit()

    try:
        mrsab_path = os.path.join(umls_tables, 'MRSAB.RRF')
        MRSAB_TABLE_FILE = open(mrsab_path, "r")
    except IOError:
        print("\nNo file to use for creating MRSAB table\n")
        sys.exit()

    # try:
    #     mrmap_path = os.path.join(umls_tables, 'MRMAP.RRF')
    #     MRMAP_TABLE_FILE = open(mrmap_path, "r")
    # except IOError:
    #     print("\nNo file to use for creating MRMAP table\n")
    #     sys.exit()

    # try:
    #     mrsmap_path = os.path.join(umls_tables, 'MRMAP.RRF')
    #     MRSMAP_TABLE_FILE = open(mrsmap_path, "r")
    # except IOError:
    #     print("\nNo file to use for creating MRSMAP table\n")
        sys.exit()

    # try:
    #     mrsat_path = os.path.join(umls_tables, 'MRSAT.RRF')
    #     MRSAT_TABLE_FILE = open(mrsat_path, "r")
    # except IOError:
    #     print("\nNo file to use for creating MRSAT table\n")
    #     sys.exit()

    print("Creating tables")
    c = conn.cursor()

    # Create tables (MRSTY, MRCONSO, MRREL, MRHIER, MRRANK, SRDEF, SRSTR, SRSTRE1, SRSTRE2, MRSAB, MRSAT)
    c.execute("CREATE TABLE MRSTY( CUI varchar, TUI varchar, STN varchar, STY text, ATUI varchar, CVF varchar  ) ;")
    c.execute("CREATE TABLE MRCONSO( CUI varchar, LAT varchar, TS varchar, LUI varchar, STT varchar, SUI varchar, ISPREF varchar, AUI varchar, SAUI varchar, SCUI varchar, SDUI varchar, SAB varchar, TTY varchar, CODE varchar, STR text, SRL varchar, SUPPRESS varchar, CVF varchar ) ;")
    c.execute("CREATE TABLE MRREL( CUI1 varchar, AUI1 varchar, STYPE1 varchar, REL varchar, CUI2 varchar, AUI2 varchar, STYPE2 varchar, RELA varchar, RUI varchar, SRUI varchar, SAB varchar, SL varchar, RG varchar, DIR varchar, SUPPRESS varchar, CVF varchar ) ;")
    c.execute("CREATE TABLE MRHIER( CUI varchar, AUI varchar, CXN varchar, PAUI varchar, SAB varchar, RELA varchar, PTR varchar, HCD varchar, CVF varchar ) ;")
    c.execute("CREATE TABLE MRRANK( MRRANK_RANK varchar, SAB varchar, TTY varchar, SUPPRESS varchar ) ;")
    c.execute("CREATE TABLE SRDEF( RT varchar, UI varchar, STY_RL text, STN_RTN varchar, DEF varchar, EX varchar, UN varchar, NH varchar, ABR varchar, RIN varchar ) ;")
    c.execute("CREATE TABLE SRSTR( STY_RL1 text, RL varchar, STY_RL2 text, LS varchar ) ;")
    c.execute("CREATE TABLE SRSTRE1( UI1 varchar, UI2 varchar, UI3 varchar ) ;")
    c.execute("CREATE TABLE SRSTRE2( STY1 text, RL varchar, STY2 text ) ;")
    c.execute("CREATE TABLE MRSAB( VCUI varchar, RCUI varchar, VSAB varchar, RSAB varchar, SON varchar, SF varchar, SVER varchar, VSTART varchar, VEND varchar, IMETA varchar, RMETA varchar, SLC varchar, SCC varchar, SRL varchar, TRF varchar, CFR varchar, CXTY varchar, TTYL varchar, ATNL varchar, LAT varchar, CENC varchar, CURVER varchar, SABIN varchar, SSN varchar, SCIT varchar ) ;")
    # c.execute("CREATE TABLE MRSAT( CUI varchar, LUI varchar, SUI varchar, METAUI varchar, STYPE varchar, CODE varchar, ATUI varchar, SATUI varchar, ATN varchar, SAB varchar, ATV varchar, SUPPRESS varchar, CVF varchar ) ;")

    print("Inserting data into MRSTY table")
    for line in MRSTY_TABLE_FILE:
        line = line.strip('\n')
        assert line[-1] == '|', "str: {}, char: ".format(line, line[-1])
        line = line.split('|')
        line.pop()
        assert len(line) == 6
        c.execute(
            "INSERT INTO MRSTY( CUI, TUI, STN, STY, ATUI, CVF ) VALUES( ?, ?, ?, ?, ?, ?)", tuple(line))

    print("Inserting data into MRCONSO table")
    for line in MRCONSO_TABLE_FILE:
        line = line.strip('\n')
        assert line[-1] == '|', "str: {}, char: ".format(line, line[-1])
        line = line.split('|')
        line.pop()
        assert len(line) == 18
        c.execute("""INSERT INTO MRCONSO( CUI, LAT, TS, LUI, STT, SUI, ISPREF, AUI, SAUI, 
                                          SCUI, SDUI, SAB, TTY, CODE, STR, SRL, SUPPRESS, CVF ) 
                     VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""", tuple(line))

    print("Inserting data into MRREL table")
    for line in MRREL_TABLE_FILE:
        line = line.strip('\n')
        assert line[-1] == '|', "str: {}, char: ".format(line, line[-1])
        line = line.split('|')
        line.pop()
        assert len(line) == 16
        c.execute("""INSERT INTO MRREL(  CUI1, AUI1, STYPE1, REL, CUI2, AUI2, STYPE2, 
                                       RELA, RUI, SRUI, SAB, SL, RG, DIR, SUPPRESS, CVF ) 
                     VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );""", tuple(line))

    print("Inserting data into MRHIER table")
    for line in MRHIER_TABLE_FILE:
        line = line.strip('\n')
        assert line[-1] == '|', "str: {}, char: ".format(line, line[-1])
        line = line.split('|')
        line.pop()
        assert len(line) == 9
        c.execute("""INSERT INTO MRHIER( CUI, AUI, CXN, PAUI, 
                                         SAB, RELA, PTR, HCD, CVF ) 
                     VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ? );""", tuple(line))

    print("Inserting data into MRRANK table")
    for line in MRRANK_TABLE_FILE:
        line = line.strip('\n')
        assert line[-1] == '|', "str: {}, char: ".format(line, line[-1])
        line = line.split('|')
        line.pop()
        assert len(line) == 4
        c.execute(
            "INSERT INTO MRRANK( MRRANK_RANK, SAB, TTY, SUPPRESS ) VALUES( ?, ?, ?, ? );", tuple(line))

    print("Inserting data into SRDEF table")
    for line in SRDEF_TABLE_FILE:
        line = line.strip('\n')
        assert line[-1] == '|', "str: {}, char: ".format(line, line[-1])
        line = line.split('|')
        line.pop()
        assert len(line) == 10
        c.execute(
            """INSERT INTO SRDEF( RT, UI, STY_RL, STN_RTN, 
            					  DEF, EX, UN, NH, ABR, RIN ) 
               VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );""", tuple(line))

    print("Inserting data into SRSTR table")
    for line in SRSTR_TABLE_FILE:
        line = line.strip('\n')
        assert line[-1] == '|', "str: {}, char: ".format(line, line[-1])
        line = line.split('|')
        line.pop()
        assert len(line) == 4
        c.execute(
            "INSERT INTO SRSTR( STY_RL1, RL, STY_RL2, LS ) VALUES( ?, ?, ?, ? );", tuple(line))

    print("Inserting data into SRSTRE1 table")
    for line in SRSTRE1_TABLE_FILE:
        line = line.strip('\n')
        assert line[-1] == '|', "str: {}, char: ".format(line, line[-1])
        line = line.split('|')
        line.pop()
        assert len(line) == 3
        c.execute(
            "INSERT INTO SRSTRE1( UI1, UI2, UI3 ) VALUES( ?, ?, ? );", tuple(line))

    print("Inserting data into SRSTRE2 table")
    for line in SRSTRE2_TABLE_FILE:
        line = line.strip('\n')
        assert line[-1] == '|', "str: {}, char: ".format(line, line[-1])
        line = line.split('|')
        line.pop()
        assert len(line) == 3
        c.execute(
            "INSERT INTO SRSTRE2( STY1, RL, STY2 ) VALUES( ?, ?, ? );", tuple(line))

    print("Inserting data into MRSAB table")
    for line in MRSAB_TABLE_FILE:
        line = line.strip('\n')
        assert line[-1] == '|', "str: {}, char: ".format(line, line[-1])
        line = line.split('|')
        line.pop()
        assert len(line) == 25
        c.execute("""INSERT INTO MRSAB( VCUI, RCUI, VSAB, RSAB, SON, SF, SVER, VSTART, VEND, 
            					  IMETA, RMETA, SLC, SCC, SRL, TRF, CFR, CXTY, TTYL, ATNL, 
                   				  LAT, CENC, CURVER, SABIN, SSN, SCIT ) 
                         VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                         	?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );""", tuple(line))

    # print("Inserting data into MRSAT table")
    # for line in MRSAT_TABLE_FILE:
    #     line = line.strip('\n')
    #     assert line[-1] == '|', "str: {}, char: ".format(line, line[-1])
    #     line = line.split('|')
    #     line.pop()
    #     assert len(line) == 13
    #     c.execute("""INSERT INTO MRSAT( CUI, LUI, SUI, METAUI, STYPE, CODE,
    #               						ATUI, SATUI, ATN, SAB, ATV, SUPPRESS, CVF )
    #                  VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );""", tuple(line))

    # create indices for faster queries
    print("Creating indices")
    c.execute("CREATE INDEX X_mrsty_cui ON MRSTY (CUI);")
    c.execute("CREATE INDEX X_mrconso_cui ON MRCONSO (CUI);")
    c.execute("CREATE INDEX X_mrconso_sab ON MRCONSO (SAB);")
    c.execute("CREATE INDEX X_mrrel_cui2 ON MRREL (CUI2);")
    c.execute("CREATE INDEX X_mrrel_cui1 ON MRREL (CUI1);")
    c.execute("CREATE INDEX X_mrhier_aui ON MRHIER (AUI);")
    c.execute("CREATE INDEX X_mrhier_paui ON MRHIER (PAUI);")
    # c.execute("CREATE INDEX X_mrsat_cui ON MRSAT (CUI);")

    # Commit changes to umls_py.db
    conn.commit()

    success = True
    print("\nSQLite database created - umls_py.db")


if __name__ == "__main__":
    create_db()
