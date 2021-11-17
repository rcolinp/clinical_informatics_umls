#!/bin/sh

# Create a UMLS 2021AB SQLite Database.

# Invoke script as follows:
# -> sh create_umls_2021AB_sqlite3.sh < insert absolute OR relative path to UMLS .RRF directory >
# i.e. `sh create_umls_2021AB_sqlite3.sh `../UMLS/subset/2021AB`

# Note: 4 files - SRDEF, SRSTR, SRSTRE1 & SRSTRE2 need to be moved into the `META` directory from the`NET` directory s/p MetamorphoSys.
# Both `META` and `NET` should be located via relative path ../UMLS/subset/2021AB/

if [ ! -e umls.db ]; then
	if [ ! -d "$1" ]; then
		echo "Provide the path to the UMLS install directory as first argument when invoking this script. Download the latest version here: http://www.nlm.nih.gov/research/umls/licensedcontent/umlsknowledgesources.html (should check which file is needed)"
		exit 1
	fi
	if [ ! -d "$1/META" ]; then
		echo "There is no directory named META in the install directory you provided. Download the latest version here: http://www.nlm.nih.gov/research/umls/licensedcontent/umlsknowledgesources.html"
		exit 1
	fi

	# convert RRF files (strip last pipe and remove quote (") characters, those are giving SQLite troubles)
	if [ ! -e "$1/META/MRDEF.pipe" ]; then
		current=$(pwd)
		cd "$1/META"
		echo "-> Converting RRF files for SQLite"
		for f in MRDOC.RRF MRCONSO.RRF MRHIER.RRF MRRANK.RRF MRREL.RRF SRDEF SRSTR SRSTRE1 SRSTRE2 MRSAB.RRF MRSTY.RRF MRSAT.RRF; do
			sed -e 's/.$//' -e 's/"//g' "$f" >"${f%RRF}pipe"
		done
		cd $current
	fi

	# init the database for MRDEF
	# table structure here: http://www.ncbi.nlm.nih.gov/books/NBK9685/
	sqlite3 umls.db "CREATE TABLE MRDEF (
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
	
	# init the database for MRDOC
	# table structure here: http://www.ncbi.nlm.nih.gov/books/NBK9685/
	sqlite3 umls.db "CREATE TABLE MRDOC (
		DOCKEY varchar,
		VALUE varchar,
		TYPE varchar,
		EXPL varchar
    )"
	
	# init the database for MRSAB
	sqlite3 umls.db "CREATE TABLE MRSAB (
		VCUI varchar,
		RCUI varchar,
		VSAB varchar
			constraint MRSAB_pk
				primary key,
		RSAB varchar,
		SON text,
		SF varchar,
		SVER varchar,
		VSTART varchar,
		VEND varchar,
		IMETA varchar,
		RMETA varchar,
		SLC text,
		SCC text,
		SRL varchar,
		TFR varchar,
		CFR varchar,
		CXTY varchar,
		TTYL varchar,
		ATNL text,
		LAT varchar,
		CENC varchar,
		CURVER varchar,
		SABIN varchar,
		SSN text,
		SCIT text
	)"
	
	# init the database for MRCONSO
	# Skip the constraint (primary key) on AUI for quicker loading
	sqlite3 umls.db "CREATE TABLE MRCONSO (
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
	
	# init the database for SRDEF
	sqlite3 umls.db "CREATE TABLE SRDEF (
    	RT varchar,
   	    UI varchar,
   	    STY_RL text,
		STN_RTN varchar,
		DEF text,
		EX varchar,
		UN text,
		NH varchar,
		ABR varchar,
		RIN varchar
    )"
	
	# init the database for SRSTR
	sqlite3 umls.db "CREATE TABLE SRSTR (
		STY_RL1 text,
		RL varchar,
		STY_RL2 text,
		LS varchar
	)"
	
	# init the database for SRSTRE1
	sqlite3 umls.db "CREATE TABLE SRSTRE1 (
    	UI1 varchar,
    	UI2 varchar,
    	UI3 varchar
	)"
	
	# init the database for SRSTRE2
	sqlite3 umls.db "CREATE TABLE SRSTRE2 (
		STY1 text,
		RL varchar,
		STY2 text
    )"
	
	# init the database for MRRANK
	sqlite3 umls.db "CREATE TABLE MRRANK (
		MRRANK_RANK varchar,
		SAB varchar,
		TTY varchar,
		SUPPRESS varchar
    )"
	
	# init the database for MRSTY
	# Skip the constraint (primary key) on ATUI for quicker loading
	sqlite3 umls.db "CREATE TABLE MRSTY (
		CUI varchar,
		TUI varchar,
		STN varchar,
		STY text,
		ATUI varchar
			constraint MRSTY_pk
				primary key,
		CVF varchar
    )"
	
	# init the database for MRREL
	# Skip the constraint (primary key) on RUI for quicker loading
	sqlite3 umls.db "CREATE TABLE MRREL (
		CUI1 varchar,
		AUI1 varchar,
		STYPE1 varchar,
		REL varchar,
		CUI2 varchar,
		AUI2 varchar,
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
	# Skip the constraint (primary key) on ATUI for quicker loading
	sqlite3 umls.db "CREATE TABLE MRSAT (
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
	
	# init the database for MRHIER
	sqlite3 umls.db "CREATE TABLE MRHIER (
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
	 
	# import tables
	for f in "$1/META/"*.pipe; do
		table=$(basename ${f%.pipe})
		echo "-> Importing $table"
		sqlite3 umls.db ".import '$f' '$table'"
	done

	# create indexes
	echo "-> Creating indexes"
	sqlite3 umls.db "CREATE INDEX X_CUI_MRCONSO ON MRCONSO (CUI);"
	sqlite3 umls.db "CREATE INDEX X_CUI_MRSTY ON MRSTY (CUI);"
	sqlite3 umls.db "CREATE INDEX X_STY_MRSTY ON MRSTY (STY);"
	sqlite3 umls.db "CREATE INDEX X_AUI_MRHIER ON MRHIER (AUI);"
	sqlite3 umls.db "CREATE INDEX X_PAUI_MRHIER ON MRHIER (PAUI);"
	sqlite3 umls.db "CREATE INDEX X_CUI1_MRREL ON MRREL (CUI1);"
	sqlite3 umls.db "CREATE INDEX X_CUI2_MRREL ON MRREL (CUI2);"
	sqlite3 umls.db "CREATE INDEX X_CUI_MRSAT ON MRSAT (CUI);"
	echo "-> successfully finished creating desired indexes"

	# create faster lookup table
	echo "-> Creating fast lookup table"
	sqlite3 umls.db "CREATE TABLE lookup AS SELECT DISTINCT AUI, SUI, LUI, CUI, SCUI, SDUI, SAB, CODE, STR, TTY, ISPREF, TS, STT FROM MRCONSO WHERE SUPPRESS = 'N' AND SAB IN ('ATC', 'GO', 'HGNC', 'HPO', 'ICD9CM', 'ICD10CM', 'ICD10PCS', 'LNC', 'MDR', 'MED-RT', 'NCI', 'NCBI', 'RXNORM', 'SNOMEDCT_US')"
	sqlite3 umls.db "ALTER TABLE lookup ADD COLUMN STY text"
	sqlite3 umls.db "CREATE INDEX X_CUI_lookup ON lookup (CUI)"
	sqlite3 umls.db "UPDATE lookup SET STY = (SELECT DISTINCT GROUP_CONCAT(MRSTY.STY, '|') FROM MRSTY WHERE MRSTY.CUI = lookup.CUI GROUP BY MRSTY.CUI)"
else
	echo "=> umls.db already exists"
fi
###################################################################################################################
# References:                                                                                                     #
# Above was modified from following GitHub Repository -> https://github.com/chb/py-umls                           #
## Specifically the following script -> https://github.com/chb/py-umls/blob/master/databases/umls.sh (Cheers!)    #
##################################################################################################################
