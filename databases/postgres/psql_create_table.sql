/*
 PostgresSQL database create tables .sql (NOTE: please modify path to .RRF files)
 */
DROP TABLE IF EXISTS MRCOLS;
CREATE TABLE MRCOLS
(
    COL   varchar(20),
    DES   varchar(200),
    REF   varchar(20),
    MIN   int,
    AV    numeric(5, 2),
    MAX   int,
    FIL   varchar(50),
    DTY   varchar(20),
    dummy char(1)
);

COPY MRCOLS
    from 'MRCOLS.RRF' with delimiter AS '|' null as '';
;
alter table mrcols
    drop column dummy;
;
DROP TABLE IF EXISTS MRCONSO;
CREATE TABLE MRCONSO
(
    CUI      char(8)     NOT NULL,
    LAT      char(3)     NOT NULL,
    TS       char(1)     NOT NULL,
    LUI      char(8)     NOT NULL,
    STT      varchar(3)  NOT NULL,
    SUI      char(8)     NOT NULL,
    ISPREF   char(1)     NOT NULL,
    AUI      varchar(9)  NOT NULL,
    SAUI     varchar(50),
    SCUI     varchar(50),
    SDUI     varchar(50),
    SAB      varchar(20) NOT NULL,
    TTY      varchar(20) NOT NULL,
    CODE     varchar(50) NOT NULL,
    STR      text        NOT NULL,
    SRL      int         NOT NULL,
    SUPPRESS char(1)     NOT NULL,
    CVF      int,
    dummy    char(1)
);
copy MRCONSO
    from 'MRCONSO.RRF' with delimiter as '|' null as '';
alter table mrconso
    drop column dummy;
DROP TABLE IF EXISTS MRCUI;
CREATE TABLE MRCUI
(
    CUI1      varchar NOT NULL,
    VER       varchar NOT NULL,
    REL       varchar NOT NULL,
    RELA      varchar,
    MAPREASON text,
    CUI2      varchar,
    MAPIN     varchar(1),
    dummy     varchar(1)
);
copy MRCUI
    from 'MRCUI.RRF' with delimiter as '|' null as '';
alter table mrcui
    drop column dummy;
DROP TABLE IF EXISTS MRSAT;
CREATE TABLE MRSAT
(
    CUI      varchar NOT NULL,
    LUI      varchar,
    SUI      varchar,
    METAUI   varchar,
    STYPE    varchar NOT NULL,
    CODE     varchar,
    ATUI     varchar NOT NULL,
    SATUI    varchar,
    ATN      varchar NOT NULL,
    SAB      varchar NOT NULL,
    ATV      text,
    SUPPRESS varchar NOT NULL,
    CVF      varchar,
    dummy    char(1)
);
COPY mrsat
    from 'MRSAT.RRF' with delimiter as '|' null as '';
alter table mrsat
    drop column dummy;
DROP TABLE IF EXISTS MRDEF;
CREATE TABLE MRDEF
(
    CUI      char(8)     NOT NULL,
    AUI      varchar(9)  NOT NULL,
    ATUI     varchar(10) NOT NULL,
    SATUI    varchar(50),
    SAB      varchar(20) NOT NULL,
    DEF      text        NOT NULL,
    SUPPRESS char(1)     NOT NULL,
    CVF      int,
    dummy    char(1)
);
copy MRDEF
    from 'MRDEF.RRF' with delimiter as '|' null as '';
alter table mrdef
    drop column dummy;
DROP TABLE IF EXISTS MRDOC;
CREATE TABLE MRDOC
(
    DOCKEY varchar(50) NOT NULL,
    VALUE  varchar(200),
    TYPE   varchar(50) NOT NULL,
    EXPL   text,
    dummy  char(1)
);
copy MRDOC
    from 'MRDOC.RRF' with delimiter as '|' null as '';
alter table mrdoc
    drop column dummy;
