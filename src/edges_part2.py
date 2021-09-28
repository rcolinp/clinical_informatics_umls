import sys
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
import numpy as np
import pandas as pd


# Read MRHIER.RRF using pandas read_csv()
mrhier = pd.read_csv('/Users/robpiombino/Documents/UMLS/subset/2021AA/META/MRHIER.RRF',
                     sep='|',
                     header=None,
                     dtype=object)

# Define list containing vocabularies (UMLS.MRHIER.SAB) which will be included.
# All SABs could be included, but will increase run time, size, etc...
# --> sab_list contains same vocabularies used in `nodes_edges_part1.py`
sab_list = ['ATC', 'GO', 'HGNC', 'ICD9CM', 'ICD10CM',
            'ICD10PCS', 'MED-RT', 'NCI', 'RXNORM', 'SNOMEDCT_US']

# Where axis=1 the 9th index (column) is a 'dummy'/empty column
mrhier = mrhier.drop(9, axis=1)

# Assign column names (preserving source assigned names from UMLS)
mrhier.columns = ['CUI', 'AUI', 'CXN', 'PAUI',
                  'SAB', 'RELA', 'PTR', 'HCD', 'CVF']

# Filter mrhier to only include SAB (vocabularies) defined in the list defined above 'sab_list'
mrhier = mrhier[mrhier['SAB'].isin(
    sab_list)].drop_duplicates().replace(np.nan, '')

# We are only interested in the AUI & PTR cols --> filter dataframe accordingly
mrhier = mrhier[['AUI', 'PTR']]

hier = pd.DataFrame(data=mrhier.PTR.str.split('.').to_list(),
                    index=mrhier.AUI.reset_index(drop=True)).stack()

hier_df = hier.reset_index(drop=False)

hier_df.columns = ['PTR', 'index', 'AUI']

hier_final_df = hier_df[['PTR', 'AUI']]

hier_final_df[':TYPE'] = 'PAUI_OF'

hier_final_df.columns = [':START_ID', ':END_ID', ':TYPE']

paui_of_df = hier_final_df[hier_final_df[':START_ID'] !=
                           hier_final_df[':END_ID']].drop_duplicates().replace(np.nan, '')

paui_of_df.to_csv(path_or_buf='./import/paui_of.csv',
                  header=True,
                  index=False)

print("successfully wrote out ./import/paui_of.csv")
