import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

path_parent = os.path.dirname(os.getcwd()) + '/'
db_path = path_parent + 'TvSignals.db'
engine = create_engine('sqlite:///' + db_path, connect_args={"check_same_thread": False})