DROP TABLE IF EXISTS MRFILES;
CREATE TABLE MRFILES
(
    FIL   varchar(50),
    DES   varchar(200),
    FMT   text,
    CLS   int,
    RWS   int,
    BTS   bigint,
    dummy char(1)
);
copy MRFILES
    from 'MRFILES.RRF' with delimiter as '|' null as '';
alter table mrfiles
    drop column dummy;
DROP TABLE IF EXISTS MRHIER;
CREATE TABLE MRHIER
(
    CUI   char(8)     NOT NULL,
    AUI   varchar(9)  NOT NULL,
    CXN   int         NOT NULL,
    PAUI  varchar(9),
    SAB   varchar(20) NOT NULL,
    RELA  varchar(100),
    PTR   text,
    HCD   varchar(50),
    CVF   int,
    dummy char(1)
);
copy MRHIER
    from 'MRHIER.RRF' with delimiter as '|' null as '';
alter table mrhier
    drop column dummy;
DROP TABLE IF EXISTS MRHIST;
CREATE TABLE MRHIST
(
    CUI        char(8)     NOT NULL,
    SOURCEUI   varchar(50) NOT NULL,
    SAB        varchar(20) NOT NULL,
    SVER       varchar(20) NOT NULL,
    CHANGETYPE text        NOT NULL,
    CHANGEKEY  text        NOT NULL,
    CHANGEVAL  text        NOT NULL,
    REASON     text,
    CVF        int,
    dummy      char(1)
);
copy MRHIST
    from 'MRHIST.RRF' with delimiter as '|' null as '';
alter table mrhist
    drop column dummy;
DROP TABLE IF EXISTS MRMAP;
CREATE TABLE MRMAP
(
    MAPSETCUI   char(8),
    MAPSETSAB   varchar(20),
    MAPSUBSETID varchar(10),
    MAPRANK     int,
    MAPID       varchar(50),
    MAPSID      varchar(50),
    FROMID      varchar(50),
    FROMSID     varchar(50),
    FROMEXPR    text,
    FROMTYPE    varchar(50),
    FROMRULE    text,
    FROMRES     text,
    REL         varchar(4),
    RELA        varchar(100),
    TOID        varchar(50),
    TOSID       varchar(50),
    TOEXPR      text,
    TOTYPE      varchar(50),
    TORULE      text,
    TORES       text,
    MAPRULE     text,
    MAPRES      text,
    MAPTYPE     varchar(50),
    MAPATN      varchar(20),
    MAPATV      text,
    CVF         int,
    dummy       char(1)
);
copy MRMAP
    from 'MRMAP.RRF' with delimiter as '|' null as '';
alter table mrmap
    drop column dummy;
DROP TABLE IF EXISTS MRRANK;
CREATE TABLE MRRANK
(
    RANK     int         NOT NULL,
    SAB      varchar(20) NOT NULL,
    TTY      varchar(20) NOT NULL,
    SUPPRESS char(1)     NOT NULL,
    dummy    char(1)
);
copy MRRANK
    from 'MRRANK.RRF' with delimiter as '|' null as '';
alter table mrrank
    drop column dummy;
DROP TABLE IF EXISTS MRREL;
CREATE TABLE MRREL
(
    CUI1     char(8)     NOT NULL,
    AUI1     varchar(9),
    STYPE1   varchar(50) NOT NULL,
    REL      varchar(4)  NOT NULL,
    CUI2     char(8)     NOT NULL,
    AUI2     varchar(9),
    STYPE2   varchar(50) NOT NULL,
    RELA     varchar(100),
    RUI      varchar(10) NOT NULL,
    SRUI     varchar(50),
    SAB      varchar(20) NOT NULL,
    SL       varchar(20) NOT NULL,
    RG       varchar(10),
    DIR      varchar(1),
    SUPPRESS char(1)     NOT NULL,
    CVF      int,
    dummy    char(1)
);
copy MRREL
    from 'MRREL.RRF' with delimiter as '|' null as '';
