# !/bin/sh
#
#  Create a UMLS SQLite database.
# ** Usage of this script requires that you are a U
#   --> Please reference following link for original source -> https://github.com/chb/py-umls/blob/master/databases/umls.sh

if [ ! -e umls.db ]; then
    if [ ! -d "$1" ]; then
        echo "Provide the path to the UMLS install directory as first argument when invoking this script. Download the latest version here: http://www.nlm.nih.gov/research/umls/licensedcontent/umlsknowledgesources.html (should check which file is needed)"
        exit 1
    fi
    if [ ! -d "$1/META" ]; then
        echo "There is no directory named META in the install directory you provided. Download the latest version here: http://www.nlm.nih.gov/research/umls/licensedcontent/umlsknowledgesources.html"
        exit 1
    fi

    # Convert RRF files (strip last pipe and remove quote (") characters, those are giving SQLite troubles)
    if [ ! -e "$1/META/MRDEF.pipe" ]; then
        current=$(pwd)
        cd "$1/META"
        echo "-> Converting RRF files for SQLite"
        for f in MRCONSO.RRF MRDEF.RRF MRHIER.RRF MRRANK.RRF MRREL.RRF MRSAT.RRF MRSTY.RRF; do
            sed -e 's/.$//' -e 's/"//g' "$f" >"${f%RRF}pipe"
        done
        cd $current
    fi

    # # init the database for MRDEF
    # # table structure here: http://www.ncbi.nlm.nih.gov/books/NBK9685/ *--> include appropriate reference for each table*
    sqlite3 umls.db "CREATE TABLE MRDEF(
        CUI varchar,
        AUI varchar,
        ATUI varchar
            constraint MRDEF_pk
                primary key,
        SATUI varchar,
        SAB varchar,
        DEF text,
        SUPPRESS varchar,
        CVF varchar
    )"

    # init the database for MRCONSO
    sqlite3 umls.db "CREATE TABLE MRCONSO(
        CUI varchar,
        LAT varchar,
        TS varchar,
        LUI varchar,
        STT varchar,
        SUI varchar,
        ISPREF varchar,
        AUI varchar
            constraint MRCONSO_pk
                primary key,
        SAUI varchar,
        SCUI varchar,
        SDUI varchar,
        SAB varchar,
        TTY varchar,
        CODE varchar,
        STR text,
        SRL varchar,
        SUPPRESS varchar,
        CVF varchar
    )"

    # init the database for MRHIER
    sqlite3 umls.db "CREATE TABLE MRHIER(
        CUI varchar,
        AUI varchar,
        CXN varchar,
        PAUI varchar,
        SAB varchar,
        RELA varchar,
        PTR varchar,
        HCD varchar,
        CVF varchar
    )"

    # init the database for MRRANK
    sqlite3 umls.db "CREATE TABLE MRRANK(
        MRRANK_RANK varchar,
        SAB varchar,
        TTY varchar,
        SUPPRESS varchar
    )"

    # init the database for MRREL
    sqlite3 umls.db "CREATE TABLE MRREL(
        CUI1 varchar,
        AUI1 varchar,
        STYPE1 varchar,
        REL varchar,
        CUI2 varchar,
        AUI2 text,
        STYPE2 varchar,
        RELA varchar,
        RUI varchar
            constraint MRREL_pk
                primary key,
        SRUI varchar,
        SAB varchar,
        SL varchar,
        RG varchar,
        DIR varchar,
        SUPPRESS varchar,
        CVF varchar
    )"

    # init the database for MRSAT
    sqlite3 umls.db "CREATE TABLE MRSAT(
        CUI varchar,
        LUI varchar,
        SUI varchar,
        METAUI varchar,
        STYPE varchar,
        CODE varchar,
        ATUI varchar
            constraint MRSAT_pk
                primary key,
        SATUI varchar,
        ATN varchar,
        SAB varchar,
        ATV varchar,
        SUPPRESS varchar,
        CVF varchar
    )"

    # init the database for MRSTY
    sqlite3 umls.db "CREATE TABLE MRSTY(
        CUI varchar,
        TUI varchar,
        STN varchar,
        STY text,
        ATUI varchar
            constraint MRSTY_pk
                primary key,
        CVF varchar
    )"

    # import tables
    for f in "$1/META/"*.pipe; do
        table=$(basename ${f%.pipe})
        echo "-> Importing $table"
        sqlite3 umls.db ".import '$f' '$table'"
    done

    # create indexes
    echo "-> Creating indexes"
    sqlite3 umls.db "CREATE INDEX X_CUI_MRCONSO ON MRCONSO(CUI);"
    sqlite3 umls.db "CREATE INDEX X_CODE_MRCONSO ON MRCONSO(CODE);"
    sqlite3 umls.db "CREATE INDEX X_SAB_MRCONSO ON MRCONSO(SAB,TTY);"
    sqlite3 umls.db "CREATE INDEX X_CUI_MRSTY ON MRSTY(CUI);"
    sqlite3 umls.db "CREATE INDEX X_TUI_MRSTY ON MRSTY(TUI);"
    sqlite3 umls.db "CREATE INDEX X_CUI_MRHIER ON MRHIER(CUI);"
    sqlite3 umls.db "CREATE INDEX X_AUI_MRHIER ON MRHIER(AUI);"
    sqlite3 umls.db "CREATE INDEX X_SAB_MRHIER ON MRHIER(SAB);"
    sqlite3 umls.db "CREATE INDEX X_PAUI_MRHIER ON MRHIER(PAUI);"
    sqlite3 umls.db "CREATE INDEX X_CUI1_MRREL ON MRREL(CUI1);"
    sqlite3 umls.db "CREATE INDEX X_AUI1_MRREL ON MRREL(AUI1);"
    sqlite3 umls.db "CREATE INDEX X_CUI2_MRREL ON MRREL(CUI2);"
    sqlite3 umls.db "CREATE INDEX X_AUI2_MRREL ON MRREL(AUI2);"
    sqlite3 umls.db "CREATE INDEX X_SAB_MRREL ON MRREL(SAB);"
    sqlite3 umls.db "CREATE INDEX X_CUI_MRSAT ON MRSAT(CUI);"
    sqlite3 umls.db "CREATE INDEX X_SAB_MRSAT ON MRSAT(SAB);"
    sqlite3 umls.db "CREATE INDEX X_ATN_MRSAT ON MRSAT(ATN);"
    sqlite3 umls.db "CREATE INDEX X_CODE_MRSAT ON MRSAT(CODE);"
    echo "-> successfully indexed inherited tables"

    # create faster lookup table for parent/child relationships (hierarchies)
    echo "-> begin to create an 'optimized' parent/child table -> 'HIERARCHY'..."
    sqlite3 umls.db """CREATE TABLE HIERARCHY AS SELECT DISTINCT h.PTR   AS PTR 
                                                               , h.PAUI  AS PAUI
                                                               , c2.CUI  AS CUI
                                                               , c2.SAB  AS SAB
                                                               , c2.CODE AS CODE
                                                               , c2.STR  AS STR
                                                               , c2.TTY  AS TTY
                                                               , h.RELA  AS RELA
                                                               , c.AUI   AS AUI2
                                                               , c.CUI   as CUI2
                                                               , c.SAB   AS SAB2
                                                               , c.CODE  AS CODE2
                                                               , c.STR   AS STR2
                                                               , c.TTY   AS TTY2
                                                 FROM MRHIER h
                                                        JOIN MRCONSO c ON h.AUI = c.AUI
                                                        JOIN MRCONSO c2 ON h.PAUI = c2.AUI
                                                 WHERE c.SUPPRESS = 'N'
                                                    AND c2.SUPPRESS = 'N';"""
    echo "-> successfully created HIERARCHY table."

    echo "-> begin to index HIERARCHY table..."
    # sqlite3 umls.db "CREATE INDEX X_CUI_HIERARCHY ON HIERARCHY(CUI2);"
    sqlite3 umls.db "CREATE INDEX X_CODE_HIERARCHY ON HIERARCHY(CODE2);"
    sqlite3 umls.db "CREATE INDEX X_AUI_HIERARCHY ON HIERARCHY(AUI2);"
    # sqlite3 umls.db "CREATE INDEX X_CUI2_HIERARCHY ON HIERARCHY(CUI);"
    sqlite3 umls.db "CREATE INDEX X_CODE2_HIERARCHY ON HIERARCHY(CODE);"
    sqlite3 umls.db "CREATE INDEX X_PAUI_HIERARCHY ON HIERARCHY(PAUI);"
    echo "-> successfully completed indexing HIERARCHY table."

    echo "-> begin to create an 'optimized' semantic relationship table -> 'MRCONREL'."
    sqlite3 umls.db """CREATE TABLE MRCONREL AS SELECT DISTINCT c2.AUI    AS AUI
                                                              , c2.CUI    AS CUI
                                                              , c2.SUI    AS SUI
                                                              , c2.SAB    AS SAB
                                                              , c2.CODE   AS CODE
                                                              , c2.SCUI   AS SCUI
                                                              , c2.STR    AS STR
                                                              , c2.TTY    AS TTY
                                                              , c2.ISPREF AS ISPREF
                                                              , c2.TS     AS TS
                                                              , c2.STT    AS STT
                                                              , r.STYPE1  AS STYPE1
                                                              , r.STYPE2  AS STYPE2
                                                              , r.REL     AS REL
                                                              , r.RELA    AS RELA
                                                              , r.SAB     AS rSAB
                                                              , r.rg      AS RG
                                                              , c.AUI     AS AUI2
                                                              , c.CUI     AS CUI2
                                                              , c.SUI     AS SUI2
                                                              , c.SAB     AS SAB2
                                                              , c.CODE    AS CODE2
                                                              , c.SCUI    AS SCUI2
                                                              , c.STR     AS STR2
                                                              , c.TTY     AS TTY2
                                                              , c.ISPREF  AS ISPREF2
                                                              , c.TS      AS TS2
                                                              , c.STT     AS STT2
                                                FROM MRCONSO c
                                                        JOIN MRREL r ON c.AUI = r.AUI1
                                                        JOIN MRCONSO c2 ON r.AUI2 = c2.AUI
                                                WHERE c.SUPPRESS = 'N' 
                                                    AND c2.SUPPRESS = 'N';"""
    echo "-> successfully created table MRCONREL."

    echo "-> begin indexing table MRCONREL..."
    sqlite3 umls.db "CREATE INDEX X_CUI_MRCONREL ON MRCONREL(CUI2);"
    # sqlite3 umls.db "CREATE INDEX X_AUI_MRCONREL ON MRCONREL(AUI2);"
    sqlite3 umls.db "CREATE INDEX X_CUI2_MRCONREL ON MRCONREL(CUI);"
    # sqlite3 umls.db "CREATE INDEX X_AUI_MRCONREL ON MRCONREL(AUI);"
    echo "-> successfully indexed table MRCONREL."

    # create optimized lookup table for concepts & semantic type -> 'MRCONSTY'
    echo "-> Creating 'optimized' table which includes contents from MRCONSO & MRSTY -> 'MRCONSTY'."
    sqlite3 umls.db """CREATE TABLE MRCONSTY AS SELECT AUI, CUI, SUI, LUI, SAB, CODE, SCUI, STR, TTY FROM MRCONSO WHERE SUPPRESS = 'N' AND TS = 'P' AND ISPREF = 'Y' AND STT = 'PF';"""
    sqlite3 umls.db "ALTER TABLE MRCONSTY ADD COLUMN STY TEXT"
    sqlite3 umls.db "CREATE INDEX X_CUI_MRCONSTY ON MRCONSTY(CUI)"
    sqlite3 umls.db "UPDATE MRCONSTY SET STY = (SELECT GROUP_CONCAT(MRSTY.STY, ';') FROM MRSTY WHERE MRSTY.CUI = MRCONSTY.CUI GROUP BY MRSTY.CUI"
else
    echo "=> umls.db already exists."
fi
