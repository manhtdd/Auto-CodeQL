import json
import logging
import os
import pandas as pd

# Setup logging to both file and console
LOGS_DIR = "logs"
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)
    
log_file_path = os.path.join(LOGS_DIR, 'logs.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler()
    ]
)

def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            raw_string = file.read()
            data = json.loads(raw_string)
        return data
    except FileNotFoundError:
        logging.info(f"Error: File not found at path '{file_path}'")
    except Exception as e:
        logging.info(f"{file_path} {e}")
        
def codeql2cwe(cwe):
    if cwe == 'java/weak-cryptographic-algorithm':  # 327
        return ['CWE-327'], ['693']
    elif cwe == 'java/xxe':  # 611
        return ['CWE-611'], ['664']
    elif cwe == 'java/insecure-trustmanager':  # 295
        return ['CWE-295'], ['284']
    elif cwe == 'java/path-injection':  # 22,23,36
        return ['CWE-22', 'CWE-23', 'CWE-36'], ['664', '707']
    elif cwe == 'java/netty-http-request-or-response-splitting':
        return ['CWE-74'], ['707']
    elif cwe == 'java/implicit-cast-in-compound-assignment':  # 190 192 197 681
        return ['CWE-190', 'CWE-192', 'CWE-197'], ['664', '682']
    elif cwe == 'java/xss':  # 79
        return ['CWE-79'], ['707']
    elif cwe == 'java/zipslip':  # 29
        return ['CWE-29'], ['664']
    elif cwe == 'java/unsafe-deserialization':  # 502
        return ['CWE-502'], ['664', '707']
    elif cwe == 'java/ssrf':
        return ['CWE-918'], ['664']
    else:
        return [], ['10000']
    
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

if __name__ == "__main__":
    file_path = "/home/manhtd/Projects/auto_codeql/input/test.sarif"
    json_output = codeql_analysis(file_path)
    logging.info(json.dumps(json_output, indent=4))