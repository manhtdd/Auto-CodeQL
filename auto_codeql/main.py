import logging
import os
import subprocess
from .read_output import codeql_analysis
import time
from typing import Optional


CREATE_DATABASE_CMD = {
    "python": "cd {}; codeql database create codeql-database --language=python --source-root=. --overwrite; cd {}",
    "java": "cd {}; codeql database create codeql-database --command \"javac {}\" --language=java --source-root=. --overwrite; cd {}"
}

ANALYZE_CMD = "codeql database analyze {} --format=csv --output={} --threads={}"

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

def run_codeql(code_path: str, save_path: str, n_thread: Optional[int] = 1) -> dict:
    logging.info(f"Run CodeQL analysis for '{code_path}' and save the result to '{save_path}'")
    tmp_path = save_path + ".tmp"
    logging.info("Temporary file path: " + tmp_path)
    logging.info("Number of threads: " + str(n_thread))

    code_dir = os.path.dirname(code_path)
    logging.info(code_dir)
    codeql_database_dir = os.path.join(code_dir, "codeql-database")
    current_dir = os.getcwd()
    file_name = os.path.basename(code_path)
    logging.info(file_name)
        
    if code_path.endswith(".py"):
        logging.info("The file has a .py extension")
        create_database_cmd = CREATE_DATABASE_CMD["python"].format(code_dir, current_dir)
        logging.info(create_database_cmd)
        analyze_cmd = ANALYZE_CMD.format(codeql_database_dir, tmp_path, n_thread)
        logging.info(analyze_cmd)
    elif code_path.endswith(".java"):
        raise NotImplementedError("Java is not supported yet")
    else:
        logging.error("The file has a different extension")
        return {}
    
    command_with_timeout(create_database_cmd)
    command_with_timeout(analyze_cmd)
    
    if not os.path.exists(tmp_path):
        logging.error(f"The file '{tmp_path}' does not exist. CodeQL analysis failed !!!")
        return {}
    
    return codeql_analysis(tmp_path, save_path)
