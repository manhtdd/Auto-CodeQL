#!/bin/bash
   
INPUT_FILE_PATH=$1
INPUT_FILE=$(basename "$INPUT_FILE_PATH")
INPUT_PATH=$(dirname "$INPUT_FILE_PATH")

echo "> BUILD DATASET COMMAND:"
echo "codeql database create codeql-database --command "javac $INPUT_FILE" --language=java --source-root=$INPUT_PATH"

echo "> COMMAND'S OUTPUT:"
codeql database create codeql-database --command "javac $INPUT_FILE" --language=java --source-root=$INPUT_PATH --overwrite

echo "> FINISHED RUNNING"