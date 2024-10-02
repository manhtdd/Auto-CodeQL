# Auto CodeQL

Auto CodeQL is a Python wrapper for running CodeQL scans on your code. This package allows you to easily analyze your code for security vulnerabilities and quality issues using CodeQL.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Setup CodeQL](#setup-codeql)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Prerequisites

Before getting started, make sure you have Python 3.12+ and `pip` installed. You'll also need to download and set up CodeQL.

## Setup CodeQL

1. Download the CodeQL tar file from the [CodeQL GitHub releases page](https://github.com/github/codeql-action/releases) and extract it. For more information on which file to download, please kindly check [this website](https://docs.github.com/en/code-security/codeql-cli/getting-started-with-the-codeql-cli/setting-up-the-codeql-cli#1-download-the-codeql-cli-tar-archive).

2. Add CodeQL to your system path by creating a symbolic link:
   ```bash
   ln -s <absolute-path-to-your-extracted-codeql>/codeql /usr/local/bin/codeql
   ```

3. Verify the installation:
   ```bash
   $ codeql
   ```

   If successfully installed, you should see the following output:
   ```bash
   Usage: codeql <command> <argument>...
   Create and query CodeQL databases, or work with the QL language.

   GitHub makes this program freely available for the analysis of open-source software and certain other uses, but it is not itself free software. Type codeql --license to see the license terms.

   --license              Show the license terms for the CodeQL toolchain.
   Common options:
     -h, --help           Show this help text.
     -v, --verbose        Incrementally increase the number of progress messages printed.
     -q, --quiet          Incrementally decrease the number of progress messages printed.
   
   Commands:
     query       Compile and execute QL code.
     bqrs        Get information from .bqrs files.
     database    Create, analyze and process CodeQL databases.
     ...
   ```

## Installation

To install the `auto_codeql` package, run the following command:

```bash
pip install -e .
```

Once installed, you can import the `auto_codeql` module in Python:

```bash
$ python
Python 3.12.2 | packaged by conda-forge | (main, Feb 16 2024, 20:50:58) [GCC 12.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import auto_codeql
>>> 
```

## Usage

Here’s an example of how to use `auto_codeql` to scan a Python file:

```python
from auto_codeql import run_codeql
import json

codepath = "input/test.py"  # Path to the code to be analyzed
savepath = "input/test.sarif"  # Path where the analysis results will be saved

# Run CodeQL analysis
output = run_codeql(codepath, savepath)

# Print the output in a readable JSON format
print(json.dumps(output, indent=4))
```

### Arguments:
- `codepath`: Path to the file or directory you want to analyze.
- `savepath`: Path where the scan results will be saved (SARIF format).

### Example Output:
The output will be in JSON format and will include details about security vulnerabilities, potential bugs, and code quality issues.
