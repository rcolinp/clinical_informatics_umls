# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This .py assumes you have created an output directory named 'import' at your
    root directory (i.e. $HOME/import).
This .py assumes you are a UMLS license holder & MRHIER.RRF is located at the
    relative path -> ../UMLS/subset/2021AB/META/MRHIER.RRF

Note: script run time will range from 30 seconds to 20 minutes depending on
    vocabularies included in sab_list.
    -> This script can be broken down into smaller components and/or leverage
        more a more efficient python library/libraries (rather than pandas).
    -> relative directory ../conf/config.prop contains properties file used
        at creation of this script.

"""

import sys

if not sys.warnoptions:
    import warnings

    warnings.simplefilter("ignore")

import numpy as np
import pandas as pd
import getpass

####################################################################
root = "Users"  # root directory
home = getpass.getuser()
path_to_mrhier = "../UMLS/subset/2022AA/META/MRHIER.RRF"
####################################################################

# Read MRHIER.RRF
# Script assumes MRHIER.RRF is located in the relative directory ->
# ../UMLS/subset/2021AB/META/MRHIER.RRF


def read_transform_mrhier(path_to_mrhier: str):
    """
    Summary:
    --------

    Parameters:
    -----------

    Returns:
    --------

    """
    mrhier_rrf = pd.read_csv(path_to_mrhier, sep="|", header=None, dtype=object)
    # sab_list should contain same vocabs used in `nodes_edges_part1.py`
    sab_list = ["ATC", "GO", "ICD10CM", "NCI", "SNOMEDCT_US", "RXNORM"]
    # Where axis=1 drop 9th index (align columns correctly)
    # -> .RRF has extra column that needs to be dropped)
    mrhier = mrhier_rrf.drop(9, axis=1)
    print("Complete - MRHIER.RRF read in as .csv and empty column dropped")

    # Assign column names (preserving source assigned names from UMLS)
    mrhier.columns = ["CUI", "AUI", "CXN", "PAUI", "SAB", "RELA", "PTR", "HCD", "CVF"]
    mrhier = mrhier[mrhier["SAB"].isin(sab_list)].drop_duplicates().replace(np.nan, "")

    # We are only interested in the AUI & PTR cols --> filter dataframe
    # accordingly
    # PTR is a column containing '.' delimited AUIs where left -> right is
    # the descendant path of root node to PAUI (PARENT AUI).
    # -> The AUI column associated to each PTR column would be the next AUI
    # in the descendant path.
    mrhier = mrhier[["AUI", "PTR"]]
    print("Complete. Beginning transforming table. (this may take ~15min)...")

    return mrhier


mrhier = read_transform_mrhier(path_to_mrhier)


def explode_write_mrhier(root: str, home: str, mrhier: pd.DataFrame):
    """
    Summary:
    --------
    Provided a root and home directory along with the mrhier df.
    pd.DataFrame will be exploded to provide 1:1 mappings of
    parent -> child (vocabulary specific).

    Parameters:
    -----------

    root : str.
        The root directory name as a string.
    home : str
        Home directory name as a string.
    mrhier : pd.Dataframe.
        Pandas DataFrame 'mrhier' (columns=['AUI', 'PTR']) created via former
        part of script.

    Returns:
    --------
    mrhier: pd.DataFrame.
        Pandas DataFrame containing all UMLS vocabulary specific hierarchies from
        UMLS.MRHIER - all contexts

    """
    hier = pd.DataFrame(mrhier.PTR.str.split(".").to_list(), index=mrhier.AUI).stack()
    hier_df = hier.reset_index()[[0, "AUI"]]

    # START_ID -> PTR & END_ID -> AUI
    hier_df.columns = [":START_ID", ":END_ID"]
    hier_df[":TYPE"] = "CHILD_OF"
    hier_df = hier_df[[":START_ID", ":END_ID", ":TYPE"]]

    # START_ID should not equal END_ID -> drop if exist
    child_of_rel_ptr = (
        hier_df[hier_df[":START_ID"] != hier_df[":END_ID"]]
        .drop_duplicates()
        .replace(np.nan, "")
    )

    child_of_rel_ptr.to_csv(
        path_or_buf=f"/{root}/{home}/import/child_of_rel_ptr.csv",
        header=True,
        index=False,
    )  # file ready for import


if __name__ == "__main__":
    explode_write_mrhier(root, home, mrhier)
    print("child_of_rel_ptr.csv written out...")
