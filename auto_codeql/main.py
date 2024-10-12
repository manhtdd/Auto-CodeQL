from typing import Optional
import logging
import os
import json
import subprocess
from .read_output import codeql_analysis
import time

CREATE_DATABASE_CMD = {
    "python": "codeql database create codeql-database --language=python --source-root={} --overwrite",
    "java": "codeql database create codeql-database --command \"javac {}\" --language=java --source-root={} --overwrite"
}

ANALYZE_CMD = "codeql database analyze codeql-database --format=csv --output={} --sarif-category={}"

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
        
def command_with_timeout(cmd:str, cwd:str=".", timeout=60):
    """
    Execute a command with a specified timeout.
    :param cmd: Command to be executed.
    :param timeout: Time (in seconds) after which the command will be terminated.
    :return: Standard output and standard error of the executed command.
    """
    logging.info(f"Run:\n\t{cmd}\nAt: {cwd}")
    p = subprocess.Popen(cmd, cwd=cwd, shell=True, universal_newlines=True)
    start_time = time.time()

    while True:
        if p.poll() is not None:
            break
        elapsed_time = time.time() - start_time
        if timeout and elapsed_time > timeout:
            p.terminate()
            return 'TIMEOUT', 'TIMEOUT'
        time.sleep(1)

    out, err = p.communicate()
    return out, err

def run_codeql(codepath: str, savepath: str) -> dict:
    logging.info(codepath)
    logging.info(savepath)
    tmppath = savepath + ".tmp"
    logging.info(tmppath)
    
    dir_path = os.path.dirname(codepath)
    logging.info(dir_path)
    file_name = os.path.basename(codepath)
    logging.info(file_name)
        
    if codepath.endswith(".py"):
        logging.info("The file has a .py extension")
        create_database_cmd = CREATE_DATABASE_CMD["python"].format(dir_path)
        logging.info(create_database_cmd)
        analyze_cmd = ANALYZE_CMD.format(tmppath, "python")
        logging.info(analyze_cmd)
    elif codepath.endswith(".java"):
        logging.info("The file has a .java extension")
        create_database_cmd = CREATE_DATABASE_CMD["java"].format(file_name, dir_path)
        logging.info(create_database_cmd)
        analyze_cmd = ANALYZE_CMD.format(tmppath, "java")
        logging.info(analyze_cmd)
    else:
        logging.error("The file has a different extension")
        return {}
    
    command_with_timeout(create_database_cmd)
    command_with_timeout(analyze_cmd)
    
    if not os.path.exists(tmppath):
        logging.error(f"The file '{tmppath}' does not exist. CodeQL analysis failed !!!")
        return {}
    
    return codeql_analysis(tmppath, savepath)

if __name__ == "__main__":
    codepath = "input/test.py"
    savepath = "input/test.sarif"
    # codepath = "input/Main.java"
    # savepath = "input/main.json"
    output = run_codeql(codepath, savepath)
    logging.info(json.dumps(output, indent=4))