import csv
import sqlite3

import numpy as np
import pandas as pd


class SQLite:
    def __init__(self, db_path: str):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connection.close()

    def execute_query(self, query: str, file_name: str) -> str:
        """ """
        try:
            # Execute the query
            self.cursor.execute(query)
            # Fetch all rows of the query result
            result = self.cursor.fetchall()
            # Get the column names from the cursor description
            column_names = [desc[0] for desc in self.cursor.description]
            # Write the result to csv file
            with open(file_name, "w") as csvfile:
                writer = csv.writer(
                    csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
                )
                # Write the column names as the first row in the file
                writer.writerow(column_names)
                # Write the data rows
                for row in result:
                    writer.writerow(row)
            print(f"{file_name} :{len(result)}  records exported")
        except Exception as e:
            print(f"Error while executing query: {e}")
            raise e
        # finally:
        #     self.cursor.close()
        #     self.connection.close()
        return f"{file_name} exported"

    def get_cui_nodes(self, file_name: str = "../import/cuiNodes.csv") -> str:
        """ """
        query = "SELECT DISTINCT CUI AS `CuiId:ID`, STR AS name, 'Cui' AS `:LABEL` FROM MRCONSO WHERE SUPPRESS = 'N';"
        return self.execute_query(query, file_name)

    def get_cui_set(self, file_name: str = "../import/cuiNodes.csv"):
        df = pd.read_csv(file_name, sep=",")
        return set(df["CuiId:ID"])

    def get_aui_nodes(self, file_name: str = "../import/auiNodes.csv") -> str:
        """ """
        cui_set = self.get_cui_set()
        query = f"""
        SELECT DISTINCT AUI as `AuiId:ID`, STR AS name, SAB AS sab, CODE AS code, 
                        TTY AS tty, ISPREF AS ispref, TS AS ts, STT AS stt, 'Aui' AS `:LABEL` 
        FROM MRCONSO WHERE CUI IN {tuple(cui_set)} AND SUPPRESS = 'N';"""
        return self.execute_query(query, file_name)

    def get_sty_nodes(self, file_name: str = "../import/styNodes.csv") -> str:
        """ """
        cui_set = self.get_cui_set()
        query = f"SELECT DISTINCT TUI as `TuiId:ID`, STY as sty, STN as stn, 'SemanticType' AS `:LABEL` FROM MRSTY WHERE CUI IN {tuple(cui_set)};"
        return self.execute_query(query, file_name)

    def get_code_nodes(self, file_name: str = "../import/codeNodes.csv") -> str:
        """ """
        cui_set = self.get_cui_set()
        query = f"""
        SELECT DISTINCT (SAB||'#'||CODE) AS `CodeId:ID`, SAB as sab, CODE as code, ('Code'||';'||SAB) AS `:LABEL` 
        FROM MRCONSO 
        WHERE CUI IN {tuple(cui_set)};
        """
        return self.execute_query(query, file_name)

    def get_has_aui_rels(self, file_name: str = "../import/has_aui.csv") -> str:
        """ """
        cui_set = self.get_cui_set()
        query = f"""
            SELECT DISTINCT (SAB || '#' || CODE) AS `:START_ID`, AUI AS `:END_ID`, 'HAS_AUI' AS `:TYPE`
            FROM MRCONSO 
            WHERE CUI IN {tuple(cui_set)};
            """
        return self.execute_query(query, file_name)

    def get_has_cui_rels(self, file_name: str = "../import/has_cui.csv") -> str:
        """ """
        cui_set = self.get_cui_set()
        query = f"""
         SELECT DISTINCT AUI as `:START_ID`, CUI as `:END_ID`, 'HAS_CUI' AS `:TYPE`
         FROM MRCONSO
         WHERE CUI IN {tuple(cui_set)};
         """
        return self.execute_query(query, file_name)

    def get_has_sty_rels(self, file_name: str = "../import/has_sty.csv") -> str:
        """ """
        cui_set = self.get_cui_set()
        query = f"""
        SELECT DISTINCT CUI AS `:START_ID`, TUI AS `:END_ID`, 'HAS_STY' AS `:TYPE`
        FROM MRSTY
        WHERE CUI IN {tuple(cui_set)};
        """
        return self.execute_query(query, file_name)

    def get_parent_child_rels(
        self, file_name: str = "../import/parent_child_rels.csv"
    ) -> str:
        """"""
        cui_set = self.get_cui_set()
        query = f"""
        SELECT DISTINCT h.PAUI AS `:START_ID`, c.AUI AS `:END_ID`, 'CHILD_OF' AS `:TYPE`
        FROM MRHIER h
        JOIN MRCONSO c ON h.AUI = c.AUI
        JOIN MRCONSO c2 ON h.PAUI = c2.AUI
        WHERE h.CUI IN {tuple(cui_set)};   
        """
        return self.execute_query(query, file_name)

    def get_cui_code_rels(self, file_name: str = "../import/cui_code_rel.csv") -> str:
        cui_set = self.get_cui_set()
        query = f"""
        SELECT DISTINCT CUI AS `:START_ID`, (SAB || '#' || CODE) AS `:END_ID`, 'HAS_SOURCE_CODE' AS `:TYPE`
        FROM MRCONSO
        WHERE CUI IN {tuple(cui_set)};
        """
        return self.execute_query(query, file_name)

    def get_icdo3_code_nodes(self, file_name: str = "../import/icdoNode.csv") -> str:
        cui_set = self.get_cui_set()
        query = f"""
        SELECT DISTINCT ATV AS code, (SAB||'#'||CODE) AS `:END_ID`, SAB AS sab
        FROM MRSAT
        WHERE SAB = 'NCI'
        AND ATN = 'ICD-O-3_CODE'
        AND CUI IN {tuple(cui_set)};        
        """
        self.execute_query(query, file_name)
        df = pd.read_csv("../import/icdoNode.csv", sep=",")
        df2 = pd.read_csv("../import/cui_code_rel.csv", sep=",")
        df["sab"] = "ICDO3"
        df["CodeId:ID"] = df["sab"] + "#" + df["code"]
        df[":LABEL"] = "Code" + ";" + df["sab"]
        df[["CodeId:ID", "sab", "code", ":LABEL"]].to_csv(
            path_or_buf="../import/codeNodes.csv",
            mode="a",
            header=False,
            index=False,
        )
        df3 = df.merge(df2, how="inner", on=":END_ID")

        df3[":TYPE"] = "HAS_SOURCE_CODE"
        df_final = (
            df3[[":START_ID", "CodeId:ID", ":TYPE"]]
            .rename({"CodeId:ID": ":END_ID"}, axis=1)
            .drop_duplicates()
            .replace(np.nan, "")
        )

        df_final.to_csv(
            path_or_buf="../import/cui_code_rel.csv",
            mode="a",
            header=False,
            index=False,
        )

    def get_concept_concept_rels(
        self, query: str, file_path: str = "../import/cui_cui_rel.csv"
    ):
        cui_set = self.get_cui_set()
        query = f"""
        WITH query AS (
            SELECT DISTINCT SAB
            FROM MRCONSO
            WHERE CUI IN {tuple(cui_set)})
        SELECT MRREL.CUI2, MRREL.CUI1, CASE WHEN MRREL.RELA = '' THEN MRREL.REL ELSE MRREL.RELA END AS relationship, MRREL.SAB AS sab
        FROM MRREL
        JOIN query ON MRREL.SAB = query.SAB
        GROUP BY 1, 2, 3, 4;
        """
        df = pd.read_sql_query(query, self.connection)
        df.columns = [":START_ID", ":END_ID", ":TYPE", "sab"]
        df = df[(df[":START_ID"] != df[":END_ID"]) & (df[":TYPE"] != "SIB") & (
            df[":TYPE"] != "SY")].drop_duplicates().replace(np.nan, "")
        df[":TYPE"] = df[":TYPE"].str.upper()
        df[":TYPE"] = df[":TYPE"].str.replace("-", "_")
        df.to_csv(
            path_or_buf=file_path,
            header=True,
            index=False
        )

        return df


if __name__ == "__main__":
    sqlite = SQLite(db_path="../sqlite/umls_py.db")
    sqlite.get_cui_nodes()
    sqlite.get_aui_nodes()
    sqlite.get_sty_nodes()
    sqlite.get_code_nodes()
    sqlite.get_has_aui_rels()
    sqlite.get_has_cui_rels()
    sqlite.get_has_sty_rels()
    sqlite.get_parent_child_rels()
    sqlite.get_cui_code_rels()
    sqlite.get_icdo3_code_nodes()
    sqlite.get_concept_concept_rels()