alter table mrrel
    drop column dummy;
DROP TABLE IF EXISTS MRSAB;
CREATE TABLE MRSAB
(
    VCUI   char(8),
    RCUI   char(8)     NOT NULL,
    VSAB   varchar(20) NOT NULL,
    RSAB   varchar(20) NOT NULL,
    SON    text        NOT NULL,
    SF     varchar(20) NOT NULL,
    SVER   varchar(20),
    VSTART char(10),
    VEND   char(10),
    IMETA  varchar(10) NOT NULL,
    RMETA  varchar(10),
    SLC    text,
    SCC    text,
    SRL    int         NOT NULL,
    TFR    int,
    CFR    int,
    CXTY   varchar(50),
    TTYL   varchar(200),
    ATNL   text,
    LAT    char(3),
    CENC   varchar(20) NOT NULL,
    CURVER char(1)     NOT NULL,
    SABIN  char(1)     NOT NULL,
    SSN    text        NOT NULL,
    SCIT   text        NOT NULL,
    dummy  char(1)
);
copy MRSAB
    from 'MRSAB.RRF' with delimiter as '|' null as '';
alter table mrsab
    drop column dummy;
DROP TABLE IF EXISTS MRSAT;
CREATE TABLE MRSAT
(
    CUI      varchar NOT NULL,
    LUI      varchar,
    SUI      varchar,
    METAUI   varchar,
    STYPE    varchar NOT NULL,
    CODE     varchar,
    ATUI     varchar NOT NULL,
    SATUI    varchar,
    ATN      varchar NOT NULL,
    SAB      varchar NOT NULL,
    ATV      text,
    SUPPRESS varchar NOT NULL,
    CVF      varchar,
    dummy    char(1)
);
copy MRSAT
    from 'MRSAT.RRF' with delimiter as '|' null as '';
alter table mrsat
    drop column dummy;
DROP TABLE IF EXISTS MRSMAP;
CREATE TABLE MRSMAP
(
    MAPSETCUI char(8),
    MAPSETSAB varchar(20),
    MAPID     varchar(50),
    MAPSID    varchar(50),
    FROMEXPR  text,
    FROMTYPE  varchar(50),
    REL       varchar(4),
    RELA      varchar(100),
    TOEXPR    text,
    TOTYPE    varchar(50),
    CVF       int,
    dummy     char(1)
);
copy MRSMAP
    from 'MRSMAP.RRF' with delimiter as '|' null as '';
alter table mrsmap
    drop column dummy;
DROP TABLE IF EXISTS MRSTY;
CREATE TABLE MRSTY
(
    CUI   char(8)      NOT NULL,
    TUI   char(4)      NOT NULL,
    STN   varchar(100) NOT NULL,
    STY   varchar(50)  NOT NULL,
    ATUI  varchar(10)  NOT NULL,
    CVF   int,
    dummy char(1)
);
copy MRSTY
    from 'MRSTY.RRF' with delimiter as '|' null as '';
alter table mrsty
    drop column dummy;
DROP TABLE IF EXISTS MRXNS_ENG;
CREATE TABLE MRXNS_ENG
(
    LAT   char(3) NOT NULL,
    NSTR  text    NOT NULL,
    CUI   char(8) NOT NULL,
    LUI   char(8) NOT NULL,
    SUI   char(8) NOT NULL,
    dummy char(1)
);
copy MRXNS_ENG
    from 'MRXNS_ENG.RRF' with delimiter as '|' null as '';
alter table mrxns_eng
    drop column dummy;
DROP TABLE IF EXISTS MRXNW_ENG;
CREATE TABLE MRXNW_ENG
(
    LAT   char(3)      NOT NULL,
    NWD   varchar(100) NOT NULL,
    CUI   char(8)      NOT NULL,
    LUI   char(8)      NOT NULL,
    SUI   char(8)      NOT NULL,
    dummy char(1)
);
copy MRXNW_ENG
    from 'MRXNW_ENG.RRF' with delimiter as '|' null as '';
