1. Setup CodeQL

1.1. Download and extract codeql's `tar` file from its [GitHub website](https://github.com/github/codeql-action/releases)

1.2 Add CodeQL to your system
```
ln -s <absolute path to your downloaded codeql; e.g. /opt/codeql>/codeql /usr/local/bin/codeql
```

Expect output: You should now be able to run `codeql`
```
$ codeql
Usage: codeql <command> <argument>...
Create and query CodeQL databases, or work with the QL language.

GitHub makes this program freely available for the analysis of open-source software and certain other uses, but it is not itself free software. Type codeql --license to see the license terms.

      --license              Show the license terms for the CodeQL toolchain.
Common options:
  -h, --help                 Show this help text.
  -v, --verbose              Incrementally increase the number of progress messages printed.
  -q, --quiet                Incrementally decrease the number of progress messages printed.
Some advanced options have been hidden; try --help -v for a fuller view.
Commands:
  query       Compile and execute QL code.
  bqrs        Get information from .bqrs files.
  database    Create, analyze and process CodeQL databases.
  dataset     [Plumbing] Work with raw QL datasets.
  test        Execute QL unit tests.
  resolve     [Deep plumbing] Helper commands to resolve disk locations etc.
  execute     [Deep plumbing] Low-level commands that need special JVM options.
  version     Show the version of the CodeQL toolchain.
  generate    Commands that generate useful output.
  github      Commands useful for interacting with the GitHub API through CodeQL.
  pack        Commands to manage QL packages.
  diagnostic  [Experimental] Create, process, and export diagnostic information.
```

2. Install `auto_codeql`
```
pip install -e .
```

You should be able to `import auto_codeql` now
```
$ python
Python 3.12.2 | packaged by conda-forge | (main, Feb 16 2024, 20:50:58) [GCC 12.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import run_codeql
>>> 
```

3. Usage
An example code:
```
from auto_codeql import run_codeql

codepath = "input/test.py"
savepath = "input/test.sarif"
output = run_codeql(codepath, savepath)
print(json.dumps(output, indent=4))
```