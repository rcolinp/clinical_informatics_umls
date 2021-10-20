"""
This .py assumes you have created an output directory named 'import' at your root directory (i.e. /Users/rob/import/).
    -> (this folder will be mounted outside the neo4j directory when creating neo4j database. The 'import' directory's location does not matter, it just cannot be mounted within the container itself & the docker run --volume mounts need to reflect this behavior.)
This .py assumes you are a UMLS license holder & MRHIER.RRF is located at the relative directory -> ../UMLS/subset/2021AA/META/

Please note: This script may take upwards of ~25 minutes to complete.
    -> This script can be broken down into smaller components and/or leverage more a more efficient python library/libraries (rather than pandas).
    -> Run time will vary largely depending on personal subset created via UMLS MetamorphoSys.
       -> relative directory ../conf/config.prop contains properties file used at creation of this script.

The file created will be large depending on sab_list. Writing out to a .parquet file will limit eating up disk space. A .parquet cannot be used for import though.

"""

import sys

from pandas.core.frame import DataFrame
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
import numpy as np
import pandas as pd
import getpass

####################################################################
root = 'Users'           # root directory
home = getpass.getuser()  # home directory (using getpass2 library)
####################################################################

# Read MRHIER.RRF using pandas read_csv()
# Script assumes MRHIER.RRF is located in the relative directory -> ../UMLS/subset/2021AA/META/MRHIER.RRF
mrhier = pd.read_csv('../UMLS/subset/2021AA/META/MRHIER.RRF',
                     sep='|',
                     header=None,
                     dtype=object)

# Define list containing vocabularies (UMLS.MRHIER.SAB) which will be included.
# All SABs could be included, but will increase run time, size, etc...
# --> sab_list contains same vocabularies used in `nodes_edges_part1.py`
sab_list = ['ATC', 'GO', 'HGNC', 'HPO', 'ICD9CM',
            'ICD10CM', 'ICD10PCS', 'LNC', 'MED-RT',
            'MDR', 'NCI', 'NCBI', 'RXNORM', 'SNOMEDCT_US']

# Where axis=1 drop 9th index (align columns correctly -> .RRF has extra column that needs to be dropped)
mrhier = mrhier.drop(9, axis=1)
print("Complete - MRHIER.RRF read in as .csv and empty column dropped")

# Assign column names (preserving source assigned names from UMLS)
mrhier.columns = ['CUI', 'AUI', 'CXN', 'PAUI',
                  'SAB', 'RELA', 'PTR', 'HCD', 'CVF']

# Filter mrhier to only include SAB (vocabularies) defined in the list defined above 'sab_list'
# Define this sab_list to be in accordance to how nodes_edges_part1.py was ran
mrhier = mrhier[mrhier['SAB'].isin(
    sab_list)].drop_duplicates().replace(np.nan, "")

# We are only interested in the AUI & PTR cols --> filter dataframe accordingly
# PTR is a column containing '.' delimited AUIs where left -> right is the descendant path of root node to PAUI (PARENT AUI).
# -> The AUI column associated to each PTR column would be the next AUI in the descendant path.
mrhier = mrhier[['AUI', 'PTR']]

# Create df via str.split('.') on delimited list (PTR column & add this to a list. Index via AUI & use .stack())
# -> This will explode the dataframe and increase table size by providing each row per PTR value that was split and added to list.
print("Complete. Beginning transforming table. (this may take ~15min)...")

# Simple function to take in root directory, home directory & MRHIER DataFrame to explode


def explode_mrhier_write_csv(root: str, home: str = home, mrhier: DataFrame = mrhier):
    """
    Summary:
    --------
    Provided a root and home directory along with the mrhier dataframe, 'mrhier'
    df will be exploded to provide a 1:1 mapping of atomic parent -> immediate child to atomic parent. 

    Parameters:
    -----------
    root : str.
        The root directory name as a string.
    home : str
        Home directory name as a string.
    mrhier : dataframe.
        Two column DataFrame 'mrhier' (columns=['AUI', 'PTR']) created via former part of script.

    """
    hier = pd.DataFrame(mrhier.PTR.str.split(
        '.').to_list(), index=mrhier.AUI).stack()

    # PTR variable is currently labeled 0 (index)
    hier_df = hier.reset_index()[[0, 'AUI']]

    # rename to ":START_ID", ":END_ID" to prep file for import into Neo4j
    # START_ID -> PTR & END_ID -> AUI
    hier_df.columns = [':START_ID', ':END_ID']
    # Add a ":TYPE" column where each PTR (:START_ID) is the immediate atomic parent to the :END_ID
    hier_df[':TYPE'] = 'CHILD_OF'

    hier_df.columns = hier_df[[':START_ID', ':END_ID', ':TYPE']]

    # Ensure :START_ID != :END_ID & write to .csv -> file is now ready to be imported
    child_of_rel = hier_df[hier_df[':START_ID'] !=
                           hier_df[':END_ID']].drop_duplicates().replace(np.nan, "")
    child_of_rel.to_csv(path_or_buf=f"/{root}/{home}/import/child_of_rel.csv",
                        header=True,
                        index=False)


explode_mrhier_write_csv(root=root, home=home, mrhier=mrhier)
print("child_of_rel.csv has been written out to /Users/home/import/child_of_rel.csv and is ready for import.")
