#!/bin/sh

# Create a UMLS 2021AA SQLite3 Database.
# Example command to invoke script:
# --> `sh create_umls_2021AA_sqlite3.sh /Users/rob/Documents/UMLS/subset/2021AA`
# ---> where `UMLS` is the installation directory containing one or many subsets created via UMLS metamorphoSys. If you have multiple subsets, point the script to the corresponding subset of interest. The 2021AA directory should contain the directories generated via UMLS metamorphoSys (i.e. META, NET, LEX).

# Please note: Two files (SRDEF & SRSTRE1) were moved into the META directory from where they will naturally exist within the NET directory s/p successful run of UMLS metamorphoSys. 
# Refer to relative directory ../UMLS included in this repository as a 'reference' AND/OR check  

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
		for f in MRDEF.RRF MRDOC.RRF SRDEF SRSTRE1 MRSAB.RRF MRCONSO.RRF MRRANK.RRF MRSTY.RRF MRREL.RRF MRSAT.RRF MRHIER.RRF ; do
				sed -e 's/.$//' -e 's/"//g' "$f" > "${f%RRF}pipe"
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
        STY_RL varchar,
		STN_RTN varchar,
		DEF TEXT,
		EX varchar,
		UN TEXT,
		NH varchar,
		ABR varchar,
		RIN varchar
	)"

    # init the database for SRSTRE1
    sqlite3 umls.db "CREATE TABLE SRSTRE1 (
    	UI1 varchar,
    	UI2 varchar,
    	UI3 varchar
    )"

	# init the database for MRRANK
	sqlite3 umls.db "CREATE TABLE MRRANK (
		MRRANK_RANK varchar,
		SAB varchar,
		TTY varchar,
		SUPPRESS varchar
	)"

	# init the database for MRSTY
	sqlite3 umls.db "CREATE TABLE MRSTY (
		CUI varchar,
		TUI varchar,
		STN varchar,
		STY text,
		ATUI varchar,
		CVF varchar
	)"

	# init the database for MRREL
	sqlite3 umls.db "CREATE TABLE MRREL (
		CUI1 varchar,
		AUI1 varchar,
		STYPE1 varchar,
		REL varchar,
		CUI2 varchar,
		AUI2 text,
		STYPE2 varchar,
		RELA varchar,
		RUI varchar,
		SRUI varchar,
		SAB varchar,
		SL varchar,
		RG varchar,
		DIR varchar,
		SUPPRESS varchar,
		CVF varchar
	)"

	# init the database for MRSAT
	sqlite3 umls.db "CREATE TABLE MRSAT (
		CUI varchar,
		LUI varchar,
		SUI varchar,
		METAUI varchar,
		STYPE varchar,
		CODE varchar,
		ATUI varchar,
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
	sqlite3 umls.db "CREATE INDEX X_CUI_MRDEF ON MRDEF(CUI);"
	sqlite3 umls.db "CREATE INDEX X_SAB_MRDEF ON MRDEF(SAB);"
	sqlite3 umls.db "CREATE INDEX X_CUI_MRCONSO ON MRCONSO(CUI);"
	# sqlite3 umls.db "CREATE INDEX X_ISPREF_MRCONSO ON MRCONSO(ISPREF);"
	# sqlite3 umls.db "CREATE INDEX X_TS_MRCONSO ON MRCONSO(TS);"
	# sqlite3 umls.db "CREATE INDEX X_STT_MRCONSO ON MRCONSO(STT);"
	sqlite3 umls.db "CREATE INDEX X_SAB_MRCONSO ON MRCONSO(SAB);"
	sqlite3 umls.db "CREATE INDEX X_CUI_MRSTY ON MRSTY(CUI);"
	sqlite3 umls.db "CREATE INDEX X_TUI_MRSTY ON MRSTY(TUI);"
	sqlite3 umls.db "CREATE INDEX X_AUI_MRHIER ON MRHIER(AUI);"
	# sqlite3 umls.db "CREATE INDEX X_SAB_MRHIER ON MRHIER(SAB);"
	sqlite3 umls.db "CREATE INDEX X_PAUI_MRHIER ON MRHIER(PAUI);"
	sqlite3 umls.db "CREATE INDEX X_CUI1_MRREL ON MRREL(CUI1);"
	sqlite3 umls.db "CREATE INDEX X_CUI2_MRREL ON MRREL(CUI2);"
	sqlite3 umls.db "CREATE INDEX X_CUI_MRSAT ON MRSAT(CUI);"
	# sqlite3 umls.db "CREATE INDEX X_METAUI_MRSAT ON MRSAT(METAUI);"
	sqlite3 umls.db "CREATE INDEX X_SAB_MRSAT ON MRSAT(SAB);"
	# sqlite3 umls.db "CREATE INDEX X_ATN_MRSAT ON MRSAT(ATN);"
	# sqlite3 umls.db "CREATE INDEX X_CODE_MRSAT ON MRSAT(CODE);"
	echo "-> successfully finished creating desired indexes"
	echo "-> UMLS 2021AA local sqlite3 database build job succesfully complete."
else
	echo "=> umls.db already exists"
fi
###################################################################################################################
# References:                                                                                                     #
# Above was modified from following GitHub Repository -> https://github.com/chb/py-umls                           #
## Specifically the following script -> https://github.com/chb/py-umls/blob/master/databases/umls.sh (Cheers!)    #
###################################################################################################################