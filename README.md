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

2. Add CodeQL to your system path by adding codeql to PATH
   ```bash
   export PATH=$PATH:<absolute-path-to-your-extracted-codeql>/codeql
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
Clone this repository:
```
git clone https://github.com/manhtdd/Auto-CodeQL.git auto_codeql
cd auto_codeql
```

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
savepath = "input/test.csv"  # Path where the analysis results will be saved
n_threads = 1 #0: run maximum number of threads in local machine, n > 0: run on n threads
quality_suite = "s&q"
# Run CodeQL analysis
output = run_codeql("python", codepath, savepath, n_threads, quality_suite) ### Output is a pandas DF
```

### Arguments:
- `language`: Target programming langayge.
- `codepath`: Path to the file or directory you want to analyze.
- `savepath`: Path where the scan results will be saved (CSV format).
- `n_threads`: Number of threads for running CodeQL analysis. n = 0 will run this code on maximum number of threads in local machine; n > 0 will run this code on run on n threads
- `quality_suite`: Set of quality rules checked by CodeQL. Currently, our implementation supports three quality suites:
  + `s&p`: Set of rules for checking both `code quality and security` issues. This is our default code quality suites
  + `lgtm`: Set of rules for checking code quality issues from `LGTM.com`
  + `security`: Set of rules for checking security issues

### Example Output:
The output will be in CSV format and will all neccessary information including:
+ Name:	Name of the query that identified the result.
+ Description: Description of the query.
+ Severity:	Severity of the query.
+ Message:	Alert message.
+ Path:	Path of the file containing the alert.	/vendor/codemirror/markdown.js
+ Start line:	Line of the file where the code that triggered the alert begins.
+ Start column:	Column of the start line that marks the start of the alert code. Not included when equal to 1.
+ End line:	Line of the file where the code that triggered the alert ends. Not included when the same value as the start line.
+ End column:	Where available, the column of the end line that marks the end of the alert code. Otherwise the end line is repeated.
