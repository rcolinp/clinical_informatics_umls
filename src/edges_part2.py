"""
This .py assumes you have created an output directory named 'import' at your root directory (i.e. $HOME/import).
This .py assumes you are a UMLS license holder & MRHIER.RRF is located at the relative directory -> ../UMLS/subset/2021AA/META/

Please note: This script may take upwards of ~25 minutes to complete.
    -> This script can be broken down into smaller components and/or leverage more a more efficient python library/libraries (rather than pandas).
    -> Run time will vary largely depending on personal subset created via UMLS MetamorphoSys.
       -> relative directory ../conf/config.prop contains properties file used at creation of this script.
    
"""

import sys
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
import numpy as np
import pandas as pd

print("Reading MRHIER.RRF...")
# Read MRHIER.RRF using pandas read_csv()
mrhier = pd.read_csv('../UMLS/subset/2021AA/META/MRHIER.RRF',
                     sep='|',
                     header=None,
                     dtype=object)
print("Complete - MRHIER.RRF read in as .csv and empty column dropped")

# Define list containing vocabularies (UMLS.MRHIER.SAB) which will be included.
# All SABs could be included, but will increase run time, size, etc...
# --> sab_list contains same vocabularies used in `nodes_edges_part1.py`
sab_list = ['ATC', 'GO', 'HGNC', 'ICD9CM', 'ICD10CM', 'LNC', 'CVX', 'MVX',
            'ICD10PCS', 'MED-RT', 'NCI', 'RXNORM', 'SNOMEDCT_US']

# Where axis=1 the 9th index (column) is a 'dummy'/empty column
mrhier = mrhier.drop(9, axis=1)
print("Complete - MRHIER.RRF read in as .csv and empty column dropped")

# Assign column names (preserving source assigned names from UMLS)
mrhier.columns = ['CUI', 'AUI', 'CXN', 'PAUI',
                  'SAB', 'RELA', 'PTR', 'HCD', 'CVF']

print("Beginning filtering SAB to desired sab_list & subsetting df")
# Filter mrhier to only include SAB (vocabularies) defined in the list defined above 'sab_list'
mrhier = mrhier[mrhier['SAB'].isin(
    sab_list)].drop_duplicates().replace(np.nan, '')

# We are only interested in the AUI & PTR cols --> filter dataframe accordingly
mrhier = mrhier[['AUI', 'PTR']]
print("Complete. Beginning transforming table. (this may take ~15min)...")

hier = pd.DataFrame(data=mrhier.PTR.str.split('.').to_list(),
                    index=mrhier.AUI.reset_index(drop=True)).stack()

print("Complete! Applying required formatting requirements & writing to .csv")
hier_df = hier.reset_index(drop=False)

hier_df.columns = ['PTR', 'index', 'AUI']

hier_final_df = hier_df[['PTR', 'AUI']]

hier_final_df[':TYPE'] = 'PAUI_OF'

hier_final_df.columns = [':START_ID', ':END_ID', ':TYPE']

paui_of_df = hier_final_df[hier_final_df[':START_ID'] !=
                           hier_final_df[':END_ID']].drop_duplicates().replace(np.nan, '')

paui_of_df.to_csv(path_or_buf='$HOME/import/paui_of.csv',
                  header=True,
                  index=False)
print("Complete! paui_of.csv has been saved to $HOME/import/paui_of.csv and is ready for import.")
