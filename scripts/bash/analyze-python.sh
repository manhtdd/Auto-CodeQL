#!/bin/bash

codeql database analyze codeql-database --format=sarif-latest --output=output/output.sarif --sarif-category=python