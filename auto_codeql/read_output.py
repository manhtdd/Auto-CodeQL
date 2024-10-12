import json
import logging
import os
import pandas as pd
    
def codeql_analysis(tmp_path, save_path):
    ### Load csv with pre-defined columns in CodeQL
    data = pd.read_csv(tmp_path, names=['Name', 'Description', 'Severity', 'Message', 'Path', 'Start line', 'Start column', 'End line', 'End column'])
    data = data.dropna()
    data = data.reset_index(drop=True)
    
    ### Overwrite file_path with columns
    data.to_csv(save_path, index=False)

    if os.path.exists(tmp_path):
        os.remove(tmp_path)
    return data
