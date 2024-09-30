1. Download and extract codeql's `tar` file from its [GitHub website](https://github.com/github/codeql-action/releases)

Expect output: a folder named `codeql`. For example with path like this: `./codeql`

2. Prepaping your source code

Create a folder for all input:
```
mkdir input
```
Put your files into it, for example: `input/Main.java`

3. Create codeql-dataset

```
bash scripts/run-codeql.sh <language> <file_path; e.g. input/Main.java>
```