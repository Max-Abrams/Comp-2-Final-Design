import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "Materials.csv")

class MaterialDatabase:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path, low_memory=False)
        
        # Clean column names
        self.df.columns = self.df.columns.str.strip()

# Create the instance
db = MaterialDatabase(DATA_PATH)