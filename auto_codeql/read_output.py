import json
import logging
import os

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
    
def codeql_analysis(file_path):
    file_content = load_json(file_path)
    # if 'runs' in file_content.keys():
    #     vulss = file_content['runs']
    #     for vuls in vulss:
    #         if 'results' in vuls.keys():
    #             vuls_in = vuls['results']
    #             if vuls_in != None:
    #                 for vul in vuls_in:
    #                     rule_id = vul['ruleId']
    #                     loca = vul['locations'][0]
    #                     file = loca['physicalLocation']['artifactLocation']['uri']
    #                     line = loca['physicalLocation']['region']['startLine']
    #                     cwe, _ = codeql2cwe(rule_id)

    #                     predict = {
    #                         'file': file,
    #                         'line': line,
    #                         'rule_id': rule_id,
    #                         'cwe': cwe,
    #                         'found_by': 'code_ql'
    #                     }
                        
    #                     return predict
    #         else:
    #             logging.error(f"'result' is empty, file: {file_path}")
    #     else:
    #         logging.error(f"No key 'result' in {file_path}")
    # else:
    #     logging.error(f"No key 'runs' in {file_path}")
        
    return file_content

if __name__ == "__main__":
    file_path = "/home/manhtd/Projects/auto_codeql/input/test.sarif"
    json_output = codeql_analysis(file_path)
    logging.info(json.dumps(json_output, indent=4))