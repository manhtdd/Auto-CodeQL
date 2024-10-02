from typing import Optional
import logging
import os
import json
import subprocess
from read_output import codeql_analysis

CREATE_DATABASE_CMD = {
    "python": "codeql database create codeql-database --language=python --source-root={} --overwrite",
    "java": "codeql database create codeql-database --command \"javac {}\" --language=java --source-root={} --overwrite"
}

ANALYZE_CMD = "codeql database analyze codeql-database --format=sarif-latest --output={} --sarif-category={}"

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

def execute_command(cmd:str, cwd:str="."):
    logging.info(f"Run:\n\t{cmd}\nAt: {cwd}")
    try:
        # Check if the specified directory exists
        if not os.path.isdir(cwd):
            raise NotADirectoryError(f"{cwd} is not a valid directory")

        # Execute the command in the specified directory
        subprocess.run(cmd, cwd=cwd, shell=True, check=True)
        
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

def run_codeql(codepath: str, savepath: Optional[str] = None) -> dict:
    logging.info(codepath)
    logging.info(savepath)
    
    dir_path = os.path.dirname(codepath)
    logging.info(dir_path)
    file_name = os.path.basename(codepath)
    logging.info(file_name)
        
    if codepath.endswith(".py"):
        logging.info("The file has a .py extension")
        create_database_cmd = CREATE_DATABASE_CMD["python"].format(dir_path)
        logging.info(create_database_cmd)
        analyze_cmd = ANALYZE_CMD.format(savepath, "python")
        logging.info(analyze_cmd)
    elif codepath.endswith(".java"):
        logging.info("The file has a .java extension")
        create_database_cmd = CREATE_DATABASE_CMD["java"].format(file_name, dir_path)
        logging.info(create_database_cmd)
        analyze_cmd = ANALYZE_CMD.format(savepath, "java")
        logging.info(analyze_cmd)
    else:
        logging.error("The file has a different extension")
        return {}
    
    execute_command(create_database_cmd)
    execute_command(analyze_cmd)
    
    if not os.path.exists(savepath):
        logging.error(f"The file '{savepath}' does not exist.")
        return {}
    
    return codeql_analysis(savepath)

if __name__ == "__main__":
    codepath = "input/test.py"
    savepath = "input/test.sarif"
    # codepath = "input/Main.java"
    # savepath = "input/main.json"
    output = run_codeql(codepath, savepath)
    logging.info(json.dumps(output, indent=4))