alter table mrxnw_eng
    drop column dummy;
DROP TABLE IF EXISTS MRAUI;
CREATE TABLE MRAUI
(
    AUI1      varchar(9)  NOT NULL,
    CUI1      char(8)     NOT NULL,
    VER       varchar(10) NOT NULL,
    REL       varchar(4),
    RELA      varchar(100),
    MAPREASON text        NOT NULL,
    AUI2      varchar(9)  NOT NULL,
    CUI2      char(8)     NOT NULL,
    MAPIN     char(1)     NOT NULL,
    dummy     char(1)
);
copy MRAUI
    from 'MRAUI.RRF' with delimiter as '|' null as '';
alter table mraui
    drop column dummy;
DROP TABLE IF EXISTS MRXW_ENG;
CREATE TABLE MRXW_ENG
(
    LAT   char(3)      NOT NULL,
    WD    varchar(100) NOT NULL,
    CUI   char(8)      NOT NULL,
    LUI   char(8)      NOT NULL,
    SUI   char(8)      NOT NULL,
    dummy char(1)
);
copy MRXW_ENG
    from 'MRXW_ENG.RRF' with delimiter as '|' null as '';
alter table mrxw_eng
    drop column dummy;
DROP TABLE IF EXISTS AMBIGSUI;
CREATE TABLE AMBIGSUI
(
    SUI   char(8) NOT NULL,
    CUI   char(8) NOT NULL,
    dummy char(1)
);
copy AMBIGSUI
    from 'AMBIGSUI.RRF' with delimiter as '|' null as '';
alter table ambigsui
    drop column dummy;
DROP TABLE IF EXISTS AMBIGLUI;
CREATE TABLE AMBIGLUI
(
    LUI   char(8) NOT NULL,
    CUI   char(8) NOT NULL,
    dummy char(1)
);
copy AMBIGLUI
    from 'AMBIGLUI.RRF' with delimiter as '|' null as '';
alter table ambiglui
    drop column dummy;
DROP TABLE IF EXISTS DELETEDCUI;
CREATE TABLE DELETEDCUI
(
    PCUI  char(8) NOT NULL,
    PSTR  text    NOT NULL,
    dummy char(1)
);
copy DELETEDCUI
    from 'DELETEDCUI.RRF' with delimiter as '|' null as '';
alter table deletedcui
    drop column dummy;
DROP TABLE IF EXISTS DELETEDLUI;
CREATE TABLE DELETEDLUI
(
    PLUI  char(8) NOT NULL,
    PSTR  text    NOT NULL,
    dummy char(1)
);
copy DELETEDLUI
    from 'DELETEDLUI.RRF' with delimiter as '|' null as '';
alter table deletedlui
    drop column dummy;
DROP TABLE IF EXISTS DELETEDSUI;
CREATE TABLE DELETEDSUI
(
    PSUI  char(8) NOT NULL,
    LAT   char(3) NOT NULL,
    PSTR  text    NOT NULL,
    dummy char(1)
);
copy DELETEDSUI
    from 'DELETEDSUI.RRF' with delimiter as '|' null as '';
alter table deletedsui
    drop column dummy;
DROP TABLE IF EXISTS MERGEDCUI;
CREATE TABLE MERGEDCUI
(
    PCUI  char(8) NOT NULL,
    CUI   char(8) NOT NULL,
    dummy char(1)
);
copy MERGEDCUI
    from 'MERGEDCUI.RRF' with delimiter as '|' null as '';
alter table mergedcui
    drop column dummy;
DROP TABLE IF EXISTS MERGEDLUI;
CREATE TABLE MERGEDLUI
(
    PLUI  char(8),
    LUI   char(8),
    dummy char(1)
);
copy MERGEDLUI
    from 'MERGEDLUI.RRF' with delimiter as '|' null as '';
alter table mergedlui
    drop column dummy;