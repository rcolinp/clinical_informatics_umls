import sys
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

import numpy as np
import pandas as pd
import psycopg2
import getpass
from sqlalchemy import create_engine

# ************************************
# Database connection using getpass2
user = getpass.getuser()
password = getpass.getpass()
host = 'localhost'
dbname = 'postgres'
# ************************************

# Establish database connection (using postgres here)
engine = create_engine(
    url=f"postgresql+psycopg2://{user}:{password}@{host}/{dbname}")